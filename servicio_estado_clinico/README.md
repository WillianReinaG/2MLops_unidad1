# Servicio de estado clínico simulado

Proyecto MLOps — MVP Semana 1 · Propuesta pipeline Unidad 3

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

Este directorio es el **MVP baseline (Semana 1)**: reglas + Flask + Docker. Corresponde a **Api Deploy Dev** simplificado y al **champion inicial** frente a LightGBM.

| Documento | Enlace |
|-----------|--------|
| **Propuesta Unidad 3 (entrega)** | [`docs/PROPUESTAPipeLine.md`](../docs/PROPUESTAPipeLine.md) |
| CHANGELOG Semana 1 → Unidad 3 | [`CHANGELOG.md`](../CHANGELOG.md) |
| README del repositorio | [`README.md`](../README.md) |
| Propuesta original Semana 1 | [PDF en rama `main`](https://github.com/WillianReinaG/2MLops_unidad1/blob/main/docs/punto%201%20descripcion%20pipeline%20MLops.pdf) |

**Resumen:** LightGBM se promovería a Staging/PROD solo si supera estas reglas en F1 macro y **recall AGUDA** (~1,9 % del dataset), según gates en MLflow.

---

Trabajo académico; los umbrales no están validados clínicamente.
