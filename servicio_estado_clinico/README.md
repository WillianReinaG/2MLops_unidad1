# Servicio de estado clínico simulado

Proyecto unidad uno MLOps

## Qué hace

- Expone un servicio **Flask** en el puerto **5000**.
- La ruta **`POST /predecir`** recibe JSON y devuelve una etiqueta entre:
  - `NO ENFERMO`
  - `ENFERMEDAD LEVE`
  - `ENFERMEDAD AGUDA`
  - `ENFERMEDAD CRÓNICA`
- La página es un formulario mínimo que llama a `/predecir`.

La “predicción” es una **función determinista** definida en `modelo_simulado.py`.

### Campos JSON admitidos

`presion_sistolica`, `presion_diastolica`, `nivel_colesterol`, `nivel_glucosa`, `presencia_enfermedad`, `fumador`.

**Obligatorios:** `presion_sistolica` y `presion_diastolica`.  
**Regla de negocio:** deben enviarse **al menos tres valores** contando solo campos permitidos con valor informado (las dos presiones cuentan; falta al menos un campo más).

## Ejecución local (sin Docker)

Desde esta carpeta (`servicio_estado_clinico`):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abrir el navegador en `http://127.0.0.1:5000/`.

### Ejemplo con curl

```bash
curl -s -X POST http://127.0.0.1:5000/predecir ^
  -H "Content-Type: application/json" ^
  -d "{\"presion_sistolica\": 118, \"presion_diastolica\": 76, \"nivel_colesterol\": 1, \"nivel_glucosa\": 1, \"presencia_enfermedad\": 0, \"fumador\": false}"
```

En PowerShell puede ser más cómodo usar `Invoke-RestMethod`:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/predecir -Method POST -ContentType "application/json" -Body '{"presion_sistolica":118,"presion_diastolica":76,"nivel_colesterol":1,"nivel_glucosa":1,"presencia_enfermedad":0,"fumador":false}'
```

## Docker

### Construir la imagen

```bash
docker build -t estado-clinico-demo .
```

### Ejecutar el contenedor

```bash
docker run --rm -p 5000:5000 estado-clinico-demo
```

Servicio disponible en `http://localhost:5000/predecir` (POST) y `http://localhost:5000/` (formulario).

## Propuesta breve de pipeline MLOps (ilustrativa)

1. **Datos:** ingesta y versionado de tablas o archivos (por ejemplo carpeta `data/` con trazabilidad).
2. **Calidad:** validación de esquema y rangos antes de servir o entrenar.
3. **Modelado:** en este trabajo la lógica es una función fija; en un proyecto real habría entrenamiento y registro de artefactos.
4. **Empaquetado:** imagen Docker con dependencias fijadas (`requirements.txt`).
5. **Despliegue:** contenedor en máquina local, nube o orquestador según el curso.

---

Trabajo académico; los umbrales no están validados clínicamente.
