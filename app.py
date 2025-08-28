# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import urlparse

# ... ส่วนตั้งค่าหน้าเว็บเดิม ...

html = f"""
<!doctype html>
<html>
<head>
<!-- ส่วน head เดิม ... -->
</head>
<body>
  <div id="root">
    <iframe id="web" src="{target_url}" ... ></iframe>

    <div id="controls">
      <button id="rel">↻ Reload</button>
    </div>
  </div>

  <script>
    const relBtn = document.getElementById('rel');
    relBtn.addEventListener('click', () => {{
      const iframe = document.getElementById('web');
      try {{
        iframe.contentWindow.location.reload();
      }} catch (e) {{
        iframe.src = iframe.src;
      }}
    }});

    // Wake Lock ส่วนเดิม ...
  </script>
</body>
</html>
"""

components.html(html, height=2000 , scrolling=False)
