"""
Genera diagrama y PDF de la propuesta MLOps (Unidad 3).
Requisitos: pip install matplotlib reportlab
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer

BASE = Path(__file__).resolve().parent
DIAGRAMA = BASE / "diagrama_pipeline_mlops.png"
PDF_OUT = BASE / "Pipeline_MLOps_Propuesta_Completa.pdf"


def dibujar_diagrama() -> Path:
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    def caja(x, y, w, h, texto, color="#e8eef5"):
        box = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.03,rounding_size=0.12",
            linewidth=1.2,
            edgecolor="#2c3e50",
            facecolor=color,
        )
        ax.add_patch(box)
        ax.text(
            x + w / 2,
            y + h / 2,
            texto,
            ha="center",
            va="center",
            fontsize=8,
            weight="bold",
            color="#1a1a1a",
        )

    def flecha(x1, y1, x2, y2, style="-|>"):
        arr = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle=style,
            mutation_scale=11,
            linewidth=1.1,
            color="#34495e",
        )
        ax.add_patch(arr)

    ax.text(
        6,
        6.55,
        "Pipeline MLOps — Estado clínico simulado",
        ha="center",
        fontsize=14,
        weight="bold",
    )
    ax.text(
        6,
        6.2,
        "Flujo principal (arriba) · Despliegue (centro) · Retroalimentación (abajo)",
        ha="center",
        fontsize=8,
        style="italic",
        color="#555",
    )

    caja(0.2, 4.6, 1.3, 0.85, "1. Datos\nbrutos", "#d4e6f1")
    caja(1.7, 4.6, 1.4, 0.85, "2. Ingesta y\nversionado", "#d4e6f1")
    caja(3.3, 4.6, 1.4, 0.85, "3. Calidad y\nvalidación", "#d4e6f1")
    caja(4.9, 4.6, 1.4, 0.85, "4. Preparación\n(4 categorías)", "#d4e6f1")
    caja(6.5, 4.6, 1.5, 0.85, "5. Calibración /\nentrenamiento", "#fdebd0")
    caja(8.2, 4.6, 1.3, 0.85, "6. Empaquetado\n(Docker)", "#fdebd0")
    caja(9.7, 4.6, 1.1, 0.85, "7. Registro\nartefacto", "#fdebd0")

    for x1, x2 in [(1.5, 1.7), (3.1, 3.3), (4.7, 4.9), (6.3, 6.5), (8.0, 8.2), (9.5, 9.7)]:
        flecha(x1, 5.02, x2, 5.02)

    caja(3.5, 2.85, 2.0, 0.9, "Despliegue\nFlask + Docker\n/predecir", "#d5f5e3")
    caja(5.8, 2.85, 1.8, 0.9, "Usuarios\n(médico / demo)", "#eaeded")
    caja(7.9, 2.85, 2.0, 0.9, "Casos huérfanos\n/ baja confianza\n→ revisión humana", "#f5eef8")

    flecha(10.25, 4.6, 6.5, 3.75)
    flecha(5.5, 2.85, 5.8, 2.85)
    flecha(7.6, 3.3, 7.9, 3.3)

    caja(0.5, 0.9, 2.2, 0.95, "8a. Monitoreo\nlatencia, errores,\ndistribución clases", "#fadbd8")
    caja(3.0, 0.9, 2.2, 0.95, "8b. Retraining /\nrecalibración reglas", "#fadbd8")
    caja(5.5, 0.9, 2.2, 0.95, "8c. Nuevos datos\ny gobernanza", "#fadbd8")
    caja(8.0, 0.9, 2.5, 0.95, "Ciclo cerrado\n→ etapas 1–5", "#fadbd8")

    flecha(4.5, 2.85, 1.6, 1.85)
    flecha(2.7, 0.9, 2.7, 0.9)
    flecha(5.2, 1.375, 5.5, 1.375)
    flecha(7.7, 1.375, 8.0, 1.375)
    flecha(9.25, 1.85, 7.0, 4.6, style="-|>")

    ley = [
        mpatches.Patch(color="#d4e6f1", label="Datos"),
        mpatches.Patch(color="#fdebd0", label="Modelo / artefacto"),
        mpatches.Patch(color="#d5f5e3", label="Despliegue"),
        mpatches.Patch(color="#f5eef8", label="Casos especiales"),
        mpatches.Patch(color="#fadbd8", label="Operación y mejora"),
    ]
    ax.legend(handles=ley, loc="lower left", fontsize=7, frameon=True)

    fig.tight_layout()
    fig.savefig(DIAGRAMA, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return DIAGRAMA


def _p(text: str, style) -> Paragraph:
    return Paragraph(text, style)


def construir_pdf() -> Path:
    styles = getSampleStyleSheet()
    normal = ParagraphStyle(
        "justificado",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
    titulo = ParagraphStyle(
        "titulo",
        parent=styles["Title"],
        fontSize=15,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    subtitulo = ParagraphStyle(
        "sub",
        parent=styles["Heading2"],
        fontSize=11,
        spaceBefore=8,
        spaceAfter=6,
    )
    h3 = ParagraphStyle(
        "h3",
        parent=styles["Heading3"],
        fontSize=10,
        spaceBefore=6,
        spaceAfter=4,
    )

    doc = SimpleDocTemplate(
        str(PDF_OUT),
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
    )
    story: list = []

    story.append(_p("Propuesta de pipeline MLOps", titulo))
    story.append(
        _p(
            "<b>Proyecto:</b> Estado clínico simulado (2MLops, Unidad 3). "
            "<b>Alcance académico:</b> no sustituye criterio médico. "
            "Este documento describe el problema, la solución propuesta y "
            "cada etapa del pipeline con argumentos de diseño y viabilidad.",
            normal,
        )
    )

    story.append(_p("<b>0. Problema y propuesta</b>", subtitulo))
    story.append(
        _p(
            "<b>Problema.</b> Un médico necesita una clasificación orientativa del "
            "estado de un paciente a partir de signos medibles (presión arterial, "
            "colesterol, glucosa, hábitos). El reto MLOps es entregar esa lógica de "
            "forma reproducible, versionada y desplegable.",
            normal,
        )
    )
    story.append(
        _p(
            "<b>Usuario y salida.</b> El médico ingresa al menos tres valores vía "
            "formulario o API. El sistema devuelve una de cuatro etiquetas: "
            "<i>NO ENFERMO</i>, <i>ENFERMEDAD LEVE</i>, <i>ENFERMEDAD AGUDA</i> o "
            "<i>ENFERMEDAD CRÓNICA</i>.",
            normal,
        )
    )
    story.append(
        _p(
            "<b>Propuesta.</b> Pipeline de extremo a extremo: datos en <i>data/</i>, "
            "etiquetado con <i>scripts/ajustar_cuatro_categorias.py</i>, lógica en "
            "<i>modelo_simulado.py</i>, servicio Flask (<i>POST /predecir</i>) e "
            "imagen Docker. Incluye camino de evolución hacia ML supervisado, "
            "monitoreo y retrabajo con datos nuevos.",
            normal,
        )
    )
    story.append(
        _p(
            "<b>Argumento MLOps.</b> Sin pipeline, las reglas quedan aisladas en "
            "código sin trazabilidad. Con pipeline, cada versión del servicio se "
            "vincula a una versión de datos, pasa validaciones explícitas y se "
            "despliega en un entorno reproducible (Docker), con plan ante datos "
            "nuevos y degradación de rendimiento.",
            normal,
        )
    )

    story.append(_p("<b>Diagrama general</b>", subtitulo))
    story.append(Image(str(DIAGRAMA), width=16.5 * cm, height=9 * cm))

    story.append(PageBreak())
    story.append(_p("<b>1. Etapas del pipeline (argumento por etapa)</b>", subtitulo))

    etapas = [
        (
            "Etapa 1 — Datos brutos",
            "Almacena CSV sin transformar (<i>data/raw/enfermedades_cardiacas.csv</i>, "
            "~70 000 filas). <b>Por qué:</b> base auditable. <b>Artefacto:</b> dataset "
            "crudo. <b>Herramientas:</b> Git, DVC. <b>Éxito:</b> checksum y licencia "
            "documentados.",
        ),
        (
            "Etapa 2 — Ingesta y versionado",
            "Copia controlada hacia <i>data/processed/</i>. <b>Por qué:</b> saber qué "
            "datos produjeron cada versión del servicio. <b>Artefacto:</b> "
            "<i>enfermedades_cardiacas_limpio.csv</i>.",
        ),
        (
            "Etapa 3 — Calidad y validación",
            "Comprueba tipos, rangos (presión 50–250, colesterol/glucosa 1–3), nulos. "
            "<b>Por qué:</b> evita errores en inferencia. <b>Herramientas:</b> pandas; "
            "Great Expectations en evolución.",
        ),
        (
            "Etapa 4 — Preparación",
            "Genera <i>categoria_clinica</i> con reglas docentes. Distribución: LEVE "
            "49,9 %, CRÓNICA 30,2 %, NO ENFERMO 18,1 %, AGUDA 1,9 %. "
            "<b>Artefacto:</b> <i>enfermedades_cardiacas_4categorias.csv</i>.",
        ),
        (
            "Etapa 5 — Calibración / entrenamiento",
            "<b>Actual:</b> función determinista en <i>modelo_simulado.py</i>, "
            "alineada al script de etiquetado (baseline interpretable). "
            "<b>Evolución:</b> regresión logística o Random Forest; registro en "
            "MLflow. Promoción solo si supera reglas en validación.",
        ),
        (
            "Etapa 6 — Empaquetado",
            "Dockerfile fija Python 3.12 y Flask. <b>Por qué:</b> mismo resultado en "
            "cualquier PC del evaluador. <b>Artefacto:</b> imagen "
            "<i>estado-clinico-demo</i>.",
        ),
        (
            "Etapa 7 — Despliegue",
            "Contenedor en puerto 5000; <i>GET /</i> (formulario) y "
            "<i>POST /predecir</i>. Probado en localhost y desde otro PC en LAN.",
        ),
        (
            "Etapa 8 — Monitoreo y retrabajo",
            "Logs, latencia, distribución de clases predichas, alertas si AGUDA "
            "cae fuera del rango histórico. Triggers de recalibración: volumen de "
            "datos nuevos, caída de métricas o calendario.",
        ),
    ]
    for tit, cuerpo in etapas:
        story.append(_p(f"<b>{tit}</b>", h3))
        story.append(_p(cuerpo, normal))

    story.append(PageBreak())
    story.append(_p("<b>2. Enfermedades huérfanas y casos especiales</b>", subtitulo))
    story.append(
        _p(
            "<b>2.1 Clases minoritarias (desbalance).</b> "
            "<i>ENFERMEDAD AGUDA</i> es solo ~1,9 % del dataset. Política: (1) reglas "
            "evalúan AGUDA antes que LEVE; (2) partición estratificada en train/val/test; "
            "(3) métricas por clase (recall/F1 de AGUDA); (4) pesos de clase u oversampling "
            "en evolución ML; (5) monitoreo de frecuencia de AGUDA en producción.",
            normal,
        )
    )
    story.append(
        _p(
            "<b>2.2 Patologías raras no representadas.</b> El CSV no cubre enfermedades "
            "huérfanas por nombre. El sistema clasifica en cuatro estados agregados, no "
            "diagnostica patologías ultra-raras. Perfiles atípicos: respuesta conservadora "
            "(LEVE) o flag de revisión humana en evolución del API. Toda decisión clínica "
            "real requiere criterio médico.",
            normal,
        )
    )
    story.append(
        _p(
            "<b>2.3 Entrada insuficiente.</b> Menos de tres campos válidos → HTTP 400; "
            "no se emite predicción. Valores fuera de rango físico → rechazo en etapa 3.",
            normal,
        )
    )

    story.append(_p("<b>3. Entrenamiento y calibración</b>", subtitulo))
    story.append(
        _p(
            "<b>Nivel actual (consigna académica).</b> No hay ML entrenado. "
            "<i>ajustar_cuatro_categorias.py</i> calibra reglas sobre el CSV; "
            "<i>modelo_simulado.py</i> las aplica en inferencia. Ventaja: interpretable "
            "y auditable.",
            normal,
        )
    )
    story.append(
        _p(
            "<b>Reglas (prioridad):</b> (1) AGUDA: sistólica ≥180, diastólica ≥110, "
            "o sistólica ≥160 con glucosa ≥3; (2) CRÓNICA: presencia_enfermedad=1; "
            "(3) NO ENFERMO: PA controlada, lípidos/glucosa ≤2, no fumador; "
            "(4) LEVE: resto.",
            normal,
        )
    )
    story.append(
        _p(
            "<b>Evolución ML.</b> Features tabulares → target categoria_clinica → "
            "split 70/15/15 estratificado → baseline logístico/Random Forest → "
            "métricas F1 macro y por clase → registro versionado → promoción con "
            "aprobación manual → fallback a reglas si confianza baja.",
            normal,
        )
    )

    story.append(_p("<b>(A) Diseño</b>", subtitulo))
    story.append(
        _p(
            "<b>Restricciones:</b> alcance académico, un contenedor, datos de ejemplo, "
            "sin orquestador complejo. <b>Limitaciones:</b> no uso clínico real, sesgo "
            "poblacional, cuatro categorías simplificadas — mitigadas con disclaimer, "
            "revisión humana y plan de reentrenamiento. <b>Datos:</b> CSV tabular con "
            "presión, colesterol, glucosa, fumador, presencia_enfermedad y etiqueta "
            "derivada.",
            normal,
        )
    )

    story.append(_p("<b>(B) Desarrollo</b>", subtitulo))
    story.append(
        _p(
            "<b>Modelo:</b> reglas deterministas (implementado); ML supervisado "
            "(evolución). <b>Pruebas:</b> unitarias en umbrales; contrato API JSON/HTTP; "
            "formulario web; build Docker; acceso LAN; futura matriz de confusión en test.",
            normal,
        )
    )

    story.append(_p("<b>(C) Despliegue, monitoreo y datos futuros</b>", subtitulo))
    story.append(
        _p(
            "<b>Despliegue:</b> <i>docker build -t estado-clinico-demo .</i> y "
            "<i>docker run -p 5000:5000</i>. <b>Monitoreo:</b> logs, latencia, errores "
            "4xx/5xx, distribución de predicciones. <b>Datos nuevos:</b> ingesta "
            "versionada → validación → recalibración o reentrenamiento → evaluación → "
            "nueva imagen Docker con rollback planificado.",
            normal,
        )
    )

    story.append(Spacer(1, 0.4 * cm))
    story.append(
        _p(
            "<b>Conclusión de viabilidad.</b> La propuesta es clara, las etapas son "
            "viables y están listas para ejecución en el alcance del curso: datos, "
            "scripts, servicio y Docker ya implementados; evolución ML documentada "
            "sin bloquear la entrega actual.",
            normal,
        )
    )
    story.append(
        _p(
            "<i>Documento académico — no constituye asesoría clínica.</i>",
            styles["Italic"],
        )
    )

    doc.build(story)
    return PDF_OUT


def main() -> None:
    dibujar_diagrama()
    construir_pdf()
    print(f"Diagrama: {DIAGRAMA}")
    print(f"PDF: {PDF_OUT}")


if __name__ == "__main__":
    main()
