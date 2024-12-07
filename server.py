from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc domain của frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = pipeline('text-generation', model='Eiramai/vinallama-2b-custom-color-v2')

# Định nghĩa API request/response
class QueryRequest(BaseModel):
    input_text: str

# Prompt để định hướng câu trả lời của model
PROMPT = (
    "Bạn là chuyên gia AI tư vấn màu sắc và phối màu bằng tiếng Việt. Bạn là chuyên gia về cách chọn màu sắc phù hợp với chủ đề đã cho. "
    "Hãy trả lời rõ ràng, đúng trọng tâm, ngắn gọn và đầy đủ câu"
)


@app.post("/api/generate-color")
async def generate_color(request: QueryRequest):
    try:
        # Xây dựng prompt với nội dung câu hỏi
        prompt_with_input = PROMPT.format(request=request) + f"Câu hỏi: {request.input_text}\nTrả lời:"
        print("Prompt Sent to Model:", prompt_with_input)


        # Gửi câu hỏi kèm prompt đến model
        result = model(
            prompt_with_input,
            max_length=100,  # Tăng độ dài để tránh bị ngắt giữa chừng
            truncation=True,
            num_return_sequences=1,
            do_sample=True,  # Sampling để tránh lặp lại
            top_p=0.75,       # Giữ các token xác suất cao nhất
            temperature=0.7, # Tăng tính tự nhiên
            repetition_penalty=1.5  # Phạt nặng các nội dung lặp
        )
        
        # Lấy nội dung sau phần "Trả lời:"
        response_text = result[0]["generated_text"]
        
        # Loại bỏ phần prompt và giữ phần trả lời chính
        if "Trả lời:" in response_text:
            response_text = response_text.split("Trả lời:")[1].strip()

        # Xóa nội dung lặp (nếu có)
        unique_sentences = []
        for sentence in response_text.split(". "):  # Tách câu
            if sentence not in unique_sentences:
                unique_sentences.append(sentence)
        cleaned_text = ". ".join(unique_sentences)  # Ghép lại

        # Trả về kết quả cho người dùng
        return {"result": cleaned_text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
