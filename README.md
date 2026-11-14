# VietFarm Trace (AgroChain) — Hệ thống Truy xuất Nguồn gốc Chuỗi lạnh Nông sản

[![CI Pipeline](https://github.com/hieu-kiien/vietfarm-trace/actions/workflows/ci.yml/badge.svg)](https://github.com/hieu-kiien/vietfarm-trace/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

Hệ thống quản lý và truy xuất nguồn gốc nông sản xuyên suốt từ **vùng trồng → thu hoạch → sơ chế & vật tư → tách/gộp phả hệ → bàn giao → vận chuyển chuỗi lạnh (giám sát cảm biến nhiệt độ/độ ẩm tự động) → phân phối/tiêu thụ → thu hồi khẩn cấp theo đồ thị phả hệ → tra cứu công khai qua QR 30×30 mm và xuất báo cáo PDF A4**.

---

## 1. Khởi chạy cục bộ & Mục lục kỹ thuật

- **Chạy đầy đủ cả hệ thống bằng Docker Compose:** `docker compose up --build -d` → Web tại `http://localhost:5173`, Swagger/OpenAPI tại `http://localhost:8000/docs` *(môi trường demo `staging` cũ trên Render Free Tier không còn duy trì trực tuyến)*.
- **Mục lục tài liệu kỹ thuật & kiến trúc:** [docs/README.md](docs/README.md)

---

## 2. Tính năng nổi bật

| Phân hệ | Tính năng đã hoàn thiện |
|---|---|
| **Quản trị & Phân quyền đa đơn vị** | Xác thực JWT, phân quyền RBAC 6 vai trò (`system_admin`, `org_admin`, `grower`, `transporter`, `distributor`, `inspector`), cô lập dữ liệu cấp dòng bằng **PostgreSQL Row-Level Security (RLS)**, quản lý thành viên, mời thành viên bằng token có thời hạn và ẩn danh dữ liệu cá nhân PII theo yêu cầu mà không làm gãy chuỗi băm. |
| **Vùng trồng, Nông sản & Lô thu hoạch** | Khai báo vùng trồng có tọa độ GPS, danh mục nông sản kèm ngưỡng nhiệt độ bảo quản (`min_temp_c` / `max_temp_c`), tạo lô thu hoạch mã `8` ký tự Base32, nhập hàng loạt qua CSV, ghi nhận vật tư nông nghiệp đầu vào và công đoạn sơ chế/chế biến. |
| **Phả hệ Lô hàng (DAG Lineage)** | Tách lô có khóa dòng chống tranh chấp (`SELECT ... FOR UPDATE`), gộp nhiều lô cùng nông sản, truy vết phả hệ hai chiều (nguồn gốc ngược dòng & sản phẩm xuôi dòng) bằng đệ quy CTE chống chu trình, trực quan hóa đồ thị tương tác bằng **React Flow + Dagre**. |
| **Bàn giao, Vị trí & Tiêu thụ** | Đề nghị bàn giao liên tổ chức, xác nhận nhận/từ chối, tự động đánh dấu bàn giao quá hạn bằng job nền, theo dõi vị trí lưu kho/phân phối và ghi nhận tiêu thụ. |
| **Chuỗi lạnh & Cảm biến nhiệt độ** | Quản lý chuyến vận chuyển lạnh (`shipments`), tiếp nhận dữ liệu đo nhiệt độ/độ ẩm qua khóa thiết bị `X-Sensor-Key`, tự động phát hiện và mở/đóng vi phạm ngưỡng nhiệt độ liên tiếp, biểu đồ nhiệt độ trực quan có dải ngưỡng an toàn, thống kê chuỗi lạnh toàn hệ thống và job nén dữ liệu cảm biến theo giờ. |
| **Thu hồi khẩn cấp & Thông báo** | Phát lệnh thu hồi lô hàng, tự động lan truyền xuôi dòng đến mọi lô con/cháu chưa tiêu thụ trên đồ thị phả hệ, gửi thông báo nội bộ & email thu hồi tới các tổ chức đang giữ lô bị ảnh hưởng, ghi nhận xác nhận xử lý thu hồi bất biến. |
| **Chuỗi băm sự kiện & Kiểm toán** | Sổ cái sự kiện chỉ-thêm (`append-only`), liên kết băm mật mã `SHA-256` chuẩn hóa JSON theo **RFC 8785 (JCS)**, phát hiện mọi can thiệp trái phép, job quét toàn vẹn định kỳ và nhật ký kiểm toán (`audit_logs`). |
| **Tra cứu công khai, Nhãn QR & Báo cáo PDF** | Trang tra cứu nguồn gốc công khai không cần đăng nhập kèm bản đồ hành trình Leaflet, nhãn in QR kích thước chuẩn `30×30 mm` và xuất báo cáo truy xuất nguồn gốc chuẩn A4 định dạng **PDF** hỗ trợ đầy đủ tiếng Việt. |

---

## 3. Tài khoản & Mã lô trình diễn (Demo)

Mật khẩu mặc định cho tất cả tài khoản mẫu trên môi trường `development`: **`Password123!`** *(hoặc chọn trực tiếp thẻ vai trò trên màn hình đăng nhập để tự động điền)*.

| Vai trò | Email đăng nhập | Đơn vị | Chức năng chính trên giao diện |
|---|---|---|---|
| **Quản trị hệ thống** | `admin@system.vn` | Hệ thống Quản trị Trung tâm | Quản lý tổ chức, người dùng, danh mục nông sản, giám sát chuỗi lạnh, thu hồi, toàn vẹn chuỗi băm và nhật ký kiểm toán. |
| **Nông hộ** | `grower@caudat.vn` | Nông trại Cầu Đất | Quản lý vùng trồng, tạo lô thu hoạch, ghi nhận vật tư/sơ chế, nhật ký sự kiện và khởi tạo bàn giao. |
| **Quản trị HTX** | `admin@mocchau.vn` | HTX Nông nghiệp Mộc Châu | Quản lý lô hàng của HTX, tách/gộp lô, bàn giao, khởi tạo thu hồi, quản lý thành viên & lời mời. |
| **Đơn vị vận chuyển** | `transporter@vantai.vn` | Công ty Vận tải Lạnh | Quản lý chuyến vận chuyển lạnh, khóa cảm biến nhiệt độ, theo dõi biểu đồ nhiệt độ và vi phạm ngưỡng. |
| **Nhà phân phối** | `distributor@phanphoi.vn` | Hệ thống Phân phối | Nhận bàn giao, quản lý vị trí kho/cửa hàng, tách/gộp lô thương mại, ghi nhận tiêu thụ và xác nhận thu hồi. |
| **Thanh tra** | `inspector@chicuc.gov.vn` | Chi cục Quản lý Chất lượng | Thanh tra độc lập toàn bộ lô hàng, kiểm tra phả hệ, xác minh chuỗi băm SHA-256, phát lệnh thu hồi và xuất báo cáo PDF. |

**Mã lô mẫu để tra cứu công khai nhanh (trên nút chọn nhanh ở trang Tra cứu khi chạy cục bộ):**
- **Môi trường Local (`localhost`):** `XRVT7PXY`, `BZ84PFZ3`, `JQMB7MZ9`, `DB99A7YK`

---

## 4. Hướng dẫn cài đặt và chạy dự án

### Cách 1: Chạy bằng Docker Compose (Khuyên dùng)
Yêu cầu: **Docker Desktop**.
```sh
cp .env.example .env
# Cập nhật DB_PASSWORD và DB_ADMIN_PASSWORD trong tệp .env
docker compose up --build -d
```
- **Giao diện Web:** [http://localhost:5173](http://localhost:5173)
- **Tài liệu API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- Dừng hệ thống: `docker compose down` *(không thêm `-v` nếu muốn giữ lại dữ liệu cơ sở dữ liệu)*.

### Cách 2: Chạy trực tiếp trên máy (Python 3.12+, Node.js 20+, PostgreSQL 16+)
**Khởi động Backend:**
```sh
cd backend
python -m venv .venv
# Kích hoạt môi trường ảo (.venv\Scripts\activate trên Windows hoặc source .venv/bin/activate trên Linux/macOS)
pip install -r requirements-dev.txt
cp .env.example .env
# Cấu hình kết nối PostgreSQL trong tệp .env
python -m app.startup
```
**Khởi động Frontend (ở cửa sổ terminal thứ hai):**
```sh
cd frontend
npm ci
npm run dev
```

---

## 5. Kiểm thử và Đảm bảo chất lượng (CI/CD)

### Kiểm thử Backend (Pytest + Ruff)
Backend sử dụng cơ sở dữ liệu kiểm thử tách biệt hoàn toàn với cơ sở dữ liệu trình diễn:
```powershell
cd backend
./scripts/test-local.ps1 -TestArgs @('-q', '-m', 'not performance', '--cov=app', '--cov-report=json:coverage.json')
./scripts/test-local.ps1 -TestArgs @('-q', '-m', 'performance')
ruff check app tests alembic
ruff format --check app tests alembic
```

### Kiểm thử Frontend (73 bài kiểm thử tự động + ESLint + TypeScript Build)
```sh
cd frontend
npm test
npm run lint
npm run build
```

---

## 6. Kiến trúc bảo mật và Vận hành

- **Phân tách quyền cơ sở dữ liệu:** Ứng dụng web chạy dưới quyền runtime giới hạn (`agrochain_app`, không có `SUPERUSER` hay `BYPASSRLS`), chịu sự kiểm soát nghiêm ngặt của **PostgreSQL Row-Level Security (RLS)** theo từng phiên làm việc. Quyền quản trị chỉ được sử dụng trong bước khởi động (`python -m app.startup` để chạy Alembic migration) và các tác vụ bảo trì định kỳ.
- **Toàn vẹn dữ liệu:** Bảng `events`, `temperature_readings`, `recall_confirmations` và `audit_logs` được bảo vệ bởi trigger chặn `UPDATE`/`DELETE`. Chuỗi băm `SHA-256` chuẩn hóa theo `RFC 8785` đảm bảo phát hiện mọi thay đổi nội dung hoặc đứt gãy thứ tự sự kiện. Chi tiết xem tại [docs/database.md](docs/database.md) và [docs/EVENT-HASH-CHAIN.md](docs/EVENT-HASH-CHAIN.md).
- **Sao lưu & Phục hồi:** Tự động sao lưu hằng đêm kèm manifest số dòng và checksum SHA-256, hỗ trợ kiểm chứng diễn tập khôi phục tại [docs/BACKUP-RECOVERY.md](docs/BACKUP-RECOVERY.md) và [docs/RESTORE-DRILLS.md](docs/RESTORE-DRILLS.md).
- **Quy trình đóng góp:** Xem chi tiết tại [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 7. Giới hạn thiết kế hiện tại & Đánh đổi kỹ thuật (Known Limitations & Trade-offs)

Dự án được phát triển ở quy mô sinh viên IT tập trung vào mô hình hóa nghiệp vụ, PostgreSQL RLS và chuỗi băm kiểm tra toàn vẹn, với các đánh đổi có chủ đích sau:

- **Trạng thái Rate Limit & Cache trong bộ nhớ đơn tiến trình:** `public_trace_limiter` và `public_trace_cache` lưu trong bộ nhớ tiến trình FastAPI (`--workers 1`), chưa dùng kho chia sẻ ngoài như Redis nên giới hạn tần suất và cache không đồng bộ nếu nhân bản nhiều container/worker.
- **Tin cậy header Proxy có kiểm soát (`TRUST_PROXY_HEADERS`):** Mặc định `TRUST_PROXY_HEADERS = False` để tránh client gọi trực tiếp giả mạo `X-Forwarded-For` né rate limit; khi chạy sau reverse proxy (Nginx / Render), cần bật `TRUST_PROXY_HEADERS=True` và cấu hình `FORWARDED_ALLOW_IPS` phù hợp để `startup.py` bật `--proxy-headers` cho Uvicorn.
- **Scheduler chạy trong `lifespan` của ứng dụng web:** Tác vụ nền `scheduler.run_hourly()` chạy nội bộ trong vòng đời FastAPI thay vì tách thành worker/queue chuyên biệt; phù hợp triển khai 1 web instance nhỏ gọn.
- **Giới hạn của chuỗi băm SHA-256 tại CSDL tập trung:** Chuỗi băm RFC 8785 kết hợp trigger `append-only` phát hiện sửa đổi bất hợp pháp từ tài khoản runtime, nhưng không thay thế chữ ký số phần cứng hoặc bảo vệ trước kịch bản quản trị viên CSDL tối cao (`SUPERUSER`) viết lại toàn bộ bảng và mã băm.
