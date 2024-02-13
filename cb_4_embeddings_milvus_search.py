import os
# import numpy as np  # Add numpy for normalization
from openai import OpenAI
from dotenv import load_dotenv
from pymilvus import connections, Collection

# Load environment variables from .env file
load_dotenv()

# Create a dictionary containing environment variables
envs = os.environ

client = OpenAI(
    api_key=envs.get("OPENAI_API_KEY")
)

# Connect to Milvus
connections.connect(host='standalone', port='19530')

collection_name = 'cities_embeddings'
collection = Collection(name=collection_name)


def generate_user_query_embedding(query):
    response = client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    embedding = response.data[0].embedding
    # Normalize the embedding
    # embedding /= np.linalg.norm(embedding)
    # print(embedding)
    return embedding


print("Start searching based on vector similarity")

search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 10},
}

# best distance for related queries is 1.4 or 1.5 (means less than 1.5 or 1.4 can be considered as related)

# UNRELATED
# query_user = "What are some emerging trends in sustainable architecture?"  # 1.634
# query_user = "Can you explain the process of quantum entanglement in layman's terms?"  # 1.845
# query_user = "How does the human brain process abstract concepts like creativity and imagination?"  # 1.764
# query_user = "What are some potential applications of blockchain technology beyond cryptocurrency?" # 1.799
# query_user = "Can you discuss the impact of climate change on biodiversity in marine ecosystems?" # 1.649
# query_user = "Explain Solar system in summarised way as short as possible."  # unrelated | 1.76

# RELATED
# query_user = "Where to go for jubilant vacations?"  # 1.44
# query_user = "Can you mention a popular pastry often associated with French cuisine?" # 1.0
# query_user = "Where might one find beautiful coastal landscapes and architectural marvels in a country known for
# its diverse wildlife?"  # 1.383
# query_user = "Which city is famed for its lively music, colorful festivals, and vibrant street culture in a South American nation celebrated for its rainforests and soccer prowess?"# 0.975
# query_user = "What is the political and cultural capital of a European country known for its engineering prowess, beer gardens, and historical significance?"  # 1.11
# query_user = "Can you identify a prominent clock tower that is a symbol of national pride and heritage in a country known for its monarchy and tea culture?"  # 1.211
# query_user = "Which dish, known for its crispy texture and savory flavors, is a staple in a country with a rich history of martial arts and calligraphy?"  # 1.385
# query_user = "Where might one explore ancient ruins and archaeological wonders in a nation renowned for its mariachi music, spicy cuisine, and colorful festivals?"  # 1.06
# query_user = "Which city is famous for its bustling film industry, vibrant nightlife, and coastal charm in a country known for its diverse cultural heritage and ancient traditions?" #1.13
# query_user = 'bollywood glamorous city'  # 0.99
# query_user = 'most modern city'  # 1.3454
# query_user = 'most historical city'  # 1.365
query_user = 'For tourism which city has cheap and best Attractions and Landmarks, Accommodation, Transportation, Dining and Cuisine, Events and Festivals, Safety and Security,\
                Weather and Climate, Language and Communication, Budget and Expenses, Local Tips and Recommendations'  # 1.32
search_vector = generate_user_query_embedding(query_user)
# print(len(search_vector))  # Print the length of the search vector

result = collection.search([search_vector], anns_field="embeddings", param=search_params, limit=2,
                           output_fields=["city_description"])

# print("result")
# print(result)

system_content = ""

for hits in result:
    for hit in hits:
        # print("hit")
        # print(hit)
        if hit.distance < 1.5:
            system_content += " \n\n\n " + hit.entity.get('city_description')

print('Final System Content...')
print(system_content)
