# Ejecución y pruebas del sistema

Las pruebas se ejecutan automáticamente en la pestaña **Actions** (flujo *Pruebas del sistema*).

| Prueba | Qué verifica |
|---|---|
| `test_particion_de_datos` | 40 000 registros de entrenamiento y 10 000 de prueba |
| `test_estructura_del_modelo` | 94 reglas y primera partición en Road_Distance_km ≤ 23.155 |
| `test_identico_a_weka` | Las predicciones coinciden con las de WEKA en los 10 000 pedidos de prueba |
| `test_metricas_en_test` | MAE = 2.326 min, RMSE = 3.023 min y sesgo cercano a cero (Tabla 2 del informe) |
| `test_pedidos_nuevos` | 25.7, 120.0 y 181.4 min para los tres pedidos de ejemplo (Tabla 4) |
| `test_recorte_al_rango_observado` | Recorte de las estimaciones al intervalo [10, 180] |
| `test_app_web.js` | La app web (JavaScript) reproduce exactamente al modelo de WEKA |

`predicciones_weka_test.csv` contiene las predicciones de referencia generadas por WEKA sobre `test.arff`.

Ejecutar localmente:
```bash
pip install -r requirements.txt
pytest tests -v
node tests/test_app_web.js
```
