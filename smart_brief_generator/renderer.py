from fpdf import FPDF
import textwrap

# Robust import handling
try:
    from models import BriefData
except ImportError:
    from .models import BriefData

class PDFRenderer:
    def render(self, data: BriefData, filename: str = "campaign_brief.pdf"):
        pdf = FPDF()
        pdf.add_page()
        
        # --- Header ---
        pdf.set_font("Helvetica", "B", 24)
        pdf.cell(0, 15, "Campaign Brief", align="C", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", "I", 14)
        pdf.cell(0, 10, data.campaign_title, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)
        
        # --- Overview ---
        self._section_title(pdf, "Overview")
        self._body_text(pdf, data.overview)
        pdf.ln(5)
        
        # --- Target Audience ---
        self._section_title(pdf, "Target Audience")
        self._body_text(pdf, data.target_audience_description)
        pdf.ln(5)
        
        # --- Key Messages ---
        self._section_title(pdf, "Key Messages")
        for msg in data.key_messages:
            self._bullet_point(pdf, msg)
        pdf.ln(5)
        
        # --- Deliverables ---
        self._section_title(pdf, "Deliverables")
        for item in data.deliverables:
            self._bullet_point(pdf, item)
        pdf.ln(5)

        # --- Dos and Don'ts ---
        self._section_title(pdf, "Guidelines (Do's & Don'ts)")
        for item in data.dos_and_donts:
            self._bullet_point(pdf, item)
        pdf.ln(5)
        
        # --- Hashtags ---
        self._section_title(pdf, "Required Hashtags")
        hashtags_str = " ".join(data.hashtags)
        self._body_text(pdf, hashtags_str)
        
        # --- Save ---
        pdf.output(filename)
        print(f"PDF generated successfully: {filename}")

    def _section_title(self, pdf, title):
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, title, fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    def _body_text(self, pdf, text):
        pdf.set_font("Helvetica", size=12)
        # Use explicit align='L' to prevent justification issues
        pdf.multi_cell(w=0, h=6, text=text, align="L")
    
    def _bullet_point(self, pdf, text):
        pdf.set_font("Helvetica", size=12)
        # Indent bullet slightly
        current_x = pdf.get_x()
        pdf.set_x(current_x + 5)
        pdf.multi_cell(w=0, h=6, text=f"{chr(149)} {text}", align="L")
        # Reset X happens automatically for next line usually, but ensure consistency if needed
        pdf.set_x(current_x)
