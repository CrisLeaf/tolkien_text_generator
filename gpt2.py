from transformers import GPT2LMHeadModel, GPT2Tokenizer


def generate_text(input_text):
	inputs = tokenizer.encode(input_text, return_tensors="pt")
	outputs = model.generate(inputs, max_length=200, do_sample=True, top_p=0.9, top_k=0,
							 num_return_sequences=2)
	
	return tokenizer.decode(outputs[0], skip_special_tokens=True)
	

if __name__ == "__main__":
	tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
	model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
	
	print("Type 'quit' to exit. \nType 'reset' to restart the conversation.\n")
	user_name = input("Enter your name: ")
	print("\n")
	
	accumulated_text = ""
	
	while True:
		input_text = input(user_name + ": ")

		if input_text == "quit":
			break
		elif input_text == "reset":
			accumulated_text = ""
		
		input_text = user_name + ": " + input_text + "\nBot: "
		accumulated_text = accumulated_text + input_text
		start_index = len(accumulated_text)
		
		if len(input_text) > 150:
			accumulated_text = accumulated_text[:150]
		
		output_text = generate_text(accumulated_text)[start_index:]
		first_sentence_index = output_text.find(".")
		print("Bot: " + output_text[:first_sentence_index + 1])
		second_sentence_index = output_text[first_sentence_index + 1:].find(".")
		print(output_text[:first_sentence_index + second_sentence_index + 2])
		