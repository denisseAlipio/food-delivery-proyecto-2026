"""Pruebas del sistema de estimación del tiempo de entrega (M5P).

Verifican que el modelo desplegado reproduce las métricas reportadas en el informe
(secciones 5.1 y 6.1) y las predicciones de WEKA sobre test.arff.
"""
import io
import math
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))
from predictor import cargar_modelo, predecir, recortar  # noqa: E402


def leer_arff(ruta):
    cabecera, datos = open(ruta, encoding="utf-8").read().split("@data")
    cols = [l.split()[1] for l in cabecera.splitlines() if l.lower().startswith("@attribute")]
    return pd.read_csv(io.StringIO(datos.strip()), header=None, names=cols,
                       quotechar="'", skipinitialspace=True)


@pytest.fixture(scope="module")
def modelo():
    return cargar_modelo()


@pytest.fixture(scope="module")
def test_df():
    return leer_arff(RAIZ / "data" / "test.arff")


@pytest.fixture(scope="module")
def predicciones(modelo, test_df):
    return [predecir(modelo, fila)[0] for fila in test_df.to_dict("records")]


def test_particion_de_datos():
    assert len(leer_arff(RAIZ / "data" / "train.arff")) == 40000
    assert len(leer_arff(RAIZ / "data" / "test.arff")) == 10000


def test_estructura_del_modelo(modelo):
    def hojas(n):
        return 1 if "lm" in n else hojas(n["l"]) + hojas(n["r"])
    assert hojas(modelo["tree"]) == 94                      # 94 reglas (sección 5.1.1)
    assert modelo["tree"]["a"] == "Road_Distance_km"        # primera partición
    assert modelo["tree"]["v"] == pytest.approx(23.155)


def test_identico_a_weka(predicciones):
    weka = pd.read_csv(RAIZ / "tests" / "predicciones_weka_test.csv", header=None)[0].tolist()
    assert max(abs(a - b) for a, b in zip(predicciones, weka)) < 1e-6


def test_metricas_en_test(predicciones, test_df):
    y = test_df["Time_taken_min"].tolist()
    err = [p - r for p, r in zip(predicciones, y)]
    mae = sum(abs(e) for e in err) / len(err)
    rmse = math.sqrt(sum(e * e for e in err) / len(err))
    assert round(mae, 3) == 2.326                           # Tabla 2
    assert round(rmse, 3) == 3.023
    assert abs(sum(err) / len(err)) < 0.05                  # sesgo ≈ 0.04 min


def test_pedidos_nuevos(modelo):
    nuevos = leer_arff(RAIZ / "data" / "nuevos.arff").drop(columns="Time_taken_min")
    obtenidos = [round(predecir(modelo, f)[0], 1) for f in nuevos.to_dict("records")]
    assert obtenidos == [25.7, 120.0, 181.4]                # Tabla 4


def test_recorte_al_rango_observado():
    assert recortar(181.4) == 180 and recortar(5) == 10 and recortar(64.2) == 64.2
