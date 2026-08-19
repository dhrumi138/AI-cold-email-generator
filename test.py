from groq import Groq
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model_name = "openai/gpt-oss-20b",
    temperature =0,
    api_key=os.getenv("GROQ_API_KEY")
)

response = llm.invoke("Who was the first person to land on the moon? answer in one sentence.")

print(response.content)