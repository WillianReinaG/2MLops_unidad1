"""
Genera diagramas y PDF de la propuesta MLOps v3.0 (Unidad 3 — nivel posgrado).
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
IMGS = BASE / "imgs"
IMGS.mkdir(exist_ok=True)
DIAG_HERO = IMGS / "ml-pipeline-estado-clinico.png"
DIAG_OPS = IMGS / "arquitectura-ops-capas.png"
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


def _region(ax, x, y, w, h, titulo, color="#f8f9fa"):
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.15",
        linewidth=1.5, edgecolor="#566573", facecolor=color, alpha=0.35,
    )
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h - 0.22, titulo, ha="center", fontsize=10, weight="bold", color="#1a5276")


def dibujar_pipeline_principal() -> Path:
    """Diagrama estilo mlops-sample: Offline Training | Predictions + Bonus."""
    fig, ax = plt.subplots(figsize=(13, 9), dpi=150)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.text(6.5, 8.65, "Pipeline MLOps — Estado clínico simulado v3.0", ha="center", fontsize=14, weight="bold")
    ax.text(
        6.5, 8.25,
        "Inspirado en estructura Offline Training | Predictions (referencia: avila196/mlops-sample)",
        ha="center", fontsize=7.5, style="italic", color="#555",
    )

    _caja(ax, 4.8, 7.35, 3.4, 0.65, "GitHub  +  GitHub Actions\n(CI/CD · versionado · tests)", "#d5dbdb", fs=8)
    _flecha(ax, 6.5, 7.35, 3.5, 6.55)
    _flecha(ax, 6.5, 7.35, 9.5, 6.55)

    _region(ax, 0.4, 2.8, 5.8, 3.6, "OFFLINE TRAINING", "#ebf5fb")
    offline = [
        (0.7, 5.5, "Data Input\nDVC · MinIO/S3 · Great Expectations", "#d4e6f1"),
        (0.7, 4.35, "Model Iterations\nFeast · sklearn · LightGBM · Optuna · MLflow", "#fdebd0"),
        (0.7, 3.2, "Model Selection & Evaluation\nF1 · recall AGUDA · SHAP · k-fold", "#fdebd0"),
        (0.7, 2.05, "¿Listo para producción?\nMLflow Registry · gate vs baseline reglas", "#e8daef"),
    ]
    for x, y, t, c in offline:
        _caja(ax, x, y, 5.2, 0.95, t, c, fs=7.5)
    for i in range(len(offline) - 1):
        _flecha(ax, 3.3, offline[i][1], 3.3, offline[i + 1][1] + 0.95)

    _region(ax, 6.8, 2.8, 5.8, 3.6, "PREDICTIONS (SERVING)", "#eafaf1")
    pred = [
        (7.1, 5.5, "Model Deployment\nDocker multi-stage · GHCR · serialización joblib", "#d5f5e3"),
        (7.1, 4.35, "Inferencia local\nDocker Compose · localhost:5000 · POST /predecir", "#d5f5e3"),
        (7.1, 3.2, "Inferencia cloud\nCloud Run · HTTPS · API key", "#d5f5e3"),
        (7.1, 2.05, "Médico\n≥3 valores · 4 estados clínicos simulados", "#eaeded"),
    ]
    for x, y, t, c in pred:
        _caja(ax, x, y, 5.2, 0.95, t, c, fs=7.5)
    for i in range(len(pred) - 1):
        _flecha(ax, 9.7, pred[i][1], 9.7, pred[i + 1][1] + 0.95)

    _flecha(ax, 5.9, 4.0, 7.1, 4.8)

    _region(ax, 0.4, 0.45, 12.2, 2.05, "BONUS — Operación continua", "#fdedec")
    _caja(ax, 0.7, 0.75, 3.6, 1.2, "Model Monitoring\nPrometheus · Grafana · Evidently drift", "#fadbd8", fs=7.5)
    _caja(ax, 4.6, 0.75, 3.6, 1.2, "Retraining\nGitHub Actions / Prefect · triggers F1/drift", "#fadbd8", fs=7.5)
    _caja(ax, 8.5, 0.75, 3.6, 1.2, "MVP implementado\nreglas modelo_simulado.py · Flask · Docker", "#e8daef", fs=7.5)
    _flecha(ax, 2.5, 2.8, 2.5, 1.95)
    _flecha(ax, 6.4, 1.35, 3.3, 2.05)
    _flecha(ax, 10.3, 1.95, 10.3, 2.8)

    fig.tight_layout()
    fig.savefig(DIAG_HERO, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return DIAG_HERO


def dibujar_ops_capas() -> Path:
    """Capas MLOps, DevOps, DevSecOps, AIOps, AgentOps."""
    fig, ax = plt.subplots(figsize=(11, 7), dpi=150)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.text(5.5, 6.65, "Arquitectura operativa — Ops stack", ha="center", fontsize=13, weight="bold")

    capas = [
        (0.5, 5.5, 10.0, 0.85, "AgentOps (horizonte)\nAgentes explicativos · guardrails · HITL — sin autonomía clínica", "#f5eef8"),
        (0.5, 4.45, 10.0, 0.85, "AIOps\nEvidently drift · alertas · runbooks GHA · rollback asistido", "#fadbd8"),
        (0.5, 3.4, 10.0, 0.85, "DevSecOps\nTrivy · SBOM · Secret Manager · TLS · logs sin PII", "#fdebd0"),
        (0.5, 2.35, 10.0, 0.85, "DevOps\nGitHub Actions · GHCR · Cloud Run · Docker Compose", "#d5f5e3"),
        (0.5, 1.3, 10.0, 0.85, "MLOps\nDVC · MLflow · LightGBM · SHAP · gates · Model Card", "#d4e6f1"),
    ]
    for x, y, w, h, t, c in capas:
        _caja(ax, x, y, w, h, t, c, fs=8)

    _caja(ax, 2.5, 0.25, 6.0, 0.75, "Servicio POST /predecir  ·  MVP reglas  ·  Prod LightGBM", "#eaeded", fs=8)
    for y in [1.3, 2.35, 3.4, 4.45, 5.5]:
        _flecha(ax, 5.5, y, 5.5, 1.0)

    fig.tight_layout()
    fig.savefig(DIAG_OPS, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return DIAG_OPS


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

    story.append(_p("Propuesta pipeline MLOps — v3.0 (nivel posgrado)", titulo))
    story.append(_p(
        "<b>Sistema sociotécnico</b> para clasificación clínica simulada en cuatro estados. "
        "Integra MLOps, DevOps, DevSecOps, AIOps y horizonte AgentOps. "
        "<b>MVP:</b> reglas + Flask + Docker. <b>Producción:</b> LightGBM + MLflow. "
        "<b>Despliegue:</b> edge local y cloud (Cloud Run).", normal))

    story.append(_p("<b>Diagrama 1 — Pipeline ML (Offline | Predictions)</b>", sub))
    story.append(Image(str(DIAG_HERO), width=16.5 * cm, height=11 * cm))

    story.append(_p("<b>Diagrama 2 — Ops stack</b>", sub))
    story.append(Image(str(DIAG_OPS), width=15 * cm, height=9.5 * cm))

    story.append(PageBreak())
    story.append(_p("<b>Madurez y gobernanza</b>", sub))
    story.append(_p(
        "Madurez objetivo Google MLOps L3–L4: CI/CD, deploy automatizado, monitoreo, retrain con gates. "
        "Gobernanza: Model Card, ADR-001/002/003, RACI, registro suposiciones S1–S10.", normal))

    story.append(_p("<b>SLI / SLO (producción académica)</b>", sub))
    for row in [
        "Disponibilidad API: 99,5% mensual.",
        "Latencia p95: &lt;100 ms edge; &lt;300 ms cloud.",
        "Errores 5xx: &lt;0,5%.",
        "Recall AGUDA offline: ≥ baseline reglas.",
    ]:
        story.append(_p(f"• {row}", normal))

    story.append(_p("<b>Offline Training (síntesis)</b>", sub))
    story.append(_p(
        "GitHub Actions → DVC/S3 → Great Expectations → Feast/sklearn → LightGBM/Optuna/MLflow → "
        "SHAP + gate humano → MLflow Registry. Promoción solo si supera baseline en F1 macro y recall AGUDA.", normal))

    story.append(_p("<b>Predictions (síntesis)</b>", sub))
    story.append(_p(
        "Docker/GHCR → inferencia edge (Compose) o cloud (Cloud Run, TLS, API key). "
        "Mismo contrato POST /predecir. Adaptación vs mlops-sample: inferencia unitaria, no batch Spark.", normal))

    story.append(PageBreak())
    story.append(_p("<b>Diagrama 3 — Despliegue híbrido</b>", sub))
    story.append(Image(str(DIAG_DEPLOY), width=15 * cm, height=9 * cm))

    story.append(_p("<b>Diagrama 4 — CI/CD DevOps</b>", sub))
    story.append(Image(str(DIAG_CICD), width=16 * cm, height=6.5 * cm))

    story.append(_p("<b>Diagrama 5 — Datos → ML → serve</b>", sub))
    story.append(Image(str(DIAG_DATOS), width=15 * cm, height=7.5 * cm))

    story.append(PageBreak())
    story.append(_p("<b>AIOps y AgentOps</b>", sub))
    story.append(_p(
        "<b>AIOps:</b> Prometheus, Grafana, Evidently; alertas drift; rollback vía GitHub Actions. "
        "<b>AgentOps (futuro):</b> agentes Explainer/Ops/Intake con guardrails; sin decisión clínica autónoma.", normal))

    story.append(_p("<b>Enfermedades huérfanas</b>", sub))
    story.append(_p(
        "AGUDA ~1,9%: estratificación, class_weight, recall gate. Patologías no en CSV: no inferir; "
        "requiere_revision_humana; cuarentena de datos nuevos.", normal))

    story.append(_p("<b>MVP implementado</b>", sub))
    story.append(_p(
        "servicio_estado_clinico/: modelo_simulado.py, app.py, Dockerfile. "
        "docker run -p 5000:5000 estado-clinico-demo.", normal))

    story.append(_p("<b>Documentación complementaria</b>", sub))
    story.append(_p(
        "MODEL_CARD.md · ADR/001-003 · CHANGELOG.md · PROPUESTA_PIPELINE_MLOPS.md (texto completo).", normal))

    story.append(Spacer(1, 0.3 * cm))
    story.append(_p("<i>Documento v3.0 — simulación académica; no asesoría clínica.</i>", styles["Italic"]))

    doc.build(story)
    return PDF_OUT


def main() -> None:
    dibujar_pipeline_principal()
    dibujar_ops_capas()
    dibujar_pipeline_e2e()
    dibujar_despliegue_hibrido()
    dibujar_cicd()
    dibujar_datos_ml()
    construir_pdf()
    print(f"Hero: {DIAG_HERO}")
    print(f"Ops: {DIAG_OPS}")
    print(f"Diagramas: {DIAG_E2E}, {DIAG_DEPLOY}, {DIAG_CICD}, {DIAG_DATOS}")
    print(f"Legacy alias: {DIAG_LEGACY}")
    print(f"PDF: {PDF_OUT}")


if __name__ == "__main__":
    main()
