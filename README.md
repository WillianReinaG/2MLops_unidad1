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

## Documentación del pipeline (Unidad 3 v2.0)

| Documento | Descripción |
|-----------|-------------|
| [`docs/PROPUESTA_PIPELINE_MLOPS.md`](docs/PROPUESTA_PIPELINE_MLOPS.md) | Propuesta completa: **12 etapas**, suposiciones, tecnologías, despliegue local + cloud |
| [`docs/Pipeline_MLOps_Propuesta_Completa.pdf`](docs/Pipeline_MLOps_Propuesta_Completa.pdf) | PDF para entrega al profesor |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Cambios vs propuesta Semana 1 (`f570021`) y vs Unidad 3 intermedia (`c2d57d0`) |

### Diagramas

- [`diagrama_pipeline_e2e.png`](docs/diagrama_pipeline_e2e.png) — 12 etapas + ciclo retrain
- [`diagrama_despliegue_hibrido.png`](docs/diagrama_despliegue_hibrido.png) — médico local vs cloud
- [`diagrama_cicd_mlops.png`](docs/diagrama_cicd_mlops.png) — GitHub Actions
- [`diagrama_datos_ml.png`](docs/diagrama_datos_ml.png) — raw → ML → inferencia

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
