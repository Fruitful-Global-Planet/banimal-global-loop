/**
 * OAuth Route Handlers for Cloudflare Worker
 */

import {
  PROVIDERS,
  generateState,
  generatePKCE,
  generateSessionId,
  extractUserInfo,
  hashPassword,
  verifyPassword,
} from './auth.js';

const SESSION_COOKIE_OPTS = 'HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=2592000';
const SESSION_TTL = 30 * 24 * 60 * 60; // 30 days

/**
 * GET /auth/{provider}/start
 * Redirect to OAuth provider
 */
export async function authStart(provider, env, url) {
  const config = PROVIDERS[provider];
  if (!config) return new Response(JSON.stringify({ error: 'provider not found' }), { status: 404 });

  const state = generateState();
  const { codeVerifier, codeChallenge } = config.usePKCE ? await generatePKCE() : { codeVerifier: null, codeChallenge: null };
  const redirectUri = `${new URL(url).origin}/auth/${provider}/callback`;

  // Store state + PKCE in KV
  if (env.BANIMAL_AUTH_KV) {
    await env.BANIMAL_AUTH_KV.put(`auth_state:${state}`, JSON.stringify({ provider, codeVerifier }), { expirationTtl: 600 });
  }

  const params = new URLSearchParams();
  params.append('client_id', env[`${provider.toUpperCase()}_CLIENT_ID`]);
  params.append('redirect_uri', redirectUri);
  params.append('response_type', 'code');
  params.append('state', state);
  params.append('scope', config.scope);

  if (config.usePKCE) {
    params.append('code_challenge', codeChallenge);
    params.append('code_challenge_method', 'S256');
  }

  // Provider-specific params
  if (provider === 'apple') {
    params.append('response_mode', 'form_post');
  }
  if (provider === 'microsoft') {
    params.append('prompt', 'select_account');
  }

  return new Response(null, {
    status: 302,
    headers: { Location: `${config.authUrl}?${params}` },
  });
}

/**
 * GET /auth/{provider}/callback
 * Exchange code for token, fetch user, create session
 */
export async function authCallback(provider, url, env) {
  const config = PROVIDERS[provider];
  if (!config) return new Response(JSON.stringify({ error: 'provider not found' }), { status: 404 });

  const urlObj = new URL(url);
  const code = urlObj.searchParams.get('code');
  const state = urlObj.searchParams.get('state');

  if (!code || !state) {
    return new Response(JSON.stringify({ error: 'missing code or state' }), { status: 400 });
  }

  // Verify state
  let stateData;
  if (env.BANIMAL_AUTH_KV) {
    const stored = await env.BANIMAL_AUTH_KV.get(`auth_state:${state}`);
    if (!stored) return new Response(JSON.stringify({ error: 'invalid state' }), { status: 400 });
    stateData = JSON.parse(stored);
    await env.BANIMAL_AUTH_KV.delete(`auth_state:${state}`);
  }

  const redirectUri = `${urlObj.origin}/auth/${provider}/callback`;
  const clientId = env[`${provider.toUpperCase()}_CLIENT_ID`];
  const clientSecret = env[`${provider.toUpperCase()}_CLIENT_SECRET`];

  // Exchange code for token
  const tokenParams = new URLSearchParams();
  tokenParams.append('grant_type', 'authorization_code');
  tokenParams.append('code', code);
  tokenParams.append('redirect_uri', redirectUri);
  tokenParams.append('client_id', clientId);
  tokenParams.append('client_secret', clientSecret);

  if (config.usePKCE && stateData?.codeVerifier) {
    tokenParams.append('code_verifier', stateData.codeVerifier);
  }

  let tokenResp;
  try {
    tokenResp = await fetch(config.tokenUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: tokenParams,
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: 'token exchange failed', details: e.message }), { status: 502 });
  }

  const tokenData = await tokenResp.json();
  if (!tokenData.access_token) {
    return new Response(JSON.stringify({ error: 'no access token', details: tokenData }), { status: 502 });
  }

  // Fetch user info
  let userData;
  if (config.userUrl) {
    try {
      const userResp = await fetch(config.userUrl, {
        headers: { Authorization: `Bearer ${tokenData.access_token}` },
      });
      userData = await userResp.json();
    } catch (e) {
      return new Response(JSON.stringify({ error: 'user fetch failed' }), { status: 502 });
    }
  } else {
    // Apple: decode id_token
    const idToken = tokenData.id_token;
    if (idToken) {
      const parts = idToken.split('.');
      const payload = JSON.parse(atob(parts[1]));
      userData = payload;
    }
  }

  // Extract user data
  const user = extractUserInfo(provider, userData);
  if (!user.id) {
    return new Response(JSON.stringify({ error: 'failed to extract user id' }), { status: 502 });
  }

  // Create session
  const sessionId = generateSessionId();
  const sessionData = {
    userId: user.id,
    name: user.name,
    email: user.email,
    avatar: user.avatar,
    provider,
    createdAt: new Date().toISOString(),
  };

  if (env.BANIMAL_AUTH_KV) {
    await env.BANIMAL_AUTH_KV.put(`session:${sessionId}`, JSON.stringify(sessionData), { expirationTtl: SESSION_TTL });
  }

  // Redirect to home with session cookie
  return new Response(null, {
    status: 302,
    headers: {
      Location: '/?auth=success',
      'Set-Cookie': `banimal_session=${sessionId}; ${SESSION_COOKIE_OPTS}`,
    },
  });
}

/**
 * GET /auth/session
 * Return current session user (from cookie)
 */
export async function getSession(request, env) {
  const cookie = request.headers.get('cookie') || '';
  const sessionMatch = cookie.match(/banimal_session=([^;]+)/);
  if (!sessionMatch) return new Response(JSON.stringify({ user: null }), { status: 200 });

  const sessionId = sessionMatch[1];
  const sessionData = env.BANIMAL_AUTH_KV ? await env.BANIMAL_AUTH_KV.get(`session:${sessionId}`) : null;

  if (!sessionData) {
    return new Response(JSON.stringify({ user: null }), { status: 200 });
  }

  const user = JSON.parse(sessionData);
  return new Response(JSON.stringify({ user }), { status: 200 });
}

/**
 * POST /auth/signout
 * Delete session
 */
export async function signOut(request, env) {
  const cookie = request.headers.get('cookie') || '';
  const sessionMatch = cookie.match(/banimal_session=([^;]+)/);

  if (sessionMatch && env.BANIMAL_AUTH_KV) {
    await env.BANIMAL_AUTH_KV.delete(`session:${sessionMatch[1]}`);
  }

  return new Response(JSON.stringify({ status: 'ok' }), {
    status: 200,
    headers: {
      'Set-Cookie': `banimal_session=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0`,
    },
  });
}

/**
 * POST /auth/email/signup
 * Email + password signup
 */
export async function emailSignup(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'invalid json' }), { status: 400 });
  }

  const { email, password, name } = body;

  // Validate
  if (!email || !password || !name) {
    return new Response(JSON.stringify({ error: 'missing email, password, or name' }), { status: 400 });
  }
  if (password.length < 8) {
    return new Response(JSON.stringify({ error: 'password must be at least 8 characters' }), { status: 400 });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return new Response(JSON.stringify({ error: 'invalid email' }), { status: 400 });
  }

  // Check if user exists
  if (env.BANIMAL_AUTH_KV) {
    const existing = await env.BANIMAL_AUTH_KV.get(`email_user:${email}`);
    if (existing) {
      return new Response(JSON.stringify({ error: 'email already registered' }), { status: 409 });
    }
  }

  // Hash password
  const passwordHash = await hashPassword(password);
  const userId = `email_${generateState(16)}`;

  // Store user
  if (env.BANIMAL_AUTH_KV) {
    await env.BANIMAL_AUTH_KV.put(`email_user:${email}`, JSON.stringify({ userId, name, passwordHash }), { expirationTtl: SESSION_TTL * 365 });
    await env.BANIMAL_AUTH_KV.put(`user_profile:${userId}`, JSON.stringify({ userId, email, name, provider: 'email', createdAt: new Date().toISOString() }), { expirationTtl: SESSION_TTL * 365 });
  }

  // Create session
  const sessionId = generateSessionId();
  const sessionData = {
    userId,
    name,
    email,
    avatar: null,
    provider: 'email',
    createdAt: new Date().toISOString(),
  };

  if (env.BANIMAL_AUTH_KV) {
    await env.BANIMAL_AUTH_KV.put(`session:${sessionId}`, JSON.stringify(sessionData), { expirationTtl: SESSION_TTL });
  }

  return new Response(JSON.stringify({ status: 'ok', sessionId }), {
    status: 201,
    headers: {
      'Set-Cookie': `banimal_session=${sessionId}; ${SESSION_COOKIE_OPTS}`,
    },
  });
}

/**
 * POST /auth/email/signin
 * Email + password signin
 */
export async function emailSignin(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'invalid json' }), { status: 400 });
  }

  const { email, password } = body;

  if (!email || !password) {
    return new Response(JSON.stringify({ error: 'missing email or password' }), { status: 400 });
  }

  // Look up user
  let userRecord;
  if (env.BANIMAL_AUTH_KV) {
    const data = await env.BANIMAL_AUTH_KV.get(`email_user:${email}`);
    if (!data) {
      return new Response(JSON.stringify({ error: 'invalid email or password' }), { status: 401 });
    }
    userRecord = JSON.parse(data);
  }

  // Verify password
  const valid = await verifyPassword(password, userRecord.passwordHash);
  if (!valid) {
    return new Response(JSON.stringify({ error: 'invalid email or password' }), { status: 401 });
  }

  // Create session
  const sessionId = generateSessionId();
  const sessionData = {
    userId: userRecord.userId,
    name: userRecord.name,
    email,
    avatar: null,
    provider: 'email',
    createdAt: new Date().toISOString(),
  };

  if (env.BANIMAL_AUTH_KV) {
    await env.BANIMAL_AUTH_KV.put(`session:${sessionId}`, JSON.stringify(sessionData), { expirationTtl: SESSION_TTL });
  }

  return new Response(JSON.stringify({ status: 'ok', sessionId }), {
    status: 200,
    headers: {
      'Set-Cookie': `banimal_session=${sessionId}; ${SESSION_COOKIE_OPTS}`,
    },
  });
}

export const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};
