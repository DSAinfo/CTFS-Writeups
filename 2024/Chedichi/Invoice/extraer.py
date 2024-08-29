import PyPDF2
import re


nombre_pdf = 'invoice.pdf'
with open(nombre_pdf, 'rb') as archivo:
    lector = PyPDF2.PdfReader(archivo)
    pagina = lector.pages[0]
    patron = r"TO:\s+(.*?)\s*\n"
    contenido = re.findall(patron, pagina.extract_text())[0].replace(" ", "_")
    
print("CIT{"+contenido+"}")




