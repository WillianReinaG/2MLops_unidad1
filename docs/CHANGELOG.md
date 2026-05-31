# Changelog (documentación extendida)

> **Entrega Unidad 3:** el CHANGELOG principal que compara **Semana 1 (`main`) vs Unidad 3 (`unidad3`)** está en la raíz del repositorio: [`../CHANGELOG.md`](../CHANGELOG.md).

---

## Resumen de versiones

| Versión | Rama / momento | Documento principal |
| :--- | :--- | :--- |
| **1.0.0** | `main` — Semana 1 | `docs/punto 1 descripcion pipeline MLops.pdf` + MVP |
| **2.0.0** | `unidad3` — Unidad 3 | [`PROPUESTAPipeLine.md`](PROPUESTAPipeLine.md) + [`../CHANGELOG.md`](../CHANGELOG.md) |

---

## [2.0.0] — Unidad 3 — Alineación ejemplo `entrega3` (actual)

### Added

- [`PROPUESTAPipeLine.md`](PROPUESTAPipeLine.md): pipeline **Data Pipeline → Develop → Staging → PROD** con tecnologías y suposiciones por etapa.
- [`../CHANGELOG.md`](../CHANGELOG.md): comparación explícita con propuesta Semana 1.
- [`../README.md`](../README.md): índice del repo, diagrama Mermaid, enlace al pipeline.
- Diagrama Mermaid de topología equivalente a `PipeLineML.drawio.png` del [ejemplo del curso](https://github.com/rchicangana/healthPrediction-mlops-U2/tree/entrega3).

### Changed

- Enfoque documental: de PDF único + listas v3.x a formato **curso / entrega3** con justificación por herramienta.
- Stack: GitHub Actions (no Jenkins), DVC (no PostgreSQL para train batch), Bandit+Trivy (no SonarQube), MLflow Registry, Evidently.

### Unchanged (por diseño)

- Código MVP en `servicio_estado_clinico/` — baseline Semana 1.

---

## Historial de iteraciones documentales previas (referencia)

| Versión | Notas |
| :--- | :--- |
| 3.1.0 | Sustento por capa/fase (por qué / para qué / mejora) en `PROPUESTA_PIPELINE_MLOPS.md` |
| 3.0.0 | Ops stack, ADR, Model Card, SLI/SLO |
| 2.1.0 | Estructura Offline \| Predictions (mlops-sample) |
| 2.0.0 | Propuesta ampliada 12 etapas |
| 1.0.0 | PDF Semana 1 |

El documento [`PROPUESTA_PIPELINE_MLOPS.md`](PROPUESTA_PIPELINE_MLOPS.md) conserva iteraciones 2.x–3.x como **referencia histórica**. La entrega Unidad 3 oficial es [`PROPUESTAPipeLine.md`](PROPUESTAPipeLine.md).
