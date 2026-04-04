"""
Generador de Reporte HTML para las pruebas de Inventario App
Ejecuta las pruebas y genera un reporte HTML profesional con capturas.
"""

import unittest
import sys
import os
import time
import base64
import glob
from datetime import datetime
from io import StringIO

# Agrega el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tests.test_inventario import (
    TestHU01Acceso,
    TestHU02AgregarProducto,
    TestHU03LeerProductos,
    TestHU04EditarProducto,
    TestHU05EliminarProducto,
    TestHU06ClasificacionEstado,
    TestHU07PanelEstadisticas,
)

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
REPORT_DIR     = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORT_DIR, exist_ok=True)


class HTMLTestResult(unittest.TestResult):
    """Recolector de resultados con soporte HTML."""

    def __init__(self):
        super().__init__()
        self.results = []
        self.start_times = {}

    def startTest(self, test):
        super().startTest(test)
        self.start_times[test] = time.time()

    def _record(self, test, status, detail=""):
        elapsed = time.time() - self.start_times.get(test, time.time())
        self.results.append({
            "class":   type(test).__name__,
            "method":  test._testMethodName,
            "doc":     test._testMethodDoc or test._testMethodName,
            "status":  status,
            "detail":  detail,
            "elapsed": f"{elapsed:.2f}s",
        })

    def addSuccess(self, test):
        super().addSuccess(test)
        self._record(test, "PASS")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._record(test, "FAIL", str(err[1]))

    def addError(self, test, err):
        super().addError(test, err)
        self._record(test, "ERROR", str(err[1]))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._record(test, "SKIP", reason)


def img_to_base64(path):
    """Convierte imagen a base64 para incrustarla en HTML."""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""
    


def generate_html_report(result: HTMLTestResult, duration: float) -> str:
    """Genera el HTML completo del reporte."""

    total   = len(result.results)
    passed  = sum(1 for r in result.results if r["status"] == "PASS")
    failed  = sum(1 for r in result.results if r["status"] == "FAIL")
    errors  = sum(1 for r in result.results if r["status"] == "ERROR")
    skipped = sum(1 for r in result.results if r["status"] == "SKIP")
    pct     = int((passed / total * 100) if total else 0)

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # ── Recoge capturas por HU ───────────────────────────────────────────
    screenshots = sorted(glob.glob(os.path.join(SCREENSHOT_DIR, "*.png")))
    screenshots_html = ""
    for ss in screenshots:
        b64  = img_to_base64(ss)
        name = os.path.basename(ss)
        if b64:
            screenshots_html += f"""
            <div class="screenshot-item">
              <p class="ss-name">{name}</p>
              <img src="data:image/png;base64,{b64}" alt="{name}"/>
            </div>"""

    # ── Filas de resultados ──────────────────────────────────────────────
    rows_html = ""
    for r in result.results:
        badge_class = {"PASS": "badge-pass", "FAIL": "badge-fail",
                       "ERROR": "badge-error", "SKIP": "badge-skip"}.get(r["status"], "")
        icon = {"PASS": "", "FAIL": "", "ERROR": "", "SKIP": "⏭"}.get(r["status"], "")
        detail_cell = f'<span class="detail">{r["detail"]}</span>' if r["detail"] else ""
        rows_html += f"""
        <tr class="row-{r['status'].lower()}">
          <td><span class="hu-class">{r['class']}</span></td>
          <td>{r['method']}</td>
          <td>{r['doc']}</td>
          <td><span class="badge {badge_class}">{icon} {r['status']}</span></td>
          <td>{r['elapsed']}</td>
          <td>{detail_cell}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Reporte de Pruebas – Inventario App</title>
  <style>
    :root {{
      --pass:  #22c55e; --fail: #ef4444; --error: #f97316;
      --skip:  #a855f7; --bg: #0f172a; --surface: #1e293b;
      --card:  #334155; --text: #e2e8f0; --muted: #94a3b8;
      --accent:#38bdf8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: var(--bg); color: var(--text);
      padding: 2rem; line-height: 1.6;
    }}
    /* ── Header ── */
    .header {{
      background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
      border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2rem;
      display: flex; justify-content: space-between; align-items: center;
    }}
    .header h1 {{ font-size: 1.8rem; font-weight: 700; color: #fff; }}
    .header .meta {{ color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-top: 0.3rem; }}
    .header .logo {{ font-size: 3rem; }}
    /* ── KPI Cards ── */
    .kpi-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(140px,1fr));
      gap: 1rem; margin-bottom: 2rem;
    }}
    .kpi-card {{
      background: var(--surface); border-radius: 12px;
      padding: 1.2rem 1.5rem; text-align: center;
      border-top: 4px solid var(--accent);
    }}
    .kpi-card.pass  {{ border-color: var(--pass);  }}
    .kpi-card.fail  {{ border-color: var(--fail);  }}
    .kpi-card.error {{ border-color: var(--error); }}
    .kpi-card.skip  {{ border-color: var(--skip);  }}
    .kpi-card.total {{ border-color: var(--accent); }}
    .kpi-val {{ font-size: 2.2rem; font-weight: 800; }}
    .kpi-label {{ color: var(--muted); font-size: 0.82rem; text-transform: uppercase; letter-spacing: .05em; }}
    /* ── Progress bar ── */
    .progress-wrap {{ background: var(--surface); border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 2rem; }}
    .progress-label {{ display: flex; justify-content: space-between; margin-bottom: .5rem; font-size: .9rem; }}
    .progress-bar {{ height: 14px; background: #1e293b; border-radius: 99px; overflow: hidden; }}
    .progress-fill {{
      height: 100%; border-radius: 99px;
      background: linear-gradient(90deg, var(--pass), #16a34a);
      width: {pct}%; transition: width 1s ease;
    }}
    /* ── Table ── */
    .table-wrap {{ background: var(--surface); border-radius: 12px; overflow: hidden; margin-bottom: 2rem; }}
    table {{ width: 100%; border-collapse: collapse; font-size: .88rem; }}
    thead tr {{ background: var(--card); }}
    th {{ padding: .8rem 1rem; text-align: left; color: var(--muted); font-weight: 600;
          text-transform: uppercase; letter-spacing: .05em; font-size: .78rem; }}
    td {{ padding: .75rem 1rem; border-bottom: 1px solid #273548; vertical-align: middle; }}
    tr:last-child td {{ border-bottom: none; }}
    tr.row-pass:hover  {{ background: rgba(34,197,94,.08); }}
    tr.row-fail:hover  {{ background: rgba(239,68,68,.08); }}
    tr.row-error:hover {{ background: rgba(249,115,22,.08); }}
    .hu-class {{ font-family: monospace; background: var(--card); padding: .15rem .4rem;
                 border-radius: 4px; font-size: .82rem; color: var(--accent); }}
    .badge {{ display: inline-block; padding: .2rem .6rem; border-radius: 6px;
              font-size: .78rem; font-weight: 600; }}
    .badge-pass  {{ background: rgba(34,197,94,.18);  color: var(--pass);  }}
    .badge-fail  {{ background: rgba(239,68,68,.18);  color: var(--fail);  }}
    .badge-error {{ background: rgba(249,115,22,.18); color: var(--error); }}
    .badge-skip  {{ background: rgba(168,85,247,.18); color: var(--skip);  }}
    .detail {{ color: var(--fail); font-family: monospace; font-size: .78rem; }}
    /* ── Screenshots ── */
    .section-title {{ font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; color: var(--accent); }}
    .screenshots-grid {{
      display: grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr));
      gap: 1rem; margin-bottom: 2rem;
    }}
    .screenshot-item {{
      background: var(--surface); border-radius: 10px; overflow: hidden;
      border: 1px solid #334155;
    }}
    .screenshot-item img {{ width: 100%; display: block; }}
    .ss-name {{ padding: .5rem .75rem; font-size: .78rem; color: var(--muted);
                background: var(--card); font-family: monospace; }}
    /* ── Footer ── */
    .footer {{ text-align: center; color: var(--muted); font-size: .82rem; padding-top: 1rem; }}
  </style>
</head>
<body>

  <div class="header">
    <div>
      <h1>Reporte de Pruebas Automatizadas</h1>
      <div class="meta">Proyecto: <strong>Inventario App</strong> &nbsp;|&nbsp; {now} &nbsp;|&nbsp; Duración: {duration:.1f}s</div>
      <div class="meta">Selenium + Python &nbsp;·&nbsp; unittest</div>
    </div>
    <div class="logo">🧪</div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card total"><div class="kpi-val">{total}</div><div class="kpi-label">Total</div></div>
    <div class="kpi-card pass" ><div class="kpi-val" style="color:var(--pass)">{passed}</div><div class="kpi-label">Pasadas</div></div>
    <div class="kpi-card fail" ><div class="kpi-val" style="color:var(--fail)">{failed}</div><div class="kpi-label">Fallidas</div></div>
    <div class="kpi-card error"><div class="kpi-val" style="color:var(--error)">{errors}</div><div class="kpi-label">Errores</div></div>
    <div class="kpi-card skip" ><div class="kpi-val" style="color:var(--skip)">{skipped}</div><div class="kpi-label">Omitidas</div></div>
  </div>

  <div class="progress-wrap">
    <div class="progress-label">
      <span>Tasa de éxito</span><span><strong>{pct}%</strong></span>
    </div>
    <div class="progress-bar"><div class="progress-fill"></div></div>
  </div>

  <p class="section-title"> Detalle de Pruebas</p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Historia</th><th>Método</th><th>Descripción</th>
          <th>Estado</th><th>Tiempo</th><th>Detalle</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </div>

  <p class="section-title">📸 Capturas de Pantalla</p>
  <div class="screenshots-grid">
    {screenshots_html if screenshots_html else '<p style="color:var(--muted)">No hay capturas disponibles aún.</p>'}
  </div>

  <div class="footer">
    Generado automáticamente con Selenium WebDriver &nbsp;·&nbsp; {now}
  </div>

</body>
</html>"""
    return html


def run():
    """Punto de entrada principal."""
    print("\n" + "═"*60)
    print("    PRUEBAS AUTOMATIZADAS – INVENTARIO APP")
    print("═"*60 + "\n")

    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    clases = [
        TestHU01Acceso,
        TestHU02AgregarProducto,
        TestHU03LeerProductos,
        TestHU04EditarProducto,
        TestHU05EliminarProducto,
        TestHU06ClasificacionEstado,
        TestHU07PanelEstadisticas,
    ]
    for cls in clases:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    result  = HTMLTestResult()
    t_start = time.time()

    # Muestra salida en consola también
    stream  = StringIO()
    runner  = unittest.TextTestRunner(stream=stream, verbosity=2)
    runner.run(suite)           # corre con el runner estándar para la consola
    print(stream.getvalue())

    # Corre de nuevo para recoger en nuestro result
    suite2 = unittest.TestSuite()
    for cls in clases:
        suite2.addTests(loader.loadTestsFromTestCase(cls))
    suite2.run(result)

    duration = time.time() - t_start

    # ── Genera reporte HTML ───────────────────────────────────────────────
    html    = generate_html_report(result, duration)
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = os.path.join(REPORT_DIR, f"reporte_{ts}.html")
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(html)

    print("\n" + "═"*60)
    print(f"   Reporte HTML generado: {outfile}")
    print("═"*60 + "\n")
    return outfile

if __name__ == "__main__":
    run()

    