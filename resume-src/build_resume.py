# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.styles import ParagraphStyle

INK = colors.HexColor("#1E1E1E")
BODY = colors.HexColor("#2B2B2B")
MUTED = colors.HexColor("#6B6B6B")
ACCENT = colors.HexColor("#2C5A85")
RULE = colors.HexColor("#D9D9D9")

def build(filename, L):
    doc = SimpleDocTemplate(
        filename, pagesize=letter,
        leftMargin=0.6*inch, rightMargin=0.6*inch,
        topMargin=0.5*inch, bottomMargin=0.45*inch,
    )
    W = letter[0] - 1.2*inch

    name = ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=INK)
    headline = ParagraphStyle("headline", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=ACCENT, spaceBefore=2)
    contact = ParagraphStyle("contact", fontName="Helvetica", fontSize=9.3, leading=13, textColor=MUTED, spaceBefore=4)
    summary = ParagraphStyle("summary", fontName="Helvetica", fontSize=9.6, leading=13.5, textColor=BODY, spaceBefore=6, spaceAfter=2)
    section = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=9.2, leading=12, textColor=ACCENT, spaceBefore=10, spaceAfter=3)
    role = ParagraphStyle("role", fontName="Helvetica", fontSize=9.8, leading=13, textColor=INK)
    dates = ParagraphStyle("dates", fontName="Helvetica", fontSize=9, leading=13, textColor=MUTED, alignment=2)
    bullet = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.3, leading=12.8, textColor=BODY)
    skill_k = ParagraphStyle("skk", fontName="Helvetica-Bold", fontSize=9.3, leading=12.8, textColor=INK)
    skill_v = ParagraphStyle("skv", fontName="Helvetica", fontSize=9.3, leading=12.8, textColor=BODY)
    line = ParagraphStyle("line", fontName="Helvetica", fontSize=9.3, leading=12.8, textColor=BODY)

    def rule():
        return HRFlowable(width="100%", thickness=0.6, color=RULE, spaceBefore=1, spaceAfter=4)

    def section_head(title):
        return [Paragraph(title.upper(), section), rule()]

    def left_right(left_html, right_html, lstyle=role, rstyle=dates):
        t = Table([[Paragraph(left_html, lstyle), Paragraph(right_html, rstyle)]], colWidths=[W*0.72, W*0.28], hAlign="LEFT")
        t.setStyle(TableStyle([
            ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        return t

    story = []
    story.append(Paragraph(L["name"], name))
    story.append(Paragraph(L["headline"], headline))
    story.append(Paragraph(L["contact"], contact))
    story.append(rule())
    story.append(Paragraph(L["summary"], summary))

    story += section_head(L["experience"])
    for job in L["jobs"]:
        story.append(left_right(job["role_line"], job["dates"]))
        story.append(Spacer(1, 2))
        items = [ListItem(Paragraph(b, bullet), leftIndent=11) for b in job["bullets"]]
        story.append(ListFlowable(items, bulletType="bullet", start="•", leftIndent=11, bulletFontSize=8, bulletColor=BODY, spaceAfter=7))

    story += section_head(L["skills"])
    rows = [[Paragraph(k, skill_k), Paragraph(v, skill_v)] for k, v in L["skill_rows"]]
    st = Table(rows, colWidths=[W*0.2, W*0.8], hAlign="LEFT")
    st.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(st)

    story += section_head(L["education"])
    for edu in L["edu"]:
        story.append(left_right(edu["line"], edu["date"]))
        for cert in edu.get("certs", []):
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{cert}", line))
        story.append(Spacer(1, 3))

    story += section_head(L["additional_experience"])
    for item in L["additional"]:
        story.append(left_right(item["line"], item["dates"]))
        story.append(Spacer(1, 2))

    doc.build(story)
    print("built", filename)


EN = {
    "name": "Brian Blitz",
    "headline": "Data Analyst · Python · SQL · Power BI",
    "contact": "brian.blitz28@gmail.com &nbsp;&nbsp;·&nbsp;&nbsp; (919) 395-3489 &nbsp;&nbsp;·&nbsp;&nbsp; Las Vegas, NV "
               "&nbsp;&nbsp;·&nbsp;&nbsp; <link href=\"https://brblitz.com\"><font color=\"#2C5A85\">brblitz.com</font></link> "
               "&nbsp;&nbsp;·&nbsp;&nbsp; <link href=\"https://www.linkedin.com/in/brblitz/\"><font color=\"#2C5A85\">LinkedIn</font></link>",
    "summary": "Analytics professional with nearly 4 years of experience, an MS in Data Analytics, and demonstrated expertise in "
               "quantitative analysis, performance monitoring, and data-driven optimization. Well-versed in building automated systems for "
               "data management, analysis, and reporting to support decision-making in fast-moving environments.",
    "experience": "Experience",
    "jobs": [
        {
            "role_line": "<b>Trader I</b> · Caesars Sportsbook",
            "dates": "Aug 2024 – Present · Las Vegas, NV",
            "bullets": [
                "Built performance monitoring systems (Python, Power BI) tracking KPIs across multiple dimensions; presented findings weekly in company-wide reports.",
                "Used monitoring insights to design and implement an optimization strategy that improved performance in key markets.",
                "Built an end-to-end data pipeline for ad-hoc comparative research on pricing, improving performance across multiple markets.",
            ],
        },
        {
            "role_line": "<b>HR Data Analyst</b> · Nance Staffing",
            "dates": "Jan 2023 – Jul 2024 · Remote",
            "bullets": [
                "Built a Python pipeline to clean, process, and filter ~1,000 applicants per month against custom criteria beyond the ATS's built-in filters, contributing to a ~12% increase in 6-month retention.",
                "Designed and built a MySQL database from scratch to structure applicant data, enabling complex analytical queries and reporting that didn't exist before.",
                "Created 4 interactive Tableau dashboards giving stakeholders live visibility into key metrics and performance trends, and built tools that let the team adjust screening criteria and reports themselves.",
            ],
        },
    ],
    "skills": "Skills",
    "skill_rows": [
        ("Programming", "Python, R, SAS, SQL"),
        ("Databases", "Excel, PostgreSQL, MySQL"),
        ("Visualization", "Tableau, Power BI, MatplotLib, Plotly, RMarkdown"),
        ("Data Analysis", "Data Cleaning, Statistics, Predictive Modeling, Machine Learning"),
        ("Project Management", "Business Intelligence &amp; Healthcare Analytics"),
        ("Languages", "Spanish (fluent) &amp; Korean (basic)"),
    ],
    "education": "Education",
    "edu": [
        {
            "line": "<b>M.S. Data Analytics</b> · Colorado State – Global Campus", "date": "2023",
            "certs": [
                "SAS Institute: Predictive Analytics Management (Tier 1) · Business Intelligence (Tier 2) · Applied Data Analytics (Tier 3)",
            ],
        },
        {"line": "<b>B.A. Anthropology</b> · UNC Greensboro", "date": "2015", "certs": []},
    ],
    "additional_experience": "Additional Experience",
    "additional": [
        {"line": "<b>Head English Teacher</b> · Lingua Academy · Busan, South Korea", "dates": "2019 – 2022"},
        {"line": "<b>ESL Instructor</b> · Reading Town · Sejong-si, South Korea", "dates": "2017 – 2019"},
        {"line": "<b>Case Aide</b> · World Relief · High Point, NC", "dates": "2015 – 2017"},
        {"line": "<b>Small Business Owner</b> · Broadway Cafe · Greensboro, NC", "dates": "2012 – 2014"},
    ],
}

ES = {
    "name": "Brian Blitz",
    "headline": "Analista de Datos · Python · SQL · Power BI",
    "contact": "brian.blitz28@gmail.com &nbsp;&nbsp;·&nbsp;&nbsp; (919) 395-3489 &nbsp;&nbsp;·&nbsp;&nbsp; Las Vegas, NV "
               "&nbsp;&nbsp;·&nbsp;&nbsp; <link href=\"https://brblitz.com\"><font color=\"#2C5A85\">brblitz.com</font></link> "
               "&nbsp;&nbsp;·&nbsp;&nbsp; <link href=\"https://www.linkedin.com/in/brblitz/\"><font color=\"#2C5A85\">LinkedIn</font></link>",
    "summary": "Profesional de analítica con casi 4 años de experiencia, una maestría en Analítica de Datos, y experiencia "
               "demostrada en análisis cuantitativo, monitoreo de rendimiento y optimización basada en datos. Con amplia experiencia "
               "en la construcción de sistemas automatizados para la gestión, el análisis y la generación de reportes de datos, en "
               "apoyo a la toma de decisiones informadas dentro de entornos complejos y de ritmo acelerado.",
    "experience": "Experiencia",
    "jobs": [
        {
            "role_line": "<b>Trader I</b> · Caesars Sportsbook",
            "dates": "Ago 2024 – Actualidad · Las Vegas, NV",
            "bullets": [
                "Construí sistemas de monitoreo de rendimiento (Python, Power BI) para el seguimiento de KPIs en múltiples dimensiones; presenté los hallazgos semanalmente en informes a nivel de toda la empresa.",
                "Utilicé los hallazgos del monitoreo para diseñar e implementar una estrategia de optimización que mejoró el rendimiento en mercados clave.",
                "Construí un pipeline de datos integral para investigación comparativa ad hoc sobre precios, mejorando el rendimiento en múltiples mercados.",
            ],
        },
        {
            "role_line": "<b>Analista de Datos de RR. HH.</b> · Nance Staffing",
            "dates": "Ene 2023 – Jul 2024 · Remoto",
            "bullets": [
                "Construí un pipeline en Python para limpiar, procesar y filtrar ~1,000 postulantes al mes según criterios personalizados más allá de los filtros propios del ATS, contribuyendo a un aumento de ~12% en la retención a 6 meses.",
                "Diseñé y construí desde cero una base de datos en MySQL para estructurar los datos de los postulantes, permitiendo consultas analíticas complejas y reportes que antes no existían.",
                "Creé 4 dashboards interactivos en Tableau que dieron a las partes interesadas visibilidad en tiempo real de métricas clave y tendencias de rendimiento, y construí herramientas que permitían al equipo ajustar los criterios de selección y los reportes por su cuenta.",
            ],
        },
    ],
    "skills": "Habilidades",
    "skill_rows": [
        ("Programación", "Python, R, SAS, SQL"),
        ("Bases de datos", "Excel, PostgreSQL, MySQL"),
        ("Visualización", "Tableau, Power BI, MatplotLib, Plotly, RMarkdown"),
        ("Análisis de datos", "Limpieza de datos, Estadística, Modelado predictivo, Aprendizaje automático"),
        ("Gestión de proyectos", "Inteligencia de negocios y analítica de salud"),
        ("Idiomas", "Español (nativo) y coreano (básico)"),
    ],
    "education": "Educación",
    "edu": [
        {
            "line": "<b>Maestría en Analítica de Datos</b> · Colorado State – Global Campus", "date": "2023",
            "certs": [
                "SAS Institute: Gestión de Analítica Predictiva (Nivel 1) · Inteligencia de Negocios (Nivel 2) · Analítica de Datos Aplicada (Nivel 3)",
            ],
        },
        {"line": "<b>Licenciatura en Antropología</b> · UNC Greensboro", "date": "2015", "certs": []},
    ],
    "additional_experience": "Experiencia Adicional",
    "additional": [
        {"line": "<b>Profesor Principal de Inglés</b> · Lingua Academy · Busan, Corea del Sur", "dates": "2019 – 2022"},
        {"line": "<b>Instructor de Inglés como Segunda Lengua</b> · Reading Town · Sejong-si, Corea del Sur", "dates": "2017 – 2019"},
        {"line": "<b>Asistente de Casos</b> · World Relief · High Point, NC", "dates": "2015 – 2017"},
        {"line": "<b>Propietario de Pequeño Negocio</b> · Broadway Cafe · Greensboro, NC", "dates": "2012 – 2014"},
    ],
}

if __name__ == "__main__":
    assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    build(os.path.join(assets, "Blitz.Brian_Resume.pdf"), EN)
    build(os.path.join(assets, "Blitz.Brian_Resume_ES.pdf"), ES)
