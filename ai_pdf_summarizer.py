from PyPDF2 import PdfReader
from transformers import pipeline
import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF

pdf = FPDF(format='letter')
summarizer = pipeline(task="summarization", model="sshleifer/distilbart-cnn-12-6")

root = tk.Tk()
root.withdraw()

print("Please select a pdf file")
file_placement = filedialog.askopenfilename(
    title="open file",
    filetypes=[("text files" ,"*.pdf")]
)

def summarize_long_text(text, chunk_size=1000):
    chunks = [text[i: i+chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []

    for chunk in chunks:
        try:
            summarie = summarizer(chunk, max_length=200, min_length=10, do_sample=False)
            summaries.append(summarie[0]["summary_text"])
        except Exception as e:
            print(f"Error in chunk: {e}")

    return " ".join(summaries)            

with open(file_placement, "rb") as file:
    the_summary = ''
    reader = PdfReader(file)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            try:
                summarized_text = summarizer(text, max_length=200, min_length=10, do_sample=False)[0]["summary_text"]      
            except:
                summarized_text = summarize_long_text(text)
            
            the_summary += f"""Page {i + 1} 
            {summarized_text}
            """
    the_summary = the_summary.strip()
    pdf_name = input("Give a name to the pdf: ")
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(0, 10, "Summary", border="B", align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, the_summary.encode('latin-1', 'replace').decode('latin-1'))
    pdf.output(f"{pdf_name}.pdf")    
