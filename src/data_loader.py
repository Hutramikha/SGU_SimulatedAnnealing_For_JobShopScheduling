"""
Module: data_loader.py
Chức năng: Đọc và phân tích các tệp dữ liệu chuẩn từ OR-Library
Đầu ra: Ma trận thời gian (P) và ma trận máy (M)
"""

import numpy as np
from pathlib import Path


class DataLoader:
    """Lớp đọc và xử lý file dữ liệu job shop từ OR-Library"""
    
    def __init__(self, data_dir=None):
        # Nếu không pass data_dir, tìm từ project root (nơi source code)
        if data_dir is None:
            # project_root = thư mục chứa src/ (nơi data_loader.py nằm)
            project_root = Path(__file__).parent.parent
            self.data_dir = project_root / "data"
        else:
            self.data_dir = Path(data_dir)
        
        self.n_jobs = None
        self.n_machines = None
        self.processing_times = None  # Ma trận P (n_jobs x n_machines)
        self.machine_order = None      # Ma trận M (n_jobs x n_machines)
    
    def load_instance(self, filename):
        """
        Đọc tệp instance từ OR-Library format
        
        Format file:
            Dòng comment (optional): Mô tả instance
            Dòng đầu tiên data: Số công việc (n_jobs) và số máy (n_machines)
            Dòng 2 đến n_jobs+1: Dữ liệu công việc
            
        Mỗi dòng dữ liệu:
            machine_1 time_1 machine_2 time_2 ... machine_m time_m
        
        Args:
            filename: Tên file (ví dụ: "la01.txt")
        
        Returns:
            dict: Chứa n_jobs, n_machines, processing_times, machine_order
        """
        file_path = self.data_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} không tồn tại")
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Bỏ qua dòng comment header (nếu có)
        line_idx = 0
        while line_idx < len(lines):
            line_stripped = lines[line_idx].strip()
            # Cố gắng parse dòng hiện tại
            try:
                parts = [int(x) for x in line_stripped.split()]
                if len(parts) >= 2:
                    # Tìm được dòng chứa 2 số (n_jobs, n_machines)
                    break
            except (ValueError, IndexError):
                # Dòng này không phải data, bỏ qua
                pass
            line_idx += 1
        
        if line_idx >= len(lines):
            raise ValueError(f"File {filename} không có dòng dữ liệu valid")
        
        # Đọc số jobs và machines
        first_line = lines[line_idx].strip().split()
        self.n_jobs = int(first_line[0])
        self.n_machines = int(first_line[1])
        
        # Khởi tạo ma trận
        self.processing_times = np.zeros((self.n_jobs, self.n_machines), dtype=int)
        self.machine_order = np.zeros((self.n_jobs, self.n_machines), dtype=int)
        
        # Đọc dữ liệu từng công việc (bắt đầu từ dòng sau header)
        data_start = line_idx + 1
        for job_idx in range(self.n_jobs):
            # Tìm dòng dữ liệu tiếp theo (bỏ qua dòng trống)
            while data_start < len(lines) and lines[data_start].strip() == "":
                data_start += 1
            
            if data_start >= len(lines):
                break
            
            data = list(map(int, lines[data_start].strip().split()))
            data_start += 1
            
            # Dữ liệu được lưu dưới dạng: m1 t1 m2 t2 ... mn tn
            for machine_idx in range(self.n_machines):
                machine_id = data[2 * machine_idx]
                processing_time = data[2 * machine_idx + 1]
                
                self.machine_order[job_idx, machine_idx] = machine_id
                self.processing_times[job_idx, machine_idx] = processing_time
        
        return {
            'n_jobs': self.n_jobs,
            'n_machines': self.n_machines,
            'processing_times': self.processing_times,
            'machine_order': self.machine_order
        }
    
    def get_processing_time(self, job, operation):
        """Lấy thời gian xử lý của một thao tác"""
        return self.processing_times[job, operation]
    
    def get_machine(self, job, operation):
        """Lấy ID máy xử lý thao tác"""
        return self.machine_order[job, operation]
    
    def display_instance(self):
        """Hiển thị thông tin instance đã tải"""
        print(f"\n{'='*70}")
        print("THÔNG TIN INSTANCE")
        print(f"{'='*70}")
        print(f"Số công việc (n_jobs):     {self.n_jobs}")
        print(f"Số máy (n_machines):       {self.n_machines}")
        print(f"Tổng thao tác:             {self.n_jobs * self.n_machines}")
        print(f"\nMa trận thứ tự máy (Machine Order):")
        print(self.machine_order)
        print(f"\nMa trận thời gian xử lý (Processing Times):")
        print(self.processing_times)
        print(f"{'='*70}\n")
