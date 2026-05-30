# ADR-003: Stack de observabilidad y capa AIOps

**Estado:** Aceptado  
**Fecha:** 2026-05-29

## Contexto

Un pipeline de nivel posgrado requiere observabilidad más allá de logs ad hoc: métricas, trazas, drift y respuesta operativa semi-automatizada (AIOps).

## Decisión

**Capa 1 — Métricas (Prometheus):** latencia, RPS, error rate, distribución de clases predichas.  
**Capa 2 — Visualización (Grafana):** dashboards por entorno (staging/prod).  
**Capa 3 — ML observability (Evidently):** data drift, concept drift proxy, reportes semanales.  
**Capa 4 — AIOps (propuesto):** reglas de alerta + runbook automatizado vía GitHub Actions (rollback imagen, ticket simulado); sin auto-promote de modelos sin gate humano.

OpenTelemetry para trazas HTTP en evolución FastAPI (trace_id en logs JSON).

## Consecuencias

- (+) Detección temprana de degradación en AGUDA (~1,9 % train).
- (−) Overhead operativo; aceptable en fases 4 del roadmap.

## Alternativas descartadas

- Solo logs Flask: insuficiente para drift y SLO.
- Plataforma APM comercial única: costo en free tier académico.
