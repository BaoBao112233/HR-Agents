# Hướng Dẫn Sử Dụng Hệ Thống Quản Lý Nhân Sự

## Giới Thiệu

Hệ thống Quản Lý Nhân Sự (HR Management System) là một ứng dụng web giúp quản lý thông tin nhân viên, phòng ban và chức vụ trong công ty. Hệ thống cung cấp giao diện đơn giản, dễ sử dụng và bảo mật.

## Mục Lục

1. [Truy Cập Hệ Thống](#truy-cập-hệ-thống)
2. [Đăng Nhập](#đăng-nhập)
3. [Trang Chủ (Dashboard)](#trang-chủ-dashboard)
4. [Quản Lý Nhân Viên](#quản-lý-nhân-viên)
5. [Quản Lý Phòng Ban](#quản-lý-phòng-ban)
6. [Quản Lý Chức Vụ](#quản-lý-chức-vụ)
7. [Đăng Xuất](#đăng-xuất)
8. [Câu Hỏi Thường Gặp](#câu-hỏi-thường-gặp)

---

## Truy Cập Hệ Thống

### Địa chỉ truy cập:
- **Frontend (Giao diện người dùng)**: http://localhost:3000
- **Backend API**: http://localhost:8000

> **Lưu ý**: Đảm bảo các dịch vụ Docker đang chạy bằng cách kiểm tra:
> ```bash
> docker ps
> ```
> Bạn cần thấy 3 containers đang chạy: `hr_app`, `hr_postgres`, `hr_redis`

---

## Đăng Nhập

### Bước 1: Truy cập trang đăng nhập
1. Mở trình duyệt web (Chrome, Firefox, Edge, Safari)
2. Truy cập: http://localhost:3000/login

### Bước 2: Nhập thông tin đăng nhập

**Tài khoản Admin mặc định:**
- Email: `admin@company.com` hoặc `admin@oxii.com`
- Password: _(liên hệ quản trị viên để lấy mật khẩu)_

### Bước 3: Đăng nhập
1. Nhập email vào ô "Email"
2. Nhập mật khẩu vào ô "Password"
3. Click nút **"Log In"**
4. Nếu thông tin đúng, bạn sẽ được chuyển đến trang Dashboard

> **⚠️ Lưu ý bảo mật:**
> - Không chia sẻ mật khẩu với người khác
> - Đăng xuất khi rời khỏi máy tính
> - Thay đổi mật khẩu định kỳ

---

## Trang Chủ (Dashboard)

Sau khi đăng nhập thành công, bạn sẽ thấy **Trang Dashboard** với các thống kê tổng quan:

### Các chỉ số hiển thị:
1. **Total Employees** (Tổng số nhân viên) - Màu xanh lá
2. **Departments** (Số phòng ban) - Màu xanh dương
3. **Positions** (Số chức vụ) - Màu tím
4. **New This Month** (Nhân viên mới trong tháng) - Màu đỏ

### Menu điều hướng:
- **Dashboard**: Trang chủ, tổng quan
- **Employees**: Quản lý nhân viên
- **Departments**: Quản lý phòng ban
- **Positions**: Quản lý chức vụ

---

## Quản Lý Nhân Viên

### Xem danh sách nhân viên

1. Click vào **"Employees"** trong menu điều hướng
2. Bảng danh sách nhân viên hiển thị các thông tin:
   - **Code**: Mã nhân viên
   - **First Name**: Tên
   - **Last Name**: Họ
   - **Email**: Email công ty
   - **Phone**: Số điện thoại
   - **Status**: Trạng thái (Active/Inactive)
   - **Actions**: Các hành động (Edit, Delete)

### Thêm nhân viên mới

1. Click nút **"Add Employee"** (góc phải trên)
2. Một form sẽ hiện ra, điền các thông tin:

#### Thông tin bắt buộc (có dấu *):
- **First Name**: Tên của nhân viên
- **Last Name**: Họ của nhân viên
- **Email**: Email công ty (phải có định dạng email hợp lệ)
- **Password**: Mật khẩu để đăng nhập
- **Join Date**: Ngày bắt đầu làm việc
- **Contract Type**: Loại hợp đồng
  - Full Time (Toàn thời gian)
  - Part Time (Bán thời gian)
  - Contract (Hợp đồng)
  - Intern (Thực tập)

#### Thông tin tùy chọn:
- **Phone**: Số điện thoại liên lạc
- **Date of Birth**: Ngày sinh
- **Gender**: Giới tính (Male/Female/Other)
- **Department**: Phòng ban
- **Position**: Chức vụ

3. Click **"OK"** để lưu hoặc **"Cancel"** để hủy

> **💡 Mẹo**: 
> - Email phải là duy nhất, không thể trùng với nhân viên khác
> - Mật khẩu nên mạnh, kết hợp chữ, số và ký tự đặc biệt
> - Tạo phòng ban và chức vụ trước khi thêm nhân viên

### Chỉnh sửa thông tin nhân viên

1. Tìm nhân viên cần chỉnh sửa trong danh sách
2. Click nút **"Edit"** ở cột Actions
3. Cập nhật thông tin cần thiết
4. Click **"OK"** để lưu

### Xóa nhân viên

1. Tìm nhân viên cần xóa trong danh sách
2. Click nút **"Delete"** (màu đỏ) ở cột Actions
3. Xác nhận xóa

> **⚠️ Cảnh báo**: Việc xóa nhân viên là vĩnh viễn và không thể khôi phục!

---

## Quản Lý Phòng Ban

### Xem danh sách phòng ban

1. Click vào **"Departments"** trong menu
2. Bảng hiển thị:
   - **ID**: Mã phòng ban
   - **Name**: Tên phòng ban
   - **Description**: Mô tả chi tiết

### Thêm phòng ban mới

1. Click nút **"Add Department"**
2. Điền thông tin:
   - **Name** (Bắt buộc): Tên phòng ban
     - Ví dụ: "Phòng Nhân Sự", "Phòng Kỹ Thuật", "Phòng Kinh Doanh"
   - **Description** (Tùy chọn): Mô tả về phòng ban
     - Ví dụ: "Quản lý tuyển dụng, đào tạo và phúc lợi nhân viên"
3. Click **"OK"** để lưu

### Ví dụ các phòng ban thường gặp:
- **Phòng Hành Chính - Nhân Sự**: Quản lý con người và văn phòng
- **Phòng Kỹ Thuật**: Phát triển sản phẩm và công nghệ
- **Phòng Kinh Doanh**: Bán hàng và chăm sóc khách hàng
- **Phòng Marketing**: Tiếp thị và truyền thông
- **Phòng Kế Toán**: Quản lý tài chính và kế toán

---

## Quản Lý Chức Vụ

### Xem danh sách chức vụ

1. Click vào **"Positions"** trong menu
2. Bảng hiển thị:
   - **ID**: Mã chức vụ
   - **Title**: Tên chức vụ
   - **Level**: Cấp bậc
   - **Salary Min**: Mức lương tối thiểu
   - **Salary Max**: Mức lương tối đa

### Thêm chức vụ mới

1. Click nút **"Add Position"**
2. Điền thông tin:
   - **Title** (Bắt buộc): Tên chức vụ
     - Ví dụ: "Backend Developer", "HR Manager", "Sales Executive"
   - **Description** (Tùy chọn): Mô tả công việc
   - **Level** (Tùy chọn): Cấp bậc
     - Ví dụ: "Junior", "Senior", "Manager", "Director"
   - **Minimum Salary** (Tùy chọn): Mức lương tối thiểu (VNĐ)
   - **Maximum Salary** (Tùy chọn): Mức lương tối đa (VNĐ)
3. Click **"OK"** để lưu

### Ví dụ các chức vụ:

#### Phòng Kỹ Thuật:
- **Junior Developer** (Level: Junior, Lương: 8-15 triệu)
- **Senior Developer** (Level: Senior, Lương: 20-40 triệu)
- **Tech Lead** (Level: Lead, Lương: 35-60 triệu)

#### Phòng Nhân Sự:
- **HR Specialist** (Level: Staff, Lương: 10-18 triệu)
- **HR Manager** (Level: Manager, Lương: 25-45 triệu)

#### Phòng Kinh Doanh:
- **Sales Executive** (Level: Staff, Lương: 8-15 triệu + thưởng)
- **Sales Manager** (Level: Manager, Lương: 20-40 triệu + thưởng)

---

## Đăng Xuất

### Cách đăng xuất:
1. Click vào biểu tượng người dùng hoặc tên người dùng (góc phải trên)
2. Chọn **"Logout"** hoặc **"Đăng xuất"**
3. Bạn sẽ được chuyển về trang đăng nhập

> **💡 Lời khuyên**: Luôn đăng xuất khi:
> - Rời khỏi máy tính
> - Kết thúc ca làm việc
> - Sử dụng máy tính công cộng

---

## Câu Hỏi Thường Gặp

### 1. Tôi quên mật khẩu, phải làm sao?

**Giải pháp A - Liên hệ quản trị viên:**
- Liên hệ người quản trị hệ thống để reset mật khẩu

**Giải pháp B - Tự reset qua Database (chỉ dành cho quản trị viên):**
```bash
# Tạo password hash mới
docker exec -it hr_app python -c "
from jd_assistants.auth import get_password_hash
print(get_password_hash('MatKhauMoi123'))
"

# Cập nhật trong database
docker exec hr_postgres psql -U hr_user -d hr_db -c \
  "UPDATE users SET password_hash='<hash>' WHERE email='your@email.com';"
```

### 2. Lỗi 401 Unauthorized khi truy cập trang?

**Nguyên nhân**: Bạn chưa đăng nhập hoặc phiên đăng nhập đã hết hạn.

**Giải pháp**:
1. Truy cập lại trang đăng nhập: http://localhost:3000/login
2. Đăng nhập với tài khoản của bạn
3. Phiên đăng nhập sẽ tự động gia hạn khi bạn sử dụng hệ thống

### 3. Không thấy dữ liệu trong danh sách?

**Nguyên nhân**: Database chưa có dữ liệu.

**Giải pháp**:
1. Tạo dữ liệu mới bằng cách click nút "Add" trên mỗi trang
2. Hoặc import dữ liệu từ file CSV/Excel (nếu có tính năng)
3. Kiểm tra kết nối với database (container `hr_postgres` phải chạy)

### 4. Không kết nối được với hệ thống?

**Kiểm tra các dịch vụ đang chạy:**
```bash
docker ps
```

Phải thấy 3 containers:
- `hr_app` - Backend API (port 8000)
- `hr_postgres` - Database (port 5432)
- `hr_redis` - Cache (port 6379)

**Nếu thiếu containers, khởi động lại:**
```bash
cd /path/to/jd_assistants
docker compose up -d
```

### 5. Tôi muốn tạo tài khoản admin mới?

**Sử dụng API để đăng ký:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "MatKhauManh123!",
    "role": "ADMIN"
  }'
```

### 6. Phân biệt giữa các loại người dùng?

Hệ thống có 2 loại người dùng chính:

| Role | Quyền hạn | Mô tả |
|------|-----------|-------|
| **ADMIN** | Toàn quyền | Quản lý toàn bộ hệ thống, thêm/xóa/sửa tất cả |
| **EMPLOYEE** | Hạn chế | Chỉ xem thông tin cá nhân và cập nhật thông tin của mình |

### 7. Làm sao biết phiên bản của hệ thống?

**Kiểm tra version backend:**
```bash
docker exec hr_app python -c "import jd_assistants; print(jd_assistants.__version__)"
```

**Kiểm tra version frontend:**
```bash
cat frontend/package.json | grep version
```

### 8. Database đầy, cần làm gì?

**Xóa dữ liệu cũ không cần thiết:**
- Xóa nhân viên đã nghỉ việc lâu
- Xóa phòng ban/chức vụ không còn sử dụng

**Backup database:**
```bash
docker exec hr_postgres pg_dump -U hr_user hr_db > backup_$(date +%Y%m%d).sql
```

**Restore database:**
```bash
cat backup_20250101.sql | docker exec -i hr_postgres psql -U hr_user -d hr_db
```

---

## Hỗ Trợ Kỹ Thuật

### Liên hệ:
- **Email hỗ trợ**: support@company.com
- **Hotline**: 1900-xxxx-xxx
- **Giờ làm việc**: 8:00 - 17:30 (Thứ 2 - Thứ 6)

### Tài nguyên hữu ích:
- **Tài liệu kỹ thuật**: `/docs/technical-guide.md`
- **API Documentation**: http://localhost:8000/docs
- **GitHub Repository**: (link to repo)

---

## Lưu Ý Quan Trọng

### Bảo mật:
✅ **Nên làm:**
- Sử dụng mật khẩu mạnh (ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường, số, ký tự đặc biệt)
- Đăng xuất khi rời máy tính
- Không chia sẻ tài khoản
- Cập nhật trình duyệt lên phiên bản mới nhất

❌ **Không nên làm:**
- Lưu mật khẩu trong file text hoặc email
- Sử dụng máy tính công cộng để truy cập dữ liệu nhạy cảm
- Truy cập hệ thống qua mạng WiFi công cộng không bảo mật

### Hiệu suất:
- Sử dụng trình duyệt hiện đại (Chrome, Firefox, Edge phiên bản mới)
- Kết nối internet ổn định (ít nhất 5 Mbps)
- Đóng các tab không cần thiết để giảm tải bộ nhớ

---

## Cập Nhật và Nâng Cấp

Hệ thống sẽ được cập nhật định kỳ để:
- Sửa lỗi và cải thiện hiệu suất
- Thêm tính năng mới
- Tăng cường bảo mật

**Kiểm tra cập nhật:**
- Theo dõi thông báo từ quản trị viên
- Xem changelog tại: `/docs/CHANGELOG.md`

---

*Tài liệu này được cập nhật lần cuối: 23/11/2025*
*Phiên bản: 1.0*
