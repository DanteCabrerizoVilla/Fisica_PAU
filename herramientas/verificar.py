"""Verificación numérica de las soluciones.

Cada problema `x.md` tiene al lado un `x.py` con:

    def resolver() -> dict:      # obligatorio: clave de resultado -> valor calculado
    def comprobar(r) -> None:    # opcional: segunda vía, con assert

Este script valida las cabeceras, ejecuta cada `resolver()` y compara con los
valores declarados en la cabecera del problema.

Uso:  python herramientas/verificar.py [--filtro TEXTO]
Sale con código 1 si algún problema marcado como 'verificado' no pasa.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
import traceback

from comun import ErrorContenido, Problema, cargar_sitio, redondear_cifras, relativa

TOLERANCIA = 0.005  # 0,5 %: margen por redondeos intermedios


def cargar_modulo(p: Problema):
    spec = importlib.util.spec_from_file_location(f"verif_{p.id.replace('-', '_')}", p.script)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def verificar_problema(p: Problema) -> tuple[list[str], list[str]]:
    """Devuelve (errores, avisos) de un problema."""
    errores: list[str] = []
    avisos: list[str] = []
    numericos = [r for r in p.meta["resultados"] if "valor" in r]

    if not p.script.exists():
        if numericos:
            errores.append(f"no existe {p.script.name}")
        return errores, avisos

    try:
        modulo = cargar_modulo(p)
        calculado = modulo.resolver()
    except Exception:
        errores.append("resolver() ha fallado:\n" + traceback.format_exc(limit=3))
        return errores, avisos

    for r in numericos:
        clave, declarado = r["clave"], r["valor"]
        if clave not in calculado:
            errores.append(f"resolver() no devuelve '{clave}'")
            continue
        valor = float(calculado[clave])
        if not math.isfinite(valor):
            errores.append(f"{clave}: el valor calculado no es finito ({valor})")
            continue
        escala = max(abs(valor), abs(declarado))
        desvio = abs(valor - declarado) / escala if escala else 0.0
        if desvio > TOLERANCIA:
            errores.append(
                f"{clave}: cabecera {declarado:g}, calculado {valor:.6g} (desvío {desvio:.2%})"
            )
        elif not math.isclose(redondear_cifras(valor, r["cifras"]), declarado, rel_tol=1e-9):
            avisos.append(
                f"{clave}: cabecera {declarado:g}, pero redondeando a {r['cifras']} cifras "
                f"sale {redondear_cifras(valor, r['cifras']):g}"
            )

    sobrantes = set(calculado) - {r["clave"] for r in p.meta["resultados"]}
    if sobrantes:
        avisos.append("resolver() devuelve claves que no están en la cabecera: " + ", ".join(sorted(sobrantes)))

    if hasattr(modulo, "comprobar"):
        try:
            modulo.comprobar(calculado)
        except AssertionError as e:
            errores.append(f"comprobar() no se cumple: {e or 'assert sin mensaje'}")
        except Exception:
            errores.append("comprobar() ha fallado:\n" + traceback.format_exc(limit=3))
    return errores, avisos


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--filtro", default="", help="solo problemas cuyo id contenga este texto")
    args = ap.parse_args()

    try:
        sitio = cargar_sitio()
    except ErrorContenido as e:
        print(f"ERROR de contenido\n{e}")
        return 1

    total = fallidos = pendientes = 0
    for curso in sitio.cursos:
        for p in curso.problemas(solo_publicables=False):
            if args.filtro not in p.id:
                continue
            total += 1
            errores, avisos = verificar_problema(p)
            estado = p.meta["estado"]
            if errores and estado == "verificado":
                fallidos += 1
                marca = "FALLA"
            elif errores:
                pendientes += 1
                marca = f"pendiente ({estado})"
            elif estado != "verificado":
                pendientes += 1
                marca = f"pasa, pero sigue en '{estado}'"
            else:
                marca = "ok"
            print(f"[{marca}] {p.id}  ({relativa(p.ruta)})")
            if estado == "revisar":
                print(f"    [REVISAR] {p.meta['revisar']}")
            for e in errores:
                print("    ERROR: " + e.replace("\n", "\n      "))
            for a in avisos:
                print("    aviso: " + a)

    # Pruebas de nivel: cada una lleva al lado su comprobación (prueba-nivel.py).
    for curso in sitio.cursos:
        if curso.prueba is None or args.filtro:
            continue
        script = curso.ruta_prueba.with_suffix(".py")
        n = f"{len(curso.prueba['preguntas'])} preguntas, {sum(len(q['variantes']) for q in curso.prueba['preguntas'])} variantes"
        try:
            if not script.exists():
                raise AssertionError(f"no existe {script.name}")
            spec = importlib.util.spec_from_file_location("verif_prueba_nivel", script)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            modulo.comprobar(curso.prueba["preguntas"])
            print(f"[ok] prueba de nivel: {n}  ({relativa(curso.ruta_prueba)})")
        except AssertionError as e:
            fallidos += 1
            print(f"[FALLA] prueba de nivel  ({relativa(curso.ruta_prueba)})\n    ERROR: {e}")
        except Exception:
            fallidos += 1
            print(f"[FALLA] prueba de nivel  ({relativa(curso.ruta_prueba)})\n    " + traceback.format_exc(limit=3))

    print(f"\n{total} problemas · {total - fallidos - pendientes} verificados · "
          f"{pendientes} pendientes · {fallidos} con fallo")
    return 1 if fallidos else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
