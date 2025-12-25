# Hướng dẫn cấu hình Agent Configuration

## Tính năng mới được thêm vào

### 1. Chọn Model AI khi thêm API Key

Giờ đây khi thêm API key cho các nhà cung cấp AI, bạn có thể:
- ✅ Chọn nhà cung cấp (OpenAI, Groq, Gemini, OpenRouter)
- ✅ Nhập API key
- ✅ **Chọn model cụ thể** mà bạn muốn sử dụng

### 2. Migration Database

Nếu bạn đã có database cũ, cần chạy migration để thêm cột `model`:

```bash
cd /home/baobao/Projects/HR-Agents/jd_assistants
python migrate_add_model_column.py
```

### 3. Các thay đổi trong code

#### Backend Changes:
- **clickhouse_db.py**: Thêm cột `model` vào bảng `api_keys`
- **api_keys.py**: Cập nhật API endpoints để hỗ trợ trường `model`

#### Frontend Changes:
- **Settings.jsx**: 
  - Thêm dropdown để chọn model khi thêm API key
  - Hiển thị model đã chọn trong bảng danh sách keys
  - Model được hiển thị với tag màu tím
  - Tag "Mặc định" cho model mặc định của provider

### 4. Sử dụng tính năng

1. Vào trang **Settings** (⚙️ Cấu hình hệ thống)
2. Click **"Thêm API Key"**
3. Chọn nhà cung cấp (ví dụ: OpenAI, Groq)
4. Hệ thống sẽ hiển thị link để lấy API key
5. **Chọn model** từ danh sách models có sẵn của nhà cung cấp đó
6. Nhập API key
7. (Tùy chọn) Đặt tên cho key
8. Click **"Thêm Key"**

### 5. Models được hỗ trợ

#### OpenAI:
- gpt-4o (mặc định)
- gpt-4-turbo
- gpt-4
- gpt-3.5-turbo

#### Groq:
- llama-3.3-70b-versatile (mặc định)
- llama-3.1-70b-versatile
- mixtral-8x7b-32768

#### Google Gemini:
- gemini-1.5-pro (mặc định)
- gemini-1.5-flash
- gemini-pro

#### OpenRouter:
- anthropic/claude-3.5-sonnet (mặc định)
- openai/gpt-4-turbo
- google/gemini-pro

### 6. Lưu ý

- Model đã chọn sẽ được sử dụng cho tất cả các tính năng AI (phân tích JD, viết lại JD, đánh giá CV)
- Bạn có thể có nhiều keys cho cùng một provider nhưng với các models khác nhau
- Model mặc định của provider sẽ được đánh dấu bằng tag màu xanh lá

### 7. Troubleshooting

**Q: Không thấy dropdown chọn model?**
A: Hãy chắc chắn bạn đã chọn nhà cung cấp trước. Dropdown model chỉ hiện ra sau khi chọn provider.

**Q: Làm sao cập nhật model cho key đã tồn tại?**
A: Hiện tại cần xóa key cũ và thêm lại với model mới. Tính năng edit sẽ được thêm trong phiên bản sau.

**Q: Database có bị ảnh hưởng?**
A: Nếu bạn đã có database cũ, chạy script migration `migrate_add_model_column.py` để thêm cột `model`. Các key cũ sẽ có model là empty string.
