import os
import jdatetime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

OUTPUT_HTML_DIR = os.path.join(BASE_DIR, "output", "html")

OUTPUT_PDF_DIR = os.path.join(BASE_DIR, "output", "pdf")

WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

TAX_RATE = 0.09

COMPANY_NAME = "هلدینگ پالیز"
COMPANY_PHONE = "02112345678"
COMPANY_ADDRESS = "کرج"