import subprocess

def convert_docx_to_pdf(input_path, output_path):
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_path, input_path])
    print(f"Converted {input_path} to {output_path}")

# Example usage
