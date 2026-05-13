"""
Etiquetado académico (no clínico): asigna una de 4 categorías a cada registro
a partir de variables ya presentes en el CSV procesado.

Salida: data/processed/enfermedades_cardiacas_4categorias.csv
"""

from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[1]
ENTRADA = BASE / "data" / "processed" / "enfermedades_cardiacas_limpio.csv"
SALIDA = BASE / "data" / "processed" / "enfermedades_cardiacas_4categorias.csv"

CAT_NO = "NO ENFERMO"
CAT_LEVE = "ENFERMEDAD LEVE"
CAT_AGUDA = "ENFERMEDAD AGUDA"
CAT_CRONICA = "ENFERMEDAD CRÓNICA"


def clasificar_fila(row: pd.Series) -> str:
    sis = float(row["presion_arterial_sistolica"])
    dia = float(row["presion_arterial_diastolica"])
    col = int(row["nivel_colesterol"])
    glu = int(row["nivel_glucosa"])
    enf = int(row["presencia_enfermedad"])
    fum = bool(row["fumador"])

    # Prioridad 1: cuadro compatible con descompensación aguda (umbrales docentes)
    crisis_pa = sis >= 180 or dia >= 110
    crisis_mixta = sis >= 160 and glu >= 3
    if crisis_pa or crisis_mixta:
        return CAT_AGUDA

    # Prioridad 2: enfermedad conocida en el dataset → crónico si no entró como agudo
    if enf == 1:
        return CAT_CRONICA

    # Sin etiqueta de enfermedad: distinguir sano vs factores de riesgo leves
    presion_ok = sis < 130 and dia < 85
    metabolic_ok = col <= 2 and glu <= 2
    if presion_ok and metabolic_ok and not fum:
        return CAT_NO

    return CAT_LEVE


def main() -> None:
    df = pd.read_csv(ENTRADA)
    df["categoria_clinica"] = df.apply(clasificar_fila, axis=1)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SALIDA, index=False)
    counts = df["categoria_clinica"].value_counts()
    print(f"Escrito: {SALIDA}")
    print(counts.to_string())


if __name__ == "__main__":
    main()
