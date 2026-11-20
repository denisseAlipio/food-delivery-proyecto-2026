// Prueba de la app web: el predictor JavaScript debe dar las mismas predicciones que WEKA.
const fs = require("fs"), path = require("path");
const M5P = require(path.join(__dirname, "..", "app", "m5p.js"));
const raiz = path.join(__dirname, "..");
const modelo = JSON.parse(fs.readFileSync(path.join(raiz, "models", "m5p_tree.json"), "utf8"));
const [cab, dat] = fs.readFileSync(path.join(raiz, "data", "test.arff"), "utf8").split("@data");
const cols = cab.split("\n").filter(l => l.toLowerCase().startsWith("@attribute")).map(l => l.split(/\s+/)[1]);
const filas = dat.trim().split("\n").map(l => {
  const v = l.match(/('[^']*'|[^,]+)/g).map(s => s.replace(/'/g, "").trim());
  return Object.fromEntries(cols.map((c, i) => [c, v[i]]));
});
const weka = fs.readFileSync(path.join(__dirname, "predicciones_weka_test.csv"), "utf8").trim().split("\n").map(Number);
let maxDif = 0;
filas.forEach((f, i) => { maxDif = Math.max(maxDif, Math.abs(M5P.predecir(modelo, f).minutos - weka[i])); });
console.log(`Registros comparados: ${filas.length} | diferencia máxima JS vs WEKA: ${maxDif.toExponential(2)}`);
if (filas.length !== 10000 || maxDif > 1e-6) { console.error("FALLÓ"); process.exit(1); }
console.log("OK: la app web reproduce exactamente al modelo de WEKA");
