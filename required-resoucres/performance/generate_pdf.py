from __future__ import annotations

import html
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle


BASE_DIR = Path(__file__).resolve().parent
HTML_PATH = BASE_DIR / "angular-frontend-performance-guide.html"
PDF_PATH = BASE_DIR / "angular-frontend-performance-guide.pdf"


def build_styles() -> StyleSheet1:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="GuideTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#152923"),
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideSubtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#5c584f"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideH2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#152923"),
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideH3",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=colors.HexColor("#152923"),
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideH4",
            parent=styles["Heading4"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#152923"),
            spaceBefore=6,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideBody",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=10.5,
            leading=14,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideSmall",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#5c584f"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideBullet",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=10.5,
            leading=14,
            leftIndent=12,
            firstLineIndent=-10,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideCode",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=8.8,
            leading=11,
            backColor=colors.HexColor("#f3efe7"),
            borderColor=colors.HexColor("#d8d0c3"),
            borderWidth=0.5,
            borderPadding=8,
            borderRadius=4,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideCallout",
            parent=styles["BodyText"],
            fontName="Times-Roman",
            fontSize=10.2,
            leading=13.5,
            leftIndent=8,
            rightIndent=6,
            borderPadding=8,
            borderWidth=0.7,
            borderColor=colors.HexColor("#bfded5"),
            backColor=colors.HexColor("#f4fbf8"),
            spaceBefore=6,
            spaceAfter=8,
        )
    )
    return styles


def convert_inline(node: Tag | NavigableString) -> str:
    if isinstance(node, NavigableString):
      return html.escape(str(node))

    children = "".join(convert_inline(child) for child in node.children)
    name = node.name.lower()

    if name in {"strong", "b"}:
        return f"<b>{children}</b>"
    if name in {"em", "i"}:
        return f"<i>{children}</i>"
    if name == "code":
        return f'<font face="Courier">{children}</font>'
    if name == "a":
        href = html.escape(node.get("href", ""), quote=True)
        return f'<a href="{href}" color="#0b5e8a">{children}</a>'
    if name == "br":
        return "<br/>"
    return children


def paragraph_markup(tag: Tag) -> str:
    return "".join(convert_inline(child) for child in tag.children).strip()


def build_table(tag: Tag, styles: StyleSheet1) -> Table:
    rows = []
    max_cols = 0
    for tr in tag.find_all("tr"):
        row = []
        for cell in tr.find_all(["th", "td"], recursive=False):
            text = paragraph_markup(cell) or " "
            style_name = "GuideBody"
            if cell.name == "th":
                text = f"<b>{text}</b>"
            row.append(Paragraph(text, styles[style_name]))
        max_cols = max(max_cols, len(row))
        rows.append(row)

    if not rows:
        return Table([[Paragraph(" ", styles["GuideBody"])]] )

    for row in rows:
        while len(row) < max_cols:
            row.append(Paragraph(" ", styles["GuideBody"]))

    usable_width = A4[0] - (16 * mm) - (16 * mm)
    col_width = usable_width / max_cols
    table = Table(rows, colWidths=[col_width] * max_cols, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1ece2")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8d0c3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def build_story() -> list:
    styles = build_styles()
    soup = BeautifulSoup(HTML_PATH.read_text(encoding="utf-8"), "html.parser")
    main = soup.find("main")
    story = []

    for element in main.children:
        if isinstance(element, NavigableString):
            continue
        if not isinstance(element, Tag):
            continue

        if "section-break" in (element.get("class") or []):
            story.append(PageBreak())

        section_items = []
        for child in element.children:
            if isinstance(child, NavigableString):
                continue
            if not isinstance(child, Tag):
                continue

            name = child.name.lower()

            if name == "h1":
                section_items.append(Paragraph(paragraph_markup(child), styles["GuideTitle"]))
            elif name == "h2":
                section_items.append(Paragraph(paragraph_markup(child), styles["GuideH2"]))
            elif name == "h3":
                section_items.append(Paragraph(paragraph_markup(child), styles["GuideH3"]))
            elif name == "h4":
                section_items.append(Paragraph(paragraph_markup(child), styles["GuideH4"]))
            elif name == "p":
                style = styles["GuideSmall"] if "small" in (child.get("class") or []) else styles["GuideBody"]
                if "subtitle" in (child.get("class") or []):
                    style = styles["GuideSubtitle"]
                if "callout" in (child.get("class") or []):
                    style = styles["GuideCallout"]
                section_items.append(Paragraph(paragraph_markup(child), style))
            elif name in {"ul", "ol"}:
                items = []
                for index, li in enumerate(child.find_all("li", recursive=False), start=1):
                    prefix = "•" if name == "ul" else f"{index}."
                    markup = paragraph_markup(li)
                    items.append(Paragraph(f"{prefix} {markup}", styles["GuideBullet"]))
                section_items.extend(items)
                section_items.append(Spacer(1, 3))
            elif name == "pre":
                section_items.append(Preformatted(child.get_text("", strip=False).strip("\n"), styles["GuideCode"]))
            elif name == "table":
                section_items.append(build_table(child, styles))
                section_items.append(Spacer(1, 6))
            elif name == "div":
                classes = child.get("class") or []
                if "pill-row" in classes:
                    pills = [span.get_text(" ", strip=True) for span in child.find_all("span", class_="pill")]
                    if pills:
                        joined = " | ".join(html.escape(pill) for pill in pills)
                        section_items.append(Paragraph(joined, styles["GuideSmall"]))
                elif "callout" in classes:
                    section_items.append(Paragraph(paragraph_markup(child), styles["GuideCallout"]))
                elif "grid" in classes:
                    for card in child.find_all("div", class_="card", recursive=False):
                        for nested in card.children:
                            if isinstance(nested, NavigableString) or not isinstance(nested, Tag):
                                continue
                            nested_name = nested.name.lower()
                            if nested_name == "h3":
                                section_items.append(Paragraph(paragraph_markup(nested), styles["GuideH3"]))
                            elif nested_name in {"ul", "ol"}:
                                for index, li in enumerate(nested.find_all("li", recursive=False), start=1):
                                    prefix = "•" if nested_name == "ul" else f"{index}."
                                    section_items.append(Paragraph(f"{prefix} {paragraph_markup(li)}", styles["GuideBullet"]))
                                section_items.append(Spacer(1, 4))
                else:
                    text = paragraph_markup(child)
                    if text:
                        section_items.append(Paragraph(text, styles["GuideBody"]))

        if section_items:
            if "avoid-break" in (element.get("class") or []):
                story.append(KeepTogether(section_items))
            else:
                story.extend(section_items)

    return story


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#5c584f"))
    canvas.drawRightString(A4[0] - 16 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def main() -> None:
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title="Angular and Frontend Performance Optimization Guide",
        author="GitHub Copilot",
    )
    doc.build(build_story(), onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    main()