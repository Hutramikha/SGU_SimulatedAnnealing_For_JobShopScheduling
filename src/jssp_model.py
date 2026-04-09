"""
Module: jssp_model.py
Chức năng: Mô hình hóa bài toán JSSP - Operation-based Encoding
- Hiện thực hóa logic mã hóa Operation-based
- Tính toán Makespan từ dãy mã hóa
- Quản lý các ràng buộc về máy và công việc
"""

import numpy as np
from typing import Tuple, List


class JSSPModel:
    """Lớp mô hình hóa bài toán JSSP với Operation-based Encoding"""
    
    def __init__(self, n_jobs: int, n_machines: int, 
                 processing_times: np.ndarray, machine_order: np.ndarray):
        """
        Khởi tạo mô hình JSSP
        
        Args:
            n_jobs: Số công việc
            n_machines: Số máy
            processing_times: Ma trận thời gian xử lý (n_jobs x n_machines)
            machine_order: Ma trận thứ tự máy (n_jobs x n_machines)
        """
        self.n_jobs = n_jobs
        self.n_machines = n_machines
        self.n_operations = n_jobs * n_machines
        self.processing_times = processing_times
        self.machine_order = machine_order
    
    def generate_random_solution(self) -> List[int]:
        """
        Sinh lời giải ngẫu nhiên dạng Operation-based Encoding
        
        Nguyên lý: Mỗi số hiệu job i xuất hiện đúng m lần trong dãy
        
        Returns:
            List[int]: Dãy mã hóa [job_1, job_2, ..., job_n*m]
            
        Ví dụ: Với 2 jobs, 3 machines: [0, 1, 0, 1, 0, 1] hoặc [1, 0, 1, 0, 1, 0]
        """
        # Tạo dãy: mỗi job xuất hiện m lần
        operations = []
        for job in range(self.n_jobs):
            operations.extend([job] * self.n_machines)
        
        # Xáo trộn ngẫu nhiên
        np.random.shuffle(operations)
        return operations
    
    def solution_to_schedule(self, solution: List[int]) -> Tuple[dict, int]:
        """
        Chuyển đổi dãy mã hóa thành lịch trình chi tiết và tính Makespan
        
        Args:
            solution: Dãy mã hóa Operation-based
        
        Returns:
            Tuple:
                - schedule: Dict chứa chi tiết lịch trình cho mỗi job
                - makespan: Giá trị Makespan (C_max)
        """
        # Khởi tạo:
        # job_ready_time[j]: Thời điểm sớm nhất job j có thể thực hiện thao tác kế tiếp
        # machine_ready_time[m]: Thời điểm sớm nhất máy m sẵn sàng
        job_ready_time = [0] * self.n_jobs
        machine_ready_time = [0] * self.n_machines
        
        # Theo dõi thao tác tiếp theo cho mỗi job
        job_operation_index = [0] * self.n_jobs
        
        # Lưu chi tiết lịch trình
        schedule = {job: [] for job in range(self.n_jobs)}
        
        # Duyệt qua dãy mã hóa
        for encoded_job in solution:
            # Xác định thao tác của job này
            operation_index = job_operation_index[encoded_job]
            
            # Lấy thông tin máy và thời gian xử lý
            machine_id = int(self.machine_order[encoded_job, operation_index])
            processing_time = int(self.processing_times[encoded_job, operation_index])
            
            # Tính thời điểm bắt đầu
            # C(O_i,j) = max(job_ready_time[j], machine_ready_time[m]) + p_i,j
            start_time = max(job_ready_time[encoded_job], machine_ready_time[machine_id])
            end_time = start_time + processing_time
            
            # Cập nhật trạng thái
            job_ready_time[encoded_job] = end_time
            machine_ready_time[machine_id] = end_time
            
            # Lưu chi tiết
            schedule[encoded_job].append({
                'job': encoded_job,
                'operation': operation_index,
                'machine': machine_id,
                'start_time': start_time,
                'end_time': end_time,
                'duration': processing_time
            })
            
            # Tăng chỉ số thao tác
            job_operation_index[encoded_job] += 1
        
        # Tính Makespan: thời điểm hoàn thành công việc cuối cùng
        makespan = max(max(op['end_time'] for op in schedule[job]) 
                      for job in range(self.n_jobs) if schedule[job])
        
        return schedule, makespan
    
    def calculate_makespan(self, solution: List[int]) -> int:
        """
        Tính giá trị Makespan (hàm mục tiêu)
        
        Args:
            solution: Dãy mã hóa
        
        Returns:
            int: Giá trị Makespan
        """
        _, makespan = self.solution_to_schedule(solution)
        return makespan
    
    def is_valid_solution(self, solution: List[int]) -> bool:
        """
        Kiểm tra tính hợp lệ của lời giải
        
        Lời giải hợp lệ khi:
        - Chiều dài = n_jobs * n_machines
        - Mỗi job xuất hiện đúng n_machines lần
        
        Args:
            solution: Dãy mã hóa
        
        Returns:
            bool: True nếu hợp lệ, False nếu không
        """
        if len(solution) != self.n_operations:
            return False
        
        # Kiểm tra mỗi job xuất hiện đúng n_machines lần
        job_counts = [0] * self.n_jobs
        for job in solution:
            if job < 0 or job >= self.n_jobs:
                return False
            job_counts[job] += 1
        
        return all(count == self.n_machines for count in job_counts)
    
    def get_schedule_info(self, solution: List[int]) -> str:
        """
        Trả về chuỗi mô tả chi tiết lịch trình
        
        Args:
            solution: Dãy mã hóa
        
        Returns:
            str: Thông tin lịch trình
        """
        schedule, makespan = self.solution_to_schedule(solution)
        
        info = f"Makespan: {makespan}\n"
        info += f"{'='*70}\n"
        
        for job in range(self.n_jobs):
            info += f"Job {job}:\n"
            for op in schedule[job]:
                info += f"  Operation {op['operation']}: "
                info += f"Machine {op['machine']}, "
                info += f"Time [{op['start_time']}, {op['end_time']}]\n"
        
        return info
