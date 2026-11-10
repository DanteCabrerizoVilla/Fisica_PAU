"""Descarga a fuentes/pdf/ los exámenes oficiales listados en fuentes/fuentes.yaml.

Uso:  python herramientas/descargar_fuentes.py
No vuelve a bajar los que ya están. Los PDFs no se suben al repositorio.
"""

from __future__ import annotations

import sys
import urllib.request

from comun import RAIZ, leer_yaml

DESTINO = RAIZ / "fuentes" / "pdf"


def main() -> int:
    DESTINO.mkdir(parents=True, exist_ok=True)
    fallos = 0
    for doc in leer_yaml(RAIZ / "fuentes" / "fuentes.yaml")["documentos"]:
        archivo = DESTINO / doc["archivo"]
        if archivo.exists():
            continue
        url = f"https://drive.google.com/uc?export=download&id={doc['drive']}"
        peticion = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            datos = urllib.request.urlopen(peticion, timeout=90).read()
        except OSError as e:
            print(f"ERROR  {doc['archivo']}: {e}")
            fallos += 1
            continue
        if not datos.startswith(b"%PDF-"):
            print(f"ERROR  {doc['archivo']}: la respuesta no es un PDF")
            fallos += 1
            continue
        archivo.write_bytes(datos)
        print(f"descargado {doc['archivo']} ({len(datos) // 1024} kB)")
    print("Sin fallos." if not fallos else f"{fallos} documentos sin descargar.")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
