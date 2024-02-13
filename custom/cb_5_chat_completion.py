from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)


def chat_completion(user_input):
    # Tokenize the user input
    input_ids = tokenizer.encode(user_input, return_tensors="pt")

    # Generate response using GPT-2
    output = model.generate(input_ids, max_length=len(user_input)/2, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)

    # Decode the response tokens to get the text
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return response


# Example usage
user_question = "What is the capital of France?"
context = "France is a country located in Western Europe. Its capital city is Paris."

# Generate response based on user question and provided context
# response = chat_completion(user_question + " " + context)
response = chat_completion(context)
print("Generated response:", response)
