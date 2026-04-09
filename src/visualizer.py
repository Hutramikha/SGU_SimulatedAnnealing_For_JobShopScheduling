"""
Module: visualizer.py
Chức năng: Trực quan hóa kết quả
- Vẽ biểu đồ Gantt (lịch trình công việc)
- Vẽ đồ thị hội tụ (Makespan theo thế hệ)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Dict, List
from pathlib import Path


class Visualizer:
    """Lớp trực quan hóa kết quả"""
    
    def __init__(self, output_dir: str = "results"):
        """
        Khởi tạo Visualizer
        
        Args:
            output_dir: Thư mục lưu hình vẽ
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def plot_gantt_chart(self, schedule: Dict, jssp_model, instance_name: str = "instance"):
        """
        Vẽ biểu đồ Gantt
        
        Args:
            schedule: Dict chứa chi tiết lịch trình từ JSSPModel.solution_to_schedule()
            jssp_model: Model JSSP (để lấy thông tin)
            instance_name: Tên instance (dùng cho tên file)
        """
        # Chuẩn bị dữ liệu
        machines_tasks = {m: [] for m in range(jssp_model.n_machines)}
        colors = plt.cm.tab20(np.linspace(0, 1, jssp_model.n_jobs))
        
        # Sắp xếp tasks theo máy
        for job, operations in schedule.items():
            for op in operations:
                machine = op['machine']
                machines_tasks[machine].append({
                    'job': op['job'],
                    'start': op['start_time'],
                    'duration': op['duration'],
                    'end': op['end_time'],
                    'color': colors[job]
                })
        
        # Tạo figure
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Vẽ từng máy
        for machine in range(jssp_model.n_machines):
            y_pos = machine
            
            for task in machines_tasks[machine]:
                # Vẽ hình chữ nhật
                rect = mpatches.Rectangle(
                    (task['start'], y_pos - 0.4),
                    task['duration'],
                    0.8,
                    linewidth=1.5,
                    edgecolor='black',
                    facecolor=task['color'],
                    alpha=0.8
                )
                ax.add_patch(rect)
                
                # Thêm text
                text_x = task['start'] + task['duration'] / 2
                text_y = y_pos
                ax.text(text_x, text_y, f"J{task['job']}", 
                       ha='center', va='center', fontsize=9, fontweight='bold')
        
        # Cấu hình trục
        ax.set_ylim(-0.5, jssp_model.n_machines - 0.5)
        ax.set_xlim(0, max(task['end'] for tasks in machines_tasks.values() 
                          for task in tasks) * 1.05 if machines_tasks[0] else 0)
        
        ax.set_xlabel('Thời gian', fontsize=12, fontweight='bold')
        ax.set_ylabel('Máy', fontsize=12, fontweight='bold')
        ax.set_yticks(range(jssp_model.n_machines))
        ax.set_yticklabels([f"M{m}" for m in range(jssp_model.n_machines)])
        
        ax.set_title(f'Biểu đồ Gantt - {instance_name.upper()}', 
                    fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        # Tạo legend
        job_patches = [mpatches.Patch(color=colors[j], label=f'Job {j}', alpha=0.8)
                      for j in range(jssp_model.n_jobs)]
        ax.legend(handles=job_patches, loc='upper left', ncol=5, fontsize=9)
        
        plt.tight_layout()
        
        # Lưu hình
        file_path = self.output_dir / f"gantt_{instance_name}.png"
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    def plot_convergence(self, history: Dict, instance_name: str = "instance", 
                        bks: int = None):
        """
        Vẽ đồ thị hội tụ
        
        Args:
            history: Dict lịch sử từ SASolver.get_history()
            instance_name: Tên instance
            bks: Giá trị BKS (nếu có)
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Đồ thị 1: Makespan theo iterations
        iterations = history['iterations']
        makespan_history = history['makespan']
        
        ax1.plot(iterations, makespan_history, 'b-', linewidth=2, label='Best Makespan')
        
        if bks is not None:
            ax1.axhline(y=bks, color='g', linestyle='--', linewidth=2, label=f'BKS = {bks}')
            
            # Tính Gap
            final_gap = (makespan_history[-1] - bks) / bks * 100
            ax1.text(0.98, 0.05, f'Gap = {final_gap:.2f}%',
                    transform=ax1.transAxes, fontsize=11,
                    verticalalignment='bottom', horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax1.set_xlabel('Số lần lặp', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Makespan', fontsize=12, fontweight='bold')
        ax1.set_title('Sự hội tụ của Makespan', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='best', fontsize=10)
        
        # Đồ thị 2: Nhiệt độ theo iterations
        temperature = history['temperature']
        
        ax2.semilogy(iterations, temperature, 'r-', linewidth=2, label='Nhiệt độ')
        ax2.set_xlabel('Số lần lặp', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Nhiệt độ (log scale)', fontsize=12, fontweight='bold')
        ax2.set_title('Sự giảm nhiệt độ', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3, which='both')
        ax2.legend(loc='best', fontsize=10)
        
        # Tiêu đề chung
        fig.suptitle(f'Phân tích hội tụ - {instance_name.upper()}', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        # Lưu hình
        file_path = self.output_dir / f"convergence_{instance_name}.png"
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    def plot_multiple_convergence(self, results_dict: Dict[str, Dict], 
                                 bks_dict: Dict[str, int] = None):
        """
        Vẽ biểu đồ so sánh hội tụ của nhiều instances
        
        Args:
            results_dict: Dict {instance_name: history}
            bks_dict: Dict {instance_name: bks}
        """
        fig, ax = plt.subplots(figsize=(12, 7))
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(results_dict)))
        
        for (instance_name, history), color in zip(results_dict.items(), colors):
            iterations = history['iterations']
            makespan_history = history['makespan']
            
            ax.plot(iterations, makespan_history, linewidth=2, 
                   label=instance_name.upper(), color=color)
        
        ax.set_xlabel('Số lần lặp', fontsize=12, fontweight='bold')
        ax.set_ylabel('Makespan', fontsize=12, fontweight='bold')
        ax.set_title('So sánh hội tụ trên nhiều instances', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10, ncol=2)
        
        plt.tight_layout()
        
        # Lưu hình
        file_path = self.output_dir / "convergence_comparison.png"
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    def plot_comparison_bar(self, results_dict: Dict[str, int], 
                           bks_dict: Dict[str, int] = None):
        """
        Vẽ biểu đồ cột so sánh kết quả với BKS
        
        Args:
            results_dict: Dict {instance_name: makespan}
            bks_dict: Dict {instance_name: bks}
        """
        instances = list(results_dict.keys())
        results = list(results_dict.values())
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        x = np.arange(len(instances))
        width = 0.35
        
        # Vẽ kết quả
        bars1 = ax.bar(x - width/2, results, width, label='SA Result', color='steelblue', alpha=0.8)
        
        # Vẽ BKS nếu có
        if bks_dict:
            bks_values = [bks_dict.get(inst, 0) for inst in instances]
            bars2 = ax.bar(x + width/2, bks_values, width, label='BKS', color='orange', alpha=0.8)
            
            # Thêm giá trị trên cột
            for i, (result, bks) in enumerate(zip(results, bks_values)):
                if bks > 0:
                    gap = (result - bks) / bks * 100
                    color = 'green' if gap <= 0 else 'red'
                    ax.text(i, max(result, bks) + 20, f'{gap:+.1f}%', 
                           ha='center', va='bottom', fontsize=9, color=color, fontweight='bold')
        
        ax.set_xlabel('Instances', fontsize=12, fontweight='bold')
        ax.set_ylabel('Makespan', fontsize=12, fontweight='bold')
        ax.set_title('So sánh kết quả với BKS', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([inst.upper() for inst in instances], rotation=45, ha='right')
        ax.legend(fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Lưu hình
        file_path = self.output_dir / "comparison_bar.png"
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
