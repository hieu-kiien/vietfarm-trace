# Tài liệu Kỹ thuật Dự án

Thư mục này tổng hợp hồ sơ thiết kế, đặc tả kỹ thuật và quy trình vận hành của hệ thống **VietFarm Trace (AgroChain)**.

## Thứ tự đọc khuyến nghị

1. [Hướng dẫn cài đặt, chạy dự án & tài khoản Demo](../README.md)
2. [Định hướng sản phẩm & phạm vi hệ thống](../PRODUCT.md)
3. [Đặc tả API (OpenAPI / REST)](api.md) · [Kiến trúc CSDL & phân quyền RLS](database.md)
4. [Cơ chế chuỗi băm SHA-256 / RFC 8785](EVENT-HASH-CHAIN.md) · [Xuất báo cáo PDF A4](PDF-REPORTING.md)
5. [Mẫu đồ thị phả hệ và bộ đáp án kiểm chứng (Oracle)](LINEAGE-ACCEPTANCE.md)
6. [Quyết định kiến trúc xóa/ẩn danh dữ liệu định danh PII](PII-ANONYMIZATION.md)
7. [Quy trình sao lưu cơ sở dữ liệu và khôi phục](BACKUP-RECOVERY.md) · [Ghi chép diễn tập khôi phục](RESTORE-DRILLS.md)
8. [Vận hành hệ thống, job bảo trì và cấu hình triển khai](OPERATIONS.md)

---

## Nguyên tắc bảo toàn kiểm chứng

- Giữ nguyên chuỗi tệp nâng cấp cơ sở dữ liệu (`backend/alembic/versions/`) và các bộ đáp án kiểm thử phả hệ (`backend/tests/data/*-oracle.json`) để đảm bảo khả năng tái lập môi trường và kiểm chứng tự động.
