"""Crea la carpeta de un examen oficial con los esqueletos de sus problemas.

Uso:
  python herramientas/nuevo_examen.py 2027 modelo 1 2A 2B 3A 3B 4A 4B
  python herramientas/nuevo_examen.py 2024 ordinaria A1 A2 A3 A4 A5 B1 B2 B3 B4 B5
  python herramientas/nuevo_examen.py 2024 modelo A1 A2 --curso fisica/2-bachillerato

Genera contenido/<curso>/colecciones/<prueba>-<año>-<convocatoria>/ con
coleccion.yaml y, por cada problema, un .md en estado 'borrador' y su .py de
verificación. No sobrescribe nada que ya exista.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata

from comun import CONTENIDO, NOMBRE_CONVOCATORIA, cargar_yaml, nombre_prueba, relativa

PLANTILLA_MD = """---
id: {id}
numero: "{numero}"
titulo: "PENDIENTE"
bloque: {bloque}
subtemas: [{subtema}]
dificultad: 2
puntuacion: 2
estado: borrador
resultados:
  - {{apartado: a, clave: x, simbolo: "x", valor: 0, unidad: "", cifras: 3}}
---

## Enunciado

## Datos

## Planteamiento

## Resolución

### a) PENDIENTE

## Errores típicos
"""

PLANTILLA_PY = '''"""Verificación de {id}."""

import math

# Datos del enunciado (SI)


def resolver() -> dict:
    return {{"x": 0.0}}


def comprobar(res: dict) -> None:
    pass
'''


def slug(texto: str) -> str:
    plano = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", plano.lower()).strip("-")


def main() -> int:
    ap = argparse.ArgumentParser(description="Crea los esqueletos de un examen oficial")
    ap.add_argument("anio", type=int)
    ap.add_argument("convocatoria", choices=list(NOMBRE_CONVOCATORIA))
    ap.add_argument("problemas", nargs="+", help="números de problema, p. ej. 1 2A 2B (o A1 A2 B1 en los antiguos)")
    ap.add_argument("--curso", default="fisica/2-bachillerato")
    ap.add_argument("--pdf", default="", help="URL del enunciado oficial")
    args = ap.parse_args()

    dir_curso = CONTENIDO / args.curso
    curso = cargar_yaml((dir_curso / "curso.yaml").read_text(encoding="utf-8"))
    nombre = nombre_prueba(curso, args.anio)       # EvAU hasta 2024, PAU después
    prueba = slug(nombre)
    carpeta = dir_curso / "colecciones" / f"{prueba}-{args.anio}-{args.convocatoria}"
    carpeta.mkdir(parents=True, exist_ok=True)

    f_col = carpeta / "coleccion.yaml"
    if not f_col.exists():
        conv = NOMBRE_CONVOCATORIA[args.convocatoria]
        lineas = [
            "tipo: examen-oficial",
            f'titulo: "{curso["asignatura"]} · {nombre} {args.anio} · {conv}"',
            f"anio: {args.anio}",
            f"convocatoria: {args.convocatoria}",
        ]
        if args.pdf:
            lineas.append(f'pdf_oficial: "{args.pdf}"')
        f_col.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        print(f"creado {relativa(f_col)}")

    abreviatura = {"modelo": "mod", "ordinaria": "ord", "extraordinaria": "ext",
                   "ordinaria-coincidentes": "ordc", "extraordinaria-coincidentes": "extc"}[args.convocatoria]
    bloque = curso["bloques"][0]
    for numero in args.problemas:
        archivo = slug(numero)
        ident = f"{curso['id']}-{prueba}-{args.anio}-{abreviatura}-{archivo}"
        # "A1" se muestra como "A.1" y "2A" como "2.A"
        visible = re.sub(r"^([A-Za-z])(\d+)$|^(\d+)([A-Za-z])$",
                         lambda m: f"{m.group(1) or m.group(3)}.{m.group(2) or m.group(4)}", numero).upper()
        f_md = carpeta / f"{archivo}.md"
        if f_md.exists():
            print(f"ya existe {relativa(f_md)}, no se toca")
            continue
        f_md.write_text(
            PLANTILLA_MD.format(id=ident, numero=visible, bloque=bloque["id"], subtema=bloque["subtemas"][0]["id"]),
            encoding="utf-8",
        )
        (carpeta / f"{archivo}.py").write_text(PLANTILLA_PY.format(id=ident), encoding="utf-8")
        print(f"creado {relativa(f_md)}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
