# Propuesta de pipeline MLOps end-to-end — Estado clínico simulado

**Versión:** 2.0 (reestructuración Unidad 3)  
**Proyecto:** [WillianReinaG/2MLops_unidad1](https://github.com/WillianReinaG/2MLops_unidad1)  
**Alcance:** documentación ejecutable por un equipo ML; trabajo académico, no producto clínico certificado.

---

## Resumen ejecutivo

### Problema

Un médico necesita clasificar de forma orientativa el estado de un paciente en una de cuatro categorías (`NO ENFERMO`, `ENFERMEDAD LEVE`, `ENFERMEDAD AGUDA`, `ENFERMEDAD CRÓNICA`) a partir de **al menos tres signos medibles** (presión, colesterol, glucosa, hábitos, antecedentes). El reto MLOps no es solo predecir, sino operar un ciclo **reproducible, versionado, desplegable y observable** de extremo a extremo.

### Solución propuesta

Pipeline de **12 etapas** que cubre gobernanza, datos, ML, empaquetado, **despliegue híbrido (local + nube)**, observabilidad y reentrenamiento continuo.

| Rol | Implementación |
|-----|----------------|
| **MVP / baseline (ya en repo)** | Reglas deterministas en `servicio_estado_clinico/modelo_simulado.py` + Flask + Docker |
| **Producción objetivo (equipo ML)** | Modelo supervisado **LightGBM** registrado en MLflow, servido en el mismo contrato API `POST /predecir` |

### Modos de uso del médico

1. **Local:** `docker compose up` en su PC (CPU, sin GPU; imagen <500 MB).
2. **Remoto:** peticiones HTTPS a API en **Google Cloud Run** o **AWS App Runner** con API key.

Ambos modos comparten **misma imagen Docker**, **mismo JSON de entrada/salida** y **mismo modelo versionado** desde MLflow Model Registry.

### Diagramas

| Figura | Archivo |
|--------|---------|
| Pipeline 12 etapas | [`diagrama_pipeline_e2e.png`](diagrama_pipeline_e2e.png) |
| Despliegue híbrido | [`diagrama_despliegue_hibrido.png`](diagrama_despliegue_hibrido.png) |
| CI/CD MLOps | [`diagrama_cicd_mlops.png`](diagrama_cicd_mlops.png) |
| Flujo datos → ML → serve | [`diagrama_datos_ml.png`](diagrama_datos_ml.png) |

Historial de cambios vs Semana 1: [`CHANGELOG.md`](CHANGELOG.md).

---

## Registro maestro de suposiciones

| ID | Suposición | Implicación si es falsa | Validación |
|----|------------|-------------------------|------------|
| S1 | Datos tabulares CSV (~70k filas) representan el dominio académico | Sesgo y métricas no generalizables | Análisis exploratorio + Evidently drift |
| S2 | Cuatro categorías agregadas son suficientes para el caso de uso | Diagnósticos finos no cubiertos | Alcance documentado; revisión humana |
| S3 | Inferencia CPU <100 ms; modelo <10 MB | Latencia inaceptable en local | Benchmark en contenedor |
| S4 | Médico tiene Docker Desktop o conectividad HTTPS | No puede usar el servicio | Modo alternativo documentado |
| S5 | No se almacenan datos clínicos reales en logs | Riesgo de privacidad | Logs JSON sin PII; retención 30 días |
| S6 | Clase AGUDA ~1,9 % del dataset | Modelo ignora minoría | Estratificación, class_weight, recall AGUDA |
| S7 | Reglas MVP calibradas alineadas al CSV | Desalineación train/serve | Tests de paridad reglas vs etiquetas CSV |
| S8 | Equipo ML tiene acceso a GitHub + cloud free tier | No se despliega cloud | Fallback solo local |

---

## Plantilla de etapas

Cada etapa incluye: **Objetivo · Suposiciones · Entradas/Salidas · Tecnologías · Proceso · Criterios · Riesgos · Relación con repo**.

---

## Etapa 0 — Encuadre del problema y alcance clínico simulado

### Objetivo

Definir el alcance, actores, métricas de negocio simuladas y límites clínicos antes de cualquier pipeline técnico.

### Suposiciones

- El problema es **triaje orientativo**, no diagnóstico definitivo.
- El médico acepta disclaimer en UI y documentación.
- **Implicación si falla:** uso clínico real sin supervisión → mitigar con gates de aprobación y flag `requiere_revision_humana`.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| Requisitos del curso, CSV en `data/` | Documento de alcance, matriz RACI, definición de KPIs |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| Markdown en repo | Versionado con Git, revisable en PR | Confluence (dependencia externa, no reproducible en entrega académica) |
| Matriz RACI ligera | Clarifica roles sin burocracia | ITIL completo (excesivo para el curso) |

### Proceso

1. Documentar usuario (médico), entradas mínimas (≥3 campos), salidas (4 etiquetas).
2. Definir KPIs: latencia p95, tasa error 4xx, F1 macro, recall AGUDA.
3. Fijar exclusiones: enfermedades huérfanas por nombre, multi-región, HA.

### Criterios de aceptación

- Alcance firmado por el equipo; KPIs numéricos definidos.
- Disclaimer clínico presente en propuesta y UI.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Alcance difuso | Checklist de exclusiones explícitas |

### Relación con repo

**Implementado:** README y aviso en `templates/index.html`. **Propuesto:** ampliar KPIs en `docs/`.

---

## Etapa 1 — Ingesta y versionado de datos

### Objetivo

Capturar y versionar datasets de forma reproducible vinculando cada experimento a un snapshot de datos.

### Suposiciones

- El volumen (~70k filas, <50 MB) cabe en Git + DVC sin lake corporativo.
- **Implicación si falla:** usar solo object storage (S3) sin DVC remoto.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| `data/raw/enfermedades_cardiacas.csv` | Snapshot `data@vN` con hash DVC |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **Git** | Metadatos, scripts, `.dvc` | Solo carpetas manuales (sin trazabilidad) |
| **DVC** | Versionado de blobs grandes, reproducibilidad | Delta Lake (overkill para CSV único) |
| **MinIO** (local) / **S3** (cloud) | Remote DVC barato y estándar | Git LFS (límites y costo en repos grandes) |

### Proceso

1. `dvc init`; configurar remote MinIO local o bucket S3.
2. `dvc add data/raw/...` y `data/processed/...`.
3. Tag `data-v1.0.0` alineado a commit Git.
4. CI verifica que `dvc pull` + hash coincide antes de entrenar.

### Criterios de aceptación

- Cada run MLflow referencia `data_version` en tags.
- Reproducibilidad: mismo hash → mismas métricas ± tolerancia.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Remote DVC no configurado | MinIO en docker-compose de desarrollo |

### Relación con repo

**Implementado:** CSV en `data/raw/` y `data/processed/`. **Propuesto:** DVC + remote.

---

## Etapa 2 — Catálogo y linaje de datos

### Objetivo

Documentar columnas, propietarios, transformaciones y linaje raw → processed → features.

### Suposiciones

- Un catálogo ligero basta; no hay centenas de fuentes.
- **Implicación si falla:** linaje mínimo solo vía DVC + MLflow tags.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| Schemas CSV, scripts de transformación | Catálogo de columnas + grafo de linaje |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **DVC pipeline** stages | Linaje embebido en repo | Apache Atlas (infra pesada) |
| **OpenMetadata** (opcional cloud) | UI de descubrimiento si el equipo crece | DataHub self-hosted (RAM alta en laptop médico) |

### Proceso

1. Documentar schema en catálogo (columna, tipo, rango, nullable).
2. Registrar transformaciones: raw → limpio → 4 categorías → features.
3. Enlazar cada stage DVC a commit y script (`scripts/ajustar_cuatro_categorias.py`).

### Criterios de aceptación

- Toda columna usada en entrenamiento tiene entrada en catálogo.
- Linaje raw → `categoria_clinica` trazable en un diagrama.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Catálogo desactualizado | PR obligatorio al cambiar schema |

### Relación con repo

**Implementado:** columnas implícitas en CSV. **Propuesto:** catálogo YAML en `docs/data_catalog.yaml`.

---

## Etapa 3 — Validación y quality gates

### Objetivo

Bloquear pipelines downstream si los datos no cumplen esquema, rangos y reglas de negocio.

### Suposiciones

- Rangos físicos conocidos (PA 50–250 mmHg, colesterol/glucosa 1–3).
- **Implicación si falla:** filas inválidas distorsionan entrenamiento → gate falla CI.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| CSV procesado | Suite GX/Pandera + informe HTML; gate pass/fail |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **Great Expectations** | Expectativas declarativas, informes HTML, integración CI | Validación ad hoc solo pandas (no auditable) |
| **Pandera** (complemento) | Schemas Python tipados en scripts | Solo asserts manuales |

### Proceso

1. Definir expectations: tipos, rangos, unicidad de `id`, proporción nulos máxima.
2. Ejecutar checkpoint en CI (GitHub Actions) antes de train.
3. Fallo → no promover modelo ni reconstruir imagen prod.

### Criterios de aceptación

- 100 % filas cumplen expectations o filas rechazadas documentadas.
- CI falla si checkpoint falla.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Expectations demasiado rígidas | Revisión periódica con datos nuevos |

### Relación con repo

**Implementado:** validación en API (`validar_entrada_minima`). **Propuesto:** GX sobre CSV batch.

---

## Etapa 4 — Feature engineering y feature store

### Objetivo

Producir features consistentes entre entrenamiento e inferencia, eliminando training-serving skew.

### Suposiciones

- Seis features tabulares bastan; no hay embeddings ni texto.
- **Implicación si falla:** añadir features derivadas (IMC) con mismo pipeline sklearn.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| `enfermedades_cardiacas_4categorias.csv` | `features.parquet` + definición Feast offline |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **pandas** | Estándar, equipo lo conoce | Spark (innecesario a 70k filas) |
| **scikit-learn Pipeline** + ColumnTransformer | Serializable con el modelo | Transformaciones duplicadas en train y serve |
| **Feast** (offline store) | Contrato feature train/serve reproducible | Feature store enterprise Tecton (costo/complejidad) |

### Proceso

1. Seleccionar features: presión sistólica/diastólica, colesterol, glucosa, fumador, presencia_enfermedad.
2. Codificar categóricas (OneHot/boolean) en Pipeline sklearn.
3. Materializar parquet versionado; registrar en Feast entity `paciente`.
4. Exportar pipeline + modelo como un solo artefacto MLflow.

### Criterios de aceptación

- Misma transformación en batch (train) y online (API) vía artefacto único.
- Tests de paridad: muestra CSV → features idénticas batch vs online.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Skew train/serve | Un solo Pipeline serializado |

### Relación con repo

**Implementado:** campos API en `modelo_simulado.py`. **Propuesto:** Pipeline sklearn + Feast.

---

## Etapa 5 — Entrenamiento y experimentación

### Objetivo

Entrenar modelo supervisado multiclass optimizado para CPU y registrar experimentos trazables.

### Suposiciones

- LightGBM supera baseline de reglas en F1 macro y recall AGUDA.
- **Implicación si falla:** mantener reglas en Production hasta nuevo experimento.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| `features.parquet`, split estratificado | Runs MLflow con params, metrics, artefacto `.pkl` |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **LightGBM** | Tabular, CPU rápido, maneja desbalance | Deep learning (overkill, requiere GPU) |
| **Optuna** | HPO eficiente, pocas trials | GridSearch exhaustivo (lento) |
| **MLflow Tracking** | Estándar MLOps, integra registry | Logs en spreadsheets |

### Proceso

1. Split 70/15/15 estratificado por `categoria_clinica`.
2. Optuna optimiza: `num_leaves`, `learning_rate`, `class_weight` (refuerzo AGUDA).
3. Log en MLflow: `data_version`, git commit, hiperparámetros, F1 por clase.
4. Guardar Pipeline completo (preprocess + LGBM).

### Criterios de aceptación

- F1 macro val > baseline reglas.
- Recall AGUDA val ≥ baseline reglas.
- Reproducibilidad con `random_state` fijo.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Overfitting a mayoría LEVE | Estratificación + métricas por clase |

### Relación con repo

**Implementado:** reglas en `modelo_simulado.py`. **Propuesto:** script `ml/train.py` (documentado, no obligatorio en repo).

---

## Etapa 6 — Evaluación, explicabilidad y aprobación humana

### Objetivo

Validar modelo en test, explicar predicciones y obtener gate manual antes de producción.

### Suposiciones

- SHAP TreeExplainer es suficiente para explicabilidad tabular simulada.
- **Implicación si falla:** importancia de features nativa LightGBM como fallback.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| Modelo candidato, test set | Informe evaluación + SHAP + decisión approve/reject |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **MLflow** metrics | Comparación entre runs | Métricas manuales |
| **SHAP** | Explicaciones locales por predicción | LIME (menos estable en tabular) |
| **Gate manual** (PR + aprobador) | Control humano académico/clínico simulado | Auto-promote (riesgo) |

### Proceso

1. Evaluar en test: matriz confusión, F1, recall AGUDA.
2. Generar SHAP summary y ejemplos por clase.
3. Comparar vs baseline reglas (`modelo_simulado.py`) en mismo test.
4. Aprobador registra decisión en MLflow comment + merge PR.

### Criterios de aceptación

- Test F1 macro ≥ baseline AND recall AGUDA ≥ baseline.
- Informe SHAP archivado en MLflow artifacts.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Métricas buenas en test pero mal en prod | Monitoreo Evidently post-deploy |

### Relación con repo

**Implementado:** tests manuales API. **Propuesto:** suite evaluación automatizada.

---

## Etapa 7 — Registro y promoción de modelos

### Objetivo

Gestionar versiones del modelo con estados Staging → Production y rollback.

### Suposiciones

- Un solo modelo activo en Production por entorno.
- **Implicación si falla:** A/B testing documentado como fase posterior.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| Artefacto aprobado en MLflow | `estado-clinico-lgbm@Production` |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **MLflow Model Registry** | Integrado con tracking, stages | Carpeta `models/` sin gobernanza |
| Tags: `data_version`, `git_sha` | Trazabilidad completa | Versionado semver manual |

### Proceso

1. Registrar modelo desde run ganador.
2. Promover a Staging → smoke tests en contenedor.
3. Promover a Production tras gate; retirar versión anterior a Archived.
4. Baseline reglas permanece tag `baseline-rules` para comparación.

### Criterios de aceptación

- Production apunta a un único version ID.
- Rollback a versión anterior <15 min (redeploy imagen).

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Promoción accidental | Solo CI/CD puede cambiar stage Production |

### Relación con repo

**Implementado:** código reglas versionado en Git. **Propuesto:** registry MLflow.

---

## Etapa 8 — Empaquetado reproducible

### Objetivo

Construir imagen Docker que embeba o descargue modelo Production y dependencias fijadas.

### Suposiciones

- Imagen final <500 MB, sin GPU.
- **Implicación si falla:** descarga modelo al arranque desde MLflow (cold start mayor).

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| Modelo Production, API spec | Imagen en **GHCR** `ghcr.io/org/estado-clinico:sha` |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **Docker multi-stage** | Imagen mínima | Instalar deps en runtime |
| **FastAPI + joblib** (evolución API) o Flask actual | FastAPI: OpenAPI, async ligero | Mantener solo Flask sin cambio (válido MVP) |
| **GHCR** | Integración nativa GitHub Actions | Docker Hub rate limits |

### Proceso

1. Stage build: exportar modelo desde MLflow a `/app/model`.
2. Stage runtime: Python slim, requirements pinneados, usuario non-root.
3. Healthcheck `GET /health`.
4. CI publica imagen tagged por git SHA y `latest-prod`.

### Criterios de aceptación

- `docker pull` + run → `/predecir` responde en <2 s cold start local.
- Misma imagen pasa escaneo básico (Trivy en CI).

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Modelo desincronizado de imagen | Build solo desde Production registry ID |

### Relación con repo

**Implementado:** `servicio_estado_clinico/Dockerfile` (reglas). **Propuesto:** Dockerfile prod con artefacto MLflow.

---

## Etapa 9 — Despliegue local (médico en su PC)

### Objetivo

Permitir inferencia offline/low-latency en laptop del médico sin dependencia de nube.

### Suposiciones

- Docker Desktop disponible (Windows/Mac); 4 GB RAM libres.
- **Implicación si falla:** instalador alternativo Python venv documentado en README.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| Imagen GHCR, `docker-compose.yml` | `http://localhost:5000/predecir` |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **Docker Compose** perfil `local` | Un comando; incluye MLflow opcional dev | Instalación manual pip (menos reproducible) |
| Mapeo `-p 5000:5000` | Compatible con MVP actual | Puerto dinámico (confunde al médico) |

### Proceso

1. `docker compose --profile local up`.
2. Formulario `GET /` o `POST /predecir` con JSON actual.
3. Modelo cargado desde volumen o embebido en imagen.
4. Documentar requisitos mínimos: CPU 2 cores, 4 GB RAM, 2 GB disco.

### Criterios de aceptación

- Médico obtiene predicción con ≥3 campos sin internet.
- Latencia p95 <100 ms tras warm-up.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Firewall bloquea puerto | Instrucciones Windows/Linux en README |

### Relación con repo

**Implementado:** `docker run -p 5000:5000` probado. **Propuesto:** compose con perfil local.

---

## Etapa 10 — Despliegue cloud (médico remoto)

### Objetivo

Exponer la misma API vía HTTPS para médicos sin Docker local o en movilidad.

### Suposiciones

- Conectividad estable; latencia red <200 ms aceptable.
- **Implicación si falla:** modo local como fallback.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| Imagen GHCR | URL `https://estado-clinico-xxx.run.app/predecir` |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **Google Cloud Run** | Serverless, escala a cero, pago por uso, HTTPS incluido | EC2 24/7 (costo fijo innecesario) |
| **AWS App Runner** (alternativa) | Equivalente serverless | Kubernetes (complejidad operativa) |
| **API key** en header | Auth simple académica | OAuth completo (overkill) |

### Proceso

1. CI despliega imagen a Cloud Run tras promote Production.
2. Variables: `MLFLOW_MODEL_URI`, `API_KEY` desde Secret Manager.
3. TLS terminado en Cloud Run; logs sin payload completo (PII mínima).
4. Médico configura cliente (formulario web apuntando a URL cloud o curl).

### Criterios de aceptación

- HTTPS válido; 401 sin API key; 200 con key válida.
- Auto-scale 0→1 instancias; cold start <5 s aceptable académicamente.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Exposición pública | API key + rate limiting Cloud Run |

### Relación con repo

**Implementado:** acceso LAN documentado. **Propuesto:** deploy Cloud Run vía GitHub Actions.

---

## Etapa 11 — Observabilidad, monitoreo y drift

### Objetivo

Detectar degradación operativa y de modelo (data drift, concept drift) en local y cloud.

### Suposiciones

- Volumen de tráfico académico bajo; métricas batch diarias bastan.
- **Implicación si falla:** revisión manual semanal de logs.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| Logs API, muestras de input | Dashboard Grafana + alertas drift |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **Prometheus** + **Grafana** | Estándar métricas latencia/errores | Solo logs texto |
| **Evidently AI** | Reportes drift tabular listos | Custom drift scripts |
| Logs **JSON** estructurados | Parseables, sin PII | Logs free-text |

### Proceso

1. Instrumentar: `http_requests_total`, `latency_seconds`, `predictions_by_class`.
2. Evidently compara ventana producción vs referencia train semanalmente.
3. Alertas: F1 online estimado ↓, drift en presión/glucosa, spike 5xx.
4. Distribución AGUDA fuera de rango 1–3 % → investigar.

### Criterios de aceptación

- Dashboard operativo en 24 h post-deploy.
- Alerta configurada para error rate >5 %.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Sin labels en prod | Drift unsupervised + muestreo manual etiquetado |

### Relación con repo

**Implementado:** logs Flask básicos. **Propuesto:** stack observabilidad.

---

## Etapa 12 — Retraining continuo y gobernanza de cambios

### Objetivo

Reentrenar o recalibrar ante datos nuevos, drift o calendario, con rollback seguro.

### Suposiciones

- Nuevos datos llegan en lotes CSV periódicos.
- **Implicación si falla:** retrain manual documentado.

### Entradas / salidas

| Entrada | Salida |
|---------|--------|
| Trigger (drift / N registros / cron) | Nuevo modelo Staging o recalibración reglas |

### Tecnologías

| Elegida | Por qué | Alternativa descartada |
|---------|---------|------------------------|
| **GitHub Actions** scheduled | Ya en GitHub; sin infra extra | Airflow managed (costo) |
| **Prefect** (alternativa) | Orquestación Python rica | Cron shell scripts (frágil) |
| MLflow rollback | Un click a versión anterior | Redeploy manual sin registry |

### Triggers propuestos

1. ≥5 000 registros nuevos versionados en DVC.
2. Evidently drift score > umbral acordado.
3. F1 online cae >10 % vs baseline.
4. Calendario trimestral + aprobación manual.

### Proceso

1. Workflow `retrain.yaml`: pull data → GX → train → eval → register Staging.
2. Smoke test automático; aprobador promueve a Production.
3. Rebuild imagen → deploy Cloud Run + tag local compose.
4. Si falla smoke: rollback registry + redeploy imagen anterior.

### Criterios de aceptación

- Pipeline retrain ejecutable en <60 min CPU.
- Rollback probado al menos una vez en staging.

### Riesgos y mitigación

| Riesgo | Mitigación |
|--------|------------|
| Retrain empeora AGUDA | Gate recall AGUDA obligatorio |

### Relación con repo

**Implementado:** script etiquetado manual. **Propuesto:** workflow CI retrain.

---

## Enfermedades huérfanas y desbalance

### Clase minoritaria (AGUDA ~1,9 %)

| Acción | Etapa | Detalle |
|--------|-------|---------|
| Estratificación | 5 | Split mantiene AGUDA en train/val/test |
| `class_weight` / scale_pos_weight | 5 | LightGBM penaliza errores en AGUDA |
| Prioridad reglas | MVP | AGUDA evaluada antes que LEVE |
| Métrica gate | 6 | Recall AGUDA ≥ baseline |
| Monitoreo | 11 | Alerta si frecuencia predicha AGUDA ∉ [1%,3%] |

### Patologías raras no en el dataset

- El sistema **no** nombra enfermedades huérfanas.
- Perfiles atípicos: respuesta `ENFERMEDAD LEVE` + `"requiere_revision_humana": true` (extensión API propuesta).
- Datos nuevos de patologías no vistas → cuarentena en bucket `raw/quarantine/`; no entrenan prod sin revisión.

---

## Baseline MVP vs producción objetivo

| Aspecto | MVP (implementado) | Producción (objetivo equipo ML) |
|---------|-------------------|--------------------------------|
| Lógica | Reglas `modelo_simulado.py` | LightGBM + sklearn Pipeline |
| Trazabilidad | Git | Git + DVC + MLflow |
| Despliegue | Docker local | Docker local **y** Cloud Run |
| Explicabilidad | Reglas legibles | SHAP + reglas fallback |
| Promoción | Commit manual | MLflow Registry + CI |

**Criterio de promoción ML → Production:** F1 macro y recall AGUDA en test superan al baseline de reglas en el mismo split.

---

## Seguridad y cumplimiento académico

- Disclaimer clínico en UI y documentos.
- API key para cloud; rotación semestral.
- Secretos en GitHub Secrets / GCP Secret Manager (nunca en repo).
- TLS obligatorio en cloud; logs sin valores de presión identificables si hay riesgo PII.
- Retención logs 30 días en entorno académico.

---

## CI/CD end-to-end

Ver [`diagrama_cicd_mlops.png`](diagrama_cicd_mlops.png).

| Job | Trigger | Acción |
|-----|---------|--------|
| `lint-test` | PR | ruff, pytest unitarios + contrato API |
| `data-quality` | PR / schedule | DVC pull + Great Expectations |
| `train` | manual / schedule | Optuna + MLflow |
| `build-push` | merge main | Docker build → GHCR |
| `deploy-staging` | tag | Cloud Run staging + smoke |
| `deploy-prod` | approve | Cloud Run prod + rollback tag |

---

## Plan de puesta en marcha (equipo ML)

| Fase | Duración | Entregables | Roles |
|------|----------|-------------|-------|
| 0 — Baseline | 1 sem | MVP reglas operativo (hecho) | Dev |
| 1 — Datos | 1–2 sem | DVC, GX, catálogo | Data Eng |
| 2 — ML | 2 sem | LightGBM en MLflow, SHAP, beats baseline | ML Eng |
| 3 — Deploy híbrido | 1 sem | GHCR, compose local, Cloud Run | MLOps |
| 4 — Observabilidad | 1 sem | Grafana, Evidently, retrain workflow | MLOps |

**Total estimado:** 6–7 semanas para equipo de 2–3 personas part-time académico.

---

## Viabilidad

- Datos, scripts MVP y Docker **ya existen** en el repositorio.
- Stack propuesto usa herramientas **open source** y free tiers cloud.
- Modelo tabular CPU-friendly; médico puede operar **local o remoto** con el mismo contrato API.
- Cada etapa tiene suposiciones, tecnologías justificadas, criterios de aceptación y relación con el código actual.

---

*Documento académico v2.0 — no constituye asesoría clínica. Ver [CHANGELOG.md](CHANGELOG.md) para evolución desde Semana 1.*
