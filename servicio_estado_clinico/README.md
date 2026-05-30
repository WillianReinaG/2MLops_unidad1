# Servicio de estado clínico simulado

Proyecto unidad uno MLOps

## Qué hace

- Expone un servicio **Flask** en el puerto **5000**.
- La ruta **`POST /predecir`** recibe JSON y devuelve una etiqueta entre:
  - `NO ENFERMO`
  - `ENFERMEDAD LEVE`
  - `ENFERMEDAD AGUDA`
  - `ENFERMEDAD CRÓNICA`
- La página es un formulario mínimo que llama a `/predecir`.

La “predicción” es una **función determinista** definida en `modelo_simulado.py`.

### Campos JSON admitidos

`presion_sistolica`, `presion_diastolica`, `nivel_colesterol`, `nivel_glucosa`, `presencia_enfermedad`, `fumador`.

**Obligatorios:** `presion_sistolica` y `presion_diastolica`.  
**Regla de negocio:** deben enviarse **al menos tres valores** contando solo campos permitidos con valor informado (las dos presiones cuentan; falta al menos un campo más).

## Ejecución local (sin Docker)

Desde esta carpeta (`servicio_estado_clinico`):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abrir el navegador en `http://127.0.0.1:5000/`.

### Ejemplo con curl

```bash
curl -s -X POST http://127.0.0.1:5000/predecir ^
  -H "Content-Type: application/json" ^
  -d "{\"presion_sistolica\": 118, \"presion_diastolica\": 76, \"nivel_colesterol\": 1, \"nivel_glucosa\": 1, \"presencia_enfermedad\": 0, \"fumador\": false}"
```

En PowerShell puede ser más cómodo usar `Invoke-RestMethod`:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/predecir -Method POST -ContentType "application/json" -Body '{"presion_sistolica":118,"presion_diastolica":76,"nivel_colesterol":1,"nivel_glucosa":1,"presencia_enfermedad":0,"fumador":false}'
```

## Docker

### Construir la imagen

```bash
docker build -t estado-clinico-demo .
```

### Ejecutar el contenedor

```bash
docker run --rm -p 5000:5000 estado-clinico-demo
```

Servicio disponible en `http://localhost:5000/predecir` (POST) y `http://localhost:5000/` (formulario).

## Rol de este servicio en el pipeline MLOps

Este directorio contiene el **MVP baseline ya implementado**: reglas deterministas en `modelo_simulado.py`, servidas vía Flask y Docker.

La **propuesta de producción** (documentada, no implementada aquí) define un modelo **LightGBM** en MLflow Registry, despliegue **local + cloud** (Cloud Run) y pipeline de **12 etapas**. Ver documentación completa:

| Documento | Enlace |
|-----------|--------|
| Propuesta v3.0 (posgrado / Ops stack) | [`docs/PROPUESTA_PIPELINE_MLOPS.md`](../docs/PROPUESTA_PIPELINE_MLOPS.md) |
| PDF entrega | [`docs/Pipeline_MLOps_Propuesta_Completa.pdf`](../docs/Pipeline_MLOps_Propuesta_Completa.pdf) |
| Model Card | [`docs/MODEL_CARD.md`](../docs/MODEL_CARD.md) |
| ADR (decisiones de arquitectura) | [`docs/ADR/`](../docs/ADR/) |
| CHANGELOG | [`docs/CHANGELOG.md`](../docs/CHANGELOG.md) |
| Diagrama pipeline | [`docs/imgs/ml-pipeline-estado-clinico.png`](../docs/imgs/ml-pipeline-estado-clinico.png) |
| Diagrama Ops stack | [`docs/imgs/arquitectura-ops-capas.png`](../docs/imgs/arquitectura-ops-capas.png) |

**Resumen:** este servicio cumple la consigna académica con reglas interpretables. El equipo ML promovería LightGBM a producción solo si supera este baseline en F1 macro y recall de la clase AGUDA (~1,9 % del dataset).

---

Trabajo académico; los umbrales no están validados clínicamente.
