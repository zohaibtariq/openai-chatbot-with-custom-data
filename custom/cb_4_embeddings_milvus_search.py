import os
from dotenv import load_dotenv
from pymilvus import connections, Collection
from transformers import BertModel, BertTokenizer
import torch

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'  # You can change this to other BERT models if needed
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Load environment variables from .env file
load_dotenv()

# Create a dictionary containing environment variables
envs = os.environ

# Connect to Milvus
connections.connect(host='standalone', port='19530')

collection_name = 'cities_embeddings_custom'
collection = Collection(name=collection_name)


def generate_user_query_embedding(query):
    inputs = tokenizer(query, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze(0).numpy()


print("\n\n\nCUSTOM - Start searching based on vector similarity")

search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 10},
}

# best distance for related queries is 1.4 or 1.5 (means less than 1.5 or 1.4 can be considered as related)

# UNRELATED
# query_user = "What are some emerging trends in sustainable architecture?"  # 65
# query_user = "Can you explain the process of quantum entanglement in layman's terms?"  # 76
# query_user = "How does the human brain process abstract concepts like creativity and imagination?"  # 68
# query_user = "What are some potential applications of blockchain technology beyond cryptocurrency?" # 53
# query_user = "Can you discuss the impact of climate change on biodiversity in marine ecosystems?" # 55
# query_user = "Explain Solar system in summarised way as short as possible."  # 58

# RELATED
# query_user = "Where to go for jubilant vacations?"  # 61
# query_user = "Can you mention a popular pastry often associated with French cuisine?" # 47
# query_user = "Where might one find beautiful coastal landscapes and architectural marvels in a country known for its diverse wildlife?"  # 36
# query_user = "Which city is famed for its lively music, colorful festivals, and vibrant street culture in a South American nation celebrated for its rainforests and soccer prowess?"  # 26
# query_user = "What is the political and cultural capital of a European country known for its engineering prowess, beer gardens, and historical significance?"  # 35
# query_user = "Can you identify a prominent clock tower that is a symbol of national pride and heritage in a country known for its monarchy and tea culture?"  # 30
# query_user = "Which dish, known for its crispy texture and savory flavors, is a staple in a country with a rich history of martial arts and calligraphy?"  # 28
# query_user = "Where might one explore ancient ruins and archaeological wonders in a nation renowned for its mariachi music, spicy cuisine, and colorful festivals?"  # 31
# query_user = "Which city is famous for its bustling film industry, vibrant nightlife, and coastal charm in a country known for its diverse cultural heritage and ancient traditions?"  # 28
query_user = 'bollywood glamorous city'  # 50
# query_user = 'most modern city'  # 76
# query_user = 'most historical city'  # 87
# query_user = 'For tourism which city has cheap and best Attractions and Landmarks, Accommodation, Transportation, Dining and Cuisine, Events and Festivals, Safety and Security,\
#                 Weather and Climate, Language and Communication, Budget and Expenses, Local Tips and Recommendations'  # 39
search_vector = generate_user_query_embedding(query_user)
# print(len(search_vector))  # Print the length of the search vector

result = collection.search([search_vector], anns_field="embeddings", param=search_params, limit=1,
                           output_fields=["city_description"])

print("result")
print(result)

system_content = ""

for hits in result:
    for hit in hits:
        # print("hit")
        # print(hit.distance)
        # if hit.distance <= 50:
        system_content += " \n\n\nScore: " + str(hit.distance) + "\n\nContent: \n\n" + hit.entity.get('city_description')

print('\n\nCUSTOM - Final System Content...')
print(system_content)
