import os
import hashlib
import pandas as pd
import streamlit as st
from docx import Document
from PyPDF2 import PdfReader, PdfWriter

def generate_pseudonym(name):
    return hashlib.sha256(name.encode()).hexdigest()[:10]

def process_docx(file_path, pseudonym_table):
    doc = Document(file_path)
    for paragraph in doc.paragraphs:
        for name in pseudonym_table.keys():
            if name in paragraph.text:
                paragraph.text = paragraph.text.replace(name, pseudonym_table[name])
    doc.save(file_path)

def process_pdf(file_path, pseudonym_table):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        text = page.extract_text()
        for name in pseudonym_table.keys():
            if name in text:
                text = text.replace(name, pseudonym_table[name])
        page_content = page
        page_content.extract_text = lambda: text
        writer.add_page(page_content)
    output_path = file_path.replace(".pdf", "_processed.pdf")
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

def process_files(files):
    pseudonym_table = {}
    
    for file in files:
        if file.name.endswith(".docx"):
            doc = Document(file)
            for paragraph in doc.paragraphs:
                words = paragraph.text.split()
                for i in range(len(words) - 1):
                    name = f"{words[i]} {words[i+1]}"
                    if name not in pseudonym_table:
                        pseudonym_table[name] = generate_pseudonym(name)
        elif file.name.endswith(".pdf"):
            reader = pd
