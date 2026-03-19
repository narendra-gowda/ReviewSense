import asyncio
from fastapi import FastAPI, HTTPException
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from agent.schema import QueryInput
from agent.setup import agent
from config import LLM
from template.common import product_expert, general_chat
from vectorstore.retriever_factory import setup_and_initialise_vector_db

model = OllamaLLM(model=LLM, temperature=0)

template = product_expert
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

template2 = general_chat
prompt2 = ChatPromptTemplate.from_template(template2)
chain2 = prompt2 | model

is_ready = False
app = FastAPI()

@app.on_event("startup")
async def startup():
    global is_ready
    try:
        print(f"\n♻️ Initialising vector database...\n")
        await asyncio.to_thread(setup_and_initialise_vector_db)
        is_ready = True
        print("\n✅ Vector database initialised\n")
    except Exception as e:
        print(f"Vector database initialisation failed: {e}")
        is_ready = False

def run_query(input_data: QueryInput):
    docs = agent.invoke(input_data.query)
    if not docs['output']:
        docs['output'] = 'Sorry, no reviews found'
    print(docs['output'])
    if isinstance(docs['output'], bool) and docs['output'] == True:
        response = chain2.invoke({"question": docs['input']})
    else:
        response = chain.invoke({"reviews": docs['output'], "question": input_data.query})
    return response

@app.get("/health")
async def health():
    return {"status": "ok" if is_ready else "down"}

@app.post("/ask")
async def ask(input_data: QueryInput):
    if not is_ready:
        raise HTTPException(status_code=503, detail="Vector database not initialised, try again later")

    print(f"User query: {input_data}")
    response = run_query(input_data)
    return {
        "content": response,
        "role": "assistant"
    }