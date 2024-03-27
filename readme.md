
## CHAT BOT + CUSTOM DATA SET  (WITH & WITHOUT OPEN AI)

#### follow steps sequentially

```bash
git clone https://github.com/zohaibtariq/openai-chatbot-with-custom-data.git
```

```bash
cd openai-chatbot-with-custom-data
```

```bash
docker compose build --no-cache
```

```bash
docker compose up -d
```

#### navigate inside flask-chatbot-app container

```bash
docker exec -it flask-chatbot-app bash
```

---

#### MOST IMPORTANT STEP CHOOSE ANY 1

###### 1 - to run scripts of open AI code (if you have open api key)
```bash
cd openai
````

#### required for openai only, create .env file and insert openai key.  [Generate Openai API KEY](https://platform.openai.com/api-keys) 

```bash
OPENAI_API_KEY=""
```

###### 2 - to run scripts without open AI code (if you don't have open api key)
```bash
cd custom
````

---

#### 1 - Generate city embeddings and dump it to a JSON file

```bash
python3 cb_1_embedding_json_dump.py
```

#### 2 - Read JSON embeddings and dump it to Milvus Vector DB

```bash
python3 cb_2_milvus_embeddings_dump.py
```

#### 3 - Index & Load Milvus Data

```bash
python3 cb_3_milvus_index_load.py
```

#### 4 - Perform search over Milvus with embeddings

```bash
python3 cb_4_embeddings_milvus_search.py
```

#### 5 - Openai Chat Completions based on results

```bash
python3 cb_5_chat_completion.py
```


## Helpful Commands

#### to check active containers
```bash
docker ps
```

#### to check all active + inactive containers
```bash
docker ps -a
```

#### to check docker logs from host

```bash
docker logs flask-chatbot-app
```

#### ALERT use cautiously - It will delete all docker container images volumes
```bash
docker system prune -a
```