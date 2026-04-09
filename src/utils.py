"""
Module: utils.py
Chức năng: Các hàm hỗ trợ chung cho thuật toán SA
"""

import random
import numpy as np
from typing import List, Tuple


class NeighborhoodOperators:
    """Lớp chứa các toán tử lân cận (Swap và Move)"""
    
    @staticmethod
    def swap(solution: List[int]) -> List[int]:
        """
        Toán tử SWAP: Hoán đổi hai vị trí ngẫu nhiên
        
        Chọn ngẫu nhiên hai vị trí i và j, đổi chỗ phần tử tại đó
        
        Args:
            solution: Dãy mã hóa hiện tại
        
        Returns:
            List[int]: Dãy mã hóa mới sau khi Swap
        """
        new_solution = solution.copy()
        n = len(new_solution)
        
        # Chọn 2 vị trí khác nhau
        i, j = random.sample(range(n), 2)
        
        # Hoán đổi
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        
        return new_solution
    
    @staticmethod
    def move(solution: List[int]) -> List[int]:
        """
        Toán tử MOVE: Lấy một phần tử và chèn tại vị trí khác
        
        Chọn ngẫu nhiên vị trí i, lấy phần tử đó và chèn vào vị trí j
        
        Args:
            solution: Dãy mã hóa hiện tại
        
        Returns:
            List[int]: Dãy mã hóa mới sau khi Move
        """
        new_solution = solution.copy()
        n = len(new_solution)
        
        # Chọn vị trí cần di chuyển
        i = random.randint(0, n - 1)
        
        # Chọn vị trí đích (khác với i)
        j = random.randint(0, n - 1)
        while j == i:
            j = random.randint(0, n - 1)
        
        # Lấy phần tử
        element = new_solution.pop(i)
        
        # Chèn vào vị trí mới
        new_solution.insert(j, element)
        
        return new_solution
    
    @staticmethod
    def get_neighbor(solution: List[int], swap_prob: float = 0.5) -> List[int]:
        """
        Lấy một nghiệm lân cận dựa vào xác suất
        
        Args:
            solution: Dãy mã hóa hiện tại
            swap_prob: Xác suất sử dụng Swap (1 - swap_prob là xác suất Move)
        
        Returns:
            List[int]: Nghiệm lân cận mới
        """
        if random.random() < swap_prob:
            return NeighborhoodOperators.swap(solution)
        else:
            return NeighborhoodOperators.move(solution)


class CoolingSchedule:
    """Lớp quản lý hệ thống làm lạnh (Cooling Schedule)"""
    
    @staticmethod
    def geometric_cooling(current_temp: float, alpha: float) -> float:
        """
        Làm lạnh hình học: T_new = alpha * T_old
        
        Args:
            current_temp: Nhiệt độ hiện tại
            alpha: Hệ số làm lạnh (0 < alpha < 1)
        
        Returns:
            float: Nhiệt độ mới
        """
        return alpha * current_temp
    
    @staticmethod
    def adaptive_cooling(current_temp: float, 
                        makespan_best: int,
                        makespan_prev: int,
                        alpha_explore: float = 0.98,
                        alpha_exploit: float = 0.95,
                        improvement_threshold: float = 0.01) -> Tuple[float, float]:
        """
        Làm lạnh thích nghi: Điều chỉnh alpha dựa trên trạng thái hội tụ
        
        Nguyên lý:
        - Nếu có cải thiện đáng kể: Duy trì alpha cao (exploration)
        - Nếu ít cải thiện: Tăng alpha_exploit (exploitation - tập trung tinh chỉnh)
        
        Args:
            current_temp: Nhiệt độ hiện tại
            makespan_best: Makespan tốt nhất tìm được
            makespan_prev: Makespan ở vòng lặp trước
            alpha_explore: Hệ số khi đang thăm dò
            alpha_exploit: Hệ số khi đang khai thác
            improvement_threshold: Tỷ lệ cải thiện tối thiểu (%)
        
        Returns:
            Tuple: (new_temp, alpha_used)
        """
        # Tính tỷ lệ cải thiện
        if makespan_prev == 0:
            improvement_rate = 0
        else:
            improvement_rate = abs(makespan_prev - makespan_best) / makespan_prev
        
        # Chọn alpha dựa trên tỷ lệ cải thiện
        if improvement_rate > improvement_threshold:
            # Còn cải thiện tốt, tiếp tục exploration
            alpha = alpha_explore
        else:
            # Ít cải thiện, chuyển sang exploitation
            alpha = alpha_exploit
        
        new_temp = alpha * current_temp
        return new_temp, alpha


class MetropolisAcceptance:
    """Lớp thực hiện tiêu chí chấp nhận Metropolis"""
    
    @staticmethod
    def accept_probability(delta: int, temperature: float) -> float:
        """
        Tính xác suất chấp nhận nghiệm mới theo thuật toán Metropolis
        
        P(accept s') = 1           nếu Δ < 0
                       exp(-Δ/T)   nếu Δ ≥ 0
        
        Trong đó: Δ = f(s') - f(s)
        
        Args:
            delta: Độ chênh lệch năng lượng (makespan_new - makespan_old)
            temperature: Nhiệt độ hiện tại
        
        Returns:
            float: Xác suất chấp nhận trong [0, 1]
        """
        if delta < 0:
            # Nghiệm tốt hơn, chấp nhận ngay
            return 1.0
        else:
            # Nghiệm tệ hơn, tính xác suất
            if temperature == 0:
                return 0.0
            return np.exp(-delta / temperature)
    
    @staticmethod
    def should_accept(delta: int, temperature: float) -> bool:
        """
        Quyết định có nên chấp nhận nghiệm mới không
        
        Args:
            delta: Độ chênh lệch năng lượng
            temperature: Nhiệt độ hiện tại
        
        Returns:
            bool: True nếu chấp nhận, False nếu không
        """
        prob = MetropolisAcceptance.accept_probability(delta, temperature)
        return random.random() < prob


class EarlyStoppingChecker:
    """Lớp kiểm tra điều kiện Early Stopping"""
    
    def __init__(self, patience: int = 500, 
                 improvement_threshold: float = 0.01):
        """
        Khởi tạo Early Stopping Checker
        
        Args:
            patience: Số vòng lặp không cải thiện trước khi dừng
            improvement_threshold: Tỷ lệ cải thiện tối thiểu (%)
        """
        self.patience = patience
        self.improvement_threshold = improvement_threshold
        self.no_improvement_count = 0
        self.best_makespan = float('inf')
    
    def check(self, current_makespan: int) -> Tuple[bool, str]:
        """
        Kiểm tra có nên dừng sớm không
        
        Args:
            current_makespan: Makespan hiện tại
        
        Returns:
            Tuple: (should_stop, reason)
        """
        # Tính cải thiện
        improvement_rate = (self.best_makespan - current_makespan) / self.best_makespan \
                          if self.best_makespan != float('inf') else 1.0
        
        if improvement_rate > self.improvement_threshold:
            # Có cải thiện đáng kể
            self.best_makespan = current_makespan
            self.no_improvement_count = 0
            return False, "Có cải thiện"
        else:
            # Ít cải thiện
            self.no_improvement_count += 1
            
            if self.no_improvement_count >= self.patience:
                return True, f"Dừng sớm: {self.no_improvement_count} vòng không cải thiện"
            
            return False, f"Không cải thiện {self.no_improvement_count}/{self.patience}"
    
    def reset(self):
        """Reset trạng thái Early Stopping (dùng khi Reheating)"""
        self.no_improvement_count = 0
        self.best_makespan = float('inf')


def format_time(seconds: float) -> str:
    """
    Định dạng thời gian thành chuỗi dễ đọc
    
    Args:
        seconds: Số giây
    
    Returns:
        str: Chuỗi thời gian (ví dụ: "1m 23s", "45s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
