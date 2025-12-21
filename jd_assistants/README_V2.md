# HR-Agents - Hệ Thống Tuyển Dụng Thông Minh

Hệ thống HR với AI hỗ trợ phân tích CV, đánh giá ứng viên, và tối ưu hóa Job Description.

## 🎯 Tính Năng Chính

### 1. Phân Tích CV
- Upload và xử lý CV định dạng PDF
- Trích xuất thông tin tự động bằng LLM
- Lưu trữ thông tin ứng viên vào ClickHouse
- Tóm tắt thông tin ứng viên

### 2. Đánh Giá Ứng Viên
- So khớp CV với Job Description
- Tính điểm tự động (0-100)
- Giải thích lý do chấm điểm
- Lưu lịch sử đánh giá

### 3. Quản Lý Job Description
- Tạo JD mới từ requirements
- Phân tích và đánh giá chất lượng JD
- Viết lại JD chuyên nghiệp hơn
- So sánh nhiều phiên bản JD

### 4. Multi-LLM Provider Support
- **Groq**: Llama models với tốc độ cao
- **OpenRouter**: Truy cập nhiều models qua một API
- **Google Gemini**: Multimodal AI
- **OpenAI GPT**: GPT-4o, GPT-4 Turbo

### 5. API Key Management
- Lưu API keys trong database (ClickHouse)
- Quản lý keys qua Web UI
- Hỗ trợ nhiều providers cùng lúc
- Tự động chọn provider phù hợp

## 🏗️ Kiến Trúc

```
┌─────────────┐
│React Frontend│ ← Web UI
│  (Ant Design)│
└──────┬───────┘
       │
┌──────┴────────────────────────┐
│   FastAPI Backend             │
│  - CV Processing              │
│  - Candidate Scoring          │
│  - JD Analysis & Rewriting    │
│  - API Key Management         │
└───────┬───────────────────────┘
        │
   ┌────┴──────┬─────────┐
   │           │         │
┌──┴────┐  ┌──┴───┐  ┌─┴────┐
│ClickH.│  │Redis │  │ LLM  │
│  DB   │  │Cache │  │Agents│
└───────┘  └──────┘  └──────┘
```

## 🚀 Cài Đặt Nhanh

### Prerequisites
- Docker & docker-compose
- Python 3.10+
- Node.js 18+ (cho frontend)

### 1. Clone Repository
```bash
cd /home/baobao/Projects/HR-Agents/jd_assistants
```

### 2. Cấu Hình Environment
```bash
cp .env.example .env
# Edit .env và thêm thông tin ClickHouse
```

### 3. Khởi Động Services
```bash
# Start ClickHouse và Redis
docker-compose up -d clickhouse redis

# Khởi tạo database
python init_clickhouse.py

# Start application
docker-compose up -d app
```

### 4. Truy Cập Ứng Dụng
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000 (dev mode)

### 5. Login & Setup
```
Email: admin@hr-system.com
Password: admin123

⚠️ Đổi password sau khi login lần đầu!
```

### 6. Thêm API Keys
1. Vào **Settings** → **LLM API Keys**
2. Click **Add API Key**
3. Chọn provider (Groq, OpenRouter, Gemini, OpenAI)
4. Nhập API key
5. Save

## 📝 Kịch Bản Sử Dụng

### Kịch Bản 1: Phân Tích CV

1. **Upload CV**
   - Vào trang **Candidates**
   - Click **Upload CVs**
   - Chọn file PDF
   - Hệ thống tự động extract thông tin

2. **Extract Thông Tin**
   - LLM đọc CV và trích xuất:
     - Personal info (name, email, phone, etc.)
     - Education history
     - Work experience
     - Skills
   
3. **Lưu vào ClickHouse**
   - Dữ liệu được chuẩn hóa
   - Lưu vào bảng `candidates`

4. **Đánh Giá**
   - Chọn JD để match
   - Click **Score All Candidates**
   - Xem kết quả ranking

### Kịch Bản 2: Viết Job Description

1. **Tạo JD Mới**
   - Vào **JD Generator**
   - Nhập:
     - Position title
     - Experience required
     - Skills
     - Salary range
   - Click **Generate**
   
2. **Phân Tích JD**
   - Vào **JD Analysis** (mới)
   - Paste JD text
   - Click **Analyze**
   - Xem:
     - Overall score (0-100)
     - Recommendations
     - Improvements by section

3. **Viết Lại JD**
   - Vào **JD Rewriting**
   - Paste JD cũ
   - Click **Rewrite**
   - So sánh original vs rewritten

### Kịch Bản 3: Đánh Giá Ứng Viên

1. **Chọn JD Active**
   - Vào **Job Descriptions**
   - Click **Activate** trên JD muốn dùng

2. **Score Candidates**
   - Vào **CV-JD Matching**
   - Click **Score All Candidates**
   - Agent sẽ:
     - Đọc từng CV
     - So khớp với JD
     - Tính điểm 0-100
     - Giải thích lý do

3. **Xem Kết Quả**
   - Danh sách ứng viên được rank
   - Score cao → thấp
   - Lý do chi tiết cho mỗi điểm

## 🔧 Cấu Hình Chi Tiết

### ClickHouse Configuration
```env
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=your_password
CLICKHOUSE_DATABASE=hr_system
```

### LLM Providers
```env
# Default provider
DEFAULT_LLM_PROVIDER=groq

# Optional: Set API keys in env (or use UI)
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-...
GOOGLE_API_KEY=AIza...
OPENAI_API_KEY=sk-...
```

### Database Schema

**Tables:**
- `users`: User accounts
- `api_keys`: LLM API keys per user
- `candidates`: Candidate profiles
- `job_descriptions`: Job postings
- `candidate_scores`: Scoring results
- `jd_analysis`: JD analysis history

## 🛠️ Development

### Backend Development
```bash
# Install dependencies
pip install -e .

# Run locally
python -m jd_assistants.api_main
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Run Tests
```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

## 📚 API Documentation

Sau khi start application, truy cập:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

**Authentication:**
- POST `/api/v1/auth/register` - Đăng ký
- POST `/api/v1/auth/login` - Đăng nhập
- GET `/api/v1/auth/me` - Thông tin user

**API Keys:**
- GET `/api/v1/api-keys/` - List keys
- POST `/api/v1/api-keys/` - Add key
- DELETE `/api/v1/api-keys/{id}` - Delete key
- GET `/api/v1/api-keys/providers/list` - List providers

**Candidates:**
- POST `/api/v1/candidates/upload-cv` - Upload CV
- GET `/api/v1/candidates` - List candidates
- GET `/api/v1/candidates/{id}` - Get candidate
- DELETE `/api/v1/candidates/{id}` - Delete candidate

**Job Descriptions:**
- GET `/api/v1/job-descriptions` - List JDs
- POST `/api/v1/job-descriptions` - Create JD
- PUT `/api/v1/job-descriptions/{id}/activate` - Set active

**JD AI:**
- POST `/api/v1/jd-ai/analyze` - Analyze JD
- POST `/api/v1/jd-ai/rewrite` - Rewrite JD
- POST `/api/v1/jd-ai/generate` - Generate JD

**Scoring:**
- POST `/api/v1/scoring/score-all` - Score all candidates
- GET `/api/v1/scoring/scores` - Get scores

## 🐛 Troubleshooting

### ClickHouse Connection Error
```bash
# Check ClickHouse is running
docker ps | grep clickhouse

# Check connection
docker exec -it hr_clickhouse clickhouse-client
```

### LLM API Error
```bash
# Check API keys in database
# Go to Settings → API Keys
# Verify key is active
```

### Frontend Not Loading
```bash
# Rebuild frontend
cd frontend
npm run build

# Check static files
ls -la /app/static
```

## 📄 License

MIT License

## 👥 Contributors

- BaoBao112233

## 🔗 Links

- GitHub: https://github.com/BaoBao112233/HR-Agents
- Issues: https://github.com/BaoBao112233/HR-Agents/issues
