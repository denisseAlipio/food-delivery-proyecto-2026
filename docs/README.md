# Documentación del proyecto

- [Informe del proyecto (PDF)](Informe_Proyecto_Aprendizaje_Estadistico.pdf), secciones I a VI.

## Contenido del informe
| Sección | Contenido |
|---|---|
| I. Introducción | Título, antecedentes, problema, pregunta de investigación y objetivos |
| II. Requerimientos | Dominio y requisitos de datos, preprocesamiento, modelo y evaluación |
| III. Data-set | Variables, limpieza, fuga de información, normalización y partición 80/20 |
| IV. Aprendizaje | Algoritmos evaluados, métricas, validación cruzada y selección de M5P |
| V. Aplicación | Entrenamiento final, evaluación en test y pedidos nuevos |
| VI. Evaluación | Métricas ampliadas, estabilidad, sobreajuste, comparación con el método tradicional |
| VII. Despliegue | Este repositorio y la app web |

## Ficha técnica del modelo
| Característica | Valor |
|---|---|
| Algoritmo | M5P (árbol de modelos), WEKA, minNumInstances = 4 |
| Reglas | 94 hojas, cada una con un modelo lineal suavizado |
| Primera partición | Road_Distance_km ≤ 23.155 km |
| Entradas | 19 variables disponibles al registrar el pedido |
| Salida | Tiempo de entrega en minutos, recortado al rango observado [10, 180] |
| MAE / RMSE en prueba | 2.326 / 3.023 min |

## Limitaciones
- Mayor error con tráfico severo (MAE 5.70 min; 107 casos en prueba).
- Supone que `Preparation_Time_Min` es una estimación disponible al registrar el pedido.
- El truncamiento en 180 minutos impide conocer la duración real de las entregas más largas.
- Las estimaciones son orientativas; el sistema no está conectado a datos en tiempo real.
