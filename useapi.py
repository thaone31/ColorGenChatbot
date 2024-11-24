from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import LlamaTokenizerFast, LlamaForCausalLM

app = FastAPI()

# Định nghĩa schema cho yêu cầu
class Query(BaseModel):
    user_input: str
    max_length: int = 200
    num_return_sequences: int = 1


model_name = "Eiramai/vinallama-2b-custom-color-v1"
tokenizer = 'custom_tokenizer.json'
model = LlamaForCausalLM.from_pretrained(model_name)

# Endpoint cho việc tương tác với mô hình
@app.post("/chat")
async def chat(query: Query):
    try:
        response = pipe(
            query.user_input,
            max_length=query.max_length,
            num_return_sequences=query.num_return_sequences
        )
        return {"response": [text["generated_text"] for text in response]}
    except Exception as e:
        print(f"Lỗi khi sinh văn bản: {e}")
        raise HTTPException(status_code=500, detail="Đã xảy ra lỗi khi sinh văn bản")