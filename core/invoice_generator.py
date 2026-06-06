from jinja2 import Environment, FileSystemLoader
import pdfkit
import os


def render_html(template_dir, template_name, context):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    return template.render(**context)

def save_html(html_content, output_path):
    os.makedirs(os.path.dirname(output_path),exist_ok=True)
    with open(
        output_path,
        mode="w",
        encoding="utf-8"
    ) as file:
        file.write(html_content)

def generate_pdf(html_path, pdf_path, wkhtmltopdf_path):
    os.makedirs( os.path.dirname(pdf_path),exist_ok=True)
    config = pdfkit.configuration( wkhtmltopdf=wkhtmltopdf_path)
    pdfkit.from_file( html_path, pdf_path, configuration=config)

