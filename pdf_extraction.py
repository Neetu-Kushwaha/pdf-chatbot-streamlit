import sys
from QA_without_runnable import get_question_answers
import os
import pandas as pd
import pymupdf
from multi_column import column_boxes
import fitz  # PyMuPDF library
import re


def remove_images_from_pdf(pdf_document):
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        images = page.get_images(full=True)

        for image in images:
            xref = image[0]
            rect = page.get_image_rects(xref)
            if rect:
                for area in rect:
                    page.add_redact_annot(area, fill=(1, 1, 1))
                    page.apply_redactions()
    return pdf_document


def format_text(raw_text):
    heading_pattern = re.compile(r"^[A-Z ]{3,}.*$")
    subheading_pattern = re.compile(r"^\s*[•-]\s.*$")
    formatted_lines = []
    lines = raw_text.splitlines()

    for line in lines:
        if heading_pattern.match(line.strip()):
            formatted_lines.append(f"\n{line.strip()}\n{'-' * len(line.strip())}")
        elif subheading_pattern.match(line.strip()):
            formatted_lines.append(f"- {line.strip()[2:]}")
        elif line.strip():
            formatted_lines.append(f"  {line.strip()}")
    return "\n".join(formatted_lines)


def main(file_path):

    if not os.path.exists(file_path):
        print("File does not exist.")
        return


    doc = pymupdf.open(file_path)
    doc = remove_images_from_pdf(doc)
    formatted_text = ''
    formatted_text = ''
    for page_num, page in enumerate(doc):
        # print(f"Processing page {page_num + 1}...")
        # Process column boxes
        bboxes = column_boxes(page, footer_margin=0, no_image_text=True)
        if not bboxes:
            print(f"No text boxes found on page {page_num + 1}.")
        else:
            for rect in bboxes:
                text = page.get_text(clip=rect, sort=True)
                if text.strip():  # Ensure non-empty text
                    formatted_text += format_text(text) + '\n' + "-" * 80 + '\n'
    new_texts = formatted_text
    return new_texts


def chat_openai(new_texts, question):
    # print("hi")
    # Get question answers using GPT-3.5
    openai_api_key = 'YOUR API KEY'
    result = get_question_answers(new_texts, question, openai_api_key)
    return result

