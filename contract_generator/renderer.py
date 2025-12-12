from fpdf import FPDF
from models import ContractContent

class ContractPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        # self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf') 
        self.set_font("Helvetica", "", 12)
        
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 10, "CONFIDENTIAL - INFLUENCER AGREEMENT", align="R")
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def render(self, content: ContractContent, output_path: str):
        self.add_page()
        
        # Title
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, content.title, align="C")
        self.ln(15)
        
        # Intro
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, content.intro_text)
        self.ln(10)
        
        # Terms
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "TERMS AND CONDITIONS", ln=True)
        self.set_font("Helvetica", "", 11)
        
        for term in content.terms_text:
            self.multi_cell(0, 6, term)
            self.ln(4)
            
        self.add_page()
        
        # Schedule A
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "SCHEDULE A: SERVICES & DELIVERABLES", ln=True)
        self.ln(2)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, content.schedule_a)
        self.ln(10)

        # Schedule B
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "SCHEDULE B: COMPENSATION", ln=True)
        self.ln(2)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, content.schedule_b)
        self.ln(15)
        
        # Signatures
        self.add_page() 
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "SIGNATURES", ln=True)
        self.ln(5)
        self.set_font("Helvetica", "", 11)
        self.cell(0, 10, content.signatures_section, ln=True)
        self.ln(20)
        
        # Signature Blocks with "Anchor Tags" (text usually white or hidden, but here visible for demo)
        # Often usage is /s1/ for signer 1, etc.
        
        y = self.get_y()
        
        # Brand Sig
        self.cell(90, 10, "BRAND:", ln=False)
        self.cell(90, 10, "INFLUENCER:", ln=True)
        
        self.line(10, y+25, 90, y+25) # Line for brand
        self.line(100, y+25, 180, y+25) # Line for influencer
        
        self.ln(20)
        
        # Using white text for anchor tags so they are invisible to humans but visible to DocuSign API
        self.set_text_color(255, 255, 255) 
        self.cell(90, 5, "/s1/", ln=False) # Anchor for Brand
        self.cell(90, 5, "/s2/", ln=True) # Anchor for Influencer
        self.set_text_color(0, 0, 0) # Reset
        
        self.output(output_path)
