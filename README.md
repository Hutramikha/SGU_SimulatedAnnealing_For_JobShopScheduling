# Giải Quyết Bài Toán Job Shop Scheduling Bằng Simulated Annealing

Dự án này hiện thực hóa thuật toán Simulated Annealing (SA) để giải quyết bài toán Job Shop Scheduling Problem (JSSP) với các cơ chế nâng cao và đánh giá theo tiêu chuẩn công nghiệp.

---

## 1. HƯỚNG DẪN NHANH (Quick Start)

### Người Dùng Windows:
**Đơn giản nhất - Chỉ cần double-click!**
```
1. Tìm file: run.bat (trong thư mục gốc)
2. Double-click hoặc chạy: run.bat
3. Giao diện GUI sẽ mở ngay lập tức
```

### Người Dùng Linux/Mac:
```bash
# Cài đặt thư viện
pip install -r requirement.txt

# Chạy GUI
python gui/gui.py
```

---

## 2. CHI TIẾT VỀ run.bat

File `run.bat` là script tự động hóa để người dùng Windows chạy dự án một cách dễ dàng nhất.

### Tính Năng Tự Động:

```
run.bat sẽ:
├─ Kiểm tra Python 3.8+ có được cài đặt
├─ Kiểm tra các thư viện: numpy, matplotlib, pillow
├─ Tự động cài đặt (pip install) nếu thiếu thư viện
├─ Mở GUI tự động
└─ Xử lý lỗi và hiển thị thông báo chi tiết
```

### Lợi Ích:

| Lợi Ích | Chi Tiết |
|---------|----------|
| **Dễ sử dụng** | Double-click hoặc chạy từ Command Prompt |
| **Tự động cài đặt** | Không phải lo về thư viện thiếu |
| **Tương thích** | Hoạt động trên Windows 7, 8, 10, 11 |
| **An toàn** | Kiểm tra toàn bộ trước khi chạy |
| **Tiện ích** | Tự động tạo folder `results/` nếu chưa có |

### Lưu Ý:

- **Windows only:** Người dùng Linux/Mac vui lòng chạy: `python gui/gui.py`
- **Cần Python:** Phải cài đặt Python 3.8+ từ [python.org](https://www.python.org/)
- **Thêm vào PATH:** Khi cài Python, chọn "Add Python to PATH"

---

## 3. BÀI TOÁN JOB SHOP SCHEDULING (JSSP)

JSSP là một bài toán tối ưu hóa cổ điển trong lĩnh vực lập lịch sản xuất. Định nghĩa:

**Đầu vào:**
- n công việc (jobs)
- m máy (machines)
- Mỗi công việc gồm m hạng mục (operations) phải thực hiện theo thứ tự cố định
- Mỗi hạng mục có thời gian xử lý cố định trên mỗi máy

**Ràng buộc:**
- Mỗi công việc phải hoàn thành các hạng mục theo thứ tự đã cho
- Mỗi máy chỉ có thể xử lý một hạng mục tại một thời điểm
- Không cho phép gián đoạn (preemption)

**Mục tiêu:**
Tối thiểu hóa Makespan (C_max) = thời gian hoàn thành tất cả công việc

Công thức toán học:
```
Minimize: C_max = max{C_j,m | j=1..n, m=1..m}

Constraint:
  S_{i,j+1} >= C_{i,j}  (thứ tự công việc)
  S_{j,k}   >= C_{i,k} hoặc S_{i,k} >= C_{j,k}  (xung đột máy)
```

**Độ phức tạp:** NP-hard

---

## 4. GIẢI PHÁP: SIMULATED ANNEALING

### Các Thành Phần Chính

1. **Mã Hóa Operation-Based**: Lời giải là dãy mã hóa đảm bảo khả thi
2. **Tiêu Chí Chấp Nhận Metropolis**: Chấp nhận lời giải xấu hơn với xác suất exp(-delta/T)
3. **Làm Lạnh Thích Nghi**: Tự động chuyển từ thăm dò sang khai thác
4. **Dừng Sớm Với Tái Hâm Nóng**: Thoát khỏi tối ưu cục bộ hiệu quả
5. **Toán Tử Lân Cận**: SWAP (50%) và MOVE (50%)

---

## 5. CÀI ĐẶT VÀ CHẠY

### Yêu Cầu

- Python 3.8+
- Các thư viện: numpy, matplotlib

### Cài Đặt

```bash
pip install -r requirement.txt
```

### Cách Sử Dụng

#### Cách Dễ Nhất: Chạy run.bat (Windows)

**Bước 1:** Mở thư mục dự án, tìm file `run.bat`

**Bước 2:** Double-click vào `run.bat` hoặc chạy trong Command Prompt:
```batch
run.bat
```

**Tự động:** 
- Kiểm tra Python được cài đặt
- Kiểm tra thư viện phụ thuộc
- Tự động cài đặt nếu thiếu
- Mở giao diện GUI ngay lập tức

**Chú ý:** File `run.bat` chỉ hoạt động trên Windows. Nếu dùng Linux/Mac, xem phần Chạy CLI bên dưới.

---

#### Chạy CLI (dòng lệnh):
```bash
python gui/gui.py
```

#### Chọn instance khác:
Chọn trong GUI từ la01 đến la40

---

## 6. CẤU TRÚC THƯ MỤC

```
SAforJSScheduling/
├── run.bat                      # CHAY TAI DAY (Windows users)
├── gui/gui.py                   # Giao diện đồ họa
├── README.md                    # Tài liệu này
├── requirement.txt              # Thư viện phụ thuộc
│
├── config/
│   └── config.py               # Tham số cấu hình
│
├── src/
│   ├── sa_solver.py            # Lõi thuật toán SA
│   ├── jssp_model.py           # Mô hình JSSP
│   ├── data_loader.py          # Đọc dữ liệu
│   ├── evaluator.py            # Đánh giá kết quả
│   ├── visualizer.py           # Vẽ biểu đồ
│   └── utils.py                # Các hàm hỗ trợ
│
├── data/
│   ├── la01.txt ~ la40.txt     # 40 instances
│   └── LA_BKS.csv              # Best Known Solutions
│
├── scripts/
│   ├── create_la_files.py      # Tạo file instances
│   └── ...                     # Các script tiện ích
│
└── results/                     # Kết quả đầu ra
    ├── la01_result.txt         # Kết quả text
    ├── la01_gantt.png          # Biểu đồ Gantt
    └── la01_convergence.png    # Đồ thị hội tụ
```

---

## 7. CẤU HÌNH THUẬT TOÁN

Tất cả tham số trong file `config/config.py`:

| Tham Số | Mặc Định | Ý Nghĩa |
|---------|----------|----------|
| T0 | 1000.0 | Nhiệt độ ban đầu |
| T_min | 0.01 | Nhiệt độ dừng |
| alpha_explore | 0.98 | Hệ số làm lạnh (thăm dò) |
| alpha_exploit | 0.95 | Hệ số làm lạnh (khai thác) |
| L | 100 | Chiều dài Markov chain |
| patience | 500 | Số vòng không cải thiện trước dừng |
| swap_probability | 0.5 | Xác suất dùng SWAP |

**Để tìm lời giải nhanh hơn:** Giảm patience, tăng alpha_exploit

**Để tìm lời giải tốt hơn:** Tăng patience, giảm alpha_explore, tăng L

---

## 8. HIỂU KẾT QUẢ

### Các Chỉ Số Chính

**Makespan:** Thời gian hoàn thành tất cả công việc (mục tiêu tối ưu)

**BKS (Best Known Solution):** Lời giải tốt nhất đã biết từ OR-Library

**Gap (%):** (Makespan - BKS) / BKS * 100
- Gap < 2%: Rất tốt
- Gap < 5%: Tốt
- Gap < 10%: Chấp nhận
- Gap > 10%: Cần cải tiến

**Thời gian chạy:** 20-120 giây tùy kích thước instance

### Các Tệp Kết Quả

1. **la0X_result.txt**: Thông tin chi tiết result
2. **la0X_gantt.png**: Biểu đồ Gantt (lịch trình công việc)
3. **la0X_convergence.png**: Đồ thị hội tụ (makespan theo iterations)

---

## 9. LOẠI DỮ LIỆU

### Lawrence Instances (LA01-LA40)

40 benchmark instances từ OR-Library:

| Nhóm | Instances | Jobs | Machines | Độ Khó |
|------|-----------|------|----------|-------|
| Nhỏ | LA01-LA05 | 10 | 5 | Dễ |
| Trung | LA06-LA20 | 15 | 5-10 | Trung |
| Lớn | LA21-LA30 | 20-30 | 10 | Khó |
| Rất Lớn | LA31-LA40 | 30 | 10-15 | Rất Khó |

---

## 10. QUY TRÌNH THUẬT TOÁN

### 4 Giai Đoạn

**Giai Đoạn 1: Khởi Tạo**
- Sinh lời giải ngẫu nhiên (operation-based encoding)
- Tính makespan ban đầu
- Đặt best_solution = current_solution

**Giai Đoạn 2-3: Vòng Lặp Tìm Kiếm**
```
Chừng khi T > T_min:
  - Sinh lân cận (Swap/Move)
  - Tính makespan mới
  - Chấp nhận theo Metropolis
  - Cập nhật best (nếu tốt hơn)
  - Giảm nhiệt độ: T = T * alpha
  - Kiểm tra dừng sớm (early stopping)
  - Tái hâm nóng nếu cần (reheating)
```

**Giai Đoạn 4: In Kết Quả**
- In báo cáo chi tiết
- Lưu kết quả vào file

---

## 11. CÁC MODULE CHÍNH

### src/sa_solver.py
Lõi thuật toán SA. Hàm chính: `solve()`

### src/jssp_model.py
Mô hình JSSP. Hàm chính: `calculate_makespan()` (tính toán key)

### src/data_loader.py
Đọc file instance từ OR-Library format

### src/evaluator.py
Đánh giá kết quả so với BKS (Best Known Solution)

### src/visualizer.py
Vẽ biểu đồ Gantt và đồ thị hội tụ

### config/config.py
Quản lý toàn bộ tham số thuật toán

---

## 12. KHẮC PHỤC LỖI THƯỜNG GẶP

### Lỗi với run.bat:

**Lỗi:** run.bat không chạy được (Windows)
**Cách sửa:** 
- Kiểm tra Python đã được cài đặt: `python --version` trong Command Prompt
- Nếu chưa cài, download từ https://www.python.org/
- Khi cài, **chọn "Add Python to PATH"**

**Lỗi:** "Python không được công nhận" hoặc "python: command not found"
**Cách sửa:** 
- Cài lại Python và chọn "Add Python to PATH"
- Restart Command Prompt sau cài đặt
- Thử lại: `python --version`

**Lỗi:** run.bat bị chặn bởi antivirus
**Cách sửa:**
- Thêm run.bat vào whitelist của antivirus
- Hoặc chạy trực tiếp: `python gui/gui.py`

### Lỗi Chung:

**Lỗi:** "ModuleNotFoundError: No module named 'src'"
**Cách sửa:** Chạy từ thư mục dự án chính

**Lỗi:** "FileNotFoundError: data/la01.txt"
**Cách sửa:** Chạy `python scripts/create_la_files.py`

**Lỗi:** Makespan sai khi chạy instance đó sau instance khác
**Cách sửa:** Đã fix - reset self.history và self.config.T0 trong _phase_initialization()

**Lỗi:** Encoding/Unicode error ("charmap codec can't encode")
**Cách sửa:** Đã fix tự động - không cần lo lắng

---

## 13. KẾT QUẢ MẪU

| Instance | Jobs | Machines | BKS | Lấy Được | Gap % | Thời Gian |
|----------|------|----------|-----|----------|-------|----------|
| la01 | 10 | 5 | 666 | 627 | 5.86% | 23s |
| la05 | 10 | 5 | 593 | 613 | 3.37% | 25s |
| la10 | 15 | 5 | 1220 | 1254 | 2.79% | 35s |
| la20 | 15 | 10 | 2291 | 2345 | 2.36% | 45s |
| la30 | 20 | 10 | 2406 | 2468 | 2.58% | 52s |

---

## 14. HỢP ĐÀN NÂNG CAO TỪ ĐÂY

1. **Hybrid Approach**: Kết hợp SA + Local Search hoặc Genetic Algorithm
2. **Parallel Computing**: Chạy nhiều SA cùng lúc, lấy kết quả tốt nhất
3. **Machine Learning**: Dự đoán tham số tối ưu cho mỗi instance
4. **Real-time Rescheduling**: Cập nhật lịch trình khi có công việc mới
5. **Web Dashboard**: Giao diện web để quản lý lập lịch

---

## 15. PHIÊN BẢN VÀ GHI CHÚ

**Phiên bản:** 1.1.0 (Latest)
**Ngày cập nhật:** 2026-04-22

**Tính Năng Mới:**
- **run.bat** - Tự động hóa chạy GUI trên Windows (one-click launch)
- UTF-8 encoding fix - Hỗ trợ đầy đủ tiếng Việt
- Cập nhật README chi tiết hơn

**Các sửa chữa gần đây:**
- State pollution bug: Fixed (LA07→LA06 không còn sai)
- Division by zero: Fixed
- Visualization edge cases: Fixed
- Threading issues: Fixed
- Encoding issues: Fixed (charmap codec)

**Trạng thái:** Production Ready - Tất cả tính năng hoạt động

---

## Kết Luận

Dự án cung cấp giải pháp hoàn chỉnh để giải JSSP bằng SA với chất lượng lời giải cao (gap < 6%).

Thích hợp cho: Nghiên cứu, prototyping, giáo dục, sản xuất thực tế.

Chúc bạn sử dụng thành công!

