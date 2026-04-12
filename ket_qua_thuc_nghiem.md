# Báo cáo kết quả thực nghiệm

## 4.5. Kết quả thực nghiệm và phân tích trực quan

Phần này trình bày chi tiết kết quả thực nghiệm của thuật toán SA đã được tinh chỉnh trên bộ dữ liệu benchmark của Lawrence (1984). Các thí nghiệm được thực hiện trên 8 bài toán đại diện, được phân thành 4 nhóm dựa trên kích thước và độ khó: Dễ, Trung bình, Khó và Cực khó.

Để đảm bảo tính khách quan và ổn định của kết quả, mỗi bài toán được chạy độc lập 5 lần với các seed ngẫu nhiên khác nhau (1001, 2002, 3003, 4004, 5005). Các chỉ số được ghi nhận bao gồm:
- **Best Gap (%)**: Độ lệch phần trăm giữa makespan tốt nhất tìm được so với giá trị cận dưới (Lower Bound - LB).
- **Avg Gap (%)**: Độ lệch phần trăm trung bình của makespan sau 5 lần chạy so với LB.
- **Avg Time (s)**: Thời gian chạy trung bình của mỗi lần thực thi.

### 4.5.1. Kết quả thực nghiệm tổng hợp

Bảng dưới đây tổng hợp kết quả của 8 bài toán, được nhóm theo độ khó.

| Nhóm | Bài toán (Instance) | Kích thước (Jobs x Machines) | LB | Best Gap (%) | Avg Gap (%) | Avg Time (s) |
| :--- | :--- | :--- | :-: | :---: | :---: | :---: |
| **Dễ** | `la01` | 10x5 | 666 | **0.00** | 0.00 | 0.870 |
| | `la05` | 10x5 | 593 | **0.00** | 0.00 | 0.879 |
| **Trung bình** | `la16` | 10x10 | 945 | **3.92** | 4.51 | 1.582 |
| | `la20` | 10x10 | 902 | **0.55** | 1.69 | 2.559 |
| **Khó** | `la21` | 15x10 | 1046 | **3.15** | 5.03 | 2.236 |
| | `la25` | 15x10 | 977 | **5.63** | 7.76 | 2.231 |
| **Cực khó** | `la36` | 15x15 | 1268 | **3.71** | 5.58 | 3.514 |
| | `la40` | 15x15 | 1222 | **4.58** | 6.30 | 3.316 |

### 4.5.2. Phân tích chi tiết và trực quan hóa

**Phân tích kết quả:**

1.  **Nhóm Dễ (`la01`, `la05`):**
    - Với kích thước nhỏ (10x5), thuật toán SA tỏ ra cực kỳ hiệu quả, luôn tìm thấy lời giải tối ưu (makespan bằng với LB) trong tất cả các lần chạy, thể hiện qua `Best Gap` và `Avg Gap` đều là 0%. Thời gian chạy trung bình rất nhanh, dưới 1 giây.

2.  **Nhóm Trung bình (`la16`, `la20`):**
    - Kích thước bài toán tăng lên (10x10). Thuật toán vẫn cho kết quả rất tốt, đặc biệt là với `la20` khi `Best Gap` chỉ là 0.55%. Kết quả của `la16` (`Best Gap` 3.92%) cũng ở mức cạnh tranh. `Avg Gap` thấp cho thấy thuật toán hoạt động ổn định trên các bài toán có độ phức tạp vừa phải này.

3.  **Nhóm Khó (`la21`, `la25`):**
    - Khi số lượng jobs tăng lên (15x10), không gian tìm kiếm trở nên lớn hơn đáng kể. `Best Gap` tìm được nằm trong khoảng 3.15% - 5.63%. Đáng chú ý, `Avg Gap` ở nhóm này (5.03% - 7.76%) cao hơn rõ rệt so với `Best Gap`, cho thấy thuật toán gặp nhiều khó khăn hơn trong việc tìm kiếm lời giải chất lượng cao một cách nhất quán. Sự khác biệt giữa các lần chạy lớn hơn, cho thấy một số lần chạy có thể bị mắc kẹt ở các điểm tối ưu cục bộ.

4.  **Nhóm Cực khó (`la36`, `la40`):**
    - Đây là các bài toán có kích thước lớn nhất (15x15). `Best Gap` ở nhóm này (3.71% - 4.58%) vẫn giữ ở mức cạnh tranh và thậm chí còn tốt hơn so với `la25`. Điều này có thể được giải thích bởi các tham số của SA (`L=150`, `reheating_factor=0.85`) được điều chỉnh phù hợp hơn cho các không gian tìm kiếm lớn, cho phép thuật toán thoát khỏi các điểm tối ưu cục bộ hiệu quả hơn. Mặc dù vậy, `Avg Gap` vẫn còn tương đối cao (5.5% - 6.3%), khẳng định tính thách thức của các bài toán này.

### 4.5.3. Trực quan hóa và Phân tích hành vi thuật toán

Phân tích các biểu đồ giúp hiểu rõ hơn về *cách* thuật toán hoạt động và *lý do* tại sao kết quả lại khác nhau giữa các nhóm.

**Phân tích Biểu đồ hội tụ (Convergence Plot):**

Biểu đồ hội tụ ghi lại giá trị makespan tốt nhất tìm được qua từng vòng lặp, cho thấy "con đường" mà thuật toán đã đi để tìm kiếm lời giải.

1.  **Với nhóm Dễ (ví dụ `la01`):**
    - Biểu đồ hội tụ có dạng dốc đứng ở giai đoạn đầu và nhanh chóng đạt đến một đường thẳng nằm ngang ở giá trị tối ưu. Điều này cho thấy thuật toán tìm ra lời giải tốt nhất rất nhanh và không có sự cải thiện nào thêm sau đó vì đã đạt đến cận dưới.
    *Hình 4.x: Biểu đồ hội tụ của `la01` cho thấy sự hội tụ nhanh về tối ưu (convergence_la01_trials.png)*

2.  **Với nhóm Trung bình và Khó (ví dụ `la20`, `la21`):**
    - Quá trình hội tụ chậm hơn. Đồ thị có dạng bậc thang, với các giai đoạn đi ngang (khai thác) xen kẽ với các bước nhảy xuống (tìm thấy lời giải tốt hơn). Cơ chế tái nung (reheating) có thể xuất hiện dưới dạng các "gai" nhỏ, khi thuật toán cố gắng thoát khỏi các điểm tối ưu cục bộ. Sự khác biệt giữa `Best Gap` và `Avg Gap` (đặc biệt ở `la21`, `la25`) được thể hiện qua sự biến động của các đường hội tụ giữa 5 lần chạy.
    *Hình 4.y: Biểu đồ hội tụ của `la21` cho thấy quá trình tìm kiếm phức tạp hơn (convergence_la21_trials.png)*

3.  **Với nhóm Cực khó (ví dụ `la36`):**
    - Biểu đồ trở nên "nhiễu" hơn rất nhiều. Các bước nhảy vọt của makespan khi tái nung (reheating) trở nên rõ ràng và thường xuyên hơn. Đây là minh chứng cho thấy thuật toán đang tích cực chống lại việc bị mắc kẹt trong một không gian tìm kiếm khổng lồ và phức tạp. Đường cong hội tụ có thể vẫn còn xu hướng đi xuống ở những vòng lặp cuối cùng, gợi ý rằng nếu có thêm thời gian tính toán, kết quả có thể còn được cải thiện thêm.
    *Hình 4.z: Biểu đồ hội tụ của `la36` cho thấy vai trò rõ rệt của cơ chế tái nung (convergence_la36_trials.png)*

**Minh họa lời giải bằng Biểu đồ Gantt (Gantt Chart):**

Trong khi biểu đồ hội tụ phân tích *quá trình*, biểu đồ Gantt minh họa cho *kết quả cuối cùng*. Nó trực quan hóa lịch trình sản xuất tối ưu mà thuật toán đã tìm ra. Thay vì phân tích sâu, biểu đồ Gantt được dùng như một minh chứng trực quan cho một lời giải tốt. Dưới đây là gợi ý để minh họa cho lịch trình của bài toán `la20`, bài toán có kết quả `Best Gap` tốt nhất trong các nhóm phức tạp.

*Hình 4.t: Biểu đồ Gantt cho lời giải tốt nhất của bài toán `la20` (gantt_la20_trials.png)*

**Kết luận chung:**

Thuật toán SA được đề xuất đã chứng minh được hiệu quả trên nhiều loại bài toán JSSP. Nó hoạt động xuất sắc trên các bài toán nhỏ và cho kết quả cạnh tranh trên các bài toán lớn và phức tạp. Sự cân bằng giữa khám phá và khai thác, cùng với cơ chế tái nung, là chìa khóa cho hiệu suất của thuật toán. Tuy nhiên, vẫn còn khoảng trống để cải thiện, đặc biệt là tính ổn định (giảm `Avg Gap`) trên các bài toán có độ khó cao.
