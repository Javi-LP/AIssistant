from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from AIssistant import init  # Asegúrate de importar tus funciones aquí

app = FastAPI()

# Inicializa tu modelo y cadena de QA
llm_chain = init()

# Modelo para la entrada
class Question(BaseModel):
    question: str

@app.post("/ask/")
def ask_question(item: Question):
    try:
        answer = llm_chain.invoke(item.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de QA. Usa el endpoint POST /ask/ para hacer preguntas. Si quieres saber"
                       "más, usa el endpoint /docs/ para ver la documentación de la API."}
