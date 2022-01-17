def clean_text(text):
	text = text.replace("˜", "fi")
	text = text.replace("- ", "")
	text = text.replace("-", "")
	text = text.replace("\n", " ")
	
	data_splited = text.split(".")
	sentences = [sentence.lower() for sentence in data_splited if len(sentence) >= 50]
	
	def clean_special_characters(string):
		output_string = ""
		
		for letter in string:
			if letter in "abcdefghijklmnñopqrstuvwxyz0123456789+*-/%$¿¡?!, áéíóú":
				output_string += letter
		
		return output_string
	
	sentences = [clean_special_characters(sentence).strip().capitalize() for sentence in sentences]
	text = ". ".join(sentences)
	
	return " ".join(text.split())


if __name__ == "__main__":
	file_path = "text_data/books_data.txt"
	output_path = "text_data/data.txt"
	
	data = ""
	with open(file_path, "r") as f:
		for line in f.readlines():
			data += line
	
	with open(output_path, "w") as f:
		f.write(clean_text(data))