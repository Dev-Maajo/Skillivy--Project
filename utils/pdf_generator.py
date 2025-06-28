from fpdf import FPDF
import os
import re

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_left_margin(15)
        self.set_right_margin(15)

    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Skillivy: Resume Feedback Report', ln=True, align='C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, body)
        self.ln()

def remove_unicode(text):
    # Remove emojis and non-ASCII characters to avoid encoding issues
    return re.sub(r'[^\x00-\x7F]+', '', text)

def create_pdf(parsed_data, feedback, roadmap, output_path="static/generated/user_feedback.pdf"):
    # Sanitize inputs before adding to PDF
    parsed_data_clean = remove_unicode(parsed_data)
    feedback_clean = remove_unicode(feedback)
    roadmap_clean = remove_unicode(roadmap)

    pdf = PDF()
    pdf.add_page()

    pdf.chapter_title("Extracted Resume Content:")
    pdf.chapter_body(parsed_data_clean)

    pdf.chapter_title("Feedback:")
    pdf.chapter_body(feedback_clean)

    pdf.chapter_title("Career Roadmap:")
    pdf.chapter_body(roadmap_clean)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)

    return output_path
