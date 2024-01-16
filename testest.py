from file import extract_text_from_file
from chunks import get_text_chunks  # Remplacez 'your_module' par le nom de votre module ou fichier contenant get_text_chunks

# Remplacez 'your_pdf_file.pdf' par le chemin d'accès à votre fichier PDF
pdf_file_path = '2308.08155.pdf'

# Utilisez votre fonction pour extraire le texte du fichier PDF
pdf_text = extract_text_from_file(pdf_file_path,"application/pdf")

# Appelez get_text_chunks avec le texte extrait
chunks = get_text_chunks(pdf_text, chunk_token_size=None)

# Imprimez uniquement les 5 premiers chunks
for i, chunk in enumerate(chunks[:5]):
    print(f"Chunk {i + 1}:\n{chunk}\n")
