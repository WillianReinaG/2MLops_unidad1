"""
Genera diagramas y PDF de la propuesta MLOps v2.0 (Unidad 3 — reestructuración E2E).
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
DIAG_E2E = BASE / "diagrama_pipeline_e2e.png"
DIAG_DEPLOY = BASE / "diagrama_despliegue_hibrido.png"
DIAG_CICD = BASE / "diagrama_cicd_mlops.png"
DIAG_DATOS = BASE / "diagrama_datos_ml.png"
DIAG_LEGACY = BASE / "diagrama_pipeline_mlops.png"
PDF_OUT = BASE / "Pipeline_MLOps_Propuesta_Completa.pdf"


def _caja(ax, x, y, w, h, texto, color="#e8eef5", fs=7.5):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        linewidth=1.0, edgecolor="#2c3e50", facecolor=color,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center",
            fontsize=fs, weight="bold", color="#1a1a1a")


def _flecha(ax, x1, y1, x2, y2):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=10,
        linewidth=1.0, color="#34495e",
    )
    ax.add_patch(arr)


def dibujar_pipeline_e2e() -> Path:
    fig, ax = plt.subplots(figsize=(14, 5.5), dpi=150)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.text(7, 5.2, "Pipeline MLOps E2E — 12 etapas", ha="center", fontsize=13, weight="bold")

    etapas = [
        (0.1, "0\nEncuadre", "#e8daef"),
        (1.2, "1\nIngesta\nDVC", "#d4e6f1"),
        (2.3, "2\nCatálogo", "#d4e6f1"),
        (3.4, "3\nCalidad\nGX", "#d4e6f1"),
        (4.5, "4\nFeatures\nFeast", "#d4e6f1"),
        (5.6, "5\nTrain\nLGBM", "#fdebd0"),
        (6.7, "6\nEval\nSHAP", "#fdebd0"),
        (7.8, "7\nRegistry\nMLflow", "#fdebd0"),
        (8.9, "8\nPackage\nDocker", "#d5f5e3"),
        (10.0, "9\nLocal", "#d5f5e3"),
        (11.1, "10\nCloud", "#d5f5e3"),
        (12.2, "11\nMonitor", "#fadbd8"),
        (13.1, "12\nRetrain", "#fadbd8"),
    ]
    w = 0.95
    h = 0.75
    y = 3.5
    for x, txt, col in etapas:
        _caja(ax, x, y, w, h, txt, col, fs=6.5)

    for i in range(len(etapas) - 1):
        x1 = etapas[i][0] + w
        x2 = etapas[i + 1][0]
        _flecha(ax, x1, y + h / 2, x2, y + h / 2)

    _caja(ax, 5.5, 1.8, 3.0, 0.7, "Ciclo cerrado: Monitor → Retrain → Ingesta", "#fadbd8", fs=7)
    _flecha(ax, 13.5, 3.5, 7.0, 2.5)
    _flecha(ax, 7.0, 1.8, 1.5, 3.5)

    ley = [
        mpatches.Patch(color="#e8daef", label="Gobernanza"),
        mpatches.Patch(color="#d4e6f1", label="Datos"),
        mpatches.Patch(color="#fdebd0", label="ML"),
        mpatches.Patch(color="#d5f5e3", label="Deploy"),
        mpatches.Patch(color="#fadbd8", label="Ops"),
    ]
    ax.legend(handles=ley, loc="lower left", fontsize=6, ncol=5)
    fig.tight_layout()
    fig.savefig(DIAG_E2E, bbox_inches="tight", facecolor="white")
    fig.savefig(DIAG_LEGACY, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return DIAG_E2E


def dibujar_despliegue_hibrido() -> Path:
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.text(5, 5.6, "Despliegue híbrido — mismo API POST /predecir", ha="center", fontsize=12, weight="bold")

    _caja(ax, 4.0, 4.6, 2.0, 0.8, "Médico\n(formulario / API)", "#eaeded")

    _caja(ax, 0.5, 2.5, 2.2, 1.0, "Docker Compose\nlocalhost:5000\n(perfil local)", "#d5f5e3")
    _caja(ax, 7.3, 2.5, 2.2, 1.0, "Cloud Run /\nApp Runner\nHTTPS + API key", "#d5f5e3")

    _caja(ax, 0.8, 0.8, 1.8, 0.9, "Imagen GHCR\n+ modelo MLflow", "#fdebd0")
    _caja(ax, 7.6, 0.8, 1.8, 0.9, "Misma imagen\nProduction", "#fdebd0")

    _flecha(ax, 4.5, 4.6, 1.6, 3.5)
    _flecha(ax, 5.5, 4.6, 8.4, 3.5)
    _flecha(ax, 1.7, 2.5, 1.7, 1.7)
    _flecha(ax, 8.3, 2.5, 8.3, 1.7)

    ax.text(5, 0.2, "CPU <100ms · modelo <10MB · sin GPU", ha="center", fontsize=8, style="italic")
    fig.tight_layout()
    fig.savefig(DIAG_DEPLOY, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return DIAG_DEPLOY


def dibujar_cicd() -> Path:
    fig, ax = plt.subplots(figsize=(11, 4.5), dpi=150)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    ax.text(5.5, 4.1, "CI/CD MLOps — GitHub Actions", ha="center", fontsize=12, weight="bold")

    jobs = [
        (0.2, "PR:\nlint + pytest"),
        (1.6, "DVC pull +\nGreat Expectations"),
        (3.0, "Train:\nOptuna + MLflow"),
        (4.4, "Eval +\nSHAP gate"),
        (5.8, "Build Docker\n→ GHCR"),
        (7.2, "Deploy\nstaging"),
        (8.6, "Smoke\ntest"),
        (10.0, "Promote\nProduction"),
    ]
    y = 2.0
    w = 1.2
    h = 0.9
    for x, txt in jobs:
        _caja(ax, x, y, w, h, txt, "#d4e6f1", fs=6.5)
    for i in range(len(jobs) - 1):
        _flecha(ax, jobs[i][0] + w, y + h / 2, jobs[i + 1][0], y + h / 2)

    _caja(ax, 3.5, 0.5, 4.0, 0.7, "Rollback: MLflow Registry → redeploy imagen anterior", "#fadbd8", fs=7)
    fig.tight_layout()
    fig.savefig(DIAG_CICD, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return DIAG_CICD


def dibujar_datos_ml() -> Path:
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.text(5, 4.6, "Flujo datos → ML → inferencia", ha="center", fontsize=12, weight="bold")

    nodos = [
        (0.3, 3.2, "raw CSV\ndata/raw", "#d4e6f1"),
        (2.0, 3.2, "DVC\nsnapshot", "#d4e6f1"),
        (3.7, 3.2, "processed\n4 categorías", "#d4e6f1"),
        (5.4, 3.2, "features\n.parquet", "#d4e6f1"),
        (7.1, 3.2, "LightGBM\n+ Pipeline", "#fdebd0"),
        (8.6, 3.2, "MLflow\nRegistry", "#fdebd0"),
    ]
    w, h = 1.4, 0.85
    for x, y, t, c in nodos:
        _caja(ax, x, y, w, h, t, c, fs=7)
    for i in range(len(nodos) - 1):
        _flecha(ax, nodos[i][0] + w, nodos[i][1] + h / 2, nodos[i + 1][0], nodos[i + 1][1] + h / 2)

    _caja(ax, 1.5, 1.2, 2.5, 0.8, "Inferencia local\nDocker Compose", "#d5f5e3", fs=7)
    _caja(ax, 5.5, 1.2, 2.5, 0.8, "Inferencia cloud\nCloud Run", "#d5f5e3", fs=7)
    _flecha(ax, 9.0, 3.2, 2.75, 2.0)
    _flecha(ax, 9.0, 3.2, 6.75, 2.0)

    _caja(ax, 3.5, 0.2, 3.0, 0.6, "MVP baseline: reglas modelo_simulado.py", "#e8daef", fs=7)
    fig.tight_layout()
    fig.savefig(DIAG_DATOS, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return DIAG_DATOS


def _p(text, style):
    return Paragraph(text, style)


def construir_pdf() -> Path:
    styles = getSampleStyleSheet()
    normal = ParagraphStyle("j", parent=styles["BodyText"], fontSize=9, leading=12.5,
                            alignment=TA_JUSTIFY, spaceAfter=5)
    titulo = ParagraphStyle("t", parent=styles["Title"], fontSize=14, alignment=TA_CENTER, spaceAfter=10)
    sub = ParagraphStyle("s", parent=styles["Heading2"], fontSize=10.5, spaceBefore=6, spaceAfter=5)
    h3 = ParagraphStyle("h3", parent=styles["Heading3"], fontSize=9.5, spaceBefore=4, spaceAfter=3)

    doc = SimpleDocTemplate(str(PDF_OUT), pagesize=A4,
                            rightMargin=1.7 * cm, leftMargin=1.7 * cm,
                            topMargin=1.7 * cm, bottomMargin=1.7 * cm)
    story = []

    story.append(_p("Propuesta pipeline MLOps end-to-end v2.0", titulo))
    story.append(_p(
        "<b>Proyecto:</b> Estado clínico simulado (2MLops). "
        "<b>Producción objetivo:</b> LightGBM + MLflow. "
        "<b>MVP implementado:</b> reglas en modelo_simulado.py. "
        "<b>Despliegue:</b> local (Docker Compose) y cloud (Cloud Run). "
        "Alcance académico; no uso clínico real.", normal))

    story.append(_p("<b>Resumen del problema</b>", sub))
    story.append(_p(
        "Un médico ingresa al menos tres signos (presión, colesterol, glucosa, etc.) y "
        "obtiene una de cuatro etiquetas. El pipeline MLOps garantiza datos versionados, "
        "entrenamiento trazable, empaquetado reproducible, inferencia local o remota, "
        "monitoreo y reentrenamiento continuo.", normal))

    story.append(_p("<b>Registro de suposiciones (extracto)</b>", sub))
    for s in [
        "S1: CSV ~70k filas representa dominio académico.",
        "S3: Inferencia CPU &lt;100 ms; modelo &lt;10 MB.",
        "S6: Clase AGUDA ~1,9 % — requiere estratificación y recall como gate.",
        "S8: Médico usa Docker local o HTTPS cloud con API key.",
    ]:
        story.append(_p(f"• {s}", normal))

    story.append(_p("<b>Diagrama 1 — Pipeline 12 etapas</b>", sub))
    story.append(Image(str(DIAG_E2E), width=17 * cm, height=6.5 * cm))

    story.append(PageBreak())
    story.append(_p("<b>Diagrama 2 — Despliegue híbrido</b>", sub))
    story.append(Image(str(DIAG_DEPLOY), width=15 * cm, height=9 * cm))
    story.append(_p(
        "El médico puede ejecutar la solución en su PC (Docker Compose, localhost:5000) "
        "o consumir la misma API vía HTTPS en Cloud Run con API key. Misma imagen GHCR y "
        "mismo contrato JSON POST /predecir.", normal))

    story.append(_p("<b>Diagrama 3 — CI/CD</b>", sub))
    story.append(Image(str(DIAG_CICD), width=16 * cm, height=6.5 * cm))

    story.append(_p("<b>Diagrama 4 — Datos → ML → serve</b>", sub))
    story.append(Image(str(DIAG_DATOS), width=15 * cm, height=7.5 * cm))

    story.append(PageBreak())
    story.append(_p("<b>Etapas del pipeline (síntesis)</b>", sub))

    etapas_txt = [
        ("0 Encuadre", "Alcance, KPIs, disclaimer. Markdown + RACI."),
        ("1 Ingesta", "Git + DVC + MinIO/S3. Snapshot data@vN."),
        ("2 Catálogo", "Linaje DVC; OpenMetadata opcional."),
        ("3 Calidad", "Great Expectations; gate en CI."),
        ("4 Features", "pandas + sklearn Pipeline + Feast offline."),
        ("5 Entrenamiento", "LightGBM + Optuna + MLflow Tracking."),
        ("6 Evaluación", "SHAP + gate humano; beat baseline reglas."),
        ("7 Registry", "MLflow Staging → Production; rollback."),
        ("8 Empaquetado", "Docker multi-stage → GHCR."),
        ("9 Local", "Docker Compose perfil local; sin GPU."),
        ("10 Cloud", "Cloud Run / App Runner; TLS + API key."),
        ("11 Monitoreo", "Prometheus, Grafana, Evidently drift."),
        ("12 Retrain", "GitHub Actions / Prefect; triggers drift/F1/cron."),
    ]
    for tit, txt in etapas_txt:
        story.append(_p(f"<b>{tit}.</b> {txt}", normal))

    story.append(_p("<b>Enfermedades huérfanas y desbalance</b>", sub))
    story.append(_p(
        "AGUDA es ~1,9 % del dataset: estratificación, class_weight en LightGBM, "
        "recall AGUDA como criterio de promoción, monitoreo de frecuencia en producción. "
        "Patologías raras no presentes en CSV: no se diagnostican por nombre; flag "
        "requiere_revision_humana propuesto; datos nuevos en cuarentena.", normal))

    story.append(_p("<b>Baseline vs producción</b>", sub))
    story.append(_p(
        "MVP (implementado): reglas deterministas + Flask + Docker. "
        "Producción (objetivo): LightGBM registrado en MLflow. Promoción solo si "
        "F1 macro y recall AGUDA superan baseline en mismo test split.", normal))

    story.append(PageBreak())
    story.append(_p("<b>Plan de puesta en marcha (equipo ML)</b>", sub))
    story.append(_p(
        "Fase 0 (1 sem): baseline operativo — hecho. Fase 1 (1–2 sem): DVC + GX + catálogo. "
        "Fase 2 (2 sem): LightGBM en MLflow + SHAP. Fase 3 (1 sem): GHCR + local + Cloud Run. "
        "Fase 4 (1 sem): Grafana + Evidently + workflow retrain. Total ~6–7 semanas, 2–3 personas.", normal))

    story.append(_p("<b>Viabilidad</b>", sub))
    story.append(_p(
        "Stack open source y free tiers. Datos y MVP ya en repo. Cada etapa tiene "
        "suposiciones, tecnologías justificadas, criterios de aceptación y relación con "
        "código actual. Ver CHANGELOG.md para cambios vs Semana 1.", normal))

    story.append(Spacer(1, 0.3 * cm))
    story.append(_p("<i>Documento académico v2.0 — no constituye asesoría clínica.</i>", styles["Italic"]))

    doc.build(story)
    return PDF_OUT


def main() -> None:
    dibujar_pipeline_e2e()
    dibujar_despliegue_hibrido()
    dibujar_cicd()
    dibujar_datos_ml()
    construir_pdf()
    print(f"Diagramas: {DIAG_E2E}, {DIAG_DEPLOY}, {DIAG_CICD}, {DIAG_DATOS}")
    print(f"Legacy alias: {DIAG_LEGACY}")
    print(f"PDF: {PDF_OUT}")


if __name__ == "__main__":
    main()
