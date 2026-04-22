"""
Module: sa_solver.py
Chức năng: Thuật toán Simulated Annealing cải tiến để giải JSSP
- Các giai đoạn: Khởi tạo, tìm kiếm, giảm nhiệt, dừng
- Cơ chế làm lạnh thích nghi, Early Stopping, Reheating
- Cơ chế chấp nhận Metropolis
"""

import time
import sys
from typing import List, Dict, Tuple
from .jssp_model import JSSPModel
from .utils import NeighborhoodOperators, CoolingSchedule, MetropolisAcceptance, EarlyStoppingChecker

# Fix UTF-8 encoding on Windows
try:
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass  # Fallback nếu reconfigure không hỗ trợ


class SASolver:
    """Lớp giải bài toán JSSP bằng thuật toán Simulated Annealing"""
    
    def __init__(self, jssp_model: JSSPModel, config):
        """
        Khởi tạo SA Solver
        
        Args:
            jssp_model: Model JSSP
            config: Đối tượng cấu hình (SAConfig)
        """
        self.model = jssp_model
        self.config = config
        
        # Trạng thái giải pháp
        self.current_solution = None
        self.best_solution = None
        self.best_makespan = float('inf')
        self.current_makespan = float('inf')
        
        # Thống kê
        self.history = {
            'makespan': [],
            'temperature': [],
            'iterations': [],
            'accepted_count': 0,
            'rejected_count': 0
        }
        
        # Early Stopping Checker - khởi tạo một lần
        self.early_stopper = EarlyStoppingChecker(
            self.config.patience,
            self.config.improvement_threshold
        )
    
    def solve(self) -> Tuple[List[int], int, Dict]:
        """
        Giải bài toán JSSP bằng SA
        
        Trả về:
            Tuple:
                - best_solution: Dãy mã hóa tốt nhất tìm được
                - best_makespan: Giá trị Makespan tốt nhất
                - history: Dict chứa lịch sử tìm kiếm
        """
        if self.config.verbose:
            try:
                print(f"\n{'='*70}")
                print("GIAI THUAT SIMULATED ANNEALING")
                print(f"{'='*70}")
            except Exception:
                print(f"\n{'='*70}")
                print("SIMULATED ANNEALING ALGORITHM")
                print(f"{'='*70}")
            try:
                self.config.display()
            except Exception as e:
                print(f"[INFO] Could not display config details: {type(e).__name__}")
        
        start_time = time.time()
        
        # Giai đoạn 1: Khởi tạo
        self._phase_initialization()
        
        # Giai đoạn 2-3: Vòng lặp tìm kiếm
        iteration = 0
        reheating_count = 0
        
        while self.config.T0 > self.config.T_min:
            # Vòng lặp trong (Markov chain)
            for _ in range(self.config.L):
                iteration += 1
                
                # Sinh nghiệm lân cận
                neighbor_solution = NeighborhoodOperators.get_neighbor(
                    self.current_solution, 
                    self.config.swap_probability
                )
                
                # Tính Makespan
                neighbor_makespan = self.model.calculate_makespan(neighbor_solution)
                delta = neighbor_makespan - self.current_makespan
                
                # Tiêu chí chấp nhận Metropolis
                if MetropolisAcceptance.should_accept(delta, self.config.T0):
                    self.current_solution = neighbor_solution
                    self.current_makespan = neighbor_makespan
                    self.history['accepted_count'] += 1
                    
                    # Cập nhật best solution
                    if neighbor_makespan < self.best_makespan:
                        self.best_solution = neighbor_solution
                        self.best_makespan = neighbor_makespan
                else:
                    self.history['rejected_count'] += 1
            
            # Lưu lịch sử
            self.history['makespan'].append(self.best_makespan)
            self.history['temperature'].append(self.config.T0)
            self.history['iterations'].append(iteration)
            
            # In log
            if self.config.verbose and iteration % self.config.save_interval == 0:
                self._print_progress(iteration)
            
            # Giai đoạn 3: Giảm nhiệt độ (làm lạnh thích nghi)
            new_temp, alpha_used = CoolingSchedule.adaptive_cooling(
                self.config.T0,
                self.best_makespan,
                self.history['makespan'][-1] if len(self.history['makespan']) > 0 else self.best_makespan,
                self.config.alpha_explore,
                self.config.alpha_exploit,
                self.config.improvement_threshold
            )
            self.config.T0 = new_temp
            
            # Kiểm tra Early Stopping (độc lập với Reheating)
            should_stop, reason = self.early_stopper.check(self.best_makespan)
            
            if should_stop:
                # Early Stopping trigger
                if self.config.reheating_enabled:
                    # Thực hiện Reheating
                    self.config.T0 = self.config.T0 / self.config.reheating_factor
                    reheating_count += 1
                    
                    if self.config.verbose:
                        print(f"[REHEAT] Reheating #{reheating_count}: T = {self.config.T0:.4f} ({reason})")
                    
                    # Reset Early Stopper để cho phép tìm kiếm tiếp
                    self.early_stopper.reset()
                else:
                    # Không reheating, dừng luôn
                    if self.config.verbose:
                        print(f"[STOP] {reason}")
                    break
        
        # Giai đoạn 4: In kết quả
        elapsed_time = time.time() - start_time
        
        if self.config.verbose:
            self._print_results(elapsed_time, iteration)
        
        return self.best_solution, self.best_makespan, self.history
    
    def _phase_initialization(self):
        """Giai đoạn 1: Khởi tạo"""
        # Reset ALL state from previous runs
        self.early_stopper.reset()
        
        # CRITICAL: Reset history dict - prevents state pollution from previous instance
        self.history = {
            'makespan': [],
            'temperature': [],
            'iterations': [],
            'accepted_count': 0,
            'rejected_count': 0
        }
        
        # Reset temperature to initial value
        self.config.T0 = self.config.T0_initial
        
        # Sinh lời giải ngẫu nhiên
        self.current_solution = self.model.generate_random_solution()
        self.current_makespan = self.model.calculate_makespan(self.current_solution)
        
        # Cập nhật best solution
        self.best_solution = self.current_solution.copy()
        self.best_makespan = self.current_makespan
        
        if self.config.verbose:
            try:
                print(f"\n[OK] Khoi tao:")
                print(f"  - Loi giai ban dau: Makespan = {self.current_makespan}")
            except Exception:
                print(f"\n[OK] Initialization:")
                print(f"  - Initial Solution: Makespan = {self.current_makespan}")
    
    def _print_progress(self, iteration: int):
        """In thông tin tiến độ"""
        try:
            print(f"Lap {iteration:6d} | T = {self.config.T0:10.6f} | "
                  f"Best = {self.best_makespan:6d} | "
                  f"Accepted = {self.history['accepted_count']:6d} | "
                  f"Rejected = {self.history['rejected_count']:6d}")
        except Exception as e:
            print(f"Iteration {iteration:6d} | T = {self.config.T0:10.6f} | "
                  f"Best = {self.best_makespan:6d} | "
                  f"Accepted = {self.history['accepted_count']:6d} | "
                  f"Rejected = {self.history['rejected_count']:6d}")
    
    def _print_results(self, elapsed_time: float, total_iterations: int):
        """In kết quả cuối cùng"""
        try:
            print(f"\n{'='*70}")
            print("KET QUA CUOI CUNG")
            print(f"{'='*70}")
            print(f"Makespan tot nhat:   {self.best_makespan}")
            print(f"Tong lap:            {total_iterations}")
            print(f"Chap nhan:           {self.history['accepted_count']}")
            print(f"Tu choi:             {self.history['rejected_count']}")
            print(f"Thoi gian:           {elapsed_time:.2f} giay")
            
            # Check trước khi chia để tránh division by zero
            total_decisions = self.history['accepted_count'] + self.history['rejected_count']
            if total_decisions > 0:
                acceptance_rate = self.history['accepted_count'] / total_decisions * 100
                print(f"Ty le chap nhan:     {acceptance_rate:.1f}%")
            else:
                print(f"Ty le chap nhan:     N/A (Khong co quyet dinh)")
            
            print(f"{'='*70}\n")
        except Exception as e:
            # Fallback ASCII version
            print(f"\n{'='*70}")
            print("RESULTS")
            print(f"{'='*70}")
            print(f"Best Makespan:   {self.best_makespan}")
            print(f"Total Iterations: {total_iterations}")
            print(f"Accepted:        {self.history['accepted_count']}")
            print(f"Rejected:        {self.history['rejected_count']}")
            print(f"Time (s):        {elapsed_time:.2f}")
            
            total_decisions = self.history['accepted_count'] + self.history['rejected_count']
            if total_decisions > 0:
                acceptance_rate = self.history['accepted_count'] / total_decisions * 100
                print(f"Acceptance Rate: {acceptance_rate:.1f}%")
            
            print(f"{'='*70}\n")
    
    def get_schedule(self) -> Dict:
        """
        Lấy lịch trình chi tiết từ giải pháp tốt nhất
        
        Returns:
            dict: Chi tiết lịch trình
        """
        if self.best_solution is None:
            raise ValueError("Chưa chạy thuật toán, không có giải pháp")
        
        schedule, makespan = self.model.solution_to_schedule(self.best_solution)
        return schedule
    
    def get_history(self) -> Dict:
        """Lấy lịch sử tìm kiếm"""
        return self.history
    
    def reset(self):
        """Reset solver để chạy lại"""
        self.current_solution = None
        self.best_solution = None
        self.best_makespan = float('inf')
        self.current_makespan = float('inf')
        self.history = {
            'makespan': [],
            'temperature': [],
            'iterations': [],
            'accepted_count': 0,
            'rejected_count': 0
        }
        self.early_stopper.reset()
