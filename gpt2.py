from transformers import GPT2LMHeadModel, GPT2Tokenizer


def generate_text(input_text, input_length=0):
	inputs = tokenizer.encode(input_text, return_tensors="pt")
	outputs = model.generate(inputs, max_length=input_length + 50, do_sample=True, top_p=0.9,
							 top_k=0, temperature=0.7)
	
	return tokenizer.decode(outputs[0], skip_special_tokens=True)
	

if __name__ == "__main__":
	tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
	model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
	
	print("Type 'quit' to exit. \nType 'reset' to restart the conversation.\n")
	user_name = input("Enter your name: ").capitalize()
	print("\n")
	
	accumulated_text = ""
	
	while True:
		input_text = input(user_name + ": ").capitalize()
		
		if input_text == "Quit":
			break
		elif input_text == "Reset":
			accumulated_text = ""
			print("Conversation restarted!\n")
			input_text = input(user_name + ": ").capitalize()
		
		if input_text[-1] != ".":
			input_text += "."
			
		input_text = user_name + ": " + input_text + "\nBot:"
		accumulated_text += input_text
		start_index = len(accumulated_text)

		print("INPUT: " + accumulated_text)
		
		output_text = generate_text(accumulated_text, input_length=start_index)[start_index:]
		first_sentence_index = output_text.find(".")
		second_sentence_index = output_text[first_sentence_index + 1:].find(".")
		output_text = output_text[:first_sentence_index + second_sentence_index + 2]
		print("Bot:" + output_text)
		
		accumulated_text += output_text + "\n"