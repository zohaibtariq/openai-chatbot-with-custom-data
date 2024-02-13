import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a dictionary containing environment variables
envs = os.environ

client = OpenAI(
    api_key=envs.get("OPENAI_API_KEY")
)

# query_user = "Explain Solar system in summarised way as short as possible."
query_user = "Which city has presence of most bollywood celebrities?"

# print('Query user...')
# print(query_user)

system_content = f"System Content: \"Mumbai is a city in India.\
            It is known for its Gateway of India, Elephanta Caves, Marine Drive and specialty food like Pav Bhaji, \
            Vada Pav. The temperature ranges from 17 to 32 degrees Celsius,\
            Mumbai, India's bustling financial hub, is a tapestry of colonial history and Bollywood glam. \
            The Gateway of India, Elephanta Caves' ancient marvels, and the scenic Marine Drive showcase \
            Mumbai's diversity. Relish street food delights like pav bhaji and the iconic vada pav.\""

prompt = f"Prompt: \"If user question is not related to the system content as mentioned above or system content is empty \
            please Reply with *I don't know, please ask some relevant question* plus try to keep answer as short as possible.\""

system_prompt_content = system_content + " \n " + prompt

# print('Final System With Prompt Content...')
# print(system_prompt_content)

# prompt = f"The user asked: '{query_user}'. The system content is: '{system_content}'. If the user question is not related to the system content or the system content is empty,
# please Reply with *I don't know, please ask some relevant question* and try to keep the answer as short as possible."

json_input = {
    "model": "gpt-3.5-turbo-0125",  # text-davinci-002
    "messages": [
        {"role": "user", "content": query_user},
        {"role": "system", "content": system_prompt_content}
    ],
    # "stream": True,
    # "response_format": {"type": "json_object"},
}

# stream = client.chat.completions.create(**json_input)
response = client.chat.completions.create(**json_input)

# for chunk in stream:
#     print("chunk")
#     print(chunk)
#     print(chunk.choices[0].delta.content or "", end="")

# print("Response from OpenAI:", response.choices[0].text.strip())
print("Response from OpenAI:", response.choices[0].message.content)
