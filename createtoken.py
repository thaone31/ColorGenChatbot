from tokenizers import Tokenizer, models, pre_tokenizers, trainers

# Khởi tạo tokenizer từ mô hình BPE
tokenizer = Tokenizer(models.BPE())

# Cấu hình pre-tokenizer (chia câu thành các token cơ bản)
tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

# Đảm bảo bạn có tệp văn bản huấn luyện
train_files = ["Palette_Data.txt"]  # Thay đổi nếu tệp huấn luyện của bạn có tên khác

# Huấn luyện tokenizer
trainer = trainers.BpeTrainer(vocab_size=46306, min_frequency=2, show_progress=True)
tokenizer.train(files=train_files, trainer=trainer)

# Lưu tokenizer đã huấn luyện
tokenizer.save("custom_tokenizer.json")

# Kiểm tra tokenizer
encoded = tokenizer.encode("Xin chào, thế giới!")
print(encoded.tokens)
