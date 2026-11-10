"""Comprueba que todas las fórmulas del sitio construido se pintan sin error.

Abre cada página de _site/ que tenga fórmulas en Chrome o Edge sin ventana y
cuenta las que KaTeX no ha podido interpretar. Hay que construir antes.

Uso:  python herramientas/probar_formulas.py
Sale con código 1 si alguna fórmula falla.
"""

from __future__ import annotations

import functools
import http.server
import os
import re
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor

from comun import RAIZ
from probar_sim import _Silencioso, buscar_navegador

SITIO = RAIZ / "_site"


def revisar(navegador: str, url: str) -> tuple[int, int, list[str]]:
    """Devuelve (fórmulas, sin pintar, textos con error) de una página."""
    with tempfile.TemporaryDirectory() as perfil:
        orden = [navegador, "--headless=new", "--disable-gpu", "--no-first-run",
                 f"--user-data-dir={perfil}", "--virtual-time-budget=8000", "--dump-dom", url]
        if os.environ.get("CI"):
            orden.insert(1, "--no-sandbox")
        dom = subprocess.run(orden, capture_output=True, timeout=120).stdout.decode("utf-8", "replace")
    total = len(re.findall(r'class="math (?:inline|block)', dom))
    listas = len(re.findall(r'class="math (?:inline|block) listo"', dom))
    errores = re.findall(r'class="katex-error"[^>]*title="([^"]*)"', dom)
    return total, total - listas, errores


def main() -> int:
    if not SITIO.is_dir():
        print("No existe _site/. Ejecuta antes herramientas/build.py")
        return 1
    navegador = buscar_navegador()
    if not navegador:
        print("No se ha encontrado Chrome ni Edge. Indica la ruta en la variable NAVEGADOR.")
        return 1
    paginas = [p for p in sorted(SITIO.rglob("*.html")) if 'class="math ' in p.read_text(encoding="utf-8")]

    manejador = functools.partial(_Silencioso, directory=str(SITIO))
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{servidor.server_address[1]}/"
    try:
        with ThreadPoolExecutor(max_workers=3) as grupo:
            resultados = list(grupo.map(
                lambda p: revisar(navegador, base + p.relative_to(SITIO).as_posix()), paginas))
        # Con varios navegadores a la vez alguna página puede no llegar a
        # cargar a tiempo: las que salen sin pintar se repiten de una en una.
        for i, (total, sin_pintar, errores) in enumerate(resultados):
            if total == 0 or sin_pintar:
                resultados[i] = revisar(navegador, base + paginas[i].relative_to(SITIO).as_posix())
    finally:
        servidor.shutdown()

    formulas = fallos = 0
    for pagina, (total, sin_pintar, errores) in zip(paginas, resultados):
        formulas += total
        if total == 0 or sin_pintar or errores:
            fallos += 1
            print(f"FALLA  {pagina.relative_to(SITIO).as_posix()}: {total} fórmulas, "
                  f"{sin_pintar} sin pintar, {len(errores)} con error")
            for e in errores[:5]:
                print("    " + e)
    print(f"{formulas} fórmulas en {len(paginas)} páginas · {fallos} páginas con fallo")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
