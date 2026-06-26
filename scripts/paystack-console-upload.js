/**
 * Banimal Paystack Image Uploader v2
 * Paste this into your browser console at dashboard.paystack.com
 * Uploads images for all 28 products (23 physical + 4 Sam Fox digital + 1 hat)
 * Updated: 2026-06-26
 */
(async () => {
  const CDN = 'https://banimal-global-loop.vercel.app/assets';
  const API = 'https://api.paystack.co';

  const products = [
    // ── Baby Grows ──────────────────────────────────────────────────────────
    { id: '2598282', img: 'babygrow-black-0-3-COhppmaC.png' },
    { id: '2598283', img: 'babygrow-black-3-6-DFpFlTtO.png' },
    { id: '2598284', img: 'babygrow-black-6-9-CAtZxCqC.png' },
    { id: '2598286', img: 'babygrow-beige-0-3-DWpH9zhC.png' },
    { id: '2598287', img: 'babygrow-beige-3-6-BQnxLg3W.png' },
    { id: '2598291', img: 'babygrow-beige-6-9-CKJv-JZ9.png' },
    { id: '2598292', img: 'babygrow-gray-0-3-SZFJC89Y.png'  },
    { id: '2598295', img: 'babygrow-gray-3-6-CoLi__pJ.png'  },
    { id: '2598299', img: 'babygrow-gray-6-9-BsoDW7fE.png'  },
    { id: '2598300', img: 'babygrow-white-0-3-D_S66xmd.png' },
    { id: '2598302', img: 'babygrow-white-3-6-Dw98L5oQ.png' },
    { id: '2598303', img: 'babygrow-white-6-9-CZFePaHl.png' },
    // ── Round Bibs ──────────────────────────────────────────────────────────
    { id: '2598304', img: 'BR001-B9Svc9IF.png' },
    { id: '2598307', img: 'BR002-m4ScX5Ak.png' },
    // ── Bandana Bibs ────────────────────────────────────────────────────────
    { id: '2598308', img: 'BT001-BYDvu1g2.png' },
    { id: '2598310', img: 'BT002-CX4CjBt9.png' },
    { id: '2598314', img: 'BT003-Ynr1ODEe.png' },
    { id: '2598315', img: 'BT004-KZ5X0Ak7.png' },
    { id: '2598316', img: 'BT005-Ce7QfnBe.png' },
    { id: '2598317', img: 'BT007-C5WxSB9Q.png' },
    { id: '2598320', img: 'BT008-Ci-PewEt.png' },
    { id: '2598321', img: 'BT009-BYEat297.png' },
    { id: '2598323', img: 'BT010-pzlVe3nP.png' },
    // ── Sam Fox Digital Art ─────────────────────────────────────────────────
    { id: '2598705', img: 'samfox-dream-big-DqhMqlsk.jpg'   },
    { id: '2598706', img: 'samfox-first-eye-BvvyLsxG.jpg'   },
    { id: '2598707', img: 'samfox-rainbow-tata-D-dLbgP7.jpg'},
    { id: '2598708', img: 'samfox-space-puma-BAEkuXl-.jpg'  },
    // ── Hat ─────────────────────────────────────────────────────────────────
    { id: '2598709', img: 'be-fruitful-hat-B6D_moGp.jpg'    },
  ];

  // Find auth token
  const tokenKey = Object.keys(localStorage).find(k =>
    k.toLowerCase().includes('token') || k.toLowerCase().includes('access')
  );
  const token = tokenKey ? localStorage.getItem(tokenKey) : null;

  if (!token) {
    console.error('❌ No auth token found. Make sure you are logged into dashboard.paystack.com');
    return;
  }
  console.log(`✅ Token found. Uploading ${products.length} product images...\n`);

  let ok = 0, fail = 0;

  for (const p of products) {
    try {
      // 1. Download image from Vercel CDN
      const imgRes = await fetch(`${CDN}/${p.img}`);
      if (!imgRes.ok) throw new Error(`CDN fetch failed: ${imgRes.status}`);
      const imgBlob = await imgRes.blob();
      const mimeType = p.img.endsWith('.jpg') ? 'image/jpeg' : 'image/png';

      // 2. Get Paystack signed upload URL
      const urlRes = await fetch(`${API}/upload_url`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ upload_filename: p.img, upload_path: '/products' })
      });
      const urlData = await urlRes.json();
      if (!urlData.status) throw new Error(`upload_url: ${urlData.message}`);

      const { signed_url, key, path, original_filename } = urlData.data;

      // 3. PUT binary to signed URL
      const uploadRes = await fetch(signed_url, {
        method: 'PUT',
        headers: { 'Content-Type': mimeType },
        body: imgBlob
      });
      if (!uploadRes.ok) throw new Error(`PUT failed: ${uploadRes.status}`);

      // 4. Update product files array
      const updateRes = await fetch(`${API}/product/${p.id}`, {
        method: 'PUT',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({
          files: [{ key: key || path, type: 'image', path: path, original_filename: original_filename || p.img }]
        })
      });
      const ud = await updateRes.json();
      if (ud.status) { console.log(`✅ ${p.id} — ${p.img}`); ok++; }
      else throw new Error(`update: ${ud.message}`);

    } catch (e) {
      console.error(`❌ ${p.id} — ${p.img} — ${e.message}`);
      fail++;
    }
    await new Promise(r => setTimeout(r, 400)); // 400ms between uploads
  }

  console.log(`\n═══════════════════════════════════`);
  console.log(`Done: ${ok} uploaded, ${fail} failed`);
})();
