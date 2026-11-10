"""Generador del sitio estático.

Lee `contenido/`, aplica las plantillas de `plantillas/` y escribe `_site/`.

Uso:  python herramientas/build.py [--todo] [--base-url /prefijo]

  --todo       incluye también problemas en 'borrador' y 'revisar' (con aviso
               visible). Solo para previsualizar en local; nunca al publicar.
  --base-url   prefijo de las rutas (en GitHub Pages, "/nombre-del-repo").
               También se puede dar con la variable de entorno BASE_URL.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt
from markupsafe import Markup
from mdit_py_plugins.dollarmath import dollarmath_plugin

from comun import (
    NOMBRE_CONVOCATORIA,
    RAIZ,
    SECCIONES,
    Curso,
    ErrorContenido,
    Problema,
    Sitio,
    cargar_sitio,
    numero_tex,
    trocear,
)

SALIDA = RAIZ / "_site"
EXT_RECURSOS = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}


# --------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------

def crear_markdown() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    md.use(dollarmath_plugin, allow_labels=False, double_inline=False)

    render_imagen = md.renderer.rules["image"]

    def imagen(tokens, idx, options, env):
        """Las imágenes relativas se sirven desde la carpeta de su colección."""
        token = tokens[idx]
        src = token.attrGet("src") or ""
        if env.get("base") and not re.match(r"^([a-z]+:|/|#)", src):
            token.attrSet("src", f"{env['base']}/{src}")
        token.attrSet("loading", "lazy")
        return render_imagen(tokens, idx, options, env)

    md.renderer.rules["image"] = imagen
    return md


# --------------------------------------------------------------------------
# Construcción
# --------------------------------------------------------------------------

class Constructor:
    def __init__(self, sitio: Sitio, base_url: str, todo: bool):
        self.sitio = sitio
        self.base = base_url.rstrip("/")
        self.todo = todo
        self.md = crear_markdown()
        self.paginas = 0
        self.env = Environment(
            loader=FileSystemLoader(RAIZ / "plantillas"),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.globals.update(
            sitio=sitio.meta,
            cursos=sitio.cursos,
            url=self.url,
            nav=self.navegacion(),
            nav_activa=self.nav_activa,
            contacto=self.contacto(),
            modo_borrador=todo,
        )
        self.env.filters["md"] = self.a_html
        self.env.filters["mdi"] = self.a_html_en_linea

    # ---- utilidades -------------------------------------------------------

    def url(self, ruta: str = "") -> str:
        ruta = ruta.strip("/")
        if not ruta:
            return f"{self.base}/"
        if "." in ruta.rsplit("/", 1)[-1]:
            return f"{self.base}/{ruta}"
        return f"{self.base}/{ruta}/"

    def a_html(self, texto: str, base: str = "") -> Markup:
        return Markup(self.md.render(texto or "", {"base": base}))

    def a_html_en_linea(self, texto: str) -> Markup:
        return Markup(self.md.renderInline(texto or ""))

    def navegacion(self) -> list[dict]:
        cursos = self.sitio.cursos
        if len(cursos) == 1:
            c = cursos[0]
            nav = [{"texto": "Problemas", "ruta": c.url}]
            if c.temas:
                nav.append({"texto": "Teoría", "ruta": f"{c.url}/teoria"})
            if c.simulaciones:
                nav.append({"texto": "Simulaciones", "ruta": f"{c.url}/simulaciones"})
        else:
            nav = [{"texto": c.meta["titulo"], "ruta": c.url} for c in cursos]
        nav.append({"texto": "Clases", "ruta": "clases"})
        return nav

    def nav_activa(self, ruta_actual: str) -> str:
        """Ruta de la entrada del menú que corresponde a la página actual."""
        # El formulario cuelga del curso, pero pertenece a la sección de teoría.
        if ruta_actual.endswith("/formulario"):
            ruta_actual = ruta_actual[: -len("formulario")] + "teoria/formulario"
        coinciden = [
            n["ruta"] for n in self.env.globals["nav"]
            if ruta_actual == n["ruta"] or ruta_actual.startswith(n["ruta"] + "/")
        ]
        return max(coinciden, key=len, default="")

    def contacto(self) -> dict:
        c = self.sitio.meta.get("contacto", {})
        whatsapp = re.sub(r"\D", "", str(c.get("whatsapp") or ""))
        correo = (c.get("correo") or "").strip()
        return {
            "whatsapp": f"https://wa.me/{whatsapp}" if whatsapp else "",
            "correo": correo,
        }

    @staticmethod
    def ancla(texto: str) -> str:
        """Identificador para enlazar un apartado: 'Leyes de Kepler' -> 'leyes-de-kepler'."""
        plano = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
        return re.sub(r"[^a-z0-9]+", "-", plano.lower()).strip("-")

    def visibles(self, curso: Curso) -> list[Problema]:
        return curso.problemas(solo_publicables=not self.todo)

    def escribir(self, ruta: str, plantilla: str, **contexto) -> None:
        destino = SALIDA / ruta.strip("/") / "index.html" if not ruta.endswith(".html") else SALIDA / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        html = self.env.get_template(plantilla).render(ruta_actual=ruta.strip("/"), **contexto)
        destino.write_text(html, encoding="utf-8", newline="\n")
        self.paginas += 1

    # ---- datos derivados --------------------------------------------------

    def ficha(self, p: Problema) -> dict:
        """Resumen de un problema para listados, filtros y problemas.json."""
        col = p.coleccion
        curso = col.curso
        subtemas = curso.subtemas(p.meta["bloque"])
        return {
            "id": p.id,
            "url": self.url(p.url),
            "numero": p.meta["numero"],
            "titulo": p.meta["titulo"],
            "coleccion": col.slug,
            "coleccion_etiqueta": col.etiqueta,
            "oficial": col.oficial,
            "anio": col.meta.get("anio"),
            "convocatoria": col.meta.get("convocatoria"),
            "bloque": p.meta["bloque"],
            "bloque_nombre": curso.bloques[p.meta["bloque"]]["nombre"],
            "subtemas": p.meta["subtemas"],
            "subtemas_nombres": [subtemas[s] for s in p.meta["subtemas"]],
            "dificultad": p.meta["dificultad"],
            "dificultad_nombre": curso.meta["dificultades"][p.meta["dificultad"]]["nombre"],
            "puntuacion": p.meta.get("puntuacion"),
            "estado": p.meta["estado"],
        }

    def resultados(self, p: Problema) -> list[dict]:
        """Resultados agrupados por apartado, ya en LaTeX."""
        grupos: dict[str, list[Markup]] = defaultdict(list)
        for r in p.meta["resultados"]:
            if "valor" in r:
                tex = f"{r['simbolo']} = {numero_tex(r['valor'], r['cifras'])}"
                if r.get("unidad"):
                    tex += f"\\ \\mathrm{{{r['unidad']}}}"
                grupos[r["apartado"]].append(Markup(f'<span class="math inline">{Markup.escape(tex)}</span>'))
            else:
                grupos[r["apartado"]].append(self.a_html_en_linea(r["texto"]))
        return [{"apartado": a, "lineas": ls} for a, ls in grupos.items()]

    # ---- páginas ----------------------------------------------------------

    def construir(self) -> None:
        if SALIDA.exists():
            shutil.rmtree(SALIDA)
        SALIDA.mkdir()
        shutil.copytree(RAIZ / "static", SALIDA / "static")
        (SALIDA / ".nojekyll").write_text("", encoding="utf-8")

        resumen_cursos = []
        for curso in self.sitio.cursos:
            resumen_cursos.append(self.construir_curso(curso))

        self.escribir("", "portada.html", resumen_cursos=resumen_cursos)
        self.escribir("clases", "clases.html", clases=self.sitio.clases)
        self.escribir("404.html", "404.html")

    def construir_curso(self, curso: Curso) -> dict:
        problemas = self.visibles(curso)
        fichas = {p.id: self.ficha(p) for p in problemas}
        por_bloque: dict[str, list[Problema]] = defaultdict(list)
        for p in problemas:
            por_bloque[p.meta["bloque"]].append(p)
        bloques = [
            {**b, "total": len(por_bloque[b["id"]]), "ruta": f"{curso.url}/bloques/{b['id']}"}
            for b in curso.meta["bloques"]
        ]
        colecciones = [
            {"col": c, "problemas": [fichas[p.id] for p in c.problemas if p.id in fichas]}
            for c in curso.colecciones
        ]
        colecciones = [c for c in colecciones if c["problemas"]]
        sims_por_id = {s.id: s for s in curso.simulaciones}
        temas = {t.bloque: t for t in curso.temas}

        self.escribir(
            curso.url, "curso.html",
            curso=curso, bloques=bloques, colecciones=colecciones, fichas=list(fichas.values()),
        )

        # Índice de datos para los filtros y el generador de hojas.
        destino = SALIDA / curso.url / "problemas.json"
        destino.write_text(
            json.dumps(list(fichas.values()), ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )

        for b in bloques:
            grupos = []
            for s in b["subtemas"]:
                lista = [fichas[p.id] for p in por_bloque[b["id"]] if s["id"] in p.meta["subtemas"]]
                if lista:
                    grupos.append({"subtema": s, "problemas": lista})
            sims = [s for s in curso.simulaciones if s.meta["bloque"] == b["id"]]
            self.escribir(b["ruta"], "bloque.html", curso=curso, bloque=b, grupos=grupos, simulaciones=sims,
                          tema=temas.get(b["id"]))

        for c in colecciones:
            col = c["col"]
            for f in col.ruta.iterdir():
                if f.suffix.lower() in EXT_RECURSOS:
                    (SALIDA / col.url).mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, SALIDA / col.url / f.name)
            self.escribir(col.url, "coleccion.html", curso=curso, col=col, problemas=c["problemas"],
                          convocatoria=NOMBRE_CONVOCATORIA.get(col.meta.get("convocatoria"), ""))
            lista = [p for p in col.problemas if p.id in fichas]
            for i, p in enumerate(lista):
                parecidos = [
                    fichas[q.id] for q in por_bloque[p.meta["bloque"]]
                    if q.id != p.id and set(q.meta["subtemas"]) & set(p.meta["subtemas"])
                ][:4]
                self.escribir(
                    p.url, "problema.html",
                    curso=curso, col=col, p=p, ficha=fichas[p.id],
                    base_recursos=self.url(col.url).rstrip("/"),
                    nombres_seccion=SECCIONES,
                    resultados=self.resultados(p),
                    simulaciones=[
                        {"sim": sims_por_id[s],
                         "url": self.url(sims_por_id[s].url) + self.consulta(p, s)}
                        for s in p.meta.get("simulaciones", [])
                    ],
                    tema=temas.get(p.meta["bloque"]),
                    parecidos=parecidos,
                    anterior=fichas[lista[i - 1].id] if i > 0 else None,
                    siguiente=fichas[lista[i + 1].id] if i + 1 < len(lista) else None,
                )

        if curso.simulaciones:
            self.escribir(f"{curso.url}/simulaciones", "simulaciones.html", curso=curso)
            for s in curso.simulaciones:
                usada_en = [fichas[p.id] for p in problemas if s.id in p.meta.get("simulaciones", [])]
                self.escribir(s.url, "simulacion.html", curso=curso, sim=s, usada_en=usada_en,
                              bloque=curso.bloques[s.meta["bloque"]])

        if curso.temas:
            self.construir_teoria(curso, bloques)

        return {"curso": curso, "bloques": bloques, "total": len(problemas),
                "examenes": sum(1 for c in colecciones if c["col"].oficial)}

    @staticmethod
    def consulta(p: Problema, sim: str) -> str:
        """Parámetros con los que un problema abre una simulación ya rellena."""
        parametros = p.meta.get("parametros_simulacion", {}).get(sim, "")
        return f"?{parametros}" if parametros else ""

    def construir_teoria(self, curso: Curso, bloques: list[dict]) -> None:
        """Índice de teoría, una página por bloque y el formulario completo."""
        dir_teoria = curso.ruta / "teoria"
        base = f"{curso.url}/teoria"
        for f in dir_teoria.iterdir():
            if f.suffix.lower() in EXT_RECURSOS:
                (SALIDA / base).mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, SALIDA / base / f.name)

        por_id = {b["id"]: b for b in bloques}
        temas = []
        for t in curso.temas:
            trozos = trocear(t.cuerpo, 2)
            temas.append({
                "tema": t,
                "bloque": por_id[t.bloque],
                "intro": trozos[0][1],
                "apartados": [{"titulo": tit, "ancla": self.ancla(tit), "texto": txt} for tit, txt in trozos[1:]],
                "simulaciones": [s for s in curso.simulaciones if s.meta["bloque"] == t.bloque],
            })
        self.escribir(base, "teoria.html", curso=curso, temas=temas)
        self.escribir(f"{curso.url}/formulario", "formulario.html", curso=curso, temas=temas)
        for i, t in enumerate(temas):
            self.escribir(
                t["tema"].url, "tema.html", curso=curso, base_recursos=self.url(base).rstrip("/"), **t,
                anterior=temas[i - 1] if i > 0 else None,
                siguiente=temas[i + 1] if i + 1 < len(temas) else None,
            )

    # ---- comprobaciones finales ------------------------------------------

    def enlaces_rotos(self) -> list[str]:
        """Busca enlaces internos que no llevan a ningún archivo generado."""
        rotos = []
        patron = re.compile(r'(?:href|src)="([^"]+)"')
        prefijo = f"{self.base}/"
        for html in SALIDA.rglob("*.html"):
            for destino in patron.findall(html.read_text(encoding="utf-8")):
                if not destino.startswith(prefijo) or destino.startswith("//"):
                    continue
                ruta = destino[len(prefijo):].split("#")[0].split("?")[0]
                archivo = SALIDA / ruta
                if ruta == "" or ruta.endswith("/"):
                    archivo = archivo / "index.html"
                if not archivo.is_file():
                    rotos.append(f"{html.relative_to(SALIDA).as_posix()} -> {destino}")
        return rotos


def main() -> int:
    ap = argparse.ArgumentParser(description="Genera el sitio estático en _site/")
    ap.add_argument("--todo", action="store_true", help="incluye borradores y problemas por revisar")
    ap.add_argument("--base-url", default=None, help='prefijo de rutas, p. ej. "/fisica-pau"')
    args = ap.parse_args()

    try:
        sitio = cargar_sitio()
    except ErrorContenido as e:
        print(f"ERROR de contenido\n{e}")
        return 1

    base = args.base_url
    if base is None:
        base = os.environ.get("BASE_URL", sitio.meta.get("base_url", ""))
    c = Constructor(sitio, base or "", args.todo)
    c.construir()

    rotos = c.enlaces_rotos()
    if rotos:
        print("ERROR: enlaces internos rotos")
        for r in rotos:
            print("  " + r)
        return 1

    ocultos = sum(
        1 for curso in sitio.cursos for p in curso.problemas(solo_publicables=False) if not p.publicable
    )
    print(f"{c.paginas} páginas en {SALIDA.relative_to(RAIZ)}/ · base_url='{c.base}'")
    if ocultos:
        print(f"{ocultos} problemas sin verificar " + ("incluidos con aviso (--todo)" if args.todo else "no publicados"))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
