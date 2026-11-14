/**
 * Receptor de los resultados de la prueba de nivel (Google Apps Script).
 *
 * Qué hace: cada vez que un alumno termina la prueba, la web envía aquí su
 * correo y su resultado. Este programa añade una fila a la hoja de cálculo y
 * te manda un correo con el informe.
 *
 * Puesta en marcha (una sola vez, unos 5 minutos):
 *
 *  1. Crea una hoja de cálculo nueva en Google Sheets, con tu cuenta.
 *  2. Menú Extensiones → Apps Script. Borra lo que haya y pega este archivo entero.
 *  3. Pulsa Implementar → Nueva implementación → tipo «Aplicación web».
 *       - Ejecutar como: Yo
 *       - Quién tiene acceso: Cualquier usuario
 *     Acepta los permisos que pide (escribir en la hoja y enviarte correo).
 *  4. Copia la «URL de la aplicación web» (termina en /exec) y pégala en
 *     contenido/sitio.yaml, en contacto → informes_url.
 *
 * Si más adelante cambias este código, hay que hacer Implementar → Gestionar
 * implementaciones → editar → Versión nueva, o seguirá funcionando el antiguo.
 *
 * Los correos de aviso llegan a la cuenta de Google dueña de la hoja. Para
 * dejar de recibirlos, pon AVISAR_POR_CORREO en false.
 *
 * Protección contra envíos automáticos (spam). La dirección /exec es pública:
 * cualquiera que la conozca puede mandar datos. Por eso, antes de apuntar nada,
 * se comprueba que el envío parece de una persona que ha hecho la prueba:
 *   - el campo trampa, invisible para las personas, llega vacío;
 *   - el resultado es coherente (30 preguntas, aciertos que cuadran por bloque,
 *     identificadores de pregunta reales);
 *   - la prueba ha durado un tiempo razonable;
 *   - el navegador ha resuelto un pequeño cálculo («sello») ligado a ese
 *     resultado, que a una persona no le cuesta nada y a un programa que mande
 *     miles de envíos sí;
 *   - el mismo envío no se acepta dos veces;
 *   - hay un máximo de envíos por correo y por hora.
 * Los límites están en las constantes de abajo.
 */

const AVISAR_POR_CORREO = true;
const HOJA = "Resultados";
const CABECERA = ["Fecha", "Correo", "Nombre", "Acepta publicidad", "Aciertos", "Total",
                  "Por bloque", "Falla", "No sabe", "Variantes", "Duración (min)"];

// ---- Límites contra spam ----------------------------------------------------
const PREGUNTAS = 30;               // número de preguntas de la prueba
const DURACION_MINIMA = 90;         // segundos: menos que esto no es una persona leyendo
const DURACION_MAXIMA = 6 * 3600;   // segundos
const DIFICULTAD = "000";           // el sello SHA-256 debe empezar así (igual que en la web)
const POR_CORREO_Y_HORA = 3;        // envíos aceptados del mismo correo en una hora
const POR_HORA = 40;                // envíos aceptados en total en una hora
const AVISOS_POR_DIA = 60;          // correos de aviso al día (Gmail limita a 100)
const TAMANO_MAXIMO = 20000;        // caracteres del envío

function doPost(e) {
  const cerrojo = LockService.getScriptLock();
  try {
    const texto = (e && e.postData && e.postData.contents) || "";
    if (texto.length > TAMANO_MAXIMO) throw new Error("envío demasiado grande");
    const datos = JSON.parse(texto);
    cerrojo.waitLock(10000);
    let avisar_ = false;
    try {
      revisar(datos, Date.now());
      hoja().appendRow(validar(datos));
      avisar_ = AVISAR_POR_CORREO && contar("avisos:" + dia(), 86400) <= AVISOS_POR_DIA;
    } finally {
      cerrojo.releaseLock();
    }
    if (avisar_) avisar(datos);
    return respuesta({ ok: true });
  } catch (error) {
    return respuesta({ ok: false, error: String(error && error.message || error) });
  }
}

/** Abrir la dirección en el navegador sirve para comprobar que está en marcha. */
function doGet() {
  return respuesta({ ok: true, mensaje: "Receptor de la prueba de nivel en marcha." });
}

function respuesta(objeto) {
  return ContentService.createTextOutput(JSON.stringify(objeto)).setMimeType(ContentService.MimeType.JSON);
}

function hoja() {
  const libro = SpreadsheetApp.getActiveSpreadsheet();
  let h = libro.getSheetByName(HOJA);
  if (!h) {
    h = libro.insertSheet(HOJA);
    h.appendRow(CABECERA);
    h.setFrozenRows(1);
    h.getRange(1, 1, 1, CABECERA.length).setFontWeight("bold");
  }
  return h;
}

// ---- Comprobaciones contra spam ---------------------------------------------

/** Lanza un error si el envío no parece de una persona. Si lo acepta, apunta los contadores. */
function revisar(d, ahora) {
  if (!d || typeof d !== "object") throw new Error("formato no válido");
  if (d.web) throw new Error("campo trampa relleno");
  validar(d);                                   // estructura y coherencia del resultado

  const duracion = Number(d.duracion);
  if (!(duracion >= DURACION_MINIMA && duracion <= DURACION_MAXIMA)) throw new Error("duración no válida");
  const t = Number(d.t);
  if (!(t > ahora - 3600 * 1000 && t < ahora + 5 * 60 * 1000)) throw new Error("hora no válida");

  const huella = sha256(textoSello(d));
  if (huella.indexOf(DIFICULTAD) !== 0) throw new Error("sello no válido");

  const cache = CacheService.getScriptCache();
  if (cache.get("sello:" + huella)) throw new Error("envío repetido");
  const correo = String(d.correo).trim().toLowerCase();
  if (leer("correo:" + correo) >= POR_CORREO_Y_HORA) throw new Error("demasiados envíos de este correo");
  if (leer("hora:" + hora()) >= POR_HORA) throw new Error("demasiados envíos esta hora");

  cache.put("sello:" + huella, "1", 21600);
  contar("correo:" + correo, 3600);
  contar("hora:" + hora(), 3600);
}

/** Texto sobre el que el navegador calcula el sello (debe coincidir con prueba-nivel.js). */
function textoSello(d) {
  return [String(d.correo).trim().toLowerCase(), d.aciertos, d.total, d.variantes, d.t, d.duracion, d.sello].join("|");
}

function sha256(texto) {
  const bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, texto, Utilities.Charset.UTF_8);
  return bytes.map(function (b) { return ((b + 256) % 256).toString(16).padStart(2, "0"); }).join("");
}

function leer(clave) {
  return Number(CacheService.getScriptCache().get(clave) || 0);
}

function contar(clave, segundos) {
  const n = leer(clave) + 1;
  CacheService.getScriptCache().put(clave, String(n), segundos);
  return n;
}

function hora() { return Utilities.formatDate(new Date(), "UTC", "yyyyMMddHH"); }
function dia() { return Utilities.formatDate(new Date(), "UTC", "yyyyMMdd"); }

// ---- Validación y fila de la hoja ---------------------------------------------

/** Texto corto y sin fórmulas: lo que llega de internet no se ejecuta en la hoja. */
function limpio(valor, maximo) {
  let texto = String(valor == null ? "" : valor).replace(/[\u0000-\u001f]/g, " ").trim().slice(0, maximo);
  if (/^[=+\-@]/.test(texto)) texto = "'" + texto;
  return texto;
}

function validar(d) {
  const correo = String(d.correo || "").trim();
  if (correo.length > 120 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) throw new Error("correo no válido");
  const total = Number(d.total);
  const aciertos = Number(d.aciertos);
  if (!(total === PREGUNTAS && Number.isInteger(aciertos) && aciertos >= 0 && aciertos <= total)) {
    throw new Error("resultado no válido");
  }
  const variantes = String(d.variantes || "").split(" ");
  if (variantes.length !== total || !variantes.every(function (v) { return /^[a-z]{2,6}-\d{1,2}[a-h]$/.test(v); })) {
    throw new Error("variantes no válidas");
  }
  if (!Array.isArray(d.bloques) || d.bloques.length < 1 || d.bloques.length > 12) throw new Error("bloques no válidos");
  let sumaAciertos = 0;
  let sumaTotal = 0;
  d.bloques.forEach(function (b) {
    const a = Number(b.aciertos);
    const n = Number(b.total);
    if (!(Number.isInteger(a) && Number.isInteger(n) && a >= 0 && a <= n)) throw new Error("bloque no válido");
    sumaAciertos += a;
    sumaTotal += n;
  });
  if (sumaAciertos !== aciertos || sumaTotal !== total) throw new Error("los bloques no cuadran");

  const bloques = d.bloques.slice(0, 12);
  const lista = (clave) => bloques
    .map((b) => (Array.isArray(b[clave]) ? b[clave] : []).slice(0, 12).map((x) => limpio(x, 90)))
    .reduce((todas, x) => todas.concat(x), [])
    .join("; ");
  return [
    new Date(),
    limpio(correo, 120),
    limpio(d.nombre, 40),
    d.publicidad === true ? "SÍ" : "NO",
    aciertos,
    total,
    bloques.map((b) => limpio(b.nombre, 40) + " " + Number(b.aciertos) + "/" + Number(b.total)).join("; "),
    lista("falla"),
    lista("no_sabe"),
    limpio(d.variantes, 400),
    Math.round(Number(d.duracion) / 6) / 10,
  ];
}

function avisar(d) {
  const lineas = [
    "Correo: " + limpio(d.correo, 120),
    "Nombre: " + (limpio(d.nombre, 40) || "(no lo ha puesto)"),
    "Acepta recibir publicidad: " + (d.publicidad === true ? "SÍ" : "NO"),
    "Resultado: " + Number(d.aciertos) + " de " + Number(d.total),
    "Tiempo: " + Math.round(Number(d.duracion) / 60) + " min",
    "",
  ];
  (Array.isArray(d.bloques) ? d.bloques.slice(0, 12) : []).forEach(function (b) {
    lineas.push(limpio(b.nombre, 40) + ": " + Number(b.aciertos) + "/" + Number(b.total) + " · " + limpio(b.valoracion, 40));
    (Array.isArray(b.falla) ? b.falla : []).slice(0, 12).forEach(function (x) { lineas.push("   ✗ " + limpio(x, 90)); });
    (Array.isArray(b.no_sabe) ? b.no_sabe : []).slice(0, 12).forEach(function (x) { lineas.push("   ? " + limpio(x, 90) + " (no lo sabe)"); });
  });
  MailApp.sendEmail({
    to: Session.getEffectiveUser().getEmail(),
    subject: "Prueba de nivel: " + Number(d.aciertos) + "/" + Number(d.total) + " · " + limpio(d.correo, 120),
    body: lineas.join("\n"),
  });
}
