// Simulación de hilos: usa el motor común de campo2d.js.
import { montarCampo } from "./campo2d.js";

export const montar = (contenedor) => montarCampo(contenedor, "hilos");
