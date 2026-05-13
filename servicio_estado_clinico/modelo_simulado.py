"""
Simulación académica de un clasificador de estado (no uso clínico real).

Entradas mínimas: al menos tres magnitudes entre las admitidas.
Salida: una de cuatro etiquetas de texto.
"""

from __future__ import annotations

from typing import Any, Mapping

CATEGORIAS = (
    "NO ENFERMO",
    "ENFERMEDAD LEVE",
    "ENFERMEDAD AGUDA",
    "ENFERMEDAD CRÓNICA",
)

CAMPOS_PERMITIDOS = frozenset(
    {
        "presion_sistolica",
        "presion_diastolica",
        "nivel_colesterol",
        "nivel_glucosa",
        "presencia_enfermedad",
        "fumador",
    }
)


def _bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if v in (0, 1, "0", "1"):
        return bool(int(v))
    if isinstance(v, str):
        return v.strip().lower() in ("true", "si", "sí", "yes", "on")
    return bool(v)


def _int(v: Any, default: int) -> int:
    if v is None or v == "":
        return default
    return int(float(v))


def _float(v: Any) -> float:
    return float(v)


def contar_valores_usados(datos: Mapping[str, Any]) -> int:
    n = 0
    for clave in CAMPOS_PERMITIDOS:
        if clave not in datos:
            continue
        val = datos[clave]
        if val is None or val == "":
            continue
        n += 1
    return n


def clasificar_estado(datos: Mapping[str, Any]) -> str:
    """
    Reglas docentes (prioridad de arriba hacia abajo):
    - AGUDA: criterio de descompensación con umbrales fijos.
    - CRÓNICA: indicador de enfermedad previa en el registro.
    - NO ENFERMO: perfil bajo riesgo según PA, lípidos/glucosa y tabaco.
    - LEVE: el resto de casos sin enfermedad declarada.
    """
    sis = _float(datos["presion_sistolica"])
    dia = _float(datos["presion_diastolica"])
    col = _int(datos.get("nivel_colesterol"), 2)
    glu = _int(datos.get("nivel_glucosa"), 1)
    enf = _int(datos.get("presencia_enfermedad"), 0)
    fum = _bool(datos.get("fumador", False))

    if sis >= 180 or dia >= 110 or (sis >= 160 and glu >= 3):
        return "ENFERMEDAD AGUDA"
    if enf == 1:
        return "ENFERMEDAD CRÓNICA"
    if sis < 130 and dia < 85 and col <= 2 and glu <= 2 and not fum:
        return "NO ENFERMO"
    return "ENFERMEDAD LEVE"


def validar_entrada_minima(datos: Mapping[str, Any]) -> tuple[bool, str]:
    faltan = {"presion_sistolica", "presion_diastolica"} - datos.keys()
    if faltan:
        return False, "Faltan campos obligatorios: presion_sistolica, presion_diastolica."

    try:
        _float(datos["presion_sistolica"])
        _float(datos["presion_diastolica"])
    except (TypeError, ValueError):
        return False, "presion_sistolica y presion_diastolica deben ser numéricos."

    if contar_valores_usados(datos) < 3:
        return (
            False,
            "Se requieren al menos tres valores entre los campos permitidos "
            f"(recibidos: {contar_valores_usados(datos)}).",
        )
    return True, ""
