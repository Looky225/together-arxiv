from services.file import extract_text_from_file
from io import BufferedReader

# Define the path to the example file
example_file_path = "2308.08155.pdf"

# Read the contents of the example file
with open(example_file_path, "rb") as file:
    file_buffer = BufferedReader(file)

    # Call the extract_text_from_file function to extract text
    extracted_text = extract_text_from_file(file_buffer, "application/pdf")

    # Split the extracted text into words
    words = extracted_text.split()

    # Print the first 100 words
    print("First 100 words:")
    print(" ".join(words[:100]))
