import json
from transformers import BertModel, BertTokenizer
import torch

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'  # You can change this to other BERT models if needed
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Load sample data from cities.json
with open("cities.json", "r") as cities_file:
    cities_json = json.load(cities_file)


# Generate embeddings for each city description using BERT
def generate_cities_embeddings(cities):
    embeddings = []

    for city in cities.get("cities", []):

        # Generate city description
        city_description = f'''{city["name"]} is a city in {city["country"]}.
            It is known for its {", ".join(city["famousPlaces"])} and specialty food like {city["specialtyFood"]}.
            The temperature ranges from {city["temperature"]["min"]} to {city["temperature"]["max"]} degrees Celsius,
            {city["tourismInfo"]}'''

        # Generate embedding for the city description
        city_embedding = generate_city_embedding(city_description)

        # Print the dimensions of the embeddings
        print("CUSTOM - Embeddings shape:", city_embedding.shape)

        # Append content & embedding to the list
        embeddings.append({
            "city_description": city_description,
            "embeddings": city_embedding.tolist()  # Convert tensor to list
        })

    # Save embeddings
    save_city_embeddings(embeddings)


# Store the embeddings in cities_embeddings.json
def save_city_embeddings(embeddings):
    with open("cities_embeddings.json", "w") as embeddings_file:
        json.dump(embeddings, embeddings_file, indent=4)


# Generate BERT embeddings for the city description
def generate_city_embedding(city_description):
    inputs = tokenizer(city_description, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze(0).numpy()


if __name__ == "__main__":
    # Step 1: Generate embeddings for cities and save them
    generate_cities_embeddings(cities_json)
