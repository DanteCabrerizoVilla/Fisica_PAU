"""Referencia para la corrección de la prueba de nivel.

Escribe, para cada pregunta, la clave que genera build.py y la posición en la
que queda la opción correcta. La página de pruebas comprueba que el JavaScript
da por buena esa posición y solo esa.
"""

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "herramientas"))

from build import Constructor  # noqa: E402
from comun import cargar_sitio  # noqa: E402

casos = []
for curso in cargar_sitio().cursos:
    if not curso.prueba:
        continue
    for q in curso.prueba["preguntas"]:
        orden = list(range(4))
        random.Random(q["id"]).shuffle(orden)
        correcta = orden.index(0)
        casos.append({"id": q["id"], "correcta": correcta,
                      "clave": Constructor.huella(f"{q['id']}|{correcta}|nivel")})

posiciones = [c["correcta"] for c in casos]
destino = Path(__file__).with_name("prueba_nivel.ref.json")
destino.write_text(json.dumps({"casos": casos}, indent=1), encoding="utf-8")
print(f"{destino.name}: {len(casos)} preguntas · posición de la correcta: "
      + ", ".join(f"{i + 1}ª×{posiciones.count(i)}" for i in range(4)))
