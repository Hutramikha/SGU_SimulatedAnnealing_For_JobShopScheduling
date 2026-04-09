# 📋 THỐ SỐ QUAN TRỌNG - THUẬT TOÁN SA GIẢI JSSP

## 🎯 THÔNG SỐ CHÍNH

### 1. THAM SỐ NHIỆT ĐỘ (Temperature Parameters)
| Thông Số | Ký Hiệu | Giá Trị | Ý Nghĩa |
|----------|---------|--------|---------|
| **Nhiệt độ ban đầu** | T₀ | 1000.0 | Cao để chấp nhận giải pháp tệ ở giai đoạn đầu |
| **Nhiệt độ dừng** | T_min | 0.01 | Ngưỡng dừng thuật toán (T < T_min → STOP) |

---

### 2. THAM SỐ LÀM LẠNH (Cooling Schedule Parameters)
| Thông Số | Ký Hiệu | Giá Trị | Ý Nghĩa |
|----------|---------|--------|---------|
| **Hệ số làm lạnh - Thăm dò** | α_explore | 0.98 | Chậm: T_new = 0.98 × T (giai đoạn khám phá) |
| **Hệ số làm lạnh - Khai thác** | α_exploit | 0.95 | Nhanh: T_new = 0.95 × T (giai đoạn tối ưu) |
| **Ngưỡng cải thiện** | ε | 0.01 (1%) | Nếu cải thiện > 1% → dùng α_explore |

**Công thức cập nhật nhiệt độ:**
```
T_{k+1} = α × T_k

Nếu improvement_rate > ε:
    α = α_explore = 0.98  (khám phá rộng)
Ngược lại:
    α = α_exploit = 0.95  (khai thác sâu)
```

---

### 3. THAM SỐ MARKOV CHAIN
| Thông Số | Ký Hiệu | Giá Trị | Ý Nghĩa |
|----------|---------|--------|---------|
| **Chiều dài Markov chain** | L | 100 | Số lần thử tại mỗi mức nhiệt độ |

**Ý nghĩa:** Tại mỗi T cố định, thực hiện L=100 phép thử tìm kiếm lân cận trước khi giảm T

---

### 4. THAM SỐ DỪNG SỚM (Early Stopping Parameters)
| Thông Số | Ký Hiệu | Giá Trị | Ý Nghĩa |
|----------|---------|--------|---------|
| **Ngưỡng kiên nhẫn** | patience | 500 | Nếu 500 vòng không cải thiện → dừng sớm |
| **Hệ số hâm nóng** | reheat_factor | 0.9 | Khi dừng sớm, T_new = T_old / 0.9 (hâm nóng lại) |

**Quy trình:**
```
Nếu không cải thiện trong 500 vòng liên tiếp:
  - Nếu reheating_enabled = True:
      T_new = T_old / 0.9  (hâm nóng lại để tìm lại)
  - Nếu reheating_enabled = False:
      STOP ngay lập tức
```

---

### 5. TIÊU CHÍ CHẤP NHẬN METROPOLIS (Metropolis Acceptance Criterion)
| Thông Số | Công Thức | Ý Nghĩa |
|----------|-----------|---------|
| **Giải pháp tốt hơn** | P(accept s') = 1 | Luôn chấp nhận |
| **Giải pháp tệ hơn** | P(accept s') = exp(-Δ/T) | Chấp nhận với xác suất |

**Công thức tính Δ (Delta):**
```
Δ = f(s') - f(s)
  = Makespan_mới - Makespan_hiện_tại

Nếu Δ < 0: Giải pháp tốt hơn (Makespan giảm) → Luôn chấp nhận ✓
Nếu Δ ≥ 0: Giải pháp tệ hơn (Makespan tăng) → Chấp nhận nếu random < exp(-Δ/T)
```

---

### 6. TOÁN TỬ LÂN CẬN (Neighborhood Operators)
| Toán Tử | Xác Suất | Phương Thức |
|---------|----------|-----------|
| **Swap** | 50% | Hoán đổi 2 phần tử tại vị trí i và j |
| **Move** | 50% | Lấy phần tử từ vị trí i, chèn vào vị trí j |

**Lựa chọn:** `swap_probability = 0.5` (50% Swap, 50% Move)

---

### 7. PHƯƠNG PHÁP MÃ HÓA (Encoding Method)
| Thông Số | Giá Trị | Ý Nghĩa |
|----------|--------|---------|
| **Operation-based Encoding** | [i, j, k, ...] | Danh sách n×m phần tử (mỗi job xuất hiện m lần) |
| **Độ dài dãy mã hóa** | n × m | Với n jobs, m machines → dãy có độ dài n×m |

**Ví dụ LA01:**
- n_jobs = 10, n_machines = 5
- Dãy mã hóa có độ dài = 10 × 5 = 50 phần tử
- Ví dụ: [0, 1, 2, 3, 0, 1, 2, ...]

---

### 8. HÀM MỤC TIÊU (Objective Function)
| Thông Số | Công Thức | Ý Nghĩa |
|----------|-----------|---------|
| **Makespan** | C_max | Thời gian hoàn thành tất cả công việc |

**Tính Makespan:**
```
Cho mỗi operation O_{i,j}:
    C(O_{i,j}) = max(job_ready_time[j], machine_ready_time[m]) + p_{i,j}

C_max = max(C_last_operation,j) cho mọi job j
```

**job_ready_time[j]:** Thời điểm job j sẵn sàng thực hiện operation kế tiếp
**machine_ready_time[m]:** Thời điểm máy m sẵn sàng


---

### 9. BẢN CHẤT BÀI TOÁN JSSP
| Thông Số | Giá Trị | Ý Nghĩa |
|----------|--------|---------|
| **Số công việc** | n | Thay đổi theo instance (LA01: 10 jobs) |
| **Số máy** | m | Thay đổi theo instance (LA01: 5 machines) |
| **Tổng operations** | n × m | Mỗi job phải thực hiện m operations theo trình tự |

---

## 📊 BỘ DỮ LIỆU BENCHMARK

### Các Instance LA (Lawrence - 1984)
| Nhóm | Instance | Jobs | Machines | BKS |
|------|----------|------|----------|-----|
| Nhóm 1 | LA01-LA05 | 10 | 5 | 666-690 |
| Nhóm 2 | LA06-LA10 | 15 | 5 | 926-1003 |
| Nhóm 3 | LA11-LA15 | 20 | 5 | 1222-1273 |
| Nhóm 4 | LA16-LA20 | 10 | 10 | 945-1142 |
| Nhóm 5 | LA21-LA25 | 15 | 10 | 1217-1460 |
| Nhóm 6 | LA26-LA30 | 20 | 10 | 1555-1784 |
| Nhóm 7 | LA31-LA35 | 30 | 10 | 1784-2005 |
| Nhóm 8 | LA36-LA40 | 15 | 15 | 1566-1917 |

---

## 🔄 QUY TRÌNH ALGORITHM (4 GIAI ĐOẠN)

### Giai đoạn 1: KHỞI TẠO (Initialization)
```
1. Sinh lời giải ngẫu nhiên S₀ (Operation-based Encoding)
2. Tính Makespan: f(S₀)
3. Đặt S_best = S₀, f_best = f(S₀)
4. Đặt T = T₀
```

### Giai đoạn 2: MARKOV CHAIN (Inner Loop)
```
For i = 1 to L:
    1. Sinh neighbor s' từ s (Swap hoặc Move)
    2. Tính Δ = f(s') - f(s)
    3. Nếu Δ < 0: Accept s' → s
    4. Ngược lại: Nếu random < exp(-Δ/T):
           Accept s' → s
       Ngược lại: Reject s'
    5. Nếu f(s) < f_best: Update f_best = f(s)
```

### Giai đoạn 3: LÀMẠNH (Cooling)
```
1. Tính improvement_rate = (f_best_prev - f_best_curr) / f_best_prev
2. Nếu improvement_rate > ε:
       α = α_explore = 0.98
   Ngược lại:
       α = α_exploit = 0.95
3. T_new = α × T_old
4. Kiểm tra Early Stopping:
   - Nếu 500 vòng không cải thiện:
       Nếu reheating: T = T / 0.9 (hâm nóng lại)
       Ngược lại: STOP
```

### Giai đoạn 4: ĐIỀU KIỆN DỪNG (Termination)
```
While T > T_min:
    Thực hiện Giai đoạn 2-3
    
Khi T ≤ T_min: STOP
Xuất: S_best (lời giải tốt nhất), f_best (Makespan tối ưu)
```

---

## 📈 CHỈ SỐ ĐÁNH GIÁ

### Gap Percentage
```
Gap(%) = (Result - BKS) / BKS × 100%

Mức chất lượng:
  Gap = 0%           → Optimal ✓
  Gap < 5%           → Excellent (Xuất sắc)
  5% ≤ Gap < 10%     → Good (Tốt)
  10% ≤ Gap < 15%    → Fair (Chấp nhận được)
  Gap ≥ 15%          → Poor (Kém)
```

---

## 🎯 KỲ VỌNG HIỆU NĂNG

### Trên LA01 (10×5 jobs/machines)
```
Thời gian: ~1-2 giây
Makespan tìm được: 666 (= BKS)
Gap: 0.00% (Optimal)
Acceptance rate: ~50%
Iterations: ~20,000-25,000
```

### Trên LA instances lớn hơn
```
LA11-LA20: Gap 5-10%
LA21-LA30: Gap 10-15%
LA31-LA40: Gap 15-25% (khó hơn)
```

---

## 💾 CẤU HÌNH MẶC ĐỊNH

**File:** `config/config.py` - Lớp `SAConfig`

```python
class SAConfig:
    T0 = 1000.0                    # Nhiệt độ ban đầu
    T_min = 0.01                   # Nhiệt độ dừng
    alpha_explore = 0.98           # Hệ số làm lạnh (exploration)
    alpha_exploit = 0.95           # Hệ số làm lạnh (exploitation)
    L = 100                        # Markov chain length
    patience = 500                 # Early stopping threshold
    improvement_threshold = 0.01   # Cải thiện tối thiểu
    reheating_enabled = True       # Bật/tắt reheating
    reheating_factor = 0.9         # Hệ số hâm nóng
    swap_probability = 0.5         # Xác suất Swap (50%)
```

---

## 🔧 CẬU HÌNH TUNING GỢI Ý

### Cho Small Instances (10-15 jobs)
```python
config.T0 = 800.0                  # Nhiệt độ thấp hơn
config.L = 50                      # Ít lần lặp
config.patience = 300              # Dừng sớm hơn
```

### Cho Medium Instances (15-20 jobs)
```python
config.T0 = 1200.0                 # Nhiệt độ cao hơn
config.L = 100                     # Mặc định
config.patience = 500              # Mặc định
```

### Cho Large Instances (20-30 jobs)
```python
config.T0 = 1500.0                 # Nhiệt độ cao
config.L = 150                     # Lần lặp nhiều
config.patience = 800              # Kiên nhẫn hơn
config.alpha_explore = 0.99        # Khám phá lâu hơn
```

---

## 📝 GHI CHÚ QUAN TRỌNG

1. **Adaptive Cooling:** Không cố định α, mà thay đổi dựa trên tốc độ cải thiện
2. **Metropolis Criterion:** Cho phép chấp nhận giải pháp tệ hơn để thoát local optima
3. **Early Stopping:** Tiết kiệm thời gian khi hội tụ
4. **Reheating:** Tái khám phá không gian tìm kiếm khi bị sa lầy
5. **Operation Encoding:** Đảm bảo giải pháp khả thi mà không cần repair

---

**Nguồn tham khảo:**
- Lawrence, S. (1984). Resource constrained project scheduling
- Kirkpatrick, S., et al. (1983). Optimization by simulated annealing
- Metropolis, N., et al. (1953). Equation of state calculations
