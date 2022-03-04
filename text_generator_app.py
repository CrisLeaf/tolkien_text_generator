import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM


@st.cache(allow_output_mutation=True, suppress_st_warning=True, max_entries=10, ttl=3600)
def transformer_init():
	tokenizer = AutoTokenizer.from_pretrained("CrisLeaf/generador-de-historias-de-tolkien")
	model = AutoModelForCausalLM.from_pretrained("CrisLeaf/generador-de-historias-de-tolkien",
												 pad_token_id=tokenizer.eos_token_id)
	
	return tokenizer, model

def generate_text(input_text, model, tokenizer, input_length, output_length, temperature, top_p):
	inputs = tokenizer.encode(input_text, return_tensors="pt")
	outputs = model.generate(inputs, max_length=input_length + output_length, do_sample=True,
							 temperature=temperature, top_k=0, no_repeat_ngram_size=2,
							 top_p=top_p)
	
	return tokenizer.decode(outputs[0], skip_special_tokens=True)

def main():
	html_header = """
		<head>
		<link rel="stylesheet"href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"integrity="sha512-Fo3rlrZj/k7ujTnHg4CGR2D7kSs0v4LLanw2qksYuRlEzO+tcaEPQogQ0KaoGN26/zrn20ImR1DfuLWnOo7aBA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
		</head>
		<a href="https://crisleaf.herokuapp.com/">
			<i class="fas fa-arrow-left"></i>
		</a>
		<h2 style="text-align:center;">Generador de Historias de Tolkien</h2>
		<style>
			i {
				font-size: 30px;
				color: #222;
			}
			i:hover {
				color: cornflowerblue;
				transition: color 0.3s ease;
			}
		</style>
	"""
	st.markdown(html_header, unsafe_allow_html=True)
	
	tokenizer, model = transformer_init()
	
	st.sidebar.subheader("Selecciona los Parámetros de la Red Neuronal")
	
	st.sidebar.write("Max Length:")
	output_length = st.sidebar.slider("Cantidad Máxima de palabras generadas", 10, 200, 50)
	st.sidebar.write("\n")
	st.sidebar.write("\nTemperature:")
	temperature = st.sidebar.slider("Mide la impresión del resultado (0: máxima impresión - "
									"1: mínima impresión)", 0.01, 1.0, 0.6)
	st.sidebar.write("\n")
	st.sidebar.write("Top P:")
	top_p = st.sidebar.slider("Cantidad de palabras a considerar (en masa probabilística)",
							  0.01, 1.0, 0.8)
	
	html_source_code = """
		<p class="source-code-info">
		<a href="https://huggingface.co/blog/how-to-generate">Más información.</a></p>
	"""
	st.sidebar.markdown(html_source_code, unsafe_allow_html=True)
	
	input_text = ""
	input_text = st.text_area("Ingrese las primeras palabras y la Red Neuronal completará la "
							  "historia:",
							  input_text,
							  placeholder='(Ej: "El mago tomó la espada y")')
	input_length = len(input_text.split())
	
	st.button("Generar")  # useless button for phones
	
	if input_text != "":
		st.write(generate_text(input_text, model, tokenizer, input_length,
							   output_length, temperature, top_p))
	
	html_source_code = """
		<p class="source-code">Código Fuente:
		<a href="https://github.com/CrisLeaf/tolkien_text_generator" target="_blank">
		<i class="fab fa-github"></i></a></p>
		<style>
			.source-code {
				text-align: right;
				color: #666;
			}
			.fa-github {
				color: #666;
			}
		</style>
	"""
	st.markdown(html_source_code, unsafe_allow_html=True)

if __name__ == "__main__":
	main()
