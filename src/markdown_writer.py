"""
METHOD 1: Simple text to Markdown Conversion
this method is suitable if your input text is already in a format that can be directly written to a MD file
this won't require complex parsing or styling
"""
# pip install pdfplumber || Extract text, fonts, layout, lines, shapes, and images from a PDF.
import pdfplumber   

# pip install fpdf
from fpdf import FPDF


def txt_to_pdf(input_txt_file):
    # variable pdf
    pdf = FPDF()

    pdf.add_page()

    # set style and size of font that you want
    pdf.set_font("Arial", size = 15)

    # open the txt file in read more
    f = open(input_txt_file, "r")

    for x in f:
        x = x.strip() # removes trailing \n or \r\n
        # pdf.cell(width, height, txt= the text to display, ln=1 (line break after the cell), align = 'C' - Center | 'L' = Left | 'R' - Right)
        pdf.cell(200,10, txt = x, ln = 1, align='R')

    #save the pdf with name .pdf
    pdf.output("mytext.pdf")
    pdf_to_md("mytext.pdf", "TEST.md")


def pdf_to_md(input_pdf_file, output_md_filename):
    try:
        # opens the pdf file using the library and using with ensures file is automatically closed when you're done 
        with pdfplumber.open(input_pdf_file) as pdf:
            # you init and empty string to store the complete extracted text from all the pages
            full_text = ""

            # for each page, you call extract that uses layout analysis to pull out readable text from the page
            # top to bottom, left to right (roughly) 
            for page in pdf.pages:
                text = page.extract_text()

                # checks if any text was actually extracted || if it isn't empty, it's appended to full_text, along with 2 line breaks (separate pages or sections)
                if text:
                    full_text += text + "\n\n"

        with open(output_md_filename, 'w', encoding='utf-8') as f_out:
            f_out.write(full_text)
    except FileNotFoundError:
        print(f"Error: File not found.")
    except Exception as e:
        print(f"Error in processing file: {e}")


txt_to_pdf("file_test_one.txt")