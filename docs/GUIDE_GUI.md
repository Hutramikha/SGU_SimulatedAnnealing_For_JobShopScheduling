# 🖥️ HƯỚNG DẪN SỬ DỤNG GIAO DIỆN GUI

## Cách Chạy GUI

```bash
# Chạy GUI
python gui.py

# Hoặc trên PowerShell
py gui.py
```

---

## 📋 Giao Diện Gồm 2 Tab

### Tab 1: CAU HINH (Configuration)

**Phần 1: Chọn Dữ Liệu**
- Dropdown danh sách 40 instances (LA01 → LA40)
- Nút "Tai Thong Tin" để xem thông tin instance
- Hiển thị: `la01: 10x5 | BKS=666` (jobs × machines | giá trị tối ưu)

**Phần 2: Bảng Tham Số Thuật Toán**
Hiển thị tất cả các tham số hiện tại:

| Tham Số | Giá Trị | Ý Nghĩa |
|---------|--------|---------|
| Nhiệt độ ban đầu (T0) | 1000.0 | Cao để chấp nhận giải tệ |
| Nhiệt độ dừng (T_min) | 0.01 | Ngưỡng kết thúc |
| Hệ số lạnh - Thăm dò | 0.98 | Chậm trong giai đoạn exploration |
| Hệ số lạnh - Khai thác | 0.95 | Nhanh trong giai đoạn exploitation |
| Markov chain (L) | 100 | Số phép thử tại mỗi nhiệt độ |
| Early stopping | 500 | Dừng nếu 500 vòng không cải thiện |
| Ngưỡng cải thiện (ε) | 0.10% | Ngưỡng chọn chế độ làm lạnh |
| Hệ số hâm nóng | 0.9 | T_new = T_old / factor |
| Xác suất Swap | 50% | 50% Swap, 50% Move |

**Phần 3: Nút Chạy**
- Nút "CHAY THUAT TOAN" → Bắt đầu giải
- Progress bar → Hiển thị đang chạy
- Nút "Reset" → Xóa kết quả

---

### Tab 2: KET QUA (Results) - NEW ENHANCED VERSION

**Bố Cục Mới: Paned Window (Trái + Phải)**

#### Phía Trái: Danh Sách Kết Quả (Results List)

**Treeview với 4 cột:**
| Cột | Nội Dung |
|-----|----------|
| Instance | Tên instance (LA01, LA02, ...) |
| Makespan | Giá trị makespan tìm được |
| BKS | Best Known Solution từ Lawrence 1984 |
| Gap(%) | Khoảng cách đến BKS (%) |

**Các Nút:**

1. **"Tai Danh Sach" (Reload List)**
   - Quét thư mục `results/` tìm tất cả `*_result.txt`
   - Cập nhật danh sách hiển thị
   - Hữu ích khi chạy nhiều instances liên tiếp

2. **"Delete" (Xóa Kết Quả)**
   - Chọn một dòng
   - Nhấn Delete
   - Xóa tất cả file liên quan:
     - `*_result.txt` (dữ liệu kết quả)
     - `gantt_*.png` (biểu đồ Gantt)
     - `convergence_*.png` (biểu đồ hội tụ)
   - Yêu cầu xác nhận trước khi xóa

#### Phía Phải: Chi Tiết Kết Quả (Details)

**Hộp Chi Tiết (Result Details Box):**
- Hiển thị nội dung đầy đủ file kết quả
- Bao gồm:
  ```
  Instance: LA01
  Makespan: 666
  BKS: 666
  Gap (%): 0.00
  Quality: Optimal [OK]
  
  Schedule:
  Makespan: 666
  Job 0:
    Operation 0: Machine 1, Time [180, 201]
    ...
  ```

**Bảng Nút Xem Biểu Đồ:**

1. **"Xem Gantt Chart"**
   - Hiển thị Gantt chart (PNG, 300 DPI)
   - Trục X: Thời gian
   - Trục Y: Máy xử lý
   - Các công việc được tô màu khác nhau
   - Hiệu ứng: Xanh dương = thời gian xử lý, trắng = thời gian chờ
   - Được bật CHỈ KHI chọn một dòng từ danh sách

2. **"Xem Convergence Plot"**
   - Hiển thị biểu đồ hội tụ (PNG, 300 DPI)
   - Trục trái: Makespan (thang tuyến tính)
   - Trục phải: Nhiệt độ T (thang logarit)
   - Cho thấy:
     - Quá trình giải pháp cải thiện (Best makespan)
     - Sự giảm nhiệt độ theo thời gian
     - Các điểm reheating (khi T tăng lên)
   - Được bật CHỈ KHI chọn một dòng từ danh sách

3. **"Mo Folder Results"**
   - Mở thư mục `results/` bằng Windows Explorer
   - Có thể xem trực tiếp tất cả file PNG và TXT

---

## 📊 Qui Trình Sử Dụng Với Danh Sách Kết Quả

### Mở GUI và Chạy Thuật Toán
```bash
python gui.py
```

### Bước 1: Chạy Trên Tab CAU HINH
1. Chọn instance từ dropdown (ví dụ: `la01`)
2. Nhấn "Tai Thong Tin" → Xem: `la01: 10 jobs × 5 machines | BKS=666`
3. Kiểm tra bảng tham số (tất cả tham số được hiển thị)
4. Nhấn "CHAY THUAT TOAN" → Bắt đầu giải

**Quá Trình Chạy:**
- Progress bar di chuyển → Đang tìm lời giải
- Status bar: "Dang chay la01..."
- Chờ tới khi hoàn thành → Status: "Hoan tat!"

### Bước 2: Xem Danh Sách Kết Quả Trên Tab KET QUA

**Danh Sách (Phía Trái):**
- Tự động hiển thị tất cả kết quả từ folder `results/`
- Mỗi dòng: `Instance | Makespan | BKS | Gap(%)`
- Ví dụ: `LA01 | 666 | 666 | N/A`

**Chọn Một Kết Quả:**
- Click vào một dòng trong danh sách
- Phía phải sẽ tự động cập nhật:
  - Hộp chi tiết hiển thị toàn bộ kết quả
  - Các nút "Xem Gantt Chart" và "Xem Convergence" được **BẬT**

### Bước 3: Xem Chi Tiết Kết Quả

**Nội Dung Chi Tiết (Phía Phải):**
```
Instance: LA01
Makespan: 666
BKS: 666
Gap (%): 0.00
Quality: Optimal [OK]

Schedule:
Makespan: 666
Job 0:
  Operation 0: Machine 1, Time [180, 201]
  Operation 1: Machine 0, Time [201, 254]
  ...
```

### Bước 4: Xem Biểu Đồ

**Trong hộp chi tiết (Phía Phải):**

1. **"Xem Gantt Chart"** (sau khi chọn một item)
   - Mở PNG hiển thị:
     - Trục X: Thời gian (0 → Makespan)
     - Trục Y: Máy (Machine 0 → Machine 4)
     - Hình chữ nhật = Công việc/Thao tác
     - Màu sắc khác nhau = Các công việc khác nhau
     - Thứ tự từ trái → phải = Thứ tự thời gian
   - Ví dụ:
     ```
     Machine 4  ┌─────┐     ┌─────┐
     Machine 3      ┌──────┐
     Machine 2  ┌──────┐       ┌──────┐
     Machine 1   ┌──┐  ...
     Machine 0   └──┘
                0  100  200  300  400  500  600
     ```

2. **"Xem Convergence Plot"** (sau khi chọn một item)
   - Mở PNG hiển thị quá trình tối ưu hóa:
     - **Đường cong xanh** = Best Makespan (Trục trái, tuyến tính)
     - **Đường cong đỏ** = Nhiệt độ T (Trục phải, logarit)
     - Thấp hơn → càng tốt (Makespan giảm)
     - Có chỉ cho thấy reheating (T tăng đột ngột)

3. **"Mo Folder Results"** (luôn được bật)
   - Mở Windows Explorer tại `results/`
   - Xem trực tiếp:
     - `gantt_*.png` - All Gantt charts
     - `convergence_*.png` - All convergence plots
     - `*_result.txt` - All result files

### Bước 5: Quản Lý Danh Sách

**Tải Lại Danh Sách:**
- Click "Tai Danh Sach" (Left side, top)
- Quét lại thư mục `results/` 
- Cập nhật danh sách với những kết quả mới nhất

**Xóa Một Kết Quả:**
1. Chọn một dòng trong danh sách
2. Click nút "Delete"
3. Xác nhận xóa
4. Những file liên quan sẽ bị xóa:
   - `la01_result.txt`
   - `gantt_la01.png`
   - `convergence_la01.png`
5. Danh sách tự động refresh

---

## 💡 Mẹo & Thủ Thuật

**Chạy nhiều instances:**
- Chạy LA01 (Tab 1, CHAY THUAT TOAN)
- Chuyển sang Tab 2, xem hasil LA01
- Quay lại Tab 1, chạy LA02
- Sau khi xong, click "Tai Danh Sach" trên Tab 2
- Bây giờ sẽ thấy cả LA01 và LA02 trong danh sách

**So sánh kết quả:**
- Danh sách cho phép dễ dàng so sánh Gap% giữa các instances
- Những instance có Gap% nhỏ nhất xứng đáng chú ý

**Làm sạch results:**
- Nếu muốn xoá năm kết quả cũ
- Chọn từng cái rồi Delete
- Hoặc xoá theo thư mục (bên ngoài GUI)

---

## 🔧 Chỉnh Sửa Tham Số

Nếu muốn thay đổi tham số (T0, alpha, L, v.v.):

**Chỉnh trong file `config/config.py`:**

```python
class SAConfig:
    T0 = 1000.0                    # Đổi T0 → 1200.0 (tìm kiếm lâu hơn)
    T_min = 0.01                   # Đổi T_min → 0.001
    alpha_explore = 0.98           # Đổi α_explore → 0.99 (khám phá lâu hơn)
    alpha_exploit = 0.95           # Đổi α_exploit → 0.90 (khai thác nhanh hơn)
    L = 100                        # Đổi L → 200 (tìm kiếm sâu hơn)
    patience = 500                 # Đổi patience → 1000 (kiên nhẫn hơn)
```

Sau đó mở lại GUI:
```bash
python gui.py
```

---

## 📈 Ví Dụ Sử Dụng

### Giải LA01 (10×5)
```
1. Chọn: la01 → "Tai Thong Tin" 
   → "10 jobs, 5 machines, BKS=666"
   
2. "CHAY THUAT TOAN" → Chờ ~2 giây
   → Kết quả: Makespan=666, Gap=0.00%, Optimal [OK]
   
3. "Xem Gantt Chart" → Xem timeline
4. "Xem Convergence Plot" → Xem quá trình hối tụ
```

### Giải LA20 (10×10)
```
1. Chọn: la20 → "Tai Thong Tin"
   → "10 jobs, 10 machines, BKS=1142"
   
2. "CHAY THUAT TOAN" → Chờ ~5 giây
   → Kết quả: Makespan=1200, Gap=5.1%, Good
   
3. Xem biểu đồ → Phân tích kết quả
```

### Giải LA35 (30×10) - Khó Hơn
```
1. Chọn: la35 → "Tai Thong Tin"
   → "30 jobs, 10 machines, BKS=2005"
   
2. "CHAY THUAT TOAN" → Chờ ~10 giây
   → Kết quả: Makespan=2150, Gap=7.2%, Good
   
3. Xem biểu đồ
```

---

## 💡 Tips Sử Dụng

1. **Lần Đầu Dùng:**
   - Thử LA01 (nhỏ nhất, nhanh nhất)
   - Xem kết quả vs BKS
   - Xem biểu đồ Gantt để hiểu cơ chế

2. **Thay Đổi Tham Số:**
   - Muốn tìm kiếm lâu hơn → Tăng T0, L, giảm alpha
   - Muốn chạy nhanh hơn → Giảm T0, L, tăng alpha
   - Xem file PARAMETERS_NOTES.md để hiểu ý nghĩa

3. **So Sánh Instances:**
   - Giải LA01-LA05 (dễ) → Gap < 5%
   - Giải LA21-LA30 (trung bình) → Gap 5-15%
   - Giải LA31-LA40 (khó) → Gap 15-25%

4. **Lưu Lại Kết Quả:**
   - Tab KET QUA → Copy bảng kết quả
   - "Mo Folder Results" → Lưu ảnh Gantt, Convergence

---

## ⚙️ Cấu Hình Hệ Thống

Python version: 3.8+
Libraries:
- tkinter (sẵn có)
- numpy >= 1.21.0
- matplotlib >= 3.3.0
- pillow >= 8.0.0 (tùy chọn)

Cài đặt:
```bash
pip install -r requirement.txt
```

---

## 🐛 Xử Lý Sự Cố

**Lỗi: "ModuleNotFoundError: No module named 'tkinter'"**
- Thường không xảy ra (tkinter bundled với Python)
- Nếu xảy ra: Cài đặt python lại hoặc dùng terminal của VS Code

**Lỗi: "File khong ton tai"**
- Chắc chắn file data/la01.txt tồn tại
- Đặt lại: python create_la_files.py

**GUI chạy chậm**
- Giảm L, T0, tăng alpha
- Hoặc chạy main.py (command-line) nhanh hơn

---

**Lần Cuối Update: 2026-04-09**
Tác Giả: Simulated Annealing Study
