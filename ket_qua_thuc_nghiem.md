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
    - Đây là các bài toán có kích thước lớn nhất (15x15). `Best Gap` ở nhóm này (3.71% - 4.58%) vẫn giữ ở mức cạnh tranh và thậm chí còn tốt hơn so với `la25`. Điều này có thể được giải thích bởi các tham số của SA (`L=150`, `reheating_factor=0.85`) được điều chỉnh phù hợp hơn cho các không gian tìm kiếm lớn, cho phép thuật toán thoát khỏi các điểm tối ưu cục bộ hiệu quả hơn. Mặc dù vậy, `Avg Gap` vẫn còn tương đối cao (5.58% - 6.30%), khẳng định tính thách thức của các bài toán này.

### 4.5.3. Trực quan hóa và Phân tích hành vi thuật toán

Phân tích các biểu đồ giúp hiểu rõ hơn về *cách* thuật toán hoạt động và *lý do* tại sao kết quả lại khác nhau giữa các nhóm.

**Phân tích Biểu đồ hội tụ (Convergence Plot):**

Biểu đồ hội tụ ghi lại giá trị makespan tốt nhất tìm được qua từng vòng lặp, cho thấy "con đường" mà thuật toán đã đi để tìm kiếm lời giải.

1.  **Với nhóm Dễ (ví dụ `la01`):**
    - Biểu đồ hội tụ có dạng bậc thang, giảm nhanh qua nhiều bước và đạt đến giá trị tối ưu từ khá sớm (khoảng vòng lặp thứ 14,500). Điều này cho thấy thuật toán tìm ra lời giải tốt nhất rất nhanh và không có sự cải thiện nào thêm sau đó vì đã đạt đến cận dưới.
    *Hình 4.x: Biểu đồ hội tụ của `la01` cho thấy sự hội tụ nhanh về tối ưu (convergence_la01_trials.png)*

2.  **Với nhóm Trung bình (ví dụ `la20`):**
    - Quá trình hội tụ vẫn có dạng bậc thang nhưng các bước nhảy cải thiện lời giải diễn ra thường xuyên hơn so với nhóm Dễ. Thuật toán dành nhiều thời gian hơn để "khai thác" ở các mức makespan khác nhau trước khi tìm được bước nhảy vọt tiếp theo. Kết quả `Best Gap` rất thấp (0.55%) cho thấy thuật toán vẫn hoạt động hiệu quả và tìm được lời giải rất gần với tối ưu.
    *Hình 4.y: Biểu đồ hội tụ của `la20` (convergence_la20_trials.png)*

3.  **Với nhóm Khó (ví dụ `la21`):**
    - Đồ thị hội tụ của nhóm này cho thấy rõ sự phức tạp tăng lên. Quá trình tìm kiếm trở nên "gập ghềnh" hơn với nhiều bước cải thiện nhỏ và liên tục, thay vì các bước nhảy lớn. Cơ chế tái nung (reheating) bắt đầu thể hiện vai trò rõ hơn qua các "gai" nhỏ, giúp thuật toán thoát khỏi các điểm tối ưu cục bộ. Sự chênh lệch giữa `Best Gap` và `Avg Gap` cũng được thể hiện qua sự phân tán của các đường hội tụ giữa các lần chạy.
    *Hình 4.z: Biểu đồ hội tụ của `la21` cho thấy quá trình tìm kiếm phức tạp hơn (convergence_la21_trials.png)*

4.  **Với nhóm Cực khó (ví dụ `la36`):**
    - Đồ thị có dạng bậc thang dốc và rất gập ghềnh, bao gồm vô số các bước cải thiện nhỏ và liên tục. Điều này cho thấy một quá trình tìm kiếm rất chi tiết và vất vả trong một không gian lời giải phức tạp. Vai trò của cơ chế tái nung (reheating) được thể hiện một cách gián tiếp: sau các giai đoạn đi ngang ngắn (có nguy cơ bị kẹt), thuật toán vẫn liên tục tìm được các bước nhảy xuống để cải thiện lời giải, chứng tỏ khả năng thoát khỏi tối ưu cục bộ thành công. Đường cong hội tụ vẫn còn xu hướng đi xuống ở những vòng lặp cuối, gợi ý rằng nếu có thêm thời gian tính toán, kết quả có thể còn được cải thiện thêm.
    *Hình 4.t: Biểu đồ hội tụ của `la36` cho thấy vai trò rõ rệt của cơ chế tái nung (convergence_la36_trials.png)*

**Trực quan hóa lịch trình tối ưu: Biểu đồ Gantt**

Trong khi biểu đồ hội tụ phân tích *quá trình*, biểu đồ Gantt minh họa cho *kết quả cuối cùng*. Nó trực quan hóa lịch trình sản xuất tối ưu mà thuật toán đã tìm ra.

Quan sát biểu đồ Gantt của bài toán `la20` (Hình 4.u), ta có thể thấy một số đặc điểm của một lời giải tốt:
- Lịch trình được xếp khá "đặc", các công việc được bố trí san sát nhau trên hầu hết các máy, cho thấy hiệu suất sử dụng tài nguyên cao.
- Mặc dù vẫn tồn tại các khoảng thời gian rỗi (idle time) do ràng buộc công nghệ, nhưng không có những khoảng trống quá lớn, chứng tỏ lịch trình đã được tối ưu hiệu quả.
- Điểm kết thúc của công việc cuối cùng trên biểu đồ xác định giá trị makespan tốt nhất mà thuật toán tìm được.

Do đó, biểu đồ Gantt được dùng như một minh chứng trực quan cho chất lượng của lời giải mà thuật toán đã tạo ra.

*Hình 4.u: Biểu đồ Gantt cho lời giải tốt nhất của bài toán `la20` (gantt_la20_trials.png)*

**Kết luận chung:**

Thuật toán SA được đề xuất đã chứng minh được hiệu quả trên nhiều loại bài toán JSSP. Nó hoạt động xuất sắc trên các bài toán nhỏ và cho kết quả cạnh tranh trên các bài toán lớn và phức tạp. Sự cân bằng giữa khám phá và khai thác, cùng với cơ chế tái nung, là chìa khóa cho hiệu suất của thuật toán. Tuy nhiên, vẫn còn khoảng trống để cải thiện, đặc biệt là tính ổn định (giảm `Avg Gap`) trên các bài toán có độ khó cao.

## 4.6. Đánh giá hiệu quả của các cải tiến

Hiệu quả của thuật toán SA được trình bày trong các mục trên không chỉ đến từ bản chất của thuật toán gốc, mà còn từ hai cải tiến quan trọng được tích hợp nhằm tăng cường khả năng tìm kiếm và thoát khỏi các điểm tối ưu cục bộ. Việc điều chỉnh các tham số như chiều dài chuỗi Markov (`L=150`) là một bước tinh chỉnh quan trọng, nhưng nền tảng cho hiệu suất của thuật toán đến từ các cơ chế cốt lõi sau:

### 4.6.1. Lịch trình làm nguội thích ứng (Adaptive Cooling Schedule)

Đây là cơ chế điều khiển "tốc độ" tìm kiếm của thuật toán. Thay vì dùng một hệ số làm nguội `alpha` duy nhất, thuật toán sử dụng một lịch trình hai giai đoạn:
- **Giai đoạn khám phá (Exploration):** Với `alpha_explore = 0.98`, nhiệt độ giảm chậm. Điều này cho phép thuật toán chấp nhận cả những lời giải kém hơn trong thời gian dài, thúc đẩy việc "khám phá" các vùng rộng lớn của không gian tìm kiếm và tránh hội tụ quá sớm vào một lời giải tốt nhưng chưa phải tối ưu.
- **Giai đoạn khai thác (Exploitation):** Khi nhiệt độ giảm xuống một ngưỡng nhất định, hệ số `alpha_exploit = 0.95` được áp dụng, làm nhiệt độ giảm nhanh hơn. Thuật toán trở nên "tham lam" hơn, tập trung vào việc "khai thác" và tinh chỉnh xung quanh các khu vực có lời giải tốt đã tìm thấy.

**Hiệu quả:** Cơ chế này tạo ra sự cân bằng thông minh giữa việc tìm kiếm trên diện rộng và tinh chỉnh cục bộ. Nó giúp thuật toán vừa có khả năng tìm ra các khu vực hứa hẹn trên toàn cục, vừa có khả năng hội tụ nhanh khi đã ở gần điểm tối ưu.

### 4.6.2. Cơ chế kiểm soát hội tụ và tái khám phá

Cơ chế này là sự kết hợp giữa tiêu chuẩn chấp nhận Metropolis và kỹ thuật tái nung (reheating), đóng vai trò then chốt trong việc giúp thuật toán thoát khỏi các điểm tối ưu cục bộ.

- **Tiêu chuẩn chấp nhận Metropolis:** Cho phép thuật toán chấp nhận một lời giải xấu hơn với một xác suất nhất định. Đây là nền tảng giúp SA khác biệt với các thuật toán tìm kiếm cục bộ đơn thuần.
- **Cơ chế Tái nung (Reheating):** Đây là cải tiến quan trọng nhất giúp thuật toán giải quyết các bài toán phức tạp. Khi thuật toán không tìm thấy lời giải tốt hơn sau một số vòng lặp nhất định (`patience`), nhiệt độ sẽ được tăng trở lại một cách đột ngột (`T = T / reheating_factor`). Vì `reheating_factor` có giá trị 0.85 (nhỏ hơn 1), phép chia này thực chất sẽ làm **tăng** nhiệt độ, giúp thuật toán "hâm nóng" lại quá trình tìm kiếm.

**Hiệu quả:**
- **Thoát khỏi tối ưu cục bộ:** Vai trò của tái nung được thể hiện rõ nhất trên các biểu đồ hội tụ của các bài toán khó như `la21` và `la36`. Khi đồ thị đi ngang (dấu hiệu bị kẹt), một cú "sốc" nhiệt độ sẽ giúp thuật toán chấp nhận các nước đi xấu, từ đó "nhảy" ra khỏi thung lũng tối ưu cục bộ và tiếp tục tìm kiếm ở một khu vực khác.
- **Cải thiện kết quả ở bài toán khó:** Kết quả thực nghiệm cho thấy `Best Gap` của nhóm "Cực khó" (`la36`, `la40`) lại tốt hơn một số bài toán ở nhóm "Khó" (`la25`). Điều này chứng tỏ cơ chế tái nung hoạt động đặc biệt hiệu quả trên các không gian tìm kiếm khổng lồ và phức tạp, nơi khả năng bị mắc kẹt là rất cao. Nếu không có cơ chế này, thuật toán có thể đã dừng lại ở một lời giải kém chất lượng hơn nhiều.

**Kết luận:** Tóm lại, cơ chế này là "van an toàn" của thuật toán. Nó cho phép SA vừa duy trì khả năng khám phá cơ bản (Metropolis), vừa có một chiến lược mạnh mẽ (Tái nung) để can thiệp khi quá trình tìm kiếm bị đình trệ, đảm bảo hiệu quả trên cả những bài toán khó nhất.

**Tổng kết:** Sự kết hợp của hai cải tiến trên đã tạo ra một thuật toán SA mạnh mẽ và linh hoạt. Lịch trình làm nguội thích ứng cân bằng giữa khám phá và khai thác, trong khi cơ chế kiểm soát hội tụ và tái khám phá cung cấp "sức mạnh" cần thiết để giải quyết các bài toán quy mô lớn và phức tạp, giúp thuật toán tránh được những cạm bẫy phổ biến của các phương pháp tìm kiếm cục bộ.
