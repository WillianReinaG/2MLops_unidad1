# 2MLops — Estado clínico simulado

Trabajo académico de MLOps: clasificación simulada en cuatro estados de salud, pipeline **end-to-end** documentado, servicio Flask (MVP) y despliegue Docker.

**Repositorio:** [github.com/WillianReinaG/2MLops_unidad1](https://github.com/WillianReinaG/2MLops_unidad1) · **Rama:** `unidad3`

## Estructura del proyecto

| Carpeta / archivo | Contenido |
|-------------------|-----------|
| `data/` | CSV brutos y procesados (~70 000 registros) |
| `scripts/` | Etiquetado académico en 4 categorías |
| `servicio_estado_clinico/` | **MVP baseline:** API Flask, formulario, Dockerfile (reglas deterministas) |
| `docs/` | Propuesta MLOps v2.0, PDF, diagramas y CHANGELOG |

## Documentación del pipeline (Unidad 3 v2.1)

| Documento | Descripción |
|-----------|-------------|
| [`docs/PROPUESTA_PIPELINE_MLOPS.md`](docs/PROPUESTA_PIPELINE_MLOPS.md) | Case Challenge + Part 1/2/3 (estructura [mlops-sample](https://github.com/avila196/mlops-sample)) + apéndices técnicos |
| [`docs/Pipeline_MLOps_Propuesta_Completa.pdf`](docs/Pipeline_MLOps_Propuesta_Completa.pdf) | PDF para entrega |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Evolución Semana 1 → v2.1 |

### Diagramas

| Figura | Archivo |
|--------|---------|
| **Pipeline principal (Offline \| Predictions)** | [`docs/imgs/ml-pipeline-estado-clinico.png`](docs/imgs/ml-pipeline-estado-clinico.png) |
| 12 etapas E2E | [`docs/diagrama_pipeline_e2e.png`](docs/diagrama_pipeline_e2e.png) |
| Despliegue híbrido | [`docs/diagrama_despliegue_hibrido.png`](docs/diagrama_despliegue_hibrido.png) |
| CI/CD | [`docs/diagrama_cicd_mlops.png`](docs/diagrama_cicd_mlops.png) |
| Datos → ML | [`docs/diagrama_datos_ml.png`](docs/diagrama_datos_ml.png) |

Regenerar PDF y diagramas:

```powershell
pip install matplotlib reportlab
python docs/generar_pdf_pipeline_mlops.py
```

## MVP vs producción (según la propuesta)

| | MVP (implementado) | Producción objetivo (documentada) |
|--|-------------------|-----------------------------------|
| Modelo | Reglas en `modelo_simulado.py` | LightGBM + MLflow Registry |
| Despliegue | Docker local | Docker local **+** Cloud Run |
| Uso médico | `localhost:5000` | Local o HTTPS con API key |

## Servicio de predicción (MVP)

Ver [`servicio_estado_clinico/README.md`](servicio_estado_clinico/README.md).

```powershell
cd servicio_estado_clinico
docker build -t estado-clinico-demo .
docker run --rm -p 5000:5000 estado-clinico-demo
```

## Aviso

Proyecto universitario. **No usar para decisiones clínicas reales.**
