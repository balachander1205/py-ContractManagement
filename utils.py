import openai
from PyPDF2 import PdfReader
from pdfminer import high_level

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = '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'

def supplier_agreement_llm_call(document_text):
    prompt = f"You are given a supplier legal document and extract the following fields and return as a JSON, if you are unable to find the corresponding value for a field return None for the field. Here is the document:\n\n{document_text}"

    response = openai.Completion.create(
                    model="text-davinci-004",  # Replace with the appropriate model name if different
                    prompt=prompt,
                    max_tokens=1500  # Adjust the number of tokens as needed
                    )
    return response.choices[0].text.strip()

# PDF text miner logic for multiple / single page
def read_pdf_file(local_pdf_filename):
  reader = PdfReader(local_pdf_filename)
  number_of_pages = len(reader.pages)
  print("number_of_pages=",number_of_pages)
  extracted_text = ""
  # if there are more than 1 page
  if(number_of_pages > 1):
    for i in range(number_of_pages):
      print("I=",i)
      pages = [i]
      text = high_level.extract_text(local_pdf_filename, "", pages)
      extracted_text+=text
  # if there is only 1 page in pdf file
  if(number_of_pages==1):
    print(number_of_pages)
    pages = [0] # just the first page
    text = high_level.extract_text(local_pdf_filename, "", pages)
    extracted_text+=text
  print("extracted_text=",extracted_text)
  return extracted_text