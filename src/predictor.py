"""Predictor del tiempo de entrega con el modelo M5P exportado de WEKA.

El archivo models/m5p_tree.json contiene el árbol y los modelos lineales exactos de
m5p_final.model (extraídos con src/exportar_modelo.py), por lo que este predictor
reproduce las predicciones de WEKA sin necesidad de Java.
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RANGO_MIN, RANGO_MAX = 10, 180


def cargar_modelo(ruta=RAIZ / "models" / "m5p_tree.json"):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def transformar(features, pedido):
    """Convierte el pedido al vector binarizado (NominalToBinary) que usa M5P."""
    x = {}
    for f in features:
        if "=" not in f:
            x[f] = float(pedido[f])
        else:
            atributo, valores = f.split("=", 1)
            x[f] = 1.0 if str(pedido[atributo]) in valores.split(",") else 0.0
    return x


def predecir(modelo, pedido):
    """Devuelve (minutos estimados, número de modelo lineal usado)."""
    x = transformar(modelo["features"], pedido)
    nodo = modelo["tree"]
    while "lm" not in nodo:
        nodo = nodo["l"] if x[nodo["a"]] <= nodo["v"] else nodo["r"]
    y = nodo["b"] + sum(w * x[f] for f, w in nodo["w"].items())
    return y, nodo["lm"]


def recortar(minutos):
    """Post-procesamiento propuesto en la sección 5.1.4: rango observado [10, 180]."""
    return min(max(minutos, RANGO_MIN), RANGO_MAX)


if __name__ == "__main__":
    modelo = cargar_modelo()
    ejemplo = {"Order_Hour": 20, "Day_of_Week": "Friday", "Is_Weekend": 0, "Is_Festival": 0,
               "Weather": "Rain", "Pickup_Zone": "CBD", "Dropoff_Zone": "Suburban",
               "Vehicle_Type": "Scooter", "Rider_Experience_Years": 3, "Rider_Rating": 4.0,
               "Restaurant_Rating": 4.1, "Cuisine_Type": "Pizza", "Order_Items": 3,
               "Restaurant_Load": "High", "Preparation_Time_Min": 30, "Road_Distance_km": 25,
               "Traffic_Level": "High", "Number_of_Signals": 12, "Delivery_Priority": "Normal"}
    minutos, lm = predecir(modelo, ejemplo)
    print(f"Tiempo estimado: {recortar(minutos):.1f} min (modelo lineal LM{lm})")
