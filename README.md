# Estimación del tiempo de entrega de pedidos de Food Delivery

**Proyecto de Aprendizaje Estadístico · Universidad Privada Antenor Orrego · Ingeniería de Sistemas e Inteligencia Artificial · Trujillo, 2026**

[![Pruebas del sistema](https://github.com/denisseAlipio/food-delivery-proyecto-2026/actions/workflows/pruebas.yml/badge.svg)](https://github.com/denisseAlipio/food-delivery-proyecto-2026/actions/workflows/pruebas.yml)
[![App web](https://img.shields.io/badge/App%20web-abrir-c2410c)](https://denissealipio.github.io/food-delivery-proyecto-2026/)
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1SwHf8QqrWQLs5FxrrGMVRuFaSPu-qEHL?usp=sharing)

| [📄 Documentación](#-documentación-del-proyecto) | [💻 Código](#-código-del-sistema) | [✅ Ejecución y pruebas](#-ejecución-y-pruebas-del-sistema) | [🌐 App web](https://denissealipio.github.io/food-delivery-proyecto-2026/) |
|---|---|---|---|

Sistema de aprendizaje supervisado (regresión) que estima, en minutos, el tiempo total de entrega de un pedido de Food Delivery a partir de variables disponibles al momento de registrarlo: distancia, tiempo de preparación, tráfico, clima, tipo de vehículo, datos del repartidor y del restaurante.

**Integrantes:** Alipio De La Cruz, Ghinna Denisse · Chinchay Galarreta, Josue · Fernandez Velasco, Yeriko · González Recuenco, Diego · Ocampo Rivera, Dooren · Vilca Díaz, Eduardo Abraham

---

## 📄 Documentación del proyecto

- **Informe completo:** [`docs/Informe_Proyecto_Aprendizaje_Estadistico.pdf`](docs/Informe_Proyecto_Aprendizaje_Estadistico.pdf)
- **Resumen técnico:** [`docs/README.md`](docs/README.md)

### Problema
Estimar el tiempo de entrega solo con distancia y velocidad promedio es insuficiente: la preparación, el tráfico, el clima y las condiciones del repartidor interactúan entre sí. El proyecto busca el modelo de regresión con menor error sobre pedidos no utilizados en el entrenamiento.

### Datos y metodología
- Dataset: `Food_Delivery_Time_Prediction.csv`, 50 000 registros y 24 atributos; variable objetivo `Time_taken_min` (10 a 180 min).
- Preprocesamiento en WEKA 3.9.5: se excluyeron `Order_ID`, `Order_Date`, `Delivery_Distance_Category` y `Average_Speed_kmph` (fuga de información). Quedan 19 predictores.
- Partición 80/20 con semilla 42: `train.arff` (40 000) y `test.arff` (10 000).
- Comparación en Google Colab (python-weka-wrapper3) con validación cruzada de 5 pliegues.

### Resultados

| Modelo | MAE (min) | RMSE (min) | r |
|---|---|---|---|
| ZeroR (línea base) | 27.541 | 35.452 | −0.013 |
| Regresión Lineal | 6.355 | 9.230 | 0.966 |
| **M5P (seleccionado)** | **2.405** | **3.128** | **0.996** |
| Random Forest | 6.542 | 9.281 | 0.979 |
| Additive Regression | 3.074 | 4.049 | 0.994 |

Evaluación final de M5P sobre el conjunto de prueba (10 000 pedidos): **MAE 2.326 min · RMSE 3.023 min · R² 0.993**; el 91.0 % de los pedidos se estimó con un error de 5 minutos o menos. Frente al método tradicional (preparación + distancia ÷ velocidad promedio), el sistema reduce el MAE entre 59 % y 86 %.

---

## 💻 Código del sistema

```
├── src/
│   ├── Proyecto_FoodDelivery_Colab.ipynb   Desarrollo, aplicación y evaluación (secciones 4.2, 5.1 y 6)
│   ├── predictor.py                        Predictor en Python a partir del modelo exportado
│   └── exportar_modelo.py                  Extrae el árbol M5P exacto desde m5p_final.model
├── models/
│   ├── m5p_final.model                     Modelo M5P entrenado (WEKA)
│   └── m5p_tree.json                       Mismo modelo exportado: 94 reglas y sus modelos lineales
├── data/
│   ├── train.arff · test.arff              Conjuntos de entrenamiento y prueba
│   └── nuevos.arff                         Tres pedidos nuevos de ejemplo
├── app/                                    App web (HTML + JavaScript, sin servidor)
├── tests/                                  Pruebas automáticas
└── .github/workflows/                      Ejecución de pruebas y publicación de la app
```

Detalle en [`src/README.md`](src/README.md).

---

## ✅ Ejecución y pruebas del sistema

**Ejecutar en Colab:** abrir el [cuaderno](https://colab.research.google.com/drive/1SwHf8QqrWQLs5FxrrGMVRuFaSPu-qEHL?usp=sharing), elegir *Entorno de ejecución → Ejecutar todo* y subir `train.arff` y `test.arff`.

**Ejecutar localmente:**
```bash
pip install -r requirements.txt
python src/predictor.py          # estima un pedido de ejemplo
pytest tests -v                  # pruebas del modelo
node tests/test_app_web.js       # prueba de la app web
```

**Pruebas automáticas:** se ejecutan en la pestaña **Actions** en cada cambio del repositorio. Verifican que el modelo desplegado reproduce los resultados del informe. Detalle en [`tests/README.md`](tests/README.md).

---

## 🌐 App web

**https://denissealipio.github.io/food-delivery-proyecto-2026/**

Formulario que estima el tiempo de entrega de un pedido nuevo con el modelo M5P. Funciona en computadora y celular, sin servidor.
