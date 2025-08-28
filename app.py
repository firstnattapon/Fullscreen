# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import urlparse

# ---- Page setup: กำหนดหน้าแบบกว้าง + ซ่อน header/sidebar/footer ----
st.set_page_config(
    page_title="Fullscreen Wrapper",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      header {visibility: hidden;}
      footer {visibility: hidden;}
      /* ลบ padding รอบ content ให้เต็มจอมากที่สุด */
      .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---- กำหนด URL ปลายทาง (ค่าเริ่มต้นเป็นลิงก์ของคุณ) ----
DEFAULT_URL = "https://monica.im/share/artifact?id=3vibZExEztirQ7KXRgqauG"

# รองรับทั้ง st.query_params (ใหม่) และ experimental_get_query_params (เก่า)
try:
    target_url = st.query_params.get("u", DEFAULT_URL)
except Exception:
    target_url = st.experimental_get_query_params().get("u", [DEFAULT_URL])[0]

# ---- Whitelist โดเมน (กันคนยิงไปเว็บเสี่ยง) ----
ALLOWED = {
    "monica.im",
    "github.com",
    "raw.githubusercontent.com",
    "streamlit.io",
    "streamlit.app",
}
netloc = urlparse(target_url).netloc.split(":")[0].lower()
allowed = any(netloc == d or netloc.endswith("." + d) for d in ALLOWED)
if not allowed:
    st.error(f"โดเมนนี้ไม่ได้อยู่ในรายการที่อนุญาต: {netloc}")
    st.stop()

# ---- HTML ภายใน component: iframe + ปุ่ม Reload (ล่างซ้าย) + Wake Lock ----
html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<style>
  html, body, #root {{
    height: 100%;
    margin: 0;
    background: #000;
  }}
  #root {{
    position: fixed; inset: 0;
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
    padding-left: env(safe-area-inset-left);
    padding-right: env(safe-area-inset-right);
  }}
  iframe#web {{
    position: absolute; inset: 0;
    width: 100%; height: 100%;
    border: 0; display: block;
    background: #000;
  }}
  #controls {{
    position: fixed; left: 12px; bottom: 12px;  /* ย้ายมุมล่างซ้าย */
    z-index: 9999; display: flex; gap: 8px;
  }}
  button {{
    font: inherit;
    padding: 8px 12px;
    border-radius: 12px;
    border: 0;
    box-shadow: 0 1px 4px rgba(0,0,0,.25);
    background: #fff;
  }}
</style>
</head>
<body>
  <div id="root">
    <iframe id="web"
      src="{target_url}"
      allow="autoplay; clipboard-read; clipboard-write; camera; microphone; geolocation; encrypted-media; picture-in-picture; web-share"
      referrerpolicy="no-referrer-when-downgrade"
      sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox">
    </iframe>

    <div id="controls">
      <button id="rel">↻ Reload</button>
    </div>
  </div>

  <script>
    // Reload
    const relBtn = document.getElementById('rel');
    relBtn.addEventListener('click', () => {{
      const iframe = document.getElementById('web');
      try {{
        iframe.contentWindow.location.reload();
      }} catch (e) {{
        // cross-origin อาจโดนบล็อก: fallback โหลด src เดิม
        iframe.src = iframe.src;
      }}
    }});

    // Wake Lock: กันจอดับ (ถ้าเบราว์เซอร์รองรับ)
    if ('wakeLock' in navigator) {{
      let lock;
      const requestLock = async () => {{
        try {{ lock = await navigator.wakeLock.request('screen'); }}
        catch (e) {{ /* เงียบไว้ก็ได้ */ }}
      }};
      requestLock();
      document.addEventListener('visibilitychange', () => {{
        if (document.visibilityState === 'visible') requestLock();
      }});
    }}
  </script>
</body>
</html>
"""

# หมายเหตุ: height มีผลต่อพื้นที่ component ตอนฝังในหน้า Streamlit
components.html(html, height=2050, scrolling=False)
