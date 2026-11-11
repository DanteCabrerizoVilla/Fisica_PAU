"""Carga y validación del contenido. Lo comparten build.py y verificar.py."""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

RAIZ = Path(__file__).resolve().parent.parent
CONTENIDO = RAIZ / "contenido"
ESQUEMA = json.loads((Path(__file__).parent / "esquema.json").read_text(encoding="utf-8"))

# Nombres de carpeta reservados dentro de un curso: no pueden ser colecciones.
RESERVADOS = {"bloques", "simulaciones", "hojas", "teoria", "formulario", "prueba-nivel"}

ORDEN_CONVOCATORIA = {
    "modelo": 0,
    "ordinaria": 1,
    "ordinaria-coincidentes": 2,
    "extraordinaria": 3,
    "extraordinaria-coincidentes": 4,
}
NOMBRE_CONVOCATORIA = {
    "modelo": "Modelo",
    "ordinaria": "Ordinaria",
    "ordinaria-coincidentes": "Ordinaria (coincidentes)",
    "extraordinaria": "Extraordinaria",
    "extraordinaria-coincidentes": "Extraordinaria (coincidentes)",
}

# Secciones (## ...) que puede tener la solución de un problema.
SECCIONES = {
    "enunciado": "Enunciado",
    "datos": "Datos",
    "planteamiento": "Planteamiento",
    "resolucion": "Resolución",
    "errores": "Errores típicos",
}
SECCIONES_OBLIGATORIAS = ("enunciado", "resolucion")


class ErrorContenido(Exception):
    """Fallo en los datos que impide construir o verificar."""


@dataclass
class Problema:
    ruta: Path
    slug: str
    meta: dict
    secciones: dict[str, str]          # clave de SECCIONES -> Markdown
    apartados: list[tuple[str, str]]   # (título del ###, Markdown) dentro de Resolución
    coleccion: "Coleccion" = None

    @property
    def id(self) -> str:
        return self.meta["id"]

    @property
    def publicable(self) -> bool:
        return self.meta["estado"] == "verificado"

    @property
    def script(self) -> Path:
        return self.ruta.with_suffix(".py")

    @property
    def url(self) -> str:
        return f"{self.coleccion.url}/{self.slug}"


@dataclass
class Coleccion:
    ruta: Path
    slug: str
    meta: dict
    curso: "Curso" = None
    problemas: list[Problema] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"{self.curso.url}/{self.slug}"

    @property
    def oficial(self) -> bool:
        return self.meta["tipo"] == "examen-oficial"

    @property
    def prueba(self) -> str:
        """Nombre de la prueba el año del examen (EvAU hasta 2024, PAU después)."""
        return nombre_prueba(self.curso.meta, self.meta.get("anio"))

    @property
    def etiqueta(self) -> str:
        """Texto corto para migas y listados."""
        if self.oficial:
            conv = NOMBRE_CONVOCATORIA[self.meta["convocatoria"]]
            return f"{self.prueba} {self.meta['anio']} · {conv}"
        return self.meta["titulo"]

    @property
    def orden(self):
        if self.oficial:
            return (0, -self.meta["anio"], ORDEN_CONVOCATORIA[self.meta["convocatoria"]])
        return (1, 0, 0, self.slug)


@dataclass
class Simulacion:
    ruta: Path
    meta: dict
    cuerpo: str
    curso: "Curso" = None

    @property
    def id(self) -> str:
        return self.meta["id"]

    @property
    def url(self) -> str:
        return f"{self.curso.url}/simulaciones/{self.id}"


@dataclass
class Tema:
    """Teoría y fórmulas de un bloque (teoria/<bloque>.md)."""
    ruta: Path
    meta: dict
    cuerpo: str
    curso: "Curso" = None

    @property
    def bloque(self) -> str:
        return self.meta["bloque"]

    @property
    def url(self) -> str:
        return f"{self.curso.url}/teoria/{self.bloque}"


@dataclass
class Curso:
    ruta: Path
    url: str                            # p. ej. "fisica/2-bachillerato"
    meta: dict
    colecciones: list[Coleccion] = field(default_factory=list)
    simulaciones: list[Simulacion] = field(default_factory=list)
    temas: list[Tema] = field(default_factory=list)
    prueba: dict | None = None          # prueba de nivel (prueba-nivel.yaml), si existe

    @property
    def ruta_prueba(self) -> Path:
        return self.ruta / "prueba-nivel.yaml"

    @property
    def bloques(self) -> dict[str, dict]:
        return {b["id"]: b for b in self.meta["bloques"]}

    def subtemas(self, bloque: str) -> dict[str, str]:
        return {s["id"]: s["nombre"] for s in self.bloques[bloque]["subtemas"]}

    def problemas(self, solo_publicables: bool = True) -> list[Problema]:
        return [
            p
            for c in self.colecciones
            for p in c.problemas
            if p.publicable or not solo_publicables
        ]


@dataclass
class Sitio:
    meta: dict
    cursos: list[Curso]
    clases: dict


# --------------------------------------------------------------------------
# Lectura de archivos
# --------------------------------------------------------------------------

class _Cargador(yaml.SafeLoader):
    """SafeLoader que entiende 7.56e3 como número.

    PyYAML sigue YAML 1.1, que exige signo en el exponente (7.56e+3) y deja
    7.56e3 como texto. Aquí se aceptan las dos formas.
    """


_Cargador.add_implicit_resolver(
    "tag:yaml.org,2002:float",
    re.compile(r"^[-+]?(?:\d[\d_]*\.?\d*|\.\d+)[eE][-+]?\d+$"),
    list("-+0123456789."),
)


def nombre_prueba(meta_curso: dict, anio: int | None) -> str:
    """Nombre de la prueba de acceso en un año dado."""
    if anio is not None:
        for anterior in sorted(meta_curso.get("nombres_anteriores", []), key=lambda n: n["hasta"]):
            if anio <= anterior["hasta"]:
                return anterior["nombre"]
    return meta_curso["prueba"]


def cargar_yaml(texto: str) -> dict:
    return yaml.load(texto, Loader=_Cargador) or {}


def leer_yaml(ruta: Path) -> dict:
    return cargar_yaml(ruta.read_text(encoding="utf-8"))


def separar_cabecera(ruta: Path) -> tuple[dict, str]:
    """Devuelve (cabecera YAML, cuerpo Markdown) de un archivo con '---'."""
    texto = ruta.read_text(encoding="utf-8")
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", texto, re.S)
    if not m:
        raise ErrorContenido(f"{relativa(ruta)}: falta la cabecera YAML entre '---'")
    return cargar_yaml(m.group(1)), m.group(2)


def relativa(ruta: Path) -> str:
    try:
        return ruta.relative_to(RAIZ).as_posix()
    except ValueError:
        return str(ruta)


def validar(meta: dict, tipo: str, ruta: Path) -> None:
    esquema = {"$ref": f"#/$defs/{tipo}", "$defs": ESQUEMA["$defs"]}
    errores = sorted(Draft202012Validator(esquema).iter_errors(meta), key=lambda e: list(e.path))
    if errores:
        lineas = [f"  - {'/'.join(map(str, e.path)) or '(raíz)'}: {e.message}" for e in errores]
        raise ErrorContenido(f"{relativa(ruta)}: cabecera no válida\n" + "\n".join(lineas))


def _normalizar(titulo: str) -> str:
    return re.sub(r"\s+", " ", titulo.strip().lower())


def trocear(cuerpo: str, nivel: int) -> list[tuple[str, str]]:
    """Parte un Markdown por encabezados del nivel dado. Devuelve (título, texto)."""
    marca = "#" * nivel + " "
    trozos: list[tuple[str, list[str]]] = [("", [])]
    en_codigo = False
    for linea in cuerpo.splitlines():
        if linea.lstrip().startswith("```"):
            en_codigo = not en_codigo
        if not en_codigo and linea.startswith(marca):
            trozos.append((linea[len(marca):].strip(), []))
        else:
            trozos[-1][1].append(linea)
    return [(t, "\n".join(ls).strip()) for t, ls in trozos]


def cargar_problema(ruta: Path) -> Problema:
    meta, cuerpo = separar_cabecera(ruta)
    validar(meta, "problema", ruta)

    por_titulo = {_normalizar(v): k for k, v in SECCIONES.items()}
    secciones: dict[str, str] = {}
    for titulo, texto in trocear(cuerpo, 2):
        if not titulo:
            if texto:
                raise ErrorContenido(f"{relativa(ruta)}: hay texto antes del primer '## '")
            continue
        clave = por_titulo.get(_normalizar(titulo))
        if clave is None:
            validas = ", ".join(SECCIONES.values())
            raise ErrorContenido(f"{relativa(ruta)}: sección '{titulo}' desconocida (válidas: {validas})")
        secciones[clave] = texto
    # Un borrador puede estar a medias; lo que se publica no.
    for clave in SECCIONES_OBLIGATORIAS:
        if not secciones.get(clave) and meta["estado"] == "verificado":
            raise ErrorContenido(f"{relativa(ruta)}: falta la sección '## {SECCIONES[clave]}'")
        secciones.setdefault(clave, "")

    trozos = trocear(secciones["resolucion"], 3)
    intro = trozos[0][1]
    apartados = [(t, x) for t, x in trozos[1:]]
    if not apartados:
        apartados = [("Resolución", intro)]
        intro = ""
    secciones["resolucion"] = intro
    return Problema(ruta=ruta, slug=ruta.stem, meta=meta, secciones=secciones, apartados=apartados)


def cargar_curso(ruta_rel: str) -> Curso:
    ruta = CONTENIDO / ruta_rel
    if not (ruta / "curso.yaml").exists():
        raise ErrorContenido(f"contenido/{ruta_rel}: no existe curso.yaml")
    curso = Curso(ruta=ruta, url=ruta_rel.strip("/"), meta=leer_yaml(ruta / "curso.yaml"))

    dir_sim = ruta / "simulaciones"
    if dir_sim.is_dir():
        for f in sorted(dir_sim.glob("*.md")):
            meta, cuerpo = separar_cabecera(f)
            validar(meta, "simulacion", f)
            if meta["bloque"] not in curso.bloques:
                raise ErrorContenido(f"{relativa(f)}: bloque '{meta['bloque']}' no existe en curso.yaml")
            curso.simulaciones.append(Simulacion(ruta=f, meta=meta, cuerpo=cuerpo, curso=curso))
    ids_sim = {s.id for s in curso.simulaciones}

    dir_teoria = ruta / "teoria"
    if dir_teoria.is_dir():
        orden = list(curso.bloques)
        for f in sorted(dir_teoria.glob("*.md")):
            meta, cuerpo = separar_cabecera(f)
            validar(meta, "tema", f)
            if meta["bloque"] not in curso.bloques:
                raise ErrorContenido(f"{relativa(f)}: bloque '{meta['bloque']}' no existe en curso.yaml")
            if f.stem != meta["bloque"]:
                raise ErrorContenido(f"{relativa(f)}: el archivo debe llamarse {meta['bloque']}.md")
            curso.temas.append(Tema(ruta=f, meta=meta, cuerpo=cuerpo, curso=curso))
        curso.temas.sort(key=lambda t: orden.index(t.bloque))

    if curso.ruta_prueba.exists():
        curso.prueba = cargar_prueba(curso)

    dir_col = ruta / "colecciones"
    for carpeta in sorted(p for p in dir_col.iterdir() if p.is_dir()) if dir_col.is_dir() else []:
        f_col = carpeta / "coleccion.yaml"
        if not f_col.exists():
            raise ErrorContenido(f"{relativa(carpeta)}: falta coleccion.yaml")
        if carpeta.name in RESERVADOS:
            raise ErrorContenido(f"{relativa(carpeta)}: '{carpeta.name}' es un nombre reservado")
        meta = leer_yaml(f_col)
        validar(meta, "coleccion", f_col)
        col = Coleccion(ruta=carpeta, slug=carpeta.name, meta=meta, curso=curso)
        for f in sorted(carpeta.glob("*.md"), key=lambda p: _orden_natural(p.stem)):
            p = cargar_problema(f)
            p.coleccion = col
            _comprobar_referencias(p, curso, ids_sim)
            col.problemas.append(p)
        curso.colecciones.append(col)
    curso.colecciones.sort(key=lambda c: c.orden)
    return curso


def cargar_prueba(curso: Curso) -> dict:
    """Lee y valida la prueba de nivel de un curso."""
    f = curso.ruta_prueba
    donde = relativa(f)
    datos = leer_yaml(f)
    for clave in ("titulo", "entrada", "instrucciones", "resultado", "mensaje_final", "preguntas"):
        if not datos.get(clave):
            raise ErrorContenido(f"{donde}: falta '{clave}'")
    vistos: set[str] = set()
    for q in datos["preguntas"]:
        ident = q.get("id", "(sin id)")
        for clave in ("id", "bloque", "subtema", "mide", "enunciado", "opciones"):
            if not q.get(clave):
                raise ErrorContenido(f"{donde}: a la pregunta {ident} le falta '{clave}'")
        if not re.fullmatch(r"[a-z0-9-]+", ident):
            raise ErrorContenido(f"{donde}: id '{ident}' no válido (minúsculas, cifras y guiones)")
        if ident in vistos:
            raise ErrorContenido(f"{donde}: id de pregunta repetido '{ident}'")
        vistos.add(ident)
        if q["bloque"] not in curso.bloques:
            raise ErrorContenido(f"{donde}: {ident}: bloque '{q['bloque']}' no existe en curso.yaml")
        if q["subtema"] not in curso.subtemas(q["bloque"]):
            raise ErrorContenido(f"{donde}: {ident}: subtema '{q['subtema']}' no pertenece a '{q['bloque']}'")
        if len(q["opciones"]) != 4 or len(set(q["opciones"])) != 4:
            raise ErrorContenido(f"{donde}: {ident}: debe tener cuatro opciones distintas")
    return datos


def _orden_natural(texto: str):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", texto)]


def _comprobar_referencias(p: Problema, curso: Curso, ids_sim: set[str]) -> None:
    donde = relativa(p.ruta)
    bloque = p.meta["bloque"]
    if bloque not in curso.bloques:
        raise ErrorContenido(f"{donde}: bloque '{bloque}' no existe en curso.yaml")
    validos = curso.subtemas(bloque)
    for s in p.meta["subtemas"]:
        if s not in validos:
            raise ErrorContenido(f"{donde}: subtema '{s}' no pertenece al bloque '{bloque}'")
    for s in p.meta.get("simulaciones", []):
        if s not in ids_sim:
            raise ErrorContenido(f"{donde}: la simulación '{s}' no existe")
    for s in p.meta.get("parametros_simulacion", {}):
        if s not in p.meta.get("simulaciones", []):
            raise ErrorContenido(f"{donde}: hay parámetros para '{s}', que no está en 'simulaciones'")
    claves = [r["clave"] for r in p.meta["resultados"]]
    if len(claves) != len(set(claves)):
        raise ErrorContenido(f"{donde}: hay claves de resultado repetidas")
    if p.meta["estado"] == "revisar" and not p.meta.get("revisar"):
        raise ErrorContenido(f"{donde}: estado 'revisar' sin explicar el motivo en 'revisar'")


def cargar_sitio() -> Sitio:
    meta = leer_yaml(CONTENIDO / "sitio.yaml")
    cursos = [cargar_curso(r) for r in meta["cursos"]]
    vistos: dict[str, Path] = {}
    for curso in cursos:
        for p in curso.problemas(solo_publicables=False):
            if p.id in vistos:
                raise ErrorContenido(f"id repetido '{p.id}': {relativa(p.ruta)} y {relativa(vistos[p.id])}")
            vistos[p.id] = p.ruta
    f_clases = CONTENIDO / "clases.yaml"
    clases = leer_yaml(f_clases) if f_clases.exists() else {}
    return Sitio(meta=meta, cursos=cursos, clases=clases)


# --------------------------------------------------------------------------
# Formato de números
# --------------------------------------------------------------------------

def redondear_cifras(valor: float, cifras: int) -> float:
    """Redondea a un número de cifras significativas."""
    if valor == 0:
        return 0.0
    exp = math.floor(math.log10(abs(valor)))
    return round(valor, cifras - 1 - exp)


def numero_tex(valor: float, cifras: int) -> str:
    """Número en LaTeX con coma decimal y las cifras significativas pedidas.

    Usa notación científica cuando la decimal sería larga o ambigua
    (7670 con tres cifras se escribe 7,67·10^3).
    """
    if valor == 0:
        return "0"
    valor = redondear_cifras(valor, cifras)
    exp = math.floor(math.log10(abs(valor)))
    decimales = cifras - 1 - exp
    if -2 <= exp <= 3 and decimales >= 0:
        texto = f"{valor:.{decimales}f}"
    else:
        mantisa = f"{valor / 10 ** exp:.{cifras - 1}f}"
        texto = f"{mantisa}\\cdot 10^{{{exp}}}"
    return texto.replace(".", "{,}")
