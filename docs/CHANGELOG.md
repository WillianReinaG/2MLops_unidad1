# CHANGELOG — Propuesta pipeline MLOps

Todos los cambios relevantes de la propuesta del pipeline MLOps para el proyecto **Estado clínico simulado**.

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## Referencias de versiones

| Versión | Origen | Commit / artefacto |
|---------|--------|-------------------|
| **1.0.0** | Semana 1 | `f570021` — [`punto 1 descripcion pipeline MLops.pdf`](punto%201%20descripcion%20pipeline%20MLops.pdf) |
| **1.1.0** | Unidad 3 (intermedia) | `c2d57d0` — [`PROPUESTA_PIPELINE_MLOPS.md`](PROPUESTA_PIPELINE_MLOPS.md) v1, 8 etapas ampliadas |
| **2.0.0** | Unidad 3 (reestructuración E2E) | `43777e4` — 12 etapas, ML producción, despliegue híbrido |
| **2.1.0** | Unidad 3 (estructura mlops-sample) | **Actual** — Case Challenge + Offline Training \| Predictions |

---

## [2.1.0] — Alineación con mlops-sample (actual)

### Added

- **Diagrama principal** estilo [avila196/mlops-sample](https://github.com/avila196/mlops-sample): [`imgs/ml-pipeline-estado-clinico.png`](imgs/ml-pipeline-estado-clinico.png) con bloques **Offline Training | Predictions | Bonus**.
- Carpeta **`docs/imgs/`** para figuras (equivalente a `imgs/` del sample).
- Secciones narrativas **Case Challenge**, **Part 1** (Offline Training + Predictions), **Part 2** (MVP implementado), **Part 3** (requisitos futuros).
- Subsecciones espejo del sample: Data Input, Model Iterations, Model selection & evaluation, ¿Producción?, Model deployment, Inferencia tiempo real.
- Referencia explícita al repo ejemplo en propuesta y PDF.

### Changed

- [`PROPUESTA_PIPELINE_MLOPS.md`](PROPUESTA_PIPELINE_MLOPS.md) reorganizado: narrativa Part 1/2/3 + apéndices técnicos (etapas 0–12, suposiciones, huérfanas).
- PDF v2.1 prioriza diagrama principal mlops-sample en portada.
- Comparación batch Spark/EMR (sample fintech) → inferencia unitaria médico local/cloud (nuestro dominio).

### Rationale

- El evaluador y equipos ML reconocen la estructura **Offline Training | Predictions** del curso/referencia.
- Se conserva profundidad técnica v2.0 en apéndices sin perder legibilidad del diagrama central.

---

## [2.0.0] — Reestructuración end-to-end

### Added

- Arquitectura de **12 etapas** (0–12): gobernanza, catálogo, feature store, registry, observabilidad, retraining continuo.
- **Registro maestro de suposiciones** (S1–S8) con implicaciones y validación.
- **Despliegue híbrido:** Docker Compose local (médico en PC) + **Google Cloud Run** / AWS App Runner (médico remoto).
- Stack tecnológico concreto por etapa: **DVC**, **Great Expectations**, **Feast**, **LightGBM**, **Optuna**, **MLflow** (Tracking + Registry), **SHAP**, **GHCR**, **Prometheus/Grafana**, **Evidently AI**, **GitHub Actions**, **Prefect** (alternativa).
- Cuatro diagramas: `diagrama_pipeline_e2e.png`, `diagrama_despliegue_hibrido.png`, `diagrama_cicd_mlops.png`, `diagrama_datos_ml.png`.
- Sección **Baseline MVP vs producción objetivo** (reglas vs LightGBM).
- Sección **CI/CD end-to-end** con jobs definidos.
- **Plan de puesta en marcha** por fases (0–4) con duración, roles y entregables.
- Política ML para **enfermedades huérfanas**: desbalance AGUDA, cuarentena de datos, flag `requiere_revision_humana`.
- Seguridad: API keys, Secret Manager, TLS, logs sin PII.
- Este archivo **CHANGELOG.md**.

### Changed

- Pipeline de **8 etapas lineales** → **12 etapas** con ciclo cerrado de retraining.
- **Modelo de producción objetivo:** de “función simulada / evolución opcional ML” a **LightGBM supervisado** con reglas como **baseline MVP** ya implementado.
- Herramientas de “evolución futura” → **decisiones explícitas** con alternativas descartadas justificadas en cada etapa.
- Despliegue: solo Docker local → **local + cloud** con mismo contrato API.
- Validación: lista genérica → **quality gates** (GX), evaluación con SHAP, gate humano de aprobación.
- Monitoreo: logs básicos → **Prometheus + Grafana + Evidently** (drift y rendimiento).
- Plantilla por etapa: ahora incluye **8 subsecciones obligatorias** (objetivo, suposiciones, I/O, tecnologías, proceso, criterios, riesgos, relación con repo).
- PDF regenerado como [`Pipeline_MLOps_Propuesta_Completa.pdf`](Pipeline_MLOps_Propuesta_Completa.pdf) (~8–12 páginas).

### Removed

- Formulaciones vagas del tipo “herramientas viables en evolución” sin elección concreta.
- Página vacía en PDF original (contenido incompleto de Semana 1).
- Dependencia exclusiva de un único modo de despliegue (solo localhost).

### Deprecated

- [`diagrama_pipeline_mlops.png`](diagrama_pipeline_mlops.png) — sustituido por `diagrama_pipeline_e2e.png` (se mantiene por compatibilidad hasta próxima limpieza).

---

## [1.1.0] — Unidad 3 intermedia (`c2d57d0`)

### Added

- [`PROPUESTA_PIPELINE_MLOPS.md`](PROPUESTA_PIPELINE_MLOPS.md) con argumentos por etapa.
- Sección **enfermedades huérfanas** (desbalance + patologías no representadas).
- Sección **entrenamiento/calibración** (reglas + camino ML evolutivo).
- [`Pipeline_MLOps_Propuesta_Completa.pdf`](Pipeline_MLOps_Propuesta_Completa.pdf) y [`generar_pdf_pipeline_mlops.py`](generar_pdf_pipeline_mlops.py).
- [`README.md`](../README.md) raíz con índice del proyecto.

### Changed

- README del servicio: enlace a documentación completa del pipeline.
- Propuesta Semana 1 ampliada de párrafos breves a tablas por etapa.

---

## [1.0.0] — Semana 1 (`f570021`)

### Added

- Propuesta inicial en PDF: 8 etapas (datos → monitoreo).
- Secciones (A) Diseño, (B) Desarrollo, (C) Despliegue/monitoreo.
- Diagrama simple de pipeline.
- Implementación MVP: reglas en `modelo_simulado.py`, Flask, Dockerfile, datos en `data/`.

### Limitaciones conocidas (v1.0.0)

- Texto argumentativo insuficiente para evaluación “Propuesta excelente”.
- Sin detalle de enfermedades huérfanas ni entrenamiento concreto.
- Sin despliegue cloud ni stack MLOps moderno definido.
- Tercera página del PDF vacía.

---

## Rationale — Por qué evolucionó la propuesta

| Decisión v2.0.0 | Motivo |
|-----------------|--------|
| 12 etapas vs 8 | Alinear con MLOps maduro (CD4ML): catálogo, feature store, registry, observabilidad y retrain como etapas propias, no notas al pie. |
| LightGBM en producción | Datos tabulares, CPU, interpretable con SHAP; supera reglas si se mide en F1/recall AGUDA. Reglas quedan como baseline auditable ya entregado. |
| Despliegue híbrido | Restricción del enunciado: médico en PC local **o** vía servicio remoto; Cloud Run minimiza ops y costo. |
| DVC + MLflow | Estándar de facto en equipos ML pequeños; reproducibilidad exigible por evaluador técnico. |
| Suposiciones explícitas | Problema abierto; el evaluador debe ver qué se asume y qué pasa si falla. |
| CHANGELOG | Requisito del ejercicio: evidenciar cambios Semana 1 → entrega actual. |

---

## Comparativa rápida

| Tema | v1.0.0 | v2.0.0 | v2.1.0 Actual |
|------|--------|--------|---------------|
| Estructura doc | PDF 8 etapas | 12 etapas lineales | Case Challenge + Part 1/2/3 |
| Diagrama central | Simple | 12 cajas horizontales | Offline Training \| Predictions |
| Referencia sample | No | No | Sí (mlops-sample) |
| Etapas | 8 | 12 | 12 (apéndice) + Part 1 narrativo |
| Argumentos por etapa | Escasos | Medios | Completos (plantilla 8 puntos) |
| Suposiciones | Implícitas | Parciales | Registro S1–S8 |
| Modelo producción | Reglas | Reglas + ML futuro | LightGBM (+ reglas MVP) |
| Despliegue | Local | Local | Local + Cloud |
| Tecnologías | Genéricas | Listadas | Elegidas + descartadas |
| Enfermedades huérfanas | No | Sí | Sí + política ML |
| CI/CD | No | Mencionado | Diagrama + jobs |
| CHANGELOG | No | No | Sí |
