import datetime
import json
import os
import tempfile

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Flowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.database import decompress_data, get_db_connection


class InteractiveCheckbox(Flowable):
    def __init__(self, name, checked=False, size=10):
        super().__init__()
        self.name = name
        self.checked = checked
        self.size = size

    def draw(self):
        self.canv.saveState()
        self.canv.acroForm.checkbox(
            name=self.name,
            x=0,
            y=0,
            buttonStyle='check',
            checked=self.checked,
            size=self.size
        )
        self.canv.restoreState()

    def wrap(self, availWidth, availHeight):
        return self.size, self.size

class InteractiveTextField(Flowable):
    def __init__(self, name, value="", width=240, height=12):
        super().__init__()
        self.name = name
        self.value = value
        self.width = width
        self.height = height

    def draw(self):
        self.canv.saveState()
        self.canv.acroForm.textfield(
            name=self.name,
            value=self.value,
            x=0,
            y=0,
            width=self.width,
            height=self.height
        )
        self.canv.restoreState()

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

class LastPageTimestampCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.timestamp = ""
        self.is_printer_friendly = False

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for page_idx, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            if page_idx == num_pages - 1:
                self.saveState()
                self.setFont('Helvetica', 8)
                if self.is_printer_friendly:
                    self.setFillColor(colors.black)
                else:
                    self.setFillColor(colors.HexColor("#8E8A82"))
                self.drawRightString(612 - 54, 30, f"Exported: {self.timestamp}")
                self.restoreState()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

def generate_pdf(trip_id: str, printer_friendly: bool = False) -> bytes:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get trip name and check if archived
    cursor.execute("SELECT trip_name, is_archived, compressed_items FROM trips WHERE trip_id = ?", (trip_id,))
    trip_row = cursor.fetchone()
    trip_name = trip_row['trip_name'] if trip_row else "Packing Checklist"
    is_archived = trip_row['is_archived'] == 1 if trip_row else False

    items = []
    if is_archived:
        blob = trip_row['compressed_items'] if trip_row else None
        if blob:
            items = json.loads(decompress_data(blob))
    else:
        cursor.execute("SELECT * FROM packing_items WHERE trip_id = ? ORDER BY category, sort_order, item_name ASC", (trip_id,))
        items = [dict(r) for r in cursor.fetchall()]

    conn.close()

    temp_pdf = tempfile.NamedTemporaryFile(prefix="packing_list_", suffix=".pdf", delete=False)
    temp_pdf_path = temp_pdf.name
    temp_pdf.close()

    doc = SimpleDocTemplate(
        temp_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    story = []

    # Color Palette definitions
    if printer_friendly:
        text_color = colors.black
        accent_color = colors.black
        border_color = colors.black
    else:
        # Organic Sand Theme Colors
        text_color = colors.HexColor("#3C3F3E")
        accent_color = colors.HexColor("#8C7A6B") # Warm earth
        border_color = colors.HexColor("#D3CFC9")

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=accent_color,
        spaceAfter=6
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=text_color,
        spaceAfter=20
    )

    cat_heading_style = ParagraphStyle(
        'CategoryHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=accent_color,
        spaceBefore=12,
        spaceAfter=6
    )

    item_style = ParagraphStyle(
        'ItemText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=text_color
    )

    item_indent_style = ParagraphStyle(
        'ItemTextIndent',
        parent=item_style,
        leftIndent=15
    )

    notes_style = ParagraphStyle(
        'ItemNotes',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        textColor=text_color
    )

    # Render Header
    story.append(Paragraph(f"Packing Checklist: {trip_name}", title_style))
    story.append(Paragraph(f"Layout Mode: {'Printer Friendly (Monochrome)' if printer_friendly else 'Organic Sand Form'}", meta_style))
    story.append(Spacer(1, 10))

    if not items:
        story.append(Paragraph("No items found in this packing list.", item_style))
    else:
        # Group items by category
        grouped_items = {}
        for item in items:
            cat = item['category'] or 'General'
            if cat not in grouped_items:
                grouped_items[cat] = []
            grouped_items[cat].append(item)

        # Sort items hierarchically in each category
        for cat in list(grouped_items.keys()):
            cat_items = grouped_items[cat]
            item_map = {item['id']: item for item in cat_items}
            roots = []
            children_map = {}
            for item in cat_items:
                pid = item.get('parent_id')
                if pid and pid in item_map:
                    if pid not in children_map:
                        children_map[pid] = []
                    children_map[pid].append(item)
                else:
                    roots.append(item)

            sorted_cat_items = []
            for root in roots:
                sorted_cat_items.append(root)
                if root['id'] in children_map:
                    for child in children_map[root['id']]:
                        sorted_cat_items.append(child)
            grouped_items[cat] = sorted_cat_items

        for category, cat_items in grouped_items.items():
            story.append(Paragraph(category, cat_heading_style))

            # Create a table for items under this category
            table_data = []
            for item in cat_items:
                # Layout based on layout mode
                if printer_friendly:
                    status_box = "[x]" if item['is_checked'] else "[ ]"
                    desc = item['description'] or ""
                    desc_cell = Paragraph(desc, notes_style) if desc else Paragraph("", notes_style)
                else:
                    status_box = InteractiveCheckbox(f"chk_{item['id']}", checked=bool(item['is_checked']), size=10)
                    desc = item['description'] or ""
                    desc_cell = InteractiveTextField(f"txt_{item['id']}", value=desc, width=240, height=12)

                item_label = f"{item['item_name']} (Qty: {item['quantity']})"
                if item['priority'] == 'High':
                    item_label += " [!] "

                style_to_use = item_indent_style if item.get('parent_id') else item_style

                table_data.append([
                    status_box,
                    Paragraph(item_label, style_to_use),
                    desc_cell
                ])

            t = Table(table_data, colWidths=[30, 200, 250])

            # Table styles
            t_style = [
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]
            if printer_friendly:
                t_style.append(('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black))
            else:
                t_style.append(('LINEBELOW', (0, 0), (-1, -1), 0.5, border_color))

            t.setStyle(TableStyle(t_style))
            story.append(t)
            story.append(Spacer(1, 10))

    # Build document using the custom canvas class
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def canvasmaker_factory(*args, **kwargs):
        c = LastPageTimestampCanvas(*args, **kwargs)
        c.timestamp = date_str
        c.is_printer_friendly = printer_friendly
        return c

    doc.build(story, canvasmaker=canvasmaker_factory)

    with open(temp_pdf_path, "rb") as f:
        pdf_data = f.read()

    try:
        os.remove(temp_pdf_path)
    except Exception:
        pass

    return pdf_data


def generate_markdown(trip_id: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get trip name and check if archived
    cursor.execute("SELECT trip_name, is_archived, compressed_items FROM trips WHERE trip_id = ?", (trip_id,))
    trip_row = cursor.fetchone()
    trip_name = trip_row['trip_name'] if trip_row else "Packing Checklist"
    is_archived = trip_row['is_archived'] == 1 if trip_row else False

    items = []
    if is_archived:
        blob = trip_row['compressed_items'] if trip_row else None
        if blob:
            items = json.loads(decompress_data(blob))
    else:
        cursor.execute("SELECT * FROM packing_items WHERE trip_id = ? ORDER BY category, sort_order, item_name ASC", (trip_id,))
        items = [dict(r) for r in cursor.fetchall()]

    conn.close()

    if not items:
        return f"# Packing Checklist: {trip_name}\n\nNo items found in this packing list.\n"

    # Group items by category
    grouped_items = {}
    for item in items:
        cat = item['category'] or 'General'
        if cat not in grouped_items:
            grouped_items[cat] = []
        grouped_items[cat].append(item)

    # Sort items hierarchically in each category
    for cat in list(grouped_items.keys()):
        cat_items = grouped_items[cat]
        item_map = {item['id']: item for item in cat_items}
        roots = []
        children_map = {}
        for item in cat_items:
            pid = item.get('parent_id')
            if pid and pid in item_map:
                if pid not in children_map:
                    children_map[pid] = []
                children_map[pid].append(item)
            else:
                roots.append(item)

        sorted_cat_items = []
        for root in roots:
            sorted_cat_items.append(root)
            if root['id'] in children_map:
                for child in children_map[root['id']]:
                    sorted_cat_items.append(child)
        grouped_items[cat] = sorted_cat_items

    # Build the markdown content
    md = [f"# Packing Checklist: {trip_name}\n"]
    for category, cat_items in grouped_items.items():
        md.append(f"## {category}")
        for item in cat_items:
            status_box = "[x]" if item['is_checked'] else "[ ]"
            
            # High priority flag
            prio_flag = " [!] " if item['priority'] == 'High' else " "
            
            # Check for sub-item indentation (2 spaces)
            indent = "  " if item.get('parent_id') else ""
            
            line = f"{indent}- {status_box}{prio_flag}{item['item_name']} (Qty: {item['quantity']})"
            
            desc = (item['description'] or "").strip()
            if desc:
                line += f" - {desc}"
                
            md.append(line)
        md.append("") # Spacer between categories

    return "\n".join(md).strip() + "\n"

