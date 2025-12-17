# Hướng dẫn sử dụng tính năng Streaming với Thinking

## 🎯 Tổng quan

Hệ thống đã được nâng cấp với các tính năng:
1. **Streaming responses** - Phản hồi theo thời gian thực
2. **Structured outputs** - Đầu ra có cấu trúc với Pydantic schemas
3. **Thinking process** - Hiển thị quá trình suy nghĩ của AI
4. **Real-time UI updates** - Giao diện cập nhật real-time

## 📦 Files đã thay đổi

### Backend
1. `src/jd_assistants/agent/response_schemas.py` - **MỚI** - Pydantic schemas
2. `src/jd_assistants/inference/groq.py` - Thêm streaming methods
3. `src/jd_assistants/agent/base.py` - Thêm stream và structured methods
4. `src/jd_assistants/agent/jd_rewriter.py` - Thêm streaming cho JD operations
5. `src/jd_assistants/backend/api/v1/recruitment.py` - Thêm streaming endpoints

### Frontend
6. `frontend/src/services/api.js` - Thêm streaming API functions
7. `frontend/src/pages/JDRewriting.jsx` - UI với thinking panel

## 🚀 Cách sử dụng

### 1. Trong Python Code (Backend)

#### Streaming với Structured Output
```python
from jd_assistants.agent.jd_rewriter import JDRewriterAgent
from jd_assistants.inference.groq import ChatGroq

llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key)
agent = JDRewriterAgent(llm)

# Stream analysis
async for chunk in agent.astream_analyze_jd(jd_text):
    if chunk["type"] == "progress":
        # Thinking process - in ra từng phần
        print(chunk["content"], end="", flush=True)
    elif chunk["type"] == "final":
        # Kết quả cuối cùng
        result = chunk["data"]
        print(f"Score: {result.overall_score}")
        print(f"Thinking: {result.thinking}")
```

#### Non-streaming với Structured Output
```python
# Phân tích không stream
result = agent.analyze_jd_structured(jd_text)
print(f"Thinking: {result.thinking}")
print(f"Score: {result.overall_score}")
print(f"Recommendations: {result.key_recommendations}")

# Viết lại không stream
result = agent.rewrite_jd_structured(jd_text)
print(f"Thinking: {result.thinking}")
print(f"Rewritten: {result.rewritten_jd}")
print(f"Changes: {result.key_changes}")
```

### 2. Trong API Endpoints

#### Streaming Endpoints (SSE)
```bash
# Analyze với streaming
curl -X POST http://localhost:8000/api/v1/jd-ai/analyze-stream \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "jd_text=Your job description here"

# Rewrite với streaming
curl -X POST http://localhost:8000/api/v1/jd-ai/rewrite-stream \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "jd_text=Your job description here"
```

Response format (SSE):
```
data: {"type": "thinking", "content": "Analyzing...", "accumulated": "..."}
data: {"type": "thinking", "content": " the JD", "accumulated": "Analyzing the JD"}
data: {"type": "final", "data": {...}}
```

#### Non-streaming Endpoints (vẫn hoạt động)
```bash
# Analyze không streaming
curl -X POST http://localhost:8000/api/v1/jd-ai/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "jd_text=Your job description here"
```

### 3. Trong Frontend

#### Sử dụng API Service
```javascript
import { jdAIAPI } from '../services/api';

// Stream analyze
await jdAIAPI.analyzeStream(
    jdText,
    // onProgress callback
    (progressData) => {
        console.log('Thinking:', progressData.accumulated);
        setThinkingText(progressData.accumulated);
    },
    // onFinal callback
    (finalData) => {
        console.log('Result:', finalData);
        setAnalysis(finalData);
        setThinking(finalData.thinking);
    },
    // onError callback
    (error) => {
        console.error('Error:', error);
    }
);

// Stream rewrite
await jdAIAPI.rewriteStream(
    jdText,
    (progress) => setThinkingText(progress.accumulated),
    (final) => {
        setRewritten(final.rewritten_jd);
        setThinking(final.thinking);
        console.log('Changes:', final.key_changes);
    },
    (error) => console.error(error)
);
```

#### UI Component State
```javascript
const [thinking, setThinking] = useState('');
const [showThinking, setShowThinking] = useState(true);
const [streamingProgress, setStreamingProgress] = useState('');
const [analyzing, setAnalyzing] = useState(false);
```

## 🎨 UI Features

### Thinking Process Panel
- Hiển thị tự động khi bắt đầu analyze/rewrite
- Có spinner khi đang streaming
- Hiển thị accumulated text trong real-time
- Có thể ẩn/hiện bằng nút "Hide"
- Background màu xanh nhạt (#f0f5ff)

### Analysis Results
- Overall score với color-coding (green >= 70, yellow < 70)
- Key recommendations dạng list
- Improvements theo từng section với reason

### Rewritten JD
- Hiển thị full JD đã viết lại
- Có nút "Copy to Clipboard"
- Notification hiển thị key_changes

## 📊 Schemas

### JDAnalysisResponse
```python
{
    "thinking": "Quá trình suy nghĩ của AI...",
    "overall_score": 75,
    "key_recommendations": [
        "Add company benefits",
        "Use more inclusive language"
    ],
    "improvements": [
        {
            "section": "Job Title",
            "original": "Software Engineer",
            "improved": "Senior Software Engineer - Full Stack",
            "reason": "More specific and attractive"
        }
    ]
}
```

### JDRewriteResponse
```python
{
    "thinking": "Analyzing the JD structure...",
    "rewritten_jd": "Full rewritten job description text",
    "key_changes": [
        "Restructured into clear sections",
        "Added benefits and growth opportunities",
        "Improved technical requirements clarity"
    ]
}
```

## 🧪 Testing

Chạy test script:
```bash
cd /home/baobao/Projects/HR-Agents/jd_assistants
python test_streaming.py
```

Test trong UI:
1. Start backend: `uvicorn jd_assistants.api_main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Mở http://localhost:5173/jd-rewriting
4. Paste một JD và click "Analyze" hoặc "Rewrite"
5. Xem thinking panel hiển thị real-time

## 🔧 Troubleshooting

### Backend không stream
- Kiểm tra GROQ_API_KEY đã set chưa
- Model llama-3.3-70b-versatile có hỗ trợ streaming
- Check logs: `tail -f uvicorn.log`

### Frontend không hiển thị thinking
- Mở Developer Console (F12) xem có error không
- Check Network tab xem SSE stream có data không
- Verify token authentication

### Parsing errors
- Model có thể không return đúng JSON format
- Check raw_content trong error response
- Có thể cần adjust system_prompt

## 💡 Tips

1. **Thinking field**: Chỉ xuất hiện nếu model hỗ trợ. Groq models thường hỗ trợ tốt.

2. **Streaming performance**: SSE thường nhanh hơn polling. Buffer size có thể adjust.

3. **Error handling**: Luôn có fallback - nếu stream fail, có thể retry với non-stream.

4. **User experience**: Cho user biết AI đang "suy nghĩ" giúp UX tốt hơn rất nhiều.

5. **Testing**: Test với nhiều loại JD khác nhau (ngắn, dài, nhiều section, ít section).

## 📚 Tài liệu thêm

- Pydantic docs: https://docs.pydantic.dev/
- Server-Sent Events: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- LangChain streaming: https://python.langchain.com/docs/expression_language/streaming
- FastAPI streaming: https://fastapi.tiangolo.com/advanced/streaming-response/
