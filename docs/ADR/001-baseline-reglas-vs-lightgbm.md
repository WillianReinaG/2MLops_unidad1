# ADR-001: Baseline determinista vs LightGBM en producción

**Estado:** Aceptado  
**Fecha:** 2026-05-29  
**Decisores:** Equipo ML (propuesta académica)

## Contexto

La consigna inicial exige una función simulada interpretable (`modelo_simulado.py`). La propuesta de producción objetivo requiere un modelo supervisado entrenado con trazabilidad MLOps.

## Decisión

1. **MVP / Staging inicial:** reglas deterministas versionadas en Git (implementado).
2. **Production objetivo:** LightGBM + Pipeline sklearn registrado en MLflow.
3. **Promoción:** solo si F1 macro y recall de `ENFERMEDAD AGUDA` en hold-out ≥ baseline de reglas.
4. **Fallback runtime:** si confianza del modelo < τ, devolver predicción de reglas + flag `requiere_revision_humana`.

## Consecuencias

- (+) Baseline auditable para evaluadores y médicos en demo.
- (+) Camino ML claro sin romper entregables previos.
- (−) Dos lógicas a mantener hasta convergencia; mitigado con tests de paridad en casos límite.

## Alternativas descartadas

| Alternativa | Motivo de rechazo |
|-------------|-------------------|
| Solo reglas en producción | No cumple madurez MLOps ni generalización |
| Solo ML sin baseline | Pierde interpretabilidad y comparación académica |
| Deep learning | Sin GPU; datos tabulares pequeños; explicabilidad más costosa |
