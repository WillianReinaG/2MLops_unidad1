# Model Card — Clasificador de estado clínico simulado

> Formato inspirado en [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993). Alcance académico; no producto clínico.

## Detalles del modelo

| Campo | MVP (implementado) | Producción (objetivo) |
|-------|-------------------|------------------------|
| **Nombre** | `baseline-reglas-v1` | `estado-clinico-lgbm` |
| **Versión** | Git `servicio_estado_clinico/` | MLflow Registry Production |
| **Tipo** | Reglas deterministas | LightGBM multiclass + sklearn Pipeline |
| **Autor** | Proyecto 2MLops | Equipo ML |
| **Licencia datos** | Uso académico CSV curso | Igual + DVC snapshot |

## Uso previsto

Triaje orientativo simulado en cuatro estados a partir de ≥3 signos vitales/laboratorio simplificados. **No** sustituye diagnóstico clínico ni cubre enfermedades huérfanas por nombre.

## Factores de rendimiento

**Población entrenamiento:** ~70 000 registros tabulares sintéticos/académicos.

**Distribución de clases (`categoria_clinica`):**

| Clase | % aprox. |
|-------|----------|
| ENFERMEDAD LEVE | 49,9 |
| ENFERMEDAD CRÓNICA | 30,2 |
| NO ENFERMO | 18,1 |
| ENFERMEDAD AGUDA | 1,9 |

**Métricas objetivo (producción):** F1 macro, recall AGUDA, matriz de confusión vs baseline reglas.

## Consideraciones éticas y limitaciones

- Sesgo poblacional no auditado para uso real.
- Cuatro categorías agregadas ocultan heterogeneidad clínica.
- Decisiones finales requieren criterio médico humano.
- Flag propuesto: `requiere_revision_humana` en baja confianza o perfil atípico.

## Mantenimiento

Retrain triggers: drift Evidently, N nuevos registros, calendario trimestral. Ver [`PROPUESTA_PIPELINE_MLOPS.md`](PROPUESTA_PIPELINE_MLOPS.md).
