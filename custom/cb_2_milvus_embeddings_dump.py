import json
import numpy as np
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, list_collections

# Connect to Milvus
# connections.connect(host='0.0.0.0', port='19530')
# connections.connect("test", host="standalone", port="19530")
# connections.connect(user='', password='')
connections.connect(host='standalone', port='19530')

# Define the collection name and schema
collection_name = 'cities_embeddings_custom'
field_id = FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True)
field_embeddings = FieldSchema(name='embeddings', dtype=DataType.FLOAT_VECTOR, dim=768)
field_city_description = FieldSchema(name='city_description', dtype=DataType.VARCHAR, max_length=1500)

schema = CollectionSchema(fields=[field_id, field_embeddings, field_city_description])

# Check if the collection already exists, if not create it
if collection_name not in list_collections():
    collection = Collection(name=collection_name, schema=schema)
    print(f"CUSTOM - Collection '{collection_name}' created successfully!")
else:
    collection = Collection(name=collection_name)

# Load embeddings from the JSON file
with open('cities_embeddings.json', 'r') as file:
    embeddings_data = json.load(file)

# Insert data into Milvus collection
for i, doc in enumerate(embeddings_data, start=1):
    try:
        embeddings = np.array(doc['embeddings'], dtype=np.float32)
        city_description = doc['city_description']

        # Construct entity
        entity = {
            'embeddings': embeddings.tolist(),
            'city_description': city_description
        }

        # Insert entity into Milvus collection
        collection.insert([entity])
        print(f"CUSTOM - Document {i} inserted successfully.")
    except Exception as e:
        print(f"CUSTOM - Error inserting document {i}: {e}")

print("CUSTOM - Data insertion completed.")