# Streaming và Structured Output với Thinking - Tóm tắt thay đổi

## Tổng quan
Đã thêm khả năng streaming với structured output và thinking process cho các Agent trong hệ thống HR-Agents.

## Các thay đổi chính

### 1. Backend - Schemas (`response_schemas.py`)
**File mới:** `src/jd_assistants/agent/response_schemas.py`

- Tạo Pydantic schemas cho structured outputs:
  - `JDAnalysisResponse`: Kết quả phân tích JD với thinking, overall_score, recommendations, improvements
  - `JDRewriteResponse`: Kết quả viết lại JD với thinking, rewritten_jd, key_changes
  - `JDGenerateResponse`: Kết quả tạo JD mới
  - `SalaryAssessmentResponse`: Đánh giá lương
- Mỗi schema có trường `thinking` (optional) để model có thể giải thích quá trình suy nghĩ

### 2. Inference Layer - ChatGroq (`inference/groq.py`)
**Thêm các phương thức:**

```python
def stream(input, **kwargs)  # Stream response tokens
async def astream(input, **kwargs)  # Async stream
def stream_structured(input, schema, **kwargs)  # Stream với structured output
async def astream_structured(input, schema, **kwargs)  # Async stream structured
```

### 3. Base Agent (`agent/base.py`)
**Thêm các phương thức:**

```python
def stream(input_message, **kwargs)  # Stream text responses
async def astream(input_message, **kwargs)  # Async stream
def invoke_structured(input_message, schema, **kwargs)  # Invoke với structured output
def stream_structured(input_message, schema, **kwargs)  # Stream structured - yields progress và final
async def astream_structured(input_message, schema, **kwargs)  # Async stream structured
```

Structured streaming yields:
- `{"type": "progress", "content": "...", "accumulated": "..."}` - Tiến trình
- `{"type": "final", "data": StructuredResponse}` - Kết quả cuối cùng
- `{"type": "error", "error": "...", "raw_content": "..."}` - Lỗi nếu có

### 4. JD Rewriter Agent (`agent/jd_rewriter.py`)
**Thêm các phương thức:**

```python
def analyze_jd_structured(jd_text) -> JDAnalysisResponse  # Phân tích với structured output
async def astream_analyze_jd(jd_text)  # Stream phân tích
def rewrite_jd_structured(jd_text, focus_areas) -> JDRewriteResponse  # Viết lại structured
async def astream_rewrite_jd(jd_text, focus_areas)  # Stream viết lại
def generate_jd(requirements) -> JDGenerateResponse  # Tạo JD mới
async def astream_generate_jd(requirements)  # Stream tạo JD
```

### 5. API Endpoints (`backend/api/v1/recruitment.py`)
**Thêm endpoints mới:**

#### `/api/v1/jd-ai/analyze-stream` (POST)
- Stream phân tích JD với Server-Sent Events (SSE)
- Response format: `text/event-stream`
- Gửi thinking progress và kết quả cuối

#### `/api/v1/jd-ai/rewrite-stream` (POST)
- Stream viết lại JD với SSE
- Gửi thinking progress và kết quả cuối với key_changes

**Event format:**
```json
{
  "type": "thinking|final|error",
  "content": "...",  // cho thinking
  "data": {...}      // cho final
}
```

### 6. Frontend API (`frontend/src/services/api.js`)
**Thêm functions:**

```javascript
jdAIAPI.analyzeStream(jdText, onProgress, onFinal, onError)
jdAIAPI.rewriteStream(jdText, onProgress, onFinal, onError)
```

- Sử dụng Fetch API với streaming
- Parse Server-Sent Events (SSE)
- Callbacks cho từng giai đoạn:
  - `onProgress(data)`: Cập nhật thinking process
  - `onFinal(data)`: Kết quả cuối cùng
  - `onError(error)`: Xử lý lỗi

### 7. UI Component (`frontend/src/pages/JDRewriting.jsx`)
**Thêm features:**

#### State Management:
```javascript
const [thinking, setThinking] = useState('');
const [showThinking, setShowThinking] = useState(false);
const [streamingProgress, setStreamingProgress] = useState('');
```

#### Thinking Process Panel:
- Hiển thị real-time AI thinking process
- Spinner khi đang xử lý
- Có thể ẩn/hiện panel
- Style đẹp với background color #f0f5ff
- Auto-scroll cho nội dung dài

#### Updated Handlers:
- `handleAnalyze()`: Sử dụng `analyzeStream()` thay vì `analyze()`
- `handleRewrite()`: Sử dụng `rewriteStream()` thay vì `rewrite()`
- Hiển thị key_changes trong notification khi rewrite xong

## Cách sử dụng

### Backend
```python
# Sử dụng structured output
result = agent.analyze_jd_structured(jd_text)
print(result.thinking)  # Quá trình suy nghĩ của AI
print(result.overall_score)

# Sử dụng streaming
async for chunk in agent.astream_analyze_jd(jd_text):
    if chunk["type"] == "progress":
        print(chunk["content"])  # In từng phần thinking
    elif chunk["type"] == "final":
        print(chunk["data"])  # Kết quả cuối
```

### Frontend
```javascript
// Stream analyze
await jdAIAPI.analyzeStream(
    jdText,
    (progress) => console.log('Thinking:', progress.accumulated),
    (final) => console.log('Result:', final),
    (error) => console.error('Error:', error)
);
```

## Lợi ích

1. **Real-time Feedback**: User thấy được AI đang "suy nghĩ" gì
2. **Better UX**: Không phải đợi lâu mà không biết gì đang xảy ra
3. **Transparency**: Hiểu được quá trình reasoning của AI
4. **Structured Output**: Dữ liệu có cấu trúc, dễ validate và xử lý
5. **Type Safety**: Pydantic schemas đảm bảo type safety

## Technical Notes

- SSE (Server-Sent Events) được sử dụng cho streaming
- Pydantic schemas validation tự động
- Graceful error handling ở mọi layer
- Backward compatible - các endpoint cũ vẫn hoạt động
- Models không support thinking vẫn hoạt động (thinking = null)

## Testing

Để test các tính năng mới:

1. Start backend: `uvicorn jd_assistants.api_main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Navigate to JD Rewriting page
4. Paste một JD và click "Analyze" hoặc "Rewrite"
5. Quan sát thinking process panel hiển thị real-time
