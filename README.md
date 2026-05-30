# 2MLops — Estado clínico simulado

Trabajo académico de MLOps: clasificación simulada en cuatro estados de salud a partir de signos medibles, con pipeline documentado, servicio Flask y despliegue Docker.

**Repositorio:** [github.com/WillianReinaG/2MLops_unidad1](https://github.com/WillianReinaG/2MLops_unidad1)

## Estructura del proyecto

| Carpeta / archivo | Contenido |
|-------------------|-----------|
| `data/` | CSV brutos y procesados (~70 000 registros) |
| `scripts/` | Etiquetado académico en 4 categorías |
| `servicio_estado_clinico/` | API Flask, formulario web, Dockerfile |
| `docs/` | Propuesta completa del pipeline MLOps (Markdown + PDF) |

## Documentación del pipeline (Punto 1 — Unidad 3)

- **Texto completo:** [`docs/PROPUESTA_PIPELINE_MLOPS.md`](docs/PROPUESTA_PIPELINE_MLOPS.md)
- **PDF para entrega:** [`docs/Pipeline_MLOps_Propuesta_Completa.pdf`](docs/Pipeline_MLOps_Propuesta_Completa.pdf)
- **Diagrama:** [`docs/diagrama_pipeline_mlops.png`](docs/diagrama_pipeline_mlops.png)

Regenerar PDF y diagrama:

```powershell
pip install matplotlib reportlab
python docs/generar_pdf_pipeline_mlops.py
```

## Servicio de predicción

Ver instrucciones detalladas en [`servicio_estado_clinico/README.md`](servicio_estado_clinico/README.md).

Resumen rápido con Docker:

```powershell
cd servicio_estado_clinico
docker build -t estado-clinico-demo .
docker run --rm -p 5000:5000 estado-clinico-demo
```

Abrir `http://localhost:5000/` o enviar `POST` a `http://localhost:5000/predecir`.

## Aviso

Proyecto universitario con reglas docentes. **No usar para decisiones clínicas reales.**
