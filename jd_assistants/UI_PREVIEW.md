# UI Preview - Agent Configuration

## 📱 Giao diện trang Settings

### 1. Header Section
```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  ⚙️ Cấu hình hệ thống                                                     │
│  Quản lý API keys của các nhà cung cấp AI để sử dụng các tính năng       │
│  phân tích JD, viết lại JD, và đánh giá CV.                               │
│                                                                            │
│  ℹ️ Lưu ý quan trọng                                                      │
│  • API keys của bạn được lưu trữ an toàn và chỉ bạn mới có thể truy cập. │
│  • Mỗi nhà cung cấp có thể có nhiều keys, nhưng chỉ có một key hoạt động │
│    tại một thời điểm.                                                     │
│  • Bạn cần ít nhất một API key đang hoạt động để sử dụng các tính năng AI│
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 2. API Keys Management Card
```
┌────────────────────────────────────────────────────────────────────────────┐
│  🔑 Quản lý API Keys                           [+ Thêm API Key]           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓  │
│  ┃ Nhà cung cấp  ┃ Tên Key     ┃ Model                 ┃ API Key      ┃  │
│  ┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━┫  │
│  ┃ 🔑 OpenAI     ┃ Prod Key    ┃ [gpt-4-turbo]        ┃ sk-p...y123  ┃  │
│  ┃               ┃             ┃                       ┃              ┃  │
│  ┃               ┃             ┃                       ┃ ✓ Đang hoạt  ┃  │
│  ┃               ┃             ┃                       ┃   động       ┃  │
│  ┃               ┃             ┃                       ┃ 25/12/2025   ┃  │
│  ┃               ┃             ┃                       ┃ [Xóa]        ┃  │
│  ┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━┫  │
│  ┃ 🔑 Groq       ┃ Test Key    ┃ [llama-3.3-70b-      ┃ gsk-...456   ┃  │
│  ┃               ┃             ┃  versatile]           ┃              ┃  │
│  ┃               ┃             ┃                       ┃ ✓ Đang hoạt  ┃  │
│  ┃               ┃             ┃                       ┃   động       ┃  │
│  ┃               ┃             ┃                       ┃ 24/12/2025   ┃  │
│  ┃               ┃             ┃                       ┃ [Xóa]        ┃  │
│  ┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━┛  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 3. Add API Key Modal (Step by Step)

#### Step 1: Initial Modal
```
┌────────────────────────────────────────────────────────────┐
│  + Thêm API Key mới                                  [✕]  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Nhà cung cấp AI *                                         │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Chọn nhà cung cấp AI                              ▼ │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│                                                            │
│                                                            │
│  [Thêm Key]  [Hủy]                                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

#### Step 2: After Selecting Provider (e.g., OpenAI)
```
┌────────────────────────────────────────────────────────────┐
│  + Thêm API Key mới                                  [✕]  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Nhà cung cấp AI *                                         │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 🔑 OpenAI - OpenAI's GPT models                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │ ℹ️ Lấy API key từ OpenAI                          │   │
│  │                                                    │   │
│  │ Bạn có thể lấy API key tại:                        │   │
│  │ 🔗 https://platform.openai.com/api-keys           │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  Model * (?)                                               │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Chọn model AI                                     ▼ │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  [Thêm Key]  [Hủy]                                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

#### Step 3: Model Dropdown Expanded
```
┌────────────────────────────────────────────────────────────┐
│  + Thêm API Key mới                                  [✕]  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Nhà cung cấp AI *                                         │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 🔑 OpenAI - OpenAI's GPT models                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  Model * (?)                                               │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ gpt-4o                      [Mặc định]              │ │ ← Highlighted
│  ├──────────────────────────────────────────────────────┤ │
│  │ gpt-4-turbo                                         │ │
│  ├──────────────────────────────────────────────────────┤ │
│  │ gpt-4                                               │ │
│  ├──────────────────────────────────────────────────────┤ │
│  │ gpt-3.5-turbo                                       │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

#### Step 4: Complete Form
```
┌────────────────────────────────────────────────────────────┐
│  + Thêm API Key mới                                  [✕]  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Nhà cung cấp AI *                                         │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 🔑 OpenAI - OpenAI's GPT models                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │ ℹ️ Lấy API key từ OpenAI                          │   │
│  │ Bạn có thể lấy API key tại:                        │   │
│  │ 🔗 https://platform.openai.com/api-keys           │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  Model * (?)                                               │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ gpt-4-turbo                                         │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  Tên key (Tùy chọn) (?)                                    │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Production Key                                       │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  API Key *                                                 │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ •••••••••••••••••••••••••••••••••••••••••••   🔒   │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  [Thêm Key]  [Hủy]                                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 4. Supported Providers Section
```
┌────────────────────────────────────────────────────────────────────────────┐
│  ℹ️ Các nhà cung cấp được hỗ trợ                                          │
├────────────────────────────────────────────────────────────────────────────┤
│  Dưới đây là danh sách các nhà cung cấp AI được hệ thống hỗ trợ và các   │
│  models có sẵn.                                                            │
│                                                                            │
│  ┌───────────────────────────────┬───────────────────────────────┐        │
│  │ 🔑 OpenAI                     │ 🔑 Groq                      │        │
│  │                               │                               │        │
│  │ OpenAI's GPT models           │ Fast inference with Llama    │        │
│  │                               │ models                        │        │
│  │ Model mặc định:               │                               │        │
│  │ [gpt-4o]                      │ Model mặc định:               │        │
│  │                               │ [llama-3.3-70b-versatile]     │        │
│  │ Các models có sẵn:            │                               │        │
│  │ [gpt-4o] [gpt-4-turbo]        │ Các models có sẵn:            │        │
│  │ [gpt-4] [gpt-3.5-turbo]       │ [llama-3.3-70b-versatile]     │        │
│  │                               │ [llama-3.1-70b-versatile]     │        │
│  │ 🔗 Lấy API key                │ [mixtral-8x7b-32768]          │        │
│  │                               │                               │        │
│  │                               │ 🔗 Lấy API key                │        │
│  ├───────────────────────────────┼───────────────────────────────┤        │
│  │ 🔑 Google Gemini              │ 🔑 OpenRouter                │        │
│  │                               │                               │        │
│  │ Google's multimodal AI model  │ Access to multiple models    │        │
│  │                               │ via one API                   │        │
│  │ Model mặc định:               │                               │        │
│  │ [gemini-1.5-pro]              │ Model mặc định:               │        │
│  │                               │ [anthropic/claude-3.5-sonnet] │        │
│  │ Các models có sẵn:            │                               │        │
│  │ [gemini-1.5-pro]              │ Các models có sẵn:            │        │
│  │ [gemini-1.5-flash]            │ [anthropic/claude-3.5-sonnet] │        │
│  │ [gemini-pro]                  │ [openai/gpt-4-turbo]          │        │
│  │                               │ [google/gemini-pro]           │        │
│  │ 🔗 Lấy API key                │                               │        │
│  │                               │ 🔗 Lấy API key                │        │
│  └───────────────────────────────┴───────────────────────────────┘        │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

## 🎨 Color Scheme

- **Primary Blue** (#1890ff): Icons, links, provider names
- **Purple** (#722ed1): Model tags
- **Green** (#52c41a): Active status, default model tags
- **Orange** (#fa8c16): Warning messages
- **Blue** (#1890ff): API key previews
- **Grey** (#999): Secondary text

## 📱 Responsive Design

Trên mobile (< 768px):
- Provider cards stack vertically (100% width each)
- Table scrolls horizontally
- Modal takes full width with padding

## ✨ Interactive Elements

1. **Hover Effects**:
   - Buttons: Slight background color change
   - Table rows: Light grey background on hover
   - Links: Underline appears

2. **Click Animations**:
   - Button press: Slight scale down
   - Modal open/close: Fade + slide animation

3. **Form Validation**:
   - Real-time validation on blur
   - Red border + error message for invalid fields
   - Green checkmark for valid fields

## 🔔 Notifications

Success: `🎉 API key đã được thêm thành công!`
Error: `❌ Không thể thêm API key`
Warning: `⚠️ Chưa có API key nào`
Info: `ℹ️ Lưu ý quan trọng`
