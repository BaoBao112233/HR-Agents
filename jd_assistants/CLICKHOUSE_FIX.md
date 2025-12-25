# ✅ Đã fix lỗi ClickHouse PRIMARY KEY

## 🐛 Lỗi gặp phải

```
Primary key must be a prefix of the sorting key, but the column in the position 0 is user_id, not id.
```

## 🔧 Nguyên nhân

Trong ClickHouse MergeTree engine, **PRIMARY KEY phải là prefix của ORDER BY clause**. 

Ví dụ lỗi:
```sql
ORDER BY (user_id, provider, id)
PRIMARY KEY (id)  -- ❌ Sai! id không phải là prefix của ORDER BY
```

## ✅ Giải pháp

Bỏ PRIMARY KEY riêng vì ORDER BY đã đủ cho indexing trong ClickHouse:

```sql
ORDER BY (user_id, provider, id)
-- Không cần PRIMARY KEY riêng ✅
```

## 📝 Các bảng đã sửa

1. **users** - Bỏ PRIMARY KEY
2. **api_keys** - Bỏ PRIMARY KEY (vừa thêm trường `model`)
3. **candidates** - Bỏ PRIMARY KEY
4. **job_descriptions** - Bỏ PRIMARY KEY
5. **candidate_scores** - Bỏ PRIMARY KEY
6. **jd_analysis** - Bỏ PRIMARY KEY

## 🚀 Kết quả

```bash
✅ All containers running:
- hr_app (port 8000)
- hr_clickhouse (port 8123, 9000)
- hr_redis (port 6379)

✅ Database hr_system created with tables:
- api_keys (with model field)
- candidate_scores
- candidates
- jd_analysis
- job_descriptions
- users

✅ API endpoints working:
- http://localhost:8000/api/v1/api-keys/providers/list

✅ Frontend accessible:
- http://localhost:8000/
```

## 📚 ClickHouse Best Practice

Trong ClickHouse MergeTree:
- **ORDER BY** định nghĩa cách data được sắp xếp trên disk
- **PRIMARY KEY** là tùy chọn và phải là prefix của ORDER BY
- Nếu không chỉ định PRIMARY KEY, ClickHouse tự động dùng ORDER BY làm primary key
- Đối với hầu hết use cases, chỉ cần ORDER BY là đủ

## 🔗 References

- ClickHouse MergeTree: https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree
- Primary Keys: https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes
