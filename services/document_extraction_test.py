import os
from services.file import extract_text_from_filepath

# Define the path to the test PDF file
test_pdf_path = "2308.08155.pdf"

try:
    extracted_text = extract_text_from_filepath(test_pdf_path)

    # Add assertions to verify the expected output
    assert isinstance(extracted_text, str)
    assert len(extracted_text) > 0

    # Print the first 100 characters of the extracted text
    print("Extracted text (first 100 characters):")
    print(extracted_text[:100])

    print("Test passed!")
except Exception as e:
    print(f"Test failed with exception: {e}")

# Clean up the test PDF file after the test
os.remove(test_pdf_path)
