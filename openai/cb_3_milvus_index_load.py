from pymilvus import connections, Collection

# Connect to Milvus
connections.connect(host='standalone', port='19530')

collection_name = 'cities_embeddings'
collection = Collection(name=collection_name)
collection.flush()
print(f"Number of entities in Milvus: {collection.num_entities}")

print("Start Creating index IVF_FLAT")
index = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 1536},
}

collection.create_index("embeddings", index)

collection.load()

print("Milvus data loaded")