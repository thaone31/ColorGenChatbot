from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import nltk

# Tải các tài nguyên của nltk
nltk.download('punkt')

app = FastAPI()

# Cấu hình CORS để hỗ trợ giao tiếp với frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # Thay bằng domain frontend của bạn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = pipeline('text-generation', model='Eiramai/vinallama-2b-custom-color-v2')

# Định nghĩa API request/response
class QueryRequest(BaseModel):
    input_text: str

@app.post("/api/generate-color")
async def generate_color(request: QueryRequest):
    try:
        # Cải thiện prompt để tránh lặp lại câu hỏi
        enhanced_input = (
            f"Đưa ra các gợi ý màu sắc dựa trên yêu cầu: {request.input_text}. "
            "Trả lời rõ ràng và không lặp lại câu hỏi, tập trung vào gợi ý màu sắc cụ thể."
        )

        # Sử dụng model để trả về kết quả
        result = model(enhanced_input, max_length=100, truncation=True, num_return_sequences=1)
        generated_text = result[0]["generated_text"]

        # Xử lý chuỗi để loại bỏ phần lặp
        sentences = nltk.sent_tokenize(generated_text)  # Tách thành danh sách các câu
        unique_sentences = list(dict.fromkeys(sentences))  # Loại bỏ các câu trùng lặp
        cleaned_text = " ".join(unique_sentences)  # Ghép lại thành một chuỗi

        # Trả về kết quả đã xử lý
        return {"result": cleaned_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

