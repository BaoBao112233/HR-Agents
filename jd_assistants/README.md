# HR Assistants Crew

Chào mừng bạn đến với dự án HR Assistants Crew, Tôi là Nguyễn Gia Bảo, dự án được phát triển dựa trên framwork [crewAI](https://crewai.com). Framework này được thiết kế để giúp Dev thiết lập một hệ thống AI đa tác nhân một cách dễ dàng, tận dụng khung công tác mạnh mẽ và linh hoạt mà crewAI cung cấp. Mục tiêu của CrewAI là cho phép các tác nhân của bạn hợp tác hiệu quả trong các nhiệm vụ phức tạp, tối đa hóa trí tuệ và khả năng tập thể của chúng.

## Cài đặt

Đảm bảo rằng cài đặt đúng Python >=3.10 <=3.13 trên hệ thống của mình. Dự án này sử dụng [UV](https://docs.astral.sh/uv/) để quản lý phụ thuộc và xử lý gói, mang đến trải nghiệm thiết lập và thực thi liền mạch.

Đầu tiên, nếu bạn chưa cài đặt, hãy cài đặt uv:

```bash
pip install uv
```

Tiếp theo, điều hướng đến thư mục dự án của bạn và cài đặt các phụ thuộc:

(Tùy chọn) Khóa các phụ thuộc và cài đặt chúng bằng cách sử dụng lệnh CLI:

```bash
crewai install
```

### Tùy chỉnh

**Thêm `OPENAI_API_KEY` của bạn vào file `.env`**

- Chỉnh sửa `src/jd_assistants/crews/{tên crew}/config/agents.yaml` để định nghĩa các tác nhân của bạn
- Chỉnh sửa `src/jd_assistants/crews/{tên crew}/config/tasks.yaml` để định nghĩa các nhiệm vụ của bạn
- Chỉnh sửa `src/jd_assistants/crews/{tên crew}/crew.py` để thêm logic, công cụ và các tham số cụ thể của bạn
- Chỉnh sửa `src/jd_assistants/main.py` để thêm đầu vào tùy chỉnh cho các tác nhân và nhiệm vụ của bạn

## Chạy Dự Án

Để khởi động đội ngũ AI của bạn và bắt đầu thực hiện nhiệm vụ, hãy chạy lệnh này từ thư mục gốc của dự án:

```bash
$ crewai run
```


Lệnh này khởi tạo Đội ngũ jd_assistants, lắp ráp các tác nhân và phân công cho chúng các nhiệm vụ như đã định nghĩa trong cấu hình của bạn.

Ví dụ này, không thay đổi, sẽ tạo ra một file `report.md` với đầu ra của một nghiên cứu về LLMs trong thư mục gốc.

## Hiểu Về HR Assistant Crew

HR Assistant Crew được cấu thành từ nhiều tác nhân AI, mỗi tác nhân có vai trò, mục tiêu và công cụ riêng biệt. Các tác nhân này hợp tác trong một loạt các nhiệm vụ, được định nghĩa trong `config/tasks.yaml`, tận dụng kỹ năng tập thể của chúng để đạt được các mục tiêu phức tạp. File `config/agents.yaml` phác thảo khả năng và cấu hình của từng tác nhân trong đội ngũ của bạn.

## Luồng Hoạt Động Của Dự Án

Dự án HR Assistant Crew hoạt động theo một quy trình tuần tự, bắt đầu từ việc tải lên các CV ứng viên, sau đó phân tích và đánh giá các ứng viên dựa trên các tiêu chí đã định nghĩa. Các tác nhân AI trong đội ngũ sẽ hợp tác để thực hiện các nhiệm vụ như đọc CV, chấm điểm ứng viên và tạo email phản hồi.

1. **Tải lên CV**: Người dùng cung cấp đường dẫn đến các file CV, hệ thống sẽ tự động quét và thu thập thông tin từ các file này.
2. **Phân tích CV**: Các tác nhân AI sẽ sử dụng các công cụ như PyMuPDF để đọc và trích xuất thông tin từ CV, bao gồm thông tin cá nhân, học vấn, kinh nghiệm làm việc và kỹ năng.
3. **Chấm điểm ứng viên**: Dựa trên các tiêu chí đã được định nghĩa trong `config/tasks.yaml`, hệ thống sẽ chấm điểm các ứng viên và lưu trữ kết quả.
4. **Gửi phản hồi**: Sau khi chấm điểm, hệ thống sẽ tạo email phản hồi cho từng ứng viên, thông báo về kết quả và các bước tiếp theo.

Quy trình này giúp tối ưu hóa việc tuyển dụng, đảm bảo rằng các ứng viên phù hợp nhất được lựa chọn cho các vị trí cần tuyển.

## Công Nghệ Sử Dụng

Dự án HR Assistants Crew sử dụng một số công nghệ và thư viện chính sau:

- **Python**: Ngôn ngữ lập trình chính được sử dụng để phát triển dự án.
- **crewAI**: Framework cho phép xây dựng hệ thống AI đa tác nhân, giúp các tác nhân hợp tác hiệu quả trong các nhiệm vụ phức tạp.
- **PyMuPDF**: Thư viện được sử dụng để đọc và trích xuất thông tin từ các file PDF.
- **pandas**: Thư viện để xử lý và phân tích dữ liệu, đặc biệt là để lưu trữ kết quả vào file CSV.
- **asyncio**: Thư viện hỗ trợ lập trình bất đồng bộ, cho phép thực hiện nhiều tác vụ đồng thời.
- **pydantic**: Thư viện để xác thực dữ liệu và tạo các mô hình dữ liệu.
- **UV**: Công cụ quản lý phụ thuộc và xử lý gói, giúp cài đặt và thực thi dự án một cách liền mạch.

Các công nghệ này kết hợp với nhau để tạo ra một hệ thống tuyển dụng tự động, giúp tối ưu hóa quy trình tuyển dụng và nâng cao hiệu quả làm việc.

## Hỗ Trợ

Để được hỗ trợ, đặt câu hỏi hoặc phản hồi về HR Assistants Crew hoặc crewAI.
- Truy cập [tài liệu của CrewAI](https://docs.crewai.com)
- Liên hệ với CrewAI qua [kho lưu trữ GitHub](https://github.com/joaomdmoura/crewai)
- [Tham gia Discord của CrewAI](https://discord.com/invite/X4JWnZnxPb)
- [Trò chuyện với tài liệu của CrewAI](https://chatg.pt/DWjSBZn)

Hãy cùng nhau tạo ra những điều kỳ diệu với sức mạnh và sự đơn giản của crewAI.