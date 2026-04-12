"""
Configuration module - Cấu hình tham số cho thuật toán SA
"""
from pathlib import Path


class SAConfig:
    """Lớp quản lý toàn bộ tham số của thuật toán Simulated Annealing"""
    
    def __init__(self):
        # Resolve paths từ project root
        project_root = Path(__file__).parent.parent
        
        # ==================== THAM SỐ NHIỆT ĐỘ ====================
        self.T0 = 1000.0           # Nhiệt độ ban đầu
        self.T0_initial = self.T0   # Lưu nhiệt độ ban đầu để reset giữa các lần chạy
        self.T_min = 0.01          # Nhiệt độ dừng (ngưỡng dừng)
        
        # ==================== THAM SỐ LÀMẠNH ====================
        self.alpha_explore = 0.98  # Hệ số làm lạnh giai đoạn thăm dò (exploration)
        self.alpha_exploit = 0.95  # Hệ số làm lạnh giai đoạn khai thác (exploitation)
        
        # ==================== MARKOV CHAIN ====================
        self.L = 150               # Số vòng lặp tại mỗi mức nhiệt độ (Markov chain length)
        
        # ==================== EARLY STOPPING & REHEATING ====================
        self.patience = 500        # Số vòng lặp không cải thiện trước khi dừng sớm
        self.improvement_threshold = 0.01  # Tỷ lệ cải thiện tối thiểu (%)
        self.reheating_enabled = True      # Bật/tắt cơ chế hâm nóng lại
        self.reheating_factor = 0.9        # Hệ số hâm nóng lại (T_new = T_old * reheating_factor)
        
        # ==================== TOÁN TỬ LÂN CẬN ====================
        self.swap_probability = 0.5   # Xác suất sử dụng toán tử Swap (50% Swap, 50% Move)
        
        # ==================== CẤU HÌNH DỮ LIỆU ====================
        # Sử dụng absolute paths từ project_root để hoạt động từ bất kỳ directory nào
        self.data_dir = project_root / "data"           # Thư mục chứa dữ liệu
        self.results_dir = project_root / "results"     # Thư mục chứa kết quả
        self.bks_file = project_root / "data" / "LA_BKS.csv"  # File chứa Best Known Solutions
        
        # ==================== CẤU HÌNH XUẤT RA ====================
        self.verbose = True           # In chi tiết quá trình làm việc
        self.save_results = True      # Lưu kết quả xuống file
        self.plot_convergence = True  # Vẽ đồ thị hội tụ
        self.plot_gantt = True        # Vẽ biểu đồ Gantt
        self.save_interval = 50       # In log mỗi N vòng lặp
    
    def display(self):
        """Hiển thị tất cả cấu hình hiện tại"""
        print("="*70)
        print("CẤU HÌNH THUẬT TOÁN SIMULATED ANNEALING")
        print("="*70)
        print(f"Nhiệt độ ban đầu (T0):           {self.T0}")
        print(f"Nhiệt độ dừng (T_min):          {self.T_min}")
        print(f"Hệ số làm lạnh (exploration):   {self.alpha_explore}")
        print(f"Hệ số làm lạnh (exploitation):  {self.alpha_exploit}")
        print(f"Chiều dài Markov chain (L):     {self.L}")
        print(f"Early stopping patience:        {self.patience}")
        print(f"Reheating enabled:              {self.reheating_enabled}")
        print(f"Xác suất Swap:                  {self.swap_probability}")
        print("="*70)


# Tạo instance mặc định
config = SAConfig()
