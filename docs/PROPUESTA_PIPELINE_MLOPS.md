# Propuesta de pipeline MLOps — Estado clínico simulado

**Proyecto:** 2MLops (Unidad 3)  
**Repositorio:** [WillianReinaG/2MLops_unidad1](https://github.com/WillianReinaG/2MLops_unidad1)  
**Alcance:** trabajo académico; no sustituye criterio médico ni diagnostica enfermedades raras por nombre.

---

## 0. Resumen ejecutivo

### Problema

En un entorno clínico simulado, un médico necesita obtener rápidamente una **clasificación orientativa** del estado de un paciente a partir de signos medibles (presión arterial, colesterol, glucosa, hábitos, antecedentes). El reto no es solo calcular una etiqueta, sino hacerlo de forma **reproducible, versionada y desplegable**, como exige un pipeline MLOps.

### Usuario y salida

- **Usuario:** médico o evaluador que ingresa **al menos tres valores** vía formulario web o API REST.
- **Salida:** exactamente una de cuatro etiquetas:
  - `NO ENFERMO`
  - `ENFERMEDAD LEVE`
  - `ENFERMEDAD AGUDA`
  - `ENFERMEDAD CRÓNICA`

### Propuesta de solución

Implementar un pipeline MLOps de extremo a extremo que conecte:

1. Datos tabulares en `data/` (~70 000 registros de ejemplo).
2. Scripts de preparación y etiquetado (`scripts/ajustar_cuatro_categorias.py`).
3. Lógica de predicción en `servicio_estado_clinico/modelo_simulado.py` (función determinista calibrada con los datos).
4. Servicio HTTP Flask con endpoint `POST /predecir`.
5. Empaquetado y despliegue con Docker.

La propuesta incluye además el **camino de evolución** hacia un modelo supervisado entrenado, monitoreo operativo y retrabajo con datos nuevos.

### Por qué un pipeline MLOps (argumento central)

| Sin pipeline | Con pipeline propuesto |
|--------------|------------------------|
| Reglas en código sin trazabilidad | Datos versionados + reglas/modelo versionados |
| Imposible reproducir resultados en otro PC | Docker + dependencias fijadas |
| Sin visibilidad de calidad de datos | Etapa explícita de validación |
| Cambios manuales sin control | Registro de artefactos y promoción a producción |
| Sin plan ante datos nuevos | Triggers de reentrenamiento y recalibración |

---

## 1. Diagrama general y etapas del pipeline

El diagrama en `docs/diagrama_pipeline_mlops.png` muestra ocho etapas principales y un ciclo de retroalimentación (monitoreo → nuevos datos → recalibración/reentrenamiento).

### Etapa 1 — Datos brutos

| Aspecto | Detalle |
|---------|---------|
| **Por qué** | Toda decisión posterior depende de la calidad y procedencia de los datos. Sin esta base no hay trazabilidad ni auditoría. |
| **Qué se hace aquí** | Se almacenan CSV sin transformar en `data/raw/enfermedades_cardiacas.csv`. |
| **Herramientas viables** | Git para metadatos; DVC o carpeta versionada para snapshots grandes. |
| **Artefacto** | Dataset crudo con columnas demográficas y de riesgo cardiovascular. |
| **Criterio de éxito** | Archivo accesible, con licencia/uso académico documentado y checksum registrado. |

### Etapa 2 — Ingesta y versionado

| Aspecto | Detalle |
|---------|---------|
| **Por qué** | Permite saber **qué versión de datos** produjo cada versión del servicio o del modelo. |
| **Qué se hace aquí** | Copia controlada del raw hacia `data/processed/` tras limpieza; registro de fecha y script usado. |
| **Herramientas viables** | Git + `.gitignore` selectivo; DVC; MLflow Datasets. |
| **Artefacto** | `enfermedades_cardiacas_limpio.csv`. |
| **Criterio de éxito** | Cada ejecución del pipeline de datos deja un identificador de versión reproducible. |

### Etapa 3 — Calidad y validación de datos

| Aspecto | Detalle |
|---------|---------|
| **Por qué** | Valores fuera de rango o esquemas rotos degradan predicciones y generan errores en producción. |
| **Qué se hace aquí** | Comprobación de tipos, rangos (presión 50–250 mmHg, colesterol/glucosa 1–3), nulos y duplicados antes de etiquetar o servir. |
| **Herramientas viables** | Scripts Python con pandas; Great Expectations (evolución). |
| **Artefacto** | Informe de calidad o CSV validado. |
| **Criterio de éxito** | Cero filas con tipos incorrectos; documentación de filas descartadas. |

### Etapa 4 — Preparación y feature engineering

| Aspecto | Detalle |
|---------|---------|
| **Por qué** | Transforma datos crudos en entradas consistentes para reglas o modelos ML. |
| **Qué se hace aquí** | Limpieza, codificación de variables categóricas y generación de la columna `categoria_clinica` con `scripts/ajustar_cuatro_categorias.py`. |
| **Herramientas viables** | pandas, scikit-learn (partición train/val/test si hay ML). |
| **Artefacto** | `data/processed/enfermedades_cardiacas_4categorias.csv`. |
| **Criterio de éxito** | Distribución de clases documentada; alineación con reglas de `modelo_simulado.py`. |

**Distribución actual de clases (70 000 registros):**

| Categoría | Registros | % |
|-----------|-----------|---|
| ENFERMEDAD LEVE | 34 944 | 49,9 % |
| ENFERMEDAD CRÓNICA | 21 111 | 30,2 % |
| NO ENFERMO | 12 650 | 18,1 % |
| ENFERMEDAD AGUDA | 1 295 | 1,9 % |

### Etapa 5 — Entrenamiento, calibración y registro

| Aspecto | Detalle |
|---------|---------|
| **Por qué** | Centraliza la lógica predictiva y permite comparar versiones antes de desplegar. |
| **Implementación actual** | Función determinista en `modelo_simulado.py`, calibrada con las mismas reglas que el script de etiquetado (baseline interpretable). |
| **Evolución ML** | Regresión logística o Random Forest sobre features tabulares; registro en MLflow o carpeta `models/`. |
| **Artefacto** | Código versionado + (futuro) archivo `.pkl` o reglas exportadas. |
| **Criterio de éxito** | Predicciones reproducibles; métricas documentadas si hay modelo entrenado. |

### Etapa 6 — Empaquetado

| Aspecto | Detalle |
|---------|---------|
| **Por qué** | Fija dependencias y entorno para que cualquier evaluador obtenga el mismo resultado. |
| **Qué se hace aquí** | `Dockerfile` en `servicio_estado_clinico/`: Python 3.12-slim, Flask, copia de código y plantillas. |
| **Herramientas viables** | Docker, `requirements.txt` con versiones fijadas. |
| **Artefacto** | Imagen `estado-clinico-demo`. |
| **Criterio de éxito** | `docker build` y `docker run` exitosos en Windows/Linux. |

### Etapa 7 — Despliegue

| Aspecto | Detalle |
|---------|---------|
| **Por qué** | Expone la lógica al usuario final (médico/evaluador) de forma accesible. |
| **Qué se hace aquí** | Contenedor en puerto 5000; Flask en `0.0.0.0`; rutas `GET /` (formulario) y `POST /predecir` (JSON). |
| **Herramientas viables** | Docker Desktop local; VM compartida; (evolución) cloud run / Kubernetes. |
| **Artefacto** | Servicio HTTP accesible en `http://localhost:5000/predecir`. |
| **Criterio de éxito** | Respuesta JSON correcta con ≥3 campos; acceso desde otro PC en la misma LAN. |

### Etapa 8 — Monitoreo y retrabajo

| Aspecto | Detalle |
|---------|---------|
| **Por qué** | Detecta degradación, deriva de datos y necesidad de recalibrar reglas o reentrenar. |
| **Qué se hace aquí** | Registro de peticiones, errores 4xx/5xx, latencia y distribución de clases predichas. |
| **Herramientas viables** | Logs de Flask; Prometheus/Grafana (evolución). |
| **Artefacto** | Dashboard o informe periódico de operación. |
| **Criterio de éxito** | Alertas si la tasa de AGUDA cae fuera del rango histórico (~1–3 %) o suben errores de validación. |

---

## 2. Enfermedades huérfanas y casos especiales

En este proyecto el término se aborda en **dos sentidos complementarios**, ambos habituales en MLOps aplicado a salud.

### 2.1 Clases minoritarias (desbalance de datos)

`ENFERMEDAD AGUDA` representa solo **~1,9 %** del dataset. En ML esto se conoce como **clase minoritaria** y, en contextos clínicos amplios, se relaciona con patologías poco frecuentes en la muestra de entrenamiento.

**Política del pipeline:**

1. **Prioridad de reglas en inferencia:** la lógica evalúa AGUDA antes que LEVE, evitando que casos de crisis queden absorbidos por la clase mayoritaria.
2. **Partición estratificada:** en entrenamiento ML futuro, train/val/test mantienen proporción de AGUDA en cada split.
3. **Métricas por clase:** no basta accuracy global; se exige **recall y F1 de AGUDA** como criterio de promoción.
4. **Técnicas de balanceo (evolución):** pesos de clase, SMOTE controlado o umbrales de decisión ajustados.
5. **Monitoreo:** alerta si la frecuencia de predicciones AGUDA en producción se desvía del rango histórico.

### 2.2 Enfermedades raras no representadas en los datos

El dataset cubre variables cardiovasculares genéricas; **no incluye diagnósticos de enfermedades huérfanas** (p. ej. patologías ultra-raras con pocos casos mundiales).

**Política del pipeline:**

1. **Alcance explícito:** el sistema clasifica en **cuatro estados agregados**, no diagnostica enfermedades raras por nombre.
2. **Respuesta conservadora:** perfiles atípicos o con datos insuficientes pueden clasificarse como `ENFERMEDAD LEVE` o, en evolución del API, devolver un flag `requiere_revision_humana: true`.
3. **Derivación humana:** cualquier resultado es orientativo; decisiones clínicas reales requieren criterio médico.
4. **Gobernanza de datos nuevos:** registros de patologías no vistas se archivan para análisis offline, no se usan automáticamente en producción sin revisión.

### 2.3 Tabla de decisión resumida

| Situación | Acción del pipeline |
|-----------|---------------------|
| Clase AGUDA con pocos ejemplos en train | Estratificación + métricas por clase + posible oversampling |
| Patología rara no presente en CSV | No inferir; disclaimer + revisión humana |
| Entrada con <3 campos | HTTP 400; no predecir |
| Valores fuera de rango físico | Rechazar en validación de datos (etapa 3) |

---

## 3. Entrenamiento y calibración del modelo

### 3.1 Nivel actual — Función simulada (entrega Unidad 1/3)

La consigna académica **no exige entrenar un modelo ML**. En su lugar:

1. `scripts/ajustar_cuatro_categorias.py` aplica reglas deterministas al CSV procesado y genera `categoria_clinica`.
2. `modelo_simulado.py` replica esas reglas para inferencia en tiempo real vía API.

**Argumento:** este baseline es **interpretable, auditable y reproducible**. Un evaluador puede leer las reglas y entender cada predicción sin caja negra.

**Reglas (prioridad descendente):**

1. **AGUDA:** sistólica ≥180, diastólica ≥110, o (sistólica ≥160 y glucosa ≥3).
2. **CRÓNICA:** `presencia_enfermedad == 1` (si no fue AGUDA).
3. **NO ENFERMO:** PA controlada, colesterol/glucosa ≤2, no fumador.
4. **LEVE:** resto de casos.

### 3.2 Nivel evolutivo — Modelo supervisado (pipeline ejecutable)

Si el proyecto evoluciona a ML clásico, el pipeline propone:

| Paso | Acción |
|------|--------|
| 1 | Features: presión sistólica/diastólica, colesterol, glucosa, fumador, presencia_enfermedad |
| 2 | Target: `categoria_clinica` |
| 3 | Partición: 70 % train / 15 % val / 15 % test, estratificada |
| 4 | Algoritmo baseline: regresión logística multinomial o Random Forest |
| 5 | Métricas: accuracy, F1 macro, recall por clase (especialmente AGUDA) |
| 6 | Registro: MLflow o `models/v1/` con hash del dataset |
| 7 | Promoción: solo si supera al baseline de reglas en validación |
| 8 | Fallback: reglas activas si confianza del modelo < umbral |

**Triggers de reentrenamiento:**

- Acumulación de N registros nuevos (p. ej. 5 000).
- Caída de F1 macro por debajo del umbral acordado.
- Calendario periódico (trimestral) con aprobación manual antes de sustituir la imagen Docker.

---

## (A) Diseño

### Objetivo del diseño

Entregar una solución **reproducible**: datos estructurados → lógica de predicción acotada → servicio HTTP → contenedor Docker que cualquier evaluador puede construir y ejecutar.

### Restricciones

| Restricción | Justificación |
|-------------|---------------|
| Alcance académico | No es producto clínico certificado |
| Recursos limitados | Un contenedor en máquina local o VM |
| Datos de ejemplo | Calidad y representatividad no garantizadas |
| Tiempo de curso | Sin orquestación compleja (K8s, feature store empresarial) |

### Limitaciones y mitigación

| Limitación | Mitigación |
|------------|------------|
| Reglas no sustituyen criterio médico | Disclaimer en UI y documentación |
| Sesgo poblacional del CSV | Documentar origen; no extrapolar a otras poblaciones |
| Cuatro categorías simplificadas | Revisión humana para casos límite |
| Sin alta disponibilidad | Aceptable en demo; evolución a réplicas en cloud |

### Tipo de datos

| Columna (processed) | Tipo | Uso en API |
|---------------------|------|------------|
| presion_arterial_sistolica | numérico | presion_sistolica |
| presion_arterial_diastolica | numérico | presion_diastolica |
| nivel_colesterol | entero 1–3 | nivel_colesterol |
| nivel_glucosa | entero 1–3 | nivel_glucosa |
| presencia_enfermedad | 0/1 | presencia_enfermedad |
| fumador | booleano | fumador |
| categoria_clinica | etiqueta | solo entrenamiento/evaluación |

---

## (B) Desarrollo

### Tipo de modelo

| Enfoque | Ventaja | Estado en proyecto |
|---------|---------|-------------------|
| Reglas deterministas | Interpretable, sin GPU, cumple consigna | **Implementado** |
| ML supervisado | Generaliza patrones complejos | Propuesto como evolución |

### Validación y pruebas

1. **Unitarias:** casos límite en umbrales PA (179 vs 180), combinaciones glucosa+colesterol.
2. **Contrato API:** JSON válido/inválido, códigos HTTP 200/400, campos obligatorios.
3. **Integración:** formulario web → `/predecir` → respuesta JSON.
4. **Docker:** build + run + POST desde localhost y desde otro PC en LAN.
5. **Futuro ML:** matriz de confusión en test; comparación con baseline de reglas.

---

## (C) Despliegue, monitoreo y datos futuros

### Despliegue

```bash
cd servicio_estado_clinico
docker build -t estado-clinico-demo .
docker run --rm -p 5000:5000 estado-clinico-demo
```

Acceso: `http://localhost:5000/` y `POST http://localhost:5000/predecir`.

### Monitoreo recomendado

- Logs de peticiones y errores.
- Latencia p95 del endpoint.
- Distribución de clases predichas vs histórico.
- Tasa de errores 4xx (validación de entrada).

### Nuevos datos

Sí pueden aparecer nuevos registros, cambios de definición de variables o poblaciones distintas. El pipeline debe:

1. Ingerir y versionar el nuevo lote.
2. Re-ejecutar validación de calidad.
3. Recalibrar reglas o reentrenar modelo.
4. Evaluar en hold-out antes de promover a producción.
5. Reconstruir imagen Docker y desplegar con rollback planificado.

---

## Viabilidad de ejecución

La propuesta es **viable y lista para ejecutarse** en el alcance del curso:

- Datos y scripts ya existen en el repositorio.
- El servicio Flask/Docker está implementado y probado.
- Las etapas de ML avanzado (entrenamiento supervisado, MLflow, monitoreo avanzado) están **documentadas como evolución**, no bloquean la entrega actual.
- Cada etapa tiene artefacto, herramienta y criterio de éxito definidos.

---

*Documento académico — no constituye asesoría clínica.*
