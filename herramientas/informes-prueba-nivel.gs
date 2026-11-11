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
 */

const AVISAR_POR_CORREO = true;
const HOJA = "Resultados";
const CABECERA = ["Fecha", "Correo", "Nombre", "Acepta publicidad", "Aciertos", "Total",
                  "Por bloque", "Falla", "No sabe", "Variantes"];

function doPost(e) {
  try {
    const datos = JSON.parse(e.postData.contents);
    const fila = validar(datos);
    const cerrojo = LockService.getScriptLock();
    cerrojo.waitLock(10000);
    try {
      hoja().appendRow(fila);
    } finally {
      cerrojo.releaseLock();
    }
    if (AVISAR_POR_CORREO) avisar(datos);
    return respuesta({ ok: true });
  } catch (error) {
    return respuesta({ ok: false, error: String(error) });
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
  if (!(total > 0 && total <= 60 && aciertos >= 0 && aciertos <= total)) throw new Error("resultado no válido");
  const bloques = Array.isArray(d.bloques) ? d.bloques.slice(0, 12) : [];
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
  ];
}

function avisar(d) {
  const lineas = [
    "Correo: " + limpio(d.correo, 120),
    "Nombre: " + (limpio(d.nombre, 40) || "(no lo ha puesto)"),
    "Acepta recibir publicidad: " + (d.publicidad === true ? "SÍ" : "NO"),
    "Resultado: " + Number(d.aciertos) + " de " + Number(d.total),
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
