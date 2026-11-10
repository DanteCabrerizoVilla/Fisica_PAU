"""Comprueba la física de las simulaciones contra referencias de Python.

1. Ejecuta cada pruebas/referencia_*.py (regenera los .ref.json).
2. Sirve el proyecto en local y abre pruebas/sim.html en Chrome o Edge sin
   ventana; la página importa la física en JavaScript y la compara.

Uso:  python herramientas/probar_sim.py
Sale con código 1 si alguna comprobación falla.
"""

from __future__ import annotations

import functools
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PRUEBAS = RAIZ / "pruebas"

NAVEGADORES = [
    os.environ.get("NAVEGADOR", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "google-chrome", "chromium", "chromium-browser",
]


def buscar_navegador() -> str | None:
    for n in NAVEGADORES:
        if n and (Path(n).is_file() or shutil.which(n)):
            return n
    return None


class _Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main() -> int:
    for script in sorted(PRUEBAS.glob("referencia_*.py")):
        subprocess.run([sys.executable, str(script)], check=True)

    navegador = buscar_navegador()
    if not navegador:
        print("No se ha encontrado Chrome ni Edge. Indica la ruta en la variable NAVEGADOR.")
        return 1

    manejador = functools.partial(_Silencioso, directory=str(RAIZ))
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{servidor.server_address[1]}/pruebas/sim.html"

    with tempfile.TemporaryDirectory() as perfil:
        orden = [navegador, "--headless=new", "--disable-gpu", "--no-first-run",
                 f"--user-data-dir={perfil}", "--virtual-time-budget=60000", "--dump-dom", url]
        if os.environ.get("CI"):
            orden.insert(1, "--no-sandbox")  # necesario en los ejecutores de GitHub Actions
        try:
            salida = subprocess.run(orden, capture_output=True, timeout=120).stdout.decode("utf-8", "replace")
        finally:
            servidor.shutdown()

    m = re.search(r'<script id="resultado" type="application/json">(.*?)</script>', salida, re.S)
    if not m or not m.group(1).strip():
        print("La página de pruebas no ha terminado. Ábrela a mano para ver el error:")
        print("  python -m http.server  y luego  http://localhost:8000/pruebas/sim.html")
        return 1
    import html
    resultado = json.loads(html.unescape(m.group(1)))
    for f in resultado["fallos"]:
        print(f"FALLA  {f['nombre']}  {f.get('detalle', '')}")
    print(f"{resultado['total']} comprobaciones de simulaciones · {len(resultado['fallos'])} fallos")
    return 1 if resultado["fallos"] else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
