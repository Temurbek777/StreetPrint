import subprocess
from PIL import Image

def convert_docx_to_pdf(input_path, output_path):
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_path, input_path])
    print(f"Converted {input_path} to {output_path}")

# Example usage
def convert_pptx_to_pdf(input_path, output_path):
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', input_path, '--outdir', output_path])

def convert_image_to_pdf(image_path):
    img = Image.open(image_path)
    pdf_path = image_path.replace('.jpg', '.pdf').replace('.png', '.pdf')
    img.save(pdf_path, 'PDF', resolution=100.0)
    return pdf_path