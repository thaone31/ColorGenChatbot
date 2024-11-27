from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc chỉ định chính xác domain của frontend, ví dụ: ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load model của bạn
model = pipeline('text-generation', model='Eiramai/vinallama-2b-custom-color-v2')

# Định nghĩa API request/response
class QueryRequest(BaseModel):
    input_text: str

@app.post("/api/generate-color")
async def generate_color(request: QueryRequest):
    try:
        result = model(request.input_text, max_length=100, truncation=True, num_return_sequences=1)
        return {"result": result[0]["generated_text"]}  # Định dạng JSON phù hợp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


