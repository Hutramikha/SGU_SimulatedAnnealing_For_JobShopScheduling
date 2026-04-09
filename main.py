#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main.py - Entry point chính
Chạy thuật toán SA để giải bài toán JSSP
"""

import sys
from pathlib import Path

# Thêm thư mục src vào path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config.config import SAConfig
from src.data_loader import DataLoader
from src.jssp_model import JSSPModel
from src.sa_solver import SASolver
from src.evaluator import Evaluator
from src.visualizer import Visualizer
from src.utils import format_time


def solve_single_instance(instance_name: str, config: SAConfig = None) -> dict:
    """
    Giải một instance duy nhất
    
    Args:
        instance_name: Tên instance (ví dụ: "la01")
        config: SAConfig object (nếu None sẽ dùng config mặc định)
    
    Returns:
        dict: Kết quả giải (makespan, gap, schedule, history, etc.)
    """
    if config is None:
        config = SAConfig()
    
    # 1. Đọc dữ liệu
    print(f"\n{'='*70}")
    print(f"GIẢI QUY BÀI TOÁN JSSP - INSTANCE {instance_name.upper()}")
    print(f"{'='*70}")
    
    print(f"\n[*] Đọc dữ liệu...")
    loader = DataLoader(config.data_dir)
    data = loader.load_instance(f"{instance_name}.txt")
    loader.display_instance()
    
    # 2. Tạo model
    print("[CONFIG] Tạo mô hình JSSP...")
    model = JSSPModel(
        data['n_jobs'],
        data['n_machines'],
        data['processing_times'],
        data['machine_order']
    )
    
    # 3. Giải bằng SA
    print("[RUN] Chạy thuật toán SA...")
    solver = SASolver(model, config)
    best_solution, best_makespan, history = solver.solve()
    
    # 4. Đánh giá kết quả
    print("[EVAL] Đánh giá kết quả...")
    evaluator = Evaluator(config.bks_file)
    evaluation = evaluator.evaluate_solution(best_makespan, instance_name)
    evaluator.print_evaluation(evaluation)
    
    # 5. Trực quan hóa
    if config.plot_gantt or config.plot_convergence:
        print("[VIZ] Trực quan hóa kết quả...")
        visualizer = Visualizer(config.results_dir)
        
        schedule = solver.get_schedule()
        
        if config.plot_gantt:
            gantt_file = visualizer.plot_gantt_chart(schedule, model, instance_name)
            print(f"[OK] Gantt chart: {gantt_file}")
        
        if config.plot_convergence:
            bks = evaluator.get_bks(instance_name)
            convergence_file = visualizer.plot_convergence(history, instance_name, bks)
            print(f"[OK] Convergence: {convergence_file}")
    
    # 6. Lưu kết quả
    if config.save_results:
        results_file = Path(config.results_dir) / f"{instance_name}_result.txt"
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write(f"Instance: {instance_name.upper()}\n")
            f.write(f"Makespan: {best_makespan}\n")
            f.write(f"BKS: {evaluation['bks']}\n")
            f.write(f"Gap (%): {evaluation['gap_percent'] if evaluation['gap_percent'] else 'N/A'}\n")
            f.write(f"Quality: {evaluation['quality']}\n\n")
            f.write(f"Schedule:\n{model.get_schedule_info(best_solution)}\n")
        print(f"[OK] Kết quả lưu tại: {results_file}")
    
    return {
        'instance': instance_name,
        'makespan': best_makespan,
        'bks': evaluation['bks'],
        'gap_percent': evaluation['gap_percent'],
        'quality': evaluation['quality'],
        'schedule': solver.get_schedule(),
        'history': history,
        'evaluation': evaluation
    }


def solve_multiple_instances(instance_list: list = None, config: SAConfig = None) -> dict:
    """
    Giải nhiều instances liên tiếp
    
    Args:
        instance_list: Danh sách tên instances (ví dụ: ["la01", "la02", "la03"])
                      Nếu None sẽ chạy LA01-LA10
        config: SAConfig object
    
    Returns:
        dict: Kết quả trên tất cả instances
    """
    if config is None:
        config = SAConfig()
    
    if instance_list is None:
        instance_list = [f"la{i:02d}" for i in range(1, 11)]
    
    results = {}
    
    for instance_name in instance_list:
        try:
            result = solve_single_instance(instance_name, config)
            results[instance_name] = result
        except Exception as e:
            print(f"[ERROR] Lỗi giải {instance_name}: {e}")
            results[instance_name] = None
    
    # In bảng so sánh
    evaluator = Evaluator(config.bks_file)
    results_dict = {k: v['makespan'] for k, v in results.items() if v}
    evaluator.compare_results(results_dict)
    
    # Vẽ biểu đồ so sánh
    if config.plot_convergence:
        visualizer = Visualizer(config.results_dir)
        history_dict = {k: v['history'] for k, v in results.items() if v}
        bks_dict = {k: v['bks'] for k, v in results.items() if v}
        
        visualizer.plot_multiple_convergence(history_dict, bks_dict)
        print(f"[OK] Biểu đồ so sánh khỏi tạo")
        
        visualizer.plot_comparison_bar(results_dict, bks_dict)
        print(f"[OK] Biểu đồ cột khỏi tạo")
    
    return results


if __name__ == "__main__":
    # ==================== CẤU HÌNH ====================
    config = SAConfig()
    
    # ==================== CÓ THƯỚC LỰA CHỌN ====================
    
    # 1. Giải một instance duy nhất
    print("="*70)
    print("THUẬT TOÁN SA - GIẢI BÀI TOÁN JSSP")
    print("="*70)
    
    result = solve_single_instance("la01", config)
    
    # 2. Giải nhiều instances (bỏ comment để chạy)
    # results = solve_multiple_instances(["la01", "la02", "la03"], config)
    
    print(f"\n{'='*70}")
    print("[OK] Hoan tat!")
    print(f"{'='*70}\n")
