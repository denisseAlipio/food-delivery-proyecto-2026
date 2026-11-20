# Código del sistema

| Archivo | Función |
|---|---|
| `Proyecto_FoodDelivery_Colab.ipynb` | Cuaderno de Google Colab: instalación, carga de datos, comparación de 5 modelos con validación cruzada (4.2), entrenamiento y evaluación de M5P (5.1), métricas y prototipo (6). [Abrir en Colab](https://colab.research.google.com/drive/1SwHf8QqrWQLs5FxrrGMVRuFaSPu-qEHL?usp=sharing) |
| `predictor.py` | Carga `models/m5p_tree.json` y estima el tiempo de un pedido. No requiere Java. |
| `exportar_modelo.py` | Lee `models/m5p_final.model` con python-weka-wrapper3 y exporta el árbol y los coeficientes exactos a JSON. |

## Flujo del sistema
1. **Entrenamiento (Colab + WEKA):** M5P se entrena con `train.arff` y se guarda como `m5p_final.model`.
2. **Exportación:** `exportar_modelo.py` extrae las 94 reglas y sus modelos lineales a `m5p_tree.json`.
3. **Predicción:** `predictor.py` (Python) y `app/m5p.js` (web) recorren el árbol y aplican el modelo lineal de la hoja. Producen las mismas predicciones que WEKA (diferencia máxima < 10⁻¹² min en 10 000 pedidos).
