# 2MLops — Estado clínico simulado

Propuesta **MLOps end-to-end v3.0** (nivel posgrado): MLOps · DevOps · DevSecOps · AIOps · AgentOps (horizonte). MVP de inferencia implementado con reglas + Flask + Docker.

**Repositorio:** [github.com/WillianReinaG/2MLops_unidad1](https://github.com/WillianReinaG/2MLops_unidad1) · **Rama:** `unidad3`

## Documentación principal

| Documento | Contenido |
|-----------|-----------|
| [`docs/PROPUESTA_PIPELINE_MLOPS.md`](docs/PROPUESTA_PIPELINE_MLOPS.md) | Propuesta v3.0 completa |
| [`docs/Pipeline_MLOps_Propuesta_Completa.pdf`](docs/Pipeline_MLOps_Propuesta_Completa.pdf) | PDF para entrega |
| [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md) | Model Card (limitaciones, métricas, ética) |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Evolución Semana 1 → v3.0 |
| [`docs/ADR/`](docs/ADR/) | Architecture Decision Records |

## Diagramas

| Figura | Archivo |
|--------|---------|
| Pipeline Offline \| Predictions | [`docs/imgs/ml-pipeline-estado-clinico.png`](docs/imgs/ml-pipeline-estado-clinico.png) |
| Ops stack (MLOps…AgentOps) | [`docs/imgs/arquitectura-ops-capas.png`](docs/imgs/arquitectura-ops-capas.png) |
| Despliegue híbrido | [`docs/diagrama_despliegue_hibrido.png`](docs/diagrama_despliegue_hibrido.png) |
| CI/CD | [`docs/diagrama_cicd_mlops.png`](docs/diagrama_cicd_mlops.png) |

```powershell
pip install matplotlib reportlab
python docs/generar_pdf_pipeline_mlops.py
```

## MVP vs producción

| | MVP (repo) | Producción (propuesta) |
|--|------------|------------------------|
| Modelo | Reglas `modelo_simulado.py` | LightGBM + MLflow |
| Deploy | Docker local | Edge + Cloud Run |
| Ops | Manual | CI/CD, SLO, AIOps |

## Servicio MVP

```powershell
cd servicio_estado_clinico
docker build -t estado-clinico-demo .
docker run --rm -p 5000:5000 estado-clinico-demo
```

**No usar para decisiones clínicas reales.**
