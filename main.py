#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main.py - Entry point chính
Chạy thuật toán SA để giải bài toán JSSP
"""

import sys
import random
import numpy as np
from pathlib import Path

# Thêm thư mục src vào path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config import SAConfig
from src.data_loader import DataLoader
from src.jssp_model import JSSPModel
from src.sa_solver import SASolver
from src.evaluator import Evaluator
from src.visualizer import Visualizer
from src.utils import format_time


def solve_single_instance(instance_name: str, config: SAConfig = None) -> dict:
    """
    Giải một instance duy nhất (một lần chạy)
    
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
            f.write(f"Gap (%): {evaluation['gap_percent'] if evaluation['gap_percent'] is not None else 'N/A'}\n")
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


def solve_instance_multiple_trials(instance_name: str, num_trials: int = 5, config: SAConfig = None) -> dict:
    """
    Giải một instance với 05 lần chạy độc lập (theo yêu cầu thực nghiệm)
    Trả về C_max^best (tốt nhất) và C_max^avg (trung bình) từ 05 lần chạy
    
    Args:
        instance_name: Tên instance (ví dụ: "la01")
        num_trials: Số lần chạy độc lập (mặc định: 05)
        config: SAConfig object (nếu None sẽ dùng config mặc định)
    
    Returns:
        dict: {
            'instance': tên instance,
            'bks': Best Known Solution,
            'best_makespan': C_max^best,
            'avg_makespan': C_max^avg,
            'best_gap_percent': gap tốt nhất,
            'avg_gap_percent': gap trung bình,
            'trials': [kết quả 5 lần chạy],
            'schedule': lịch trình từ lần chạy tốt nhất,
            'history': lịch sử tìm kiếm từ lần chạy tốt nhất
        }
    """
    if config is None:
        config = SAConfig()
    
    print(f"\n{'='*80}")
    print(f"THỰC NGHIỆM: {instance_name.upper()} - {num_trials} LẦN CHẠY ĐỘC LẬP")
    print(f"{'='*80}")
    print(f"\nThông số nền tảng:")
    print(f"  T0 (Nhiệt độ ban đầu):     {config.T0}")
    print(f"  α_explore (thăm dò):       {config.alpha_explore}")
    print(f"  α_exploit (khai thác):     {config.alpha_exploit}")
    print(f"  L (Markov chain):          {config.L}")
    print(f"  patience:                  {config.patience}\n")
    
    # Load dữ liệu (chỉ 1 lần)
    loader = DataLoader(config.data_dir)
    data = loader.load_instance(f"{instance_name}.txt")
    
    evaluator = Evaluator(config.bks_file)
    bks = evaluator.get_bks(instance_name)
    
    results = []
    best_trial_result = None
    best_makespan_overall = float('inf')
    
    # Chạy 05 lần độc lập
    for trial_id in range(1, num_trials + 1):
        # Set seed khác nhau mỗi lần
        seed = trial_id * 1000 + trial_id  # 1001, 2002, 3003, 4004, 5005
        random.seed(seed)
        np.random.seed(seed)
        
        print(f"[TRIAL {trial_id}/{num_trials}] Seed={seed}...", end=" ", flush=True)
        
        # Tạo model và solver (fresh instance)
        model = JSSPModel(
            data['n_jobs'],
            data['n_machines'],
            data['processing_times'],
            data['machine_order']
        )
        
        # Chạy SA
        solver = SASolver(model, config)
        best_solution, best_makespan, history = solver.solve()
        
        # Đánh giá
        evaluation = evaluator.evaluate_solution(best_makespan, instance_name)
        
        trial_result = {
            'trial': trial_id,
            'seed': seed,
            'makespan': best_makespan,
            'gap_percent': evaluation['gap_percent'],
            'schedule': solver.get_schedule(),
            'history': history
        }
        
        results.append(trial_result)
        
        # Lưu lần chạy tốt nhất (để lấy schedule và history sau)
        if best_makespan < best_makespan_overall:
            best_makespan_overall = best_makespan
            best_trial_result = trial_result
        
        print(f"Makespan={best_makespan}, Gap={evaluation['gap_percent']:.2f}%")
    
    # Tính kết quả
    makespans = [r['makespan'] for r in results]
    best_makespan = min(makespans)
    avg_makespan = sum(makespans) / len(makespans)
    
    gaps = [r['gap_percent'] for r in results if r['gap_percent'] is not None]
    best_gap = min(gaps) if gaps else None
    avg_gap = sum(gaps) / len(gaps) if gaps else None
    
    # In kết quả
    print(f"\n{'-'*80}")
    print(f"KẾT QUẢ ({instance_name.upper()}):")
    print(f"{'-'*80}")
    print(f"  Best Known Solution (BKS):    {bks}")
    print(f"  C_max^best (tốt nhất):        {best_makespan}")
    print(f"  C_max^avg (trung bình):       {avg_makespan:.1f}")
    print(f"  Gap^best:                     {best_gap:.2f}%" if best_gap else "  Gap^best: N/A")
    print(f"  Gap^avg:                      {avg_gap:.2f}%" if avg_gap else "  Gap^avg: N/A")
    print(f"\n  Chi tiết 05 lần chạy:")
    for r in results:
        print(f"    Trial {r['trial']}: Makespan={r['makespan']:4d}, Gap={r['gap_percent']:6.2f}%")
    print(f"{'-'*80}\n")
    
    return {
        'instance': instance_name,
        'num_trials': num_trials,
        'bks': bks,
        'best_makespan': best_makespan,
        'avg_makespan': avg_makespan,
        'best_gap_percent': best_gap,
        'avg_gap_percent': avg_gap,
        'trials': results,
        'schedule': best_trial_result['schedule'] if best_trial_result else None,
        'history': best_trial_result['history'] if best_trial_result else None
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
    
    print("="*70)
    print("THUẬT TOÁN SA - GIẢI BÀI TOÁN JSSP")
    print("="*70)
    
    # 1. Chạy 05 lần độc lập (theo yêu cầu thực nghiệm)
    result = solve_instance_multiple_trials("la01", num_trials=5, config=config)
    
    # 2. Hoặc chạy một lần duy nhất (bỏ comment dòng dưới để sử dụng)
    # result = solve_single_instance("la01", config)
    
    # 3. Giải nhiều instances (bỏ comment để chạy)
    # results = solve_multiple_instances(["la01", "la02", "la03"], config)
    
    print(f"\n{'='*70}")
    print("[OK] Hoan tat!")
    print(f"{'='*70}\n")
