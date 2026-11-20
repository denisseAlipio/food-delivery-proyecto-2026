// Predictor M5P exportado desde WEKA (m5p_final.model). Funciona en navegador y en Node.js.
(function (root) {
  // Convierte un pedido (valores originales) al vector binarizado que usa M5P internamente
  function transformar(features, pedido) {
    const x = {};
    for (const f of features) {
      const k = f.indexOf("=");
      if (k < 0) { x[f] = Number(pedido[f]); continue; }
      const atributo = f.slice(0, k);
      const valores = f.slice(k + 1).split(",");
      x[f] = valores.includes(String(pedido[atributo])) ? 1 : 0;
    }
    return x;
  }
  // Recorre el árbol hasta la hoja y aplica su modelo lineal
  function predecir(modelo, pedido) {
    const x = transformar(modelo.features, pedido);
    let n = modelo.tree;
    while (!("lm" in n)) n = x[n.a] <= n.v ? n.l : n.r;
    let y = n.b;
    for (const f in n.w) y += n.w[f] * x[f];
    return { minutos: y, regla: n.lm };
  }
  const api = { transformar, predecir };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.M5P = api;
})(this);
