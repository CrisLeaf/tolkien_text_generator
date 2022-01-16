import PyPDF2
from tqdm import tqdm
import os


def convert_pdf_to_string(filename):
	data = ""
	with open(filename, "rb") as f:
		pdf_reader = PyPDF2.PdfFileReader(f)
		
		for i in tqdm(range(pdf_reader.numPages)):
			page_object = pdf_reader.getPage(i)
			data += page_object.extractText()
	
	return data
	
def clean_text(string):
	string = string.replace("˜", "fi")
	
	return " ".join(string.split())


if __name__ == "__main__":
	files = os.listdir("books_data/")
	
	data = ""
	
	for filename in files:
		whole_text = convert_pdf_to_string("books_data/" + filename)
		whole_text = clean_text(whole_text)
		data += whole_text
		
	
	with open("text_data/books_text.txt", "w") as f:
		f.write(data)