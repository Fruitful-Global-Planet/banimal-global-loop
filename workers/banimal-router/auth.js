/**
 * OAuth 2.0 Authentication Handler
 * Cloudflare Worker for banimal.co.za
 * Implements Authorization Code flow + PKCE for all providers
 */

const PROVIDERS = {
  google: {
    authUrl: 'https://accounts.google.com/o/oauth2/v2/auth',
    tokenUrl: 'https://oauth2.googleapis.com/token',
    userUrl: 'https://openidconnect.googleapis.com/v1/userinfo',
    scope: 'openid email profile',
  },
  facebook: {
    authUrl: 'https://facebook.com/v19.0/dialog/oauth',
    tokenUrl: 'https://graph.facebook.com/v19.0/oauth/access_token',
    userUrl: 'https://graph.facebook.com/me?fields=id,name,email,picture',
    scope: 'email public_profile',
  },
  apple: {
    authUrl: 'https://appleid.apple.com/auth/authorize',
    tokenUrl: 'https://appleid.apple.com/auth/token',
    userUrl: null, // User data returned in token response
    scope: 'name email',
    responseMode: 'form_post',
  },
  github: {
    authUrl: 'https://github.com/login/oauth/authorize',
    tokenUrl: 'https://github.com/login/oauth/access_token',
    userUrl: 'https://api.github.com/user',
    scope: 'read:user user:email',
  },
  microsoft: {
    authUrl: 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
    tokenUrl: 'https://login.microsoftonline.com/common/oauth2/v2.0/token',
    userUrl: 'https://graph.microsoft.com/v1.0/me',
    scope: 'openid email profile',
  },
  twitter: {
    authUrl: 'https://twitter.com/i/oauth2/authorize',
    tokenUrl: 'https://api.twitter.com/2/oauth2/token',
    userUrl: 'https://api.twitter.com/2/users/me?user.fields=id,name,username,profile_image_url',
    scope: 'tweet.read users.read',
    usePKCE: true,
  },
  tiktok: {
    authUrl: 'https://open.tiktokapis.com/v2/oauth/authorize/',
    tokenUrl: 'https://open.tiktokapis.com/v2/oauth/token/',
    userUrl: 'https://open.tiktokapis.com/v2/user/info/?fields=open_id,union_id,display_name,avatar_url',
    scope: 'user.info.basic',
  },
  linkedin: {
    authUrl: 'https://www.linkedin.com/oauth/v2/authorization',
    tokenUrl: 'https://www.linkedin.com/oauth/v2/accessToken',
    userUrl: 'https://api.linkedin.com/v2/me?projection=(id,localizedFirstName,localizedLastName,profilePicture(displayImage))',
    scope: 'openid profile email',
  },
  discord: {
    authUrl: 'https://discord.com/api/oauth2/authorize',
    tokenUrl: 'https://discord.com/api/oauth2/token',
    userUrl: 'https://discord.com/api/users/@me',
    scope: 'identify email',
  },
  twitch: {
    authUrl: 'https://id.twitch.tv/oauth2/authorize',
    tokenUrl: 'https://id.twitch.tv/oauth2/token',
    userUrl: 'https://api.twitch.tv/helix/users',
    scope: 'openid user:read:email',
  },
};

// Generate random string for state
function generateState(length = 32) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// PKCE challenge generation
async function generatePKCE() {
  const codeVerifier = generateState(128);
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  const codeChallenge = btoa(String.fromCharCode(...new Uint8Array(digest)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
  return { codeVerifier, codeChallenge };
}

// Hash password with bcrypt
async function hashPassword(password) {
  // Note: In production, use bcrypt-wasm or a KV-stored hash
  // For MVP, we'll use PBKDF2 via crypto.subtle
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveBits']);
  const derivedKey = await crypto.subtle.deriveBits({ name: 'PBKDF2', salt, hash: 'SHA-256', iterations: 100000 }, key, 256);
  return btoa(String.fromCharCode(...salt)) + ':' + btoa(String.fromCharCode(...new Uint8Array(derivedKey)));
}

// Verify password against hash
async function verifyPassword(password, hash) {
  const [saltB64, hashB64] = hash.split(':');
  const salt = new Uint8Array(atob(saltB64).split('').map(c => c.charCodeAt(0)));
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveBits']);
  const derivedKey = await crypto.subtle.deriveBits({ name: 'PBKDF2', salt, hash: 'SHA-256', iterations: 100000 }, key, 256);
  return btoa(String.fromCharCode(...new Uint8Array(derivedKey))) === hashB64;
}

// Generate session ID
function generateSessionId() {
  return 'session_' + generateState(24);
}

// Extract user info from provider response
function extractUserInfo(provider, data) {
  const extractors = {
    google: () => ({
      id: data.sub,
      email: data.email,
      name: data.name,
      avatar: data.picture,
    }),
    facebook: () => ({
      id: data.id,
      email: data.email,
      name: data.name,
      avatar: data.picture?.data?.url,
    }),
    apple: () => ({
      id: data.sub,
      email: data.email,
      name: data.name,
      avatar: null,
    }),
    github: () => ({
      id: String(data.id),
      email: data.email,
      name: data.name,
      avatar: data.avatar_url,
    }),
    microsoft: () => ({
      id: data.id,
      email: data.userPrincipalName,
      name: data.displayName,
      avatar: null,
    }),
    twitter: () => ({
      id: data.data.id,
      email: null,
      name: data.data.name,
      avatar: data.data.profile_image_url,
    }),
    tiktok: () => ({
      id: data.data.user.open_id,
      email: null,
      name: data.data.user.display_name,
      avatar: data.data.user.avatar_url,
    }),
    linkedin: () => ({
      id: data.id,
      email: data.email,
      name: `${data.localizedFirstName} ${data.localizedLastName}`,
      avatar: null,
    }),
    discord: () => ({
      id: data.id,
      email: data.email,
      name: data.username,
      avatar: `https://cdn.discordapp.com/avatars/${data.id}/${data.avatar}`,
    }),
    twitch: () => ({
      id: data.data[0].id,
      email: data.data[0].email,
      name: data.data[0].display_name,
      avatar: data.data[0].profile_image_url,
    }),
  };
  return (extractors[provider] || (() => data))();
}

export {
  PROVIDERS,
  generateState,
  generatePKCE,
  hashPassword,
  verifyPassword,
  generateSessionId,
  extractUserInfo,
};
