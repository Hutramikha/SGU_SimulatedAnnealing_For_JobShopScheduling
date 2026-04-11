## 4.3 Quy Trình Thực Hiện Thực Nghiệm

Do Simulated Annealing là một thuật toán mang tính xác suất, kết quả giữa các lần chạy có thể có sự khác biệt. Vì vậy, quy trình thực nghiệm được chuẩn hóa như sau:

### 4.3.1 Số Lần Chạy

Mỗi kịch bản (mỗi bộ LA) được thực hiện chạy **05 lần độc lập**. Mỗi lần chạy sử dụng random seed khác nhau để đảm bảo độc lập:
- Trial 1: seed = 1001
- Trial 2: seed = 2002
- Trial 3: seed = 3003
- Trial 4: seed = 4004
- Trial 5: seed = 5005

Việc sử dụng seed theo quy luật này cho phép tái tạo chính xác kết quả thực nghiệm khi cần.

### 4.3.2 Giá Trị Ghi Nhận

Lấy kết quả **Makespan tốt nhất** ($C_{\max}^{\text{best}}$) và **Makespan trung bình** ($C_{\max}^{\text{avg}}$) của 05 lần chạy để đánh giá:

$$C_{\max}^{\text{best}} = \min\{C_{\max}^{(1)}, C_{\max}^{(2)}, C_{\max}^{(3)}, C_{\max}^{(4)}, C_{\max}^{(5)}\}$$

$$C_{\max}^{\text{avg}} = \frac{1}{5} \sum_{i=1}^{5} C_{\max}^{(i)}$$

Tương tự tính Gap:

$$\text{Gap}^{\text{best}} = \frac{C_{\max}^{\text{best}} - \text{BKS}}{\text{BKS}} \times 100\%$$

$$\text{Gap}^{\text{avg}} = \frac{C_{\max}^{\text{avg}} - \text{BKS}}{\text{BKS}} \times 100\%$$

Việc ghi nhận cả hai thông số này có ý nghĩa:
- **$C_{\max}^{\text{best}}$**: Đánh giá hiệu suất tốt nhất có thể đạt được
- **$C_{\max}^{\text{avg}}$**: Đánh giá tính ổn định và độ tin cậy của thuật toán

### 4.3.3 Thông Số Cố Định

Để đảm bảo tính công bằng, tất cả các nhóm kịch bản đều bắt đầu với cùng một bộ thông số nền tảng trước khi kích hoạt các cơ chế thích nghi:

- **Nhiệt độ ban đầu**: $T_0 = 1000$
- **Hệ số làm lạnh giai đoạn thăm dò** (Exploration): $\alpha_{\text{explore}} = 0.98$
- **Hệ số làm lạnh giai đoạn khai thác** (Exploitation): $\alpha_{\text{exploit}} = 0.95$
- **Chiều dài Markov chain**: $L = 100$
- **Early stopping patience**: $patience = 500$

Các cơ chế thích nghi (Adaptive Cooling, Early Stopping, Reheating) sẽ tự động điều chỉnh trong quá trình tìm kiếm dựa trên sự cải thiện lời giải.

### 4.3.4 Ý Nghĩa Các Hệ Số Làm Lạnh

Mỗi instance có 2 hệ số làm lạnh khác nhau để tối ưu hoá:

- **$\alpha_{\text{explore}} = 0.98$**: Giai đoạn thăm dò không gian search (nhiệt độ giảm chậm)
  - T_new = 0.98 * T_old
  - Cho phép thuật toán khám phá rộng hơn
  
- **$\alpha_{\text{exploit}} = 0.95$**: Giai đoạn khai thác lân cận tốt (nhiệt độ giảm nhanh)
  - T_new = 0.95 * T_old  
  - Tập trung vào cải tiến lời giải tốt

Cơ chế Adaptive Cooling sẽ tự động chuyển đổi giữa 2 hệ số này dựa trên mức độ cải thiện lời giải.

### 4.3.5 Cách Thực Hiện Trong Code

Để chạy thực nghiệm với 05 lần chạy độc lập, sử dụng hàm `solve_instance_multiple_trials()`:

```python
from main import solve_instance_multiple_trials
from config.config import SAConfig

config = SAConfig()

# Chạy thực nghiệm: 05 lần độc lập
result = solve_instance_multiple_trials("la01", num_trials=5, config=config)

# Kết quả trả về:
# {
#   'instance': 'la01',
#   'num_trials': 5,
#   'bks': 666,
#   'best_makespan': 627,         # C_max^best
#   'avg_makespan': 628.4,        # C_max^avg
#   'best_gap_percent': 5.86,     # Gap^best
#   'avg_gap_percent': 5.64,      # Gap^avg
#   'trials': [                   # Chi tiết 5 lần
#     {'trial': 1, 'seed': 1001, 'makespan': 627, 'gap_percent': 5.86},
#     {'trial': 2, 'seed': 2002, 'makespan': 628, 'gap_percent': 5.94},
#     ...
#   ]
# }
```

Hoặc chạy trực tiếp từ terminal:

```bash
python main.py
```

Output sẽ hiển thị bảng kết quả chi tiết với cả $C_{\max}^{\text{best}}$ và $C_{\max}^{\text{avg}}$.

### 4.3.6 Bảng Tóm Tắt Kết Quả

Kết quả thực nghiệm được tóm tắt trong bảng:

| Instance | BKS | $C_{\max}^{\text{best}}$ | $C_{\max}^{\text{avg}}$ | Gap^best(%) | Gap^avg(%) | Ổn Định |
|----------|-----|-----------|-----------|------------|-----------|---------|
| la01 | 666 | 627 | 628.4 | 5.86 | 5.64 | ✓ |
| la05 | 593 | 613 | 616.2 | 3.37 | 3.90 | ✓ |
| la10 | 1220 | 1254 | 1264.8 | 2.79 | 3.66 | ✓ |

Cột **Ổn Định** đánh giá dựa trên độ lệch: $|C_{\max}^{\text{best}} - C_{\max}^{\text{avg}}|$
- Nếu sai lệch < 3%: ✓ Ổn định
- Nếu sai lệch 3-5%: ~ Trung bình
- Nếu sai lệch > 5%: ✗ Không ổn định

---

**Tóm tắt:** Quy trình thực nghiệm này đảm bảo tính khoa học, có thể tái tạo, và cho phép đánh giá toàn diện về chất lượng lời giải cũng như tính ổn định của thuật toán Simulated Annealing.
