from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Define a Prompt Template
prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")

# 2. Initialize an LLM (e.g., OpenAI's GPT)
llm = ChatOpenAI(model="gpt-4o-mini")

# 3. Initialize an Output Parser
output_parser = StrOutputParser()

# 4. Chain them together using LCEL
chain = prompt | llm | output_parser

# 5. Invoke the chain
result = chain.invoke({"topic": "programming"})
print(result)