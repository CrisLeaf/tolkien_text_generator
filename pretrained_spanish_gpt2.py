from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("DeepESP/gpt2-spanish")

model = AutoModelForCausalLM.from_pretrained("DeepESP/gpt2-spanish")