# The library epub_conversion need xml_cleaner:
# pip install xml_cleaner
from epub_conversion.utils import open_book, convert_epub_to_lines
import re


filename = "example.epub"

book = open_book(filename)

lines = convert_epub_to_lines(book)

cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def cleanhtml(raw_html):
	cleantext = re.sub(cleaner, "", raw_html)
	return cleantext

lines = [cleanhtml(line) for line in lines]

with open("text_data/books_text.txt", "a") as f:
	for line in lines:
		f.write(line)
