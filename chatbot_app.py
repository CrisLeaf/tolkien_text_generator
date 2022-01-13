import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def transformer_init():
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
    
    return tokenizer, model

def generate_text(tokenizer, model, input_text, input_length=50):
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=input_length + 50, do_sample=True, top_k=0, 
                             temperature=0.7, no_repeat_ngram_size=2, top_p=0.9)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def main():
    tokenizer, model = transformer_init()
    
    st.title("GPT-2")
    input_text = st.text_area("Enter text:")
    if input_text != "":
        st.write(generate_text(tokenizer, model, input_text, input_length=len(input_text)))
    
    
if __name__ == "__main__":
    main()