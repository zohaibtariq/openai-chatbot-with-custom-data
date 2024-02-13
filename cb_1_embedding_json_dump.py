import os
from openai import OpenAI
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a dictionary containing environment variables
envs = os.environ

client = OpenAI(
    api_key=envs.get("OPENAI_API_KEY")
)

# Load sample data from cities.json
with open("cities.json", "r") as cities_file:
    cities_json = json.load(cities_file)


# Generate embeddings for each city description using ChatGPT OpenAI API
def generate_cities_embeddings(cities):

    embeddings = []

    for city in cities.get("cities", []):

        # Generate city description
        city_description = f'''{city["name"]} is a city in {city["country"]}.
            It is known for its {", ".join(city["famousPlaces"])} and specialty food like {city["specialtyFood"]}.
            The temperature ranges from {city["temperature"]["min"]} to {city["temperature"]["max"]} degrees Celsius,
            {city["tourismInfo"]}'''
        # print(city_description)

        # Generate embedding for the city description
        city_embedding = generate_city_embedding(city_description)

        # Append content & embedding to the list
        embeddings.append({
            "city_description": city_description,
            "embeddings": city_embedding
        })

    # save embeddings
    save_city_embeddings(embeddings)


# Store the embeddings in cities_embeddings.json
def save_city_embeddings(embeddings):
    with open("cities_embeddings.json", "w") as embeddings_file:
        json.dump(embeddings, embeddings_file, indent=4)


# Main function

def generate_city_embedding(city_description):
    response = client.embeddings.create(
        input=city_description,
        model="text-embedding-3-small"
    )
    # print(response.data[0].embedding)
    return response.data[0].embedding


if __name__ == "__main__":
    # Step 1: Generate embeddings for cities and save them
    generate_cities_embeddings(cities_json)
