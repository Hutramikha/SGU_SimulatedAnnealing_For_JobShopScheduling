"""
Module: evaluator.py
Chức năng: Tính toán Makespan, Gap so với BKS, và các chỉ số đánh giá
"""

import csv
from pathlib import Path
from typing import Dict, Optional


class Evaluator:
    """Lớp đánh giá kết quả giải pháp"""
    
    def __init__(self, bks_file: str = "LA_BKS.csv"):
        """
        Khởi tạo Evaluator
        
        Args:
            bks_file: Đường dẫn tới file chứa Best Known Solutions
        """
        self.bks_dict = {}
        self.load_bks(bks_file)
    
    def load_bks(self, bks_file: str):
        """
        Đọc file BKS (Best Known Solutions)
        
        Args:
            bks_file: Đường dẫn tới file BKS
        """
        file_path = Path(bks_file)
        
        if not file_path.exists():
            print(f"[WARNING] File BKS {bks_file} không found, sẽ làm việc mà không có BKS reference")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    # Bỏ qua comment và dòng trống
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse: LA01, 10, 5, 666
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 4:
                        instance_name = parts[0].strip().lower()
                        try:
                            bks_value = int(parts[3])
                            self.bks_dict[instance_name] = bks_value
                        except (ValueError, IndexError):
                            pass
        
        except Exception as e:
            print(f"[WARNING] Lỗi đọc file BKS: {e}")
    
    def get_bks(self, instance_name: str) -> Optional[int]:
        """
        Lấy BKS của một instance
        
        Args:
            instance_name: Tên instance (ví dụ: "la01")
        
        Returns:
            int: Giá trị BKS, hoặc None nếu không tìm thấy
        """
        return self.bks_dict.get(instance_name.lower())
    
    def calculate_gap(self, result: int, instance_name: str) -> Optional[float]:
        """
        Tính Gap (%) so với BKS
        
        Gap(%) = (Result - BKS) / BKS * 100%
        
        Args:
            result: Kết quả tìm được
            instance_name: Tên instance
        
        Returns:
            float: Giá trị Gap (%), hoặc None nếu không có BKS
        """
        bks = self.get_bks(instance_name)
        
        if bks is None:
            return None
        
        if result < bks:
            # Phát hiện kỷ lục mới
            gap = -((bks - result) / bks * 100)
            return gap
        else:
            gap = (result - bks) / bks * 100
            return gap
    
    def evaluate_solution(self, result: int, instance_name: str) -> Dict:
        """
        Đánh giá toàn diện một giải pháp
        
        Args:
            result: Makespan tìm được
            instance_name: Tên instance
        
        Returns:
            dict: Chứa các chỉ số đánh giá
        """
        bks = self.get_bks(instance_name)
        gap = self.calculate_gap(result, instance_name)
        
        evaluation = {
            'instance': instance_name,
            'makespan': result,
            'bks': bks,
            'gap_percent': gap
        }
        
        # Xác định mức kết quả
        if bks is None:
            evaluation['quality'] = "Unknown (No BKS)"
        elif result == bks:
            evaluation['quality'] = "Optimal [OK]"
        elif gap and gap < 5:
            evaluation['quality'] = "Excellent (< 5%)"
        elif gap and gap < 10:
            evaluation['quality'] = "Good (5-10%)"
        elif gap and gap < 15:
            evaluation['quality'] = "Fair (10-15%)"
        else:
            evaluation['quality'] = f"Poor (>{gap:.1f}%)"
        
        return evaluation
    
    def print_evaluation(self, evaluation: Dict):
        """
        In kết quả đánh giá
        
        Args:
            evaluation: Dict kết quả đánh giá
        """
        print(f"\n{'='*70}")
        print("ĐÁNH GIÁ GIẢI PHÁP")
        print(f"{'='*70}")
        print(f"Instance:          {evaluation['instance'].upper()}")
        print(f"Makespan tìm được: {evaluation['makespan']}")
        
        if evaluation['bks'] is not None:
            print(f"BKS:               {evaluation['bks']}")
            print(f"Gap (%):           {evaluation['gap_percent']:.2f}%")
        
        print(f"Chất lượng:        {evaluation['quality']}")
        print(f"{'='*70}\n")
    
    def compare_results(self, results_dict: Dict[str, int]):
        """
        So sánh kết quả trên nhiều instances
        
        Args:
            results_dict: Dict {instance_name: makespan}
        """
        print(f"\n{'='*70}")
        print("SO SÁNH KẾT QUẢ TRÊN NHIỀU INSTANCES")
        print(f"{'='*70}")
        print(f"{'Instance':<12} {'Makespan':<12} {'BKS':<12} {'Gap (%)':<12} {'Chất lượng':<20}")
        print(f"{'-'*70}")
        
        total_gap = 0
        valid_gaps = 0
        
        for instance, result in sorted(results_dict.items()):
            evaluation = self.evaluate_solution(result, instance)
            
            bks_str = str(evaluation['bks']) if evaluation['bks'] else "N/A"
            gap_str = f"{evaluation['gap_percent']:.2f}%" if evaluation['gap_percent'] is not None else "N/A"
            
            print(f"{instance:<12} {result:<12} {bks_str:<12} {gap_str:<12} {evaluation['quality']:<20}")
            
            if evaluation['gap_percent'] is not None:
                total_gap += evaluation['gap_percent']
                valid_gaps += 1
        
        print(f"{'-'*70}")
        
        if valid_gaps > 0:
            avg_gap = total_gap / valid_gaps
            print(f"Trung bình Gap: {avg_gap:.2f}%")
        
        print(f"{'='*70}\n")
