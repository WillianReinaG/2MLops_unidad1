# ADR-002: Despliegue híbrido edge (local) y cloud

**Estado:** Aceptado  
**Fecha:** 2026-05-29

## Contexto

El médico puede operar en consultorio sin internet estable o acceder remotamente al servicio. Debe existir un único contrato API (`POST /predecir`).

## Decisión

| Modo | Plataforma | Auth | Cuándo |
|------|------------|------|--------|
| Edge | Docker Compose en laptop | N/A (localhost) | Offline, baja latencia, datos no salen del dispositivo |
| Cloud | Google Cloud Run (primario) / AWS App Runner (alternativa) | API key + TLS 1.2+ | Movilidad, dispositivos sin Docker |

Misma imagen OCI desde GHCR; artefacto de modelo desde MLflow Production.

## Suposiciones

- Modelo <10 MB; inferencia p95 <100 ms en CPU.
- Cloud Run scale-to-zero aceptable (cold start <5 s académico).

## Consecuencias

- (+) Cumple restricción dual del enunciado con mínima divergencia operativa.
- (−) Dos superficies de ataque; mitigado con DevSecOps (ADR-003, escaneo Trivy, secretos en Secret Manager).

## Alternativas descartadas

- Kubernetes obligatorio: complejidad excesiva para el alcance.
- Solo SaaS propietario: vendor lock-in innecesario en academia.
