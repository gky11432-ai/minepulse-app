# ui.py - Fallback UI module
DASHBOARD_HTML = """<!DOCTYPE html>
<html>
<head><title>MinePulse AI</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-950 text-slate-100 p-6">
  <div class="max-w-4xl mx-auto space-y-4">
    <h1 class="text-2xl font-bold">MinePulse <span class="text-amber-500">AI</span> Portal</h1>
    <div class="bg-slate-900 p-4 rounded-xl border border-slate-800">
      <p class="text-sm text-emerald-400">System Online & Connected to Cloud Postgres Database.</p>
    </div>
  </div>
</body>
</html>"""

def get_form_vi_html(rows):
    return f"<html><body><h2>Form-VI Register</h2><table border='1'>{rows}</table></body></html>"
  
