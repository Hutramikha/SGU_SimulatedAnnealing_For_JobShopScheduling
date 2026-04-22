#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gui.py - Giao diện đơn giản cho thuật toán SA
Cho phép lựa chọn instance, xem tham số, và trình bày kết quả
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading
from PIL import Image, ImageTk
import sys
import random
import numpy as np
import time

# Fix UTF-8 encoding on Windows
try:
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass  # Fallback nếu reconfigure không hỗ trợ

# Thêm project root vào path (từ parent directory)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import SAConfig
from src.data_loader import DataLoader
from src.jssp_model import JSSPModel
from src.sa_solver import SASolver
from src.evaluator import Evaluator
from src.visualizer import Visualizer


class SAJSSP_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SA Solver - Job Shop Scheduling")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Tạo style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Config
        self.config = SAConfig()
        self.data_loader = DataLoader()
        self.evaluator = Evaluator()
        
        # Variables
        self.is_running = False
        self.selected_instance = tk.StringVar(value="la01")
        self.trial_mode = tk.BooleanVar(value=False)  # 5-trial mode toggle
        
        # Tạo notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Cấu hình
        self.frame_config = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_config, text="Cau Hinh")
        self.create_config_tab()
        
        # Tab 2: Kết quả
        self.frame_result = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_result, text="Ket Qua")
        self.create_result_tab()
        
        # Statusbar
        self.status_var = tk.StringVar(value="San sang")
        self.statusbar = ttk.Label(root, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_config_tab(self):
        """Tạo tab cấu hình"""
        # Frame chính
        main_frame = ttk.Frame(self.frame_config, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === PHẦN 1: CHỌN INSTANCE ===
        frame_instance = ttk.LabelFrame(main_frame, text="Chon Du Lieu", padding=10)
        frame_instance.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_instance, text="Instance:").pack(side=tk.LEFT, padx=5)
        
        # Danh sách instances
        instances = [f"la{i:02d}" for i in range(1, 41)]
        combo = ttk.Combobox(frame_instance, textvariable=self.selected_instance,
                            values=instances, state="readonly", width=10)
        combo.pack(side=tk.LEFT, padx=5)
        combo.bind("<<ComboboxSelected>>", lambda e: self.update_instance_info())
        
        # Nút Load info
        ttk.Button(frame_instance, text="Tai Thong Tin", 
                  command=self.update_instance_info).pack(side=tk.LEFT, padx=5)
        
        # Info instance
        self.info_var = tk.StringVar(value="Chon 1 instance de xem thong tin")
        ttk.Label(frame_instance, textvariable=self.info_var, 
                 foreground="blue").pack(side=tk.LEFT, padx=20)
        
        # === PHẦN 1B: CHỈ ĐỒ CHẠY 5 LẦN (TRIAL MODE) ===
        frame_trial = ttk.LabelFrame(main_frame, text="Che Do Thuc Nghiem", padding=10)
        frame_trial.pack(fill=tk.X, pady=10)
        
        ttk.Checkbutton(frame_trial, text="CHAY 5 LAN DOC LAP (5 Trials)", 
                       variable=self.trial_mode).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_trial, text="Moi trial su dung hat khac nhau (seeds: 1001-5005)", 
                 foreground="green").pack(side=tk.LEFT, padx=10)
        
        # === PHẦN 2: THAM SỐ THUẬT TOÁN ===
        frame_params = ttk.LabelFrame(main_frame, text="Tham So Thuat Toan", padding=10)
        frame_params.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tạo bảng hiển thị tham số
        columns = ("Tham So", "Gia Tri", "Y Nghia")
        tree = ttk.Treeview(frame_params, columns=columns, height=10, show="tree headings")
        tree.column("#0", width=0)
        tree.column("Tham So", anchor=tk.W, width=200)
        tree.column("Gia Tri", anchor=tk.CENTER, width=100)
        tree.column("Y Nghia", anchor=tk.W, width=250)
        
        tree.heading("Tham So", text="Tham So")
        tree.heading("Gia Tri", text="Gia Tri")
        tree.heading("Y Nghia", text="Y Nghia")
        
        # Dữ liệu tham số
        params_data = [
            ("Nhiệt độ ban đầu (T0)", f"{self.config.T0}", "Cao để chấp nhận giải tệ"),
            ("Nhiệt độ dừng (T_min)", f"{self.config.T_min}", "Ngưỡng kết thúc"),
            ("Hệ số lạnh - Thăm dò (α_explore)", f"{self.config.alpha_explore}", "Chậm (0.98)"),
            ("Hệ số lạnh - Khai thác (α_exploit)", f"{self.config.alpha_exploit}", "Nhanh (0.95)"),
            ("Markov chain (L)", f"{self.config.L}", "Số phép thử/nhiệt độ"),
            ("Early stopping (patience)", f"{self.config.patience}", "Dừng sớm nếu không cải thiện"),
            ("Ngưỡng cải thiện (ε)", f"{self.config.improvement_threshold*100:.1f}%", "Chọn chế độ làm lạnh"),
            ("Hệ số hâm nóng", f"{self.config.reheating_factor}", "T_new = T_old / factor"),
            ("Xác suất Swap", f"{self.config.swap_probability*100:.0f}%", "50% Swap, 50% Move"),
        ]
        
        for idx, (param, value, meaning) in enumerate(params_data):
            tree.insert("", "end", values=(param, value, meaning),
                       tags=("oddrow" if idx % 2 == 0 else "evenrow",))
        
        # Thêm alternating row colors
        tree.tag_configure("oddrow", background="#f0f0f0")
        tree.tag_configure("evenrow", background="white")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_params, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # === PHẦN 3: NÚT CHẠY ===
        frame_buttons = ttk.Frame(main_frame)
        frame_buttons.pack(fill=tk.X, pady=10)
        
        self.btn_run = ttk.Button(frame_buttons, text="CHAY THUAT TOAN", 
                                  command=self.run_algorithm)
        self.btn_run.pack(side=tk.LEFT, padx=5)
        
        self.progress = ttk.Progressbar(frame_buttons, mode='indeterminate')
        self.progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        ttk.Button(frame_buttons, text="Reset", 
                  command=self.reset).pack(side=tk.LEFT, padx=5)
    
    def create_result_tab(self):
        """Tạo tab kết quả"""
        # Frame chính
        main_frame = ttk.Frame(self.frame_result, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === PANED WINDOW: DANH SÁCH + CHI TIẾT ===
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Phần trái: Danh sách instances đã chạy
        frame_list = ttk.LabelFrame(paned, text="Danh Sach Ket Qua", padding=5)
        paned.add(frame_list, weight=1)
        
        # Treeview danh sách
        columns = ("Instance", "Makespan", "BKS", "Gap(%)", "Mode")
        self.results_tree = ttk.Treeview(frame_list, columns=columns, height=15, show="tree headings")
        self.results_tree.column("#0", width=0)
        self.results_tree.column("Instance", anchor=tk.W, width=70)
        self.results_tree.column("Makespan", anchor=tk.CENTER, width=75)
        self.results_tree.column("BKS", anchor=tk.CENTER, width=55)
        self.results_tree.column("Gap(%)", anchor=tk.CENTER, width=60)
        self.results_tree.column("Mode", anchor=tk.CENTER, width=70)
        
        self.results_tree.heading("Instance", text="Instance")
        self.results_tree.heading("Makespan", text="Makespan")
        self.results_tree.heading("BKS", text="BKS")
        self.results_tree.heading("Gap(%)", text="Gap(%)")
        self.results_tree.heading("Mode", text="Mode")
        
        self.results_tree.bind("<<TreeviewSelect>>", self.on_result_select)
        
        # Scrollbar
        scrollbar_list = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, 
                                      command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scrollbar_list.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Nút load danh sách
        frame_list_buttons = ttk.Frame(frame_list)
        frame_list_buttons.pack(fill=tk.X, pady=5)
        ttk.Button(frame_list_buttons, text="Tai Danh Sach",
                  command=self.load_results_list).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_list_buttons, text="Delete",
                  command=self.delete_selected_result).pack(side=tk.LEFT, padx=2)
        
        # Phần phải: Chi tiết và biểu đồ
        frame_detail = ttk.LabelFrame(paned, text="Chi Tiet", padding=5)
        paned.add(frame_detail, weight=1)
        
        # === KẾT QUẢ CHI TIẾT ===
        frame_results = ttk.LabelFrame(frame_detail, text="Ket Qua Chi Tiet", padding=10)
        frame_results.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Tạo bảng kết quả
        self.result_text = tk.Text(frame_results, height=10, width=50,
                                   font=("Courier", 9))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_results, orient=tk.VERTICAL, 
                                 command=self.result_text.yview)
        self.result_text.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # === NÚT XEM BIỂU ĐỒ ===
        frame_charts = ttk.LabelFrame(frame_detail, text="Bieu Do", padding=10)
        frame_charts.pack(fill=tk.X, pady=5)
        
        self.btn_gantt = ttk.Button(frame_charts, text="Xem Gantt Chart",
                                   command=self.show_gantt, state=tk.DISABLED)
        self.btn_gantt.pack(side=tk.LEFT, padx=3)
        
        self.btn_convergence = ttk.Button(frame_charts, text="Xem Convergence",
                                         command=self.show_convergence, state=tk.DISABLED)
        self.btn_convergence.pack(side=tk.LEFT, padx=3)
        
        self.btn_result = ttk.Button(frame_charts, text="Xem Ket Qua Chi Tiet",
                                    command=self.show_result_file, state=tk.DISABLED)
        self.btn_result.pack(side=tk.LEFT, padx=3)
        
        ttk.Button(frame_charts, text="Mo Folder Results",
                  command=self.open_results_folder).pack(side=tk.LEFT, padx=3)
        
        # Lưu instance hiện tại
        self.current_selected_instance = None
        self.current_selected_mode = None
        
        # Load danh sách ban đầu
        self.load_results_list()
    
    def update_instance_info(self):
        """Cập nhật thông tin instance"""
        try:
            instance_name = self.selected_instance.get()
            data = self.data_loader.load_instance(f"{instance_name}.txt")
            
            n_jobs = data['n_jobs']
            n_machines = data['n_machines']
            bks = self.evaluator.get_bks(instance_name)
            
            info_text = f"{instance_name.upper()}: {n_jobs}x{n_machines} | BKS={bks}"
            self.info_var.set(info_text)
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the tai du lieu: {e}")
    
    def run_algorithm(self):
        """Chạy thuật toán"""
        if self.is_running:
            messagebox.showwarning("Canh Bao", "Thuat toan dang chay!")
            return
        
        instance_name = self.selected_instance.get()
        num_trials = 5 if self.trial_mode.get() else 1
        
        # Chạy trong thread riêng
        self.is_running = True
        self.btn_run.config(state=tk.DISABLED)
        self.progress.start()
        
        trial_text = f" (5 Trials)" if num_trials == 5 else ""
        self.status_var.set(f"Dang chay {instance_name.upper()}{trial_text}...")
        
        thread = threading.Thread(target=self._solve_thread, args=(instance_name, num_trials))
        thread.daemon = True
        thread.start()
    
    def _solve_thread(self, instance_name, num_trials=1):
        """Thread chạy thuật toán (1 hoặc 5 lần)"""
        try:
            # Xác định mode: single (1 lần) hay multi (5 lần)
            mode = "multi" if num_trials > 1 else "single"
            
            # Chuẩn bị dữ liệu cho trial loop
            trial_results = []
            best_makespan_overall = float('inf')
            best_trial_index = -1
            
            # Loop: Chạy 1 lần hoặc 5 lần
            for trial_idx in range(num_trials):
                # Seed management cho reproducibility
                if num_trials > 1:
                    seed = 1001 + trial_idx * 1001  # 1001, 2002, 3003, 4004, 5005
                    random.seed(seed)
                    np.random.seed(seed)
                    self.root.after(0, lambda t=trial_idx, n=num_trials: 
                                   self.status_var.set(f"Trial {t+1}/{n}..."))
                
                # Reset ALL objects để tránh cache issues
                self.evaluator = Evaluator()
                self.data_loader = DataLoader()
                
                # Load dữ liệu
                try:
                    data = self.data_loader.load_instance(f"{instance_name}.txt")
                except Exception as e:
                    raise Exception(f"Data load failed: {e}")
                
                # Tạo model
                try:
                    model = JSSPModel(data['n_jobs'], data['n_machines'],
                                    data['processing_times'], data['machine_order'])
                except Exception as e:
                    raise Exception(f"Model creation failed: {e}")
                
                # Chạy SA
                try:
                    time_start = time.time()
                    solver = SASolver(model, self.config)
                    best_solution, best_makespan, history = solver.solve()
                    elapsed_time = time.time() - time_start
                except Exception as e:
                    raise Exception(f"SA solver failed: {e}")
                
                # Đánh giá
                try:
                    bks = self.evaluator.get_bks(instance_name)
                    evaluation = self.evaluator.evaluate_solution(best_makespan, instance_name)
                except Exception as e:
                    raise Exception(f"Evaluation failed: {e}")
                
                # Lưu kết quả trial này
                trial_result = {
                    'trial': trial_idx + 1,
                    'makespan': best_makespan,
                    'gap_percent': evaluation.get('gap_percent', None),
                    'solution': best_solution,
                    'schedule': solver.get_schedule(),
                    'history': history,
                    'model': model,
                    'solver': solver,
                    'elapsed_time': elapsed_time
                }
                trial_results.append(trial_result)
                
                # Track best overall
                if best_makespan < best_makespan_overall:
                    best_makespan_overall = best_makespan
                    best_trial_index = trial_idx
            
            # Xử lý kết quả từ model và solver tốt nhất
            best_result = trial_results[best_trial_index]
            model = best_result['model']
            schedule = best_result['schedule']
            history = best_result['history']
            
            # Naming convention dựa trên mode
            if mode == "single":
                chart_name = instance_name
                result_filename = f"{instance_name}_result.txt"
            else:  # multi
                chart_name = f"{instance_name}_trials"
                result_filename = f"{instance_name}_trials_result.txt"
            
            # Lưu biểu đồ (chỉ từ best trial, không thêm trial number vào tên)
            try:
                visualizer = Visualizer(self.config.results_dir)
                visualizer.plot_gantt_chart(schedule, model, chart_name)
                bks = self.evaluator.get_bks(instance_name)
                visualizer.plot_convergence(history, chart_name, bks)
            except Exception as e:
                print(f"[WARNING] Visualization failed: {e}")
            
            # Format kết quả
            try:
                result_text = self._format_result(instance_name, trial_results, mode)
            except Exception as e:
                raise Exception(f"Format result failed: {e}")
            
            # Lưu kết quả vào file
            try:
                result_file = self.config.results_dir / result_filename
                with open(result_file, 'w', encoding='utf-8') as f:
                    f.write(f"Instance: {instance_name.upper()}\n")
                    f.write(f"{'='*80}\n\n")
                    
                    if mode == "single":
                        evaluation = self.evaluator.evaluate_solution(best_result['makespan'], instance_name)
                        f.write(f"SINGLE RUN MODE\n")
                        f.write(f"{'-'*80}\n")
                        f.write(f"Makespan: {best_result['makespan']}\n")
                        f.write(f"BKS: {evaluation['bks']}\n")
                        gap_str = f"{evaluation['gap_percent']:.2f}" if evaluation['gap_percent'] is not None else 'N/A'
                        f.write(f"Gap (%): {gap_str}\n")
                        f.write(f"Quality: {evaluation['quality']}\n")
                        f.write(f"Time (s): {best_result['elapsed_time']:.3f}\n\n")
                        
                        # Chi tiết quá trình chạy
                        history = best_result['history']
                        f.write(f"QUA TRINH CHAY:\n")
                        f.write(f"  Tong Lap: {history['iterations'][-1] if history['iterations'] else 0}\n")
                        f.write(f"  Chap Nhan: {history['accepted_count']}\n")
                        f.write(f"  Tu Choi: {history['rejected_count']}\n")
                        f.write(f"  Ty Le Chap Nhan: {100*history['accepted_count']/(history['accepted_count']+history['rejected_count']) if (history['accepted_count']+history['rejected_count']) > 0 else 0:.1f}%\n\n")
                        
                        # Lịch sử makespan
                        if history['makespan']:
                            f.write(f"LICH SU MAKESPAN:\n")
                            f.write(f"  Kich Thuoc: {len(history['makespan'])}\n")
                            f.write(f"  Dau: {history['makespan'][0]}\n")
                            f.write(f"  Cuoi (Best): {history['makespan'][-1]}\n")
                            f.write(f"  Cai Thien: {history['makespan'][0] - history['makespan'][-1]}\n\n")
                    else:  # multi
                        # Multiple trials - record stats
                        makespans = [r['makespan'] for r in trial_results]
                        gaps = [r['gap_percent'] for r in trial_results if r['gap_percent'] is not None]
                        times = [r['elapsed_time'] for r in trial_results]
                        best_eval = self.evaluator.evaluate_solution(best_result['makespan'], instance_name)
                        best_idx = makespans.index(min(makespans))
                        
                        f.write(f"MULTI-TRIAL MODE (5 RUNS)\n")
                        f.write(f"{'-'*80}\n")
                        f.write(f"Makespan: {min(makespans)}\n")
                        f.write(f"BKS: {best_eval['bks']}\n")
                        f.write(f"Best Trial: {best_idx + 1}\n")
                        f.write(f"Number of Trials: {num_trials}\n")
                        f.write(f"Average Makespan: {np.mean(makespans):.2f}\n")
                        if gaps:
                            f.write(f"Gap (%): {min(gaps):.2f}\n")
                            f.write(f"Avg Gap (%): {np.mean(gaps):.2f}\n")
                        f.write(f"Total Time (s): {sum(times):.3f}\n")
                        f.write(f"Avg Time per Trial (s): {np.mean(times):.3f}\n\n")
                        
                        # Chi tiết từng trial
                        f.write(f"CHI TIET TUNG TRIAL:\n")
                        f.write(f"{'-'*80}\n\n")
                        for r in trial_results:
                            gap_str = f"{r['gap_percent']:.2f}" if r['gap_percent'] is not None else 'N/A'
                            history = r['history']
                            
                            f.write(f"TRIAL {r['trial']}:\n")
                            f.write(f"  Makespan: {r['makespan']}\n")
                            f.write(f"  Gap (%): {gap_str}%\n")
                            f.write(f"  Time (s): {r['elapsed_time']:.3f}\n")
                            f.write(f"  \n")
                            f.write(f"  Qua Trinh Chay:\n")
                            f.write(f"    Tong Lap: {history['iterations'][-1] if history['iterations'] else 0}\n")
                            f.write(f"    Chap Nhan: {history['accepted_count']}\n")
                            f.write(f"    Tu Choi: {history['rejected_count']}\n")
                            f.write(f"    Ty Le Chap Nhan: {100*history['accepted_count']/(history['accepted_count']+history['rejected_count']) if (history['accepted_count']+history['rejected_count']) > 0 else 0:.1f}%\n")
                            
                            if history['makespan']:
                                f.write(f"    Lich Su Makespan:\n")
                                f.write(f"      Dau: {history['makespan'][0]}\n")
                                f.write(f"      Cuoi (Best): {history['makespan'][-1]}\n")
                                f.write(f"      Cai Thien: {history['makespan'][0] - history['makespan'][-1]}\n")
                            f.write(f"\n")
                    
                    f.write(f"{'='*80}\n")
                    f.write(f"Schedule:\n")
                    f.write(f"{model.get_schedule_info(best_result['solution'])}\n")
            except Exception as e:
                raise Exception(f"Save result failed: {e}")
            
            # Cập nhật UI (thread-safe)
            self.root.after(0, self._update_result_ui, result_text)
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"[ERROR] _solve_thread: {error_msg}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda err=error_msg: messagebox.showerror("Loi", f"Loi: {err}"))
        
        finally:
            self.is_running = False
            self.root.after(0, self._finish_run)
    
    def _format_result(self, instance_name, trial_results, mode="single"):
        """Format kết quả (hỗ trợ 1 trial hoặc 5 trials)"""
        num_trials = len(trial_results)
        
        if mode == "single":
            # Single run mode
            result = trial_results[0]
            evaluation = self.evaluator.evaluate_solution(result['makespan'], instance_name)
            history = result['history']
            
            gap_display = f"{evaluation['gap_percent']:.2f}" if evaluation['gap_percent'] is not None else 'N/A'
            
            result_text = f"""
========== KET QUA (1 LAN CHAY) ==========
Instance:        {instance_name.upper()}
Makespan:        {result['makespan']}
BKS:             {evaluation['bks']}
Gap (%):         {gap_display}
Chat Luong:      {evaluation['quality']}
Time (s):        {result['elapsed_time']:.3f}

========== THONG KE ==========
Tong Lap:        {history['iterations'][-1] if history['iterations'] else 0}
Chap Nhan:       {history['accepted_count']}
Tu Choi:         {history['rejected_count']}
Ty Le Chap Nhan: {100*history['accepted_count']/(history['accepted_count']+history['rejected_count']) if (history['accepted_count']+history['rejected_count']) > 0 else 0:.1f}%

========== HIEN TRANG ==========
- Gantt chart: results/gantt_{instance_name}.png
- Convergence: results/convergence_{instance_name}.png
- Results: results/{instance_name}_result.txt
"""
        else:  # multi
            # Multiple trials mode (5 trials)
            makespans = [r['makespan'] for r in trial_results]
            gaps = [r['gap_percent'] for r in trial_results if r['gap_percent'] is not None]
            times = [r['elapsed_time'] for r in trial_results]
            
            best_idx = makespans.index(min(makespans))
            best_result = trial_results[best_idx]
            
            best_eval = self.evaluator.evaluate_solution(best_result['makespan'], instance_name)
            avg_makespan = np.mean(makespans)
            avg_gap = np.mean(gaps) if gaps else None
            avg_time = np.mean(times)
            
            # Format trial details
            trial_details = "\n".join([
                f"  Trial {r['trial']:2d}: C_max={r['makespan']:4d}, Gap={r['gap_percent']:6.2f}%, Time={r['elapsed_time']:6.3f}s"
                for r in trial_results
            ])
            
            avg_gap_str = f"{avg_gap:.2f}" if avg_gap is not None else 'N/A'
            best_gap_str = f"{best_eval['gap_percent']:.2f}" if best_eval['gap_percent'] is not None else 'N/A'
            
            result_text = f"""
========== KET QUA (5 TRIALS - MULTI-TRIAL MODE) ==========
Instance:        {instance_name.upper()}

TONG HOP:
  C_max (best):  {min(makespans)}  [Trial {best_idx+1}]
  C_max (avg):   {avg_makespan:.2f}
  BKS:           {best_eval['bks']}
  Gap (best):    {best_gap_str}%
  Gap (avg):     {avg_gap_str}%
  Time (total):  {sum(times):.3f}s
  Time (avg):    {avg_time:.3f}s

CHI TIET TUNG TRIAL:
{trial_details}

BEST TRIAL: Trial {best_idx+1}
THONG KE TU TRIAL TOT NHAT:
  Tong Lap:      {best_result['history']['iterations'][-1] if best_result['history']['iterations'] else 0}
  Chap Nhan:     {best_result['history']['accepted_count']}
  Tu Choi:       {best_result['history']['rejected_count']}
  Ty Le:         {100*best_result['history']['accepted_count']/(best_result['history']['accepted_count']+best_result['history']['rejected_count']) if (best_result['history']['accepted_count']+best_result['history']['rejected_count']) > 0 else 0:.1f}%

HIEN TRANG:
- Gantt chart: results/gantt_{instance_name}_trials.png
- Convergence: results/convergence_{instance_name}_trials.png
- Results: results/{instance_name}_trials_result.txt
"""
        
        return result_text
    
    def _update_result_ui(self, result_text):
        """Cập nhật UI kết quả"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, result_text)
    
    def _finish_run(self):
        """Kết thúc chạy"""
        self.progress.stop()
        self.btn_run.config(state=tk.NORMAL)
        self.status_var.set("Hoan tat!")
        # Tự động reload danh sách kết quả
        self.load_results_list()
    
    def show_result_file(self):
        """Mở file kết quả chi tiết"""
        if not self.current_selected_instance or not self.current_selected_mode:
            messagebox.showwarning("Canh Bao", "Hay chon mot ket qua truoc!")
            return
        
        instance_name = self.current_selected_instance
        mode = self.current_selected_mode
        
        # Xác định file name dựa trên mode
        if mode == "Multi-Trial":
            result_file = Path(self.config.results_dir) / f"{instance_name}_trials_result.txt"
        else:
            result_file = Path(self.config.results_dir) / f"{instance_name}_result.txt"
        
        if not result_file.exists():
            messagebox.showwarning("Canh Bao", f"File khong ton tai!\n{result_file}")
            return
        
        # Mở với ứng dụng mặc định
        import subprocess
        import os
        if sys.platform == 'win32':
            os.startfile(str(result_file))
        else:
            subprocess.Popen(['xdg-open', str(result_file)])
    
    def show_gantt(self):
        """Hiển thị Gantt chart"""
        if not self.current_selected_instance:
            messagebox.showwarning("Canh Bao", "Hay chon mot ket qua truoc!")
            return
        
        instance_name = self.current_selected_instance
        
        # Thử tìm file: nếu là multi-trial thì tìm _trials, nếu không thì tìm single
        gantt_file_multi = Path(self.config.results_dir) / f"gantt_{instance_name}_trials.png"
        gantt_file_single = Path(self.config.results_dir) / f"gantt_{instance_name}.png"
        
        if gantt_file_multi.exists():
            gantt_file = gantt_file_multi
        elif gantt_file_single.exists():
            gantt_file = gantt_file_single
        else:
            messagebox.showwarning("Canh Bao", f"File khong ton tai!")
            return
        
        # Mở với ứng dụng mặc định
        import subprocess
        import os
        if sys.platform == 'win32':
            os.startfile(str(gantt_file))
        else:
            subprocess.Popen(['xdg-open', str(gantt_file)])
    
    def show_convergence(self):
        """Hiển thị Convergence plot"""
        if not self.current_selected_instance:
            messagebox.showwarning("Canh Bao", "Hay chon mot ket qua truoc!")
            return
        
        instance_name = self.current_selected_instance
        
        # Thử tìm file: nếu là multi-trial thì tìm _trials, nếu không thì tìm single
        convergence_file_multi = Path(self.config.results_dir) / f"convergence_{instance_name}_trials.png"
        convergence_file_single = Path(self.config.results_dir) / f"convergence_{instance_name}.png"
        
        if convergence_file_multi.exists():
            convergence_file = convergence_file_multi
        elif convergence_file_single.exists():
            convergence_file = convergence_file_single
        else:
            messagebox.showwarning("Canh Bao", f"File khong ton tai!")
            return
        
        # Mở với ứng dụng mặc định
        import subprocess
        import os
        if sys.platform == 'win32':
            os.startfile(str(convergence_file))
        else:
            subprocess.Popen(['xdg-open', str(convergence_file)])
    
    def open_results_folder(self):
        """Mở folder results"""
        results_dir = Path(self.config.results_dir).absolute()
        
        import subprocess
        import os
        import platform
        
        try:
            if platform.system() == 'Windows':
                os.startfile(str(results_dir))
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', str(results_dir)])
            else:  # Linux
                subprocess.Popen(['xdg-open', str(results_dir)])
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the mo folder: {e}")
    
    def load_results_list(self):
        """Load danh sách kết quả từ folder results"""
        # Xóa danh sách cũ
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        results_dir = Path(self.config.results_dir)
        
        # Tìm tất cả file *_result.txt và *_trials_result.txt
        result_files_single = sorted(results_dir.glob("*_result.txt"))
        result_files_multi = sorted(results_dir.glob("*_trials_result.txt"))
        
        # Lọc ra những file _result.txt mà không phải _trials_result.txt
        result_files_single = [f for f in result_files_single if not f.name.endswith("_trials_result.txt")]
        
        # Merge và sort
        result_files = sorted(result_files_single + result_files_multi)
        
        if not result_files:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, "Khong co ket qua nao.\nHay chay thuat toan de tao ket qua!")
            self.btn_gantt.config(state=tk.DISABLED)
            self.btn_convergence.config(state=tk.DISABLED)
            return
        
        # Duyệt qua từng file kết quả
        for result_file in result_files:
            # Xác định mode dựa trên tên file
            if result_file.name.endswith("_trials_result.txt"):
                instance_name = result_file.stem.replace("_trials_result", "")
                mode = "Multi-Trial"
            else:
                instance_name = result_file.stem.replace("_result", "")
                mode = "Single"
            
            # Đọc file kết quả để lấy Makespan, BKS, Gap
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Parse chính xác
                    makespan = "N/A"
                    bks = "N/A"
                    gap = "N/A"
                    
                    lines = content.split('\n')
                    
                    # Cho multi-trial, chỉ parse phần trước "CHI TIET TUNG TRIAL"
                    chi_tiet_idx = -1
                    for i, line in enumerate(lines):
                        if "CHI TIET TUNG TRIAL" in line:
                            chi_tiet_idx = i
                            break
                    
                    # Parse từ đầu tới phần chi tiết (nếu không có chi tiết thì parse hết)
                    parse_end = chi_tiet_idx if chi_tiet_idx >= 0 else len(lines)
                    
                    for i in range(parse_end):
                        line = lines[i]
                        
                        if line.startswith("Makespan:"):
                            try:
                                makespan = line.split(":")[1].strip()
                            except:
                                pass
                        elif line.startswith("BKS:"):
                            try:
                                bks = line.split(":")[1].strip()
                            except:
                                pass
                        elif line.strip().startswith("Gap (%)"):  # Chỉ "Gap (%): " (không phải "Avg Gap (%)")
                            if "Avg" not in line:
                                try:
                                    gap = line.split(":")[1].strip().replace("%", "").strip()
                                except:
                                    pass
                    
                    # Thêm vào tree (thêm cột Mode)
                    self.results_tree.insert("", "end", 
                                            values=(instance_name.upper(), makespan, bks, gap, mode),
                                            tags=("oddrow" if len(result_files) % 2 == 0 else "evenrow",))
            except Exception as e:
                print(f"Loi doc file {result_file}: {e}")
        
        # Styling
        self.results_tree.tag_configure("oddrow", background="#f0f0f0")
        self.results_tree.tag_configure("evenrow", background="white")
    
    def on_result_select(self, event):
        """Khi chọn một item trong danh sách"""
        selection = self.results_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.results_tree.item(item, 'values')
        
        if values:
            instance_name = values[0].lower()
            mode = values[4] if len(values) > 4 else "Single"  # Get Mode column
            
            self.current_selected_instance = instance_name
            self.current_selected_mode = mode
            
            # Load kết quả chi tiết
            self.display_result_detail(instance_name, mode)
            
            # Bật nút xem biểu đồ
            self.btn_gantt.config(state=tk.NORMAL)
            self.btn_convergence.config(state=tk.NORMAL)
            self.btn_result.config(state=tk.NORMAL)
    
    def display_result_detail(self, instance_name, mode="Single"):
        """Hiển thị chi tiết kết quả"""
        # Xác định file name dựa trên mode
        if mode == "Multi-Trial":
            result_file = Path(self.config.results_dir) / f"{instance_name}_trials_result.txt"
        else:
            result_file = Path(self.config.results_dir) / f"{instance_name}_result.txt"
        
        if result_file.exists():
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, content)
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, f"File ket qua khong ton tai:\n{result_file}")
    
    def delete_selected_result(self):
        """Xóa kết quả đã chọn"""
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showwarning("Canh Bao", "Hay chon mot ket qua de xoa!")
            return
        
        item = selection[0]
        values = self.results_tree.item(item, 'values')
        
        if not values:
            return
        
        instance_name = values[0].lower()
        mode = values[4] if len(values) > 4 else "Single"  # Get Mode column
        
        # Xác nhận xóa
        if messagebox.askyesno("Xac Nhan", f"Ban chac chan muon xoa ket qua {instance_name.upper()} ({mode})?"):
            try:
                # Xác định file dựa trên mode
                if mode == "Multi-Trial":
                    result_file = Path(self.config.results_dir) / f"{instance_name}_trials_result.txt"
                    gantt_file = Path(self.config.results_dir) / f"gantt_{instance_name}_trials.png"
                    convergence_file = Path(self.config.results_dir) / f"convergence_{instance_name}_trials.png"
                else:  # Single
                    result_file = Path(self.config.results_dir) / f"{instance_name}_result.txt"
                    gantt_file = Path(self.config.results_dir) / f"gantt_{instance_name}.png"
                    convergence_file = Path(self.config.results_dir) / f"convergence_{instance_name}.png"
                
                for file in [result_file, gantt_file, convergence_file]:
                    if file.exists():
                        file.unlink()
                
                # Refresh danh sách
                self.load_results_list()
                self.result_text.delete(1.0, tk.END)
                self.btn_gantt.config(state=tk.DISABLED)
                self.btn_convergence.config(state=tk.DISABLED)
                
                messagebox.showinfo("Thong Bao", f"Da xoa ket qua {instance_name.upper()} ({mode})")
            except Exception as e:
                messagebox.showerror("Loi", f"Khong the xoa: {e}")
    
    def reset(self):
        """Reset"""
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("San sang")


def main():
    root = tk.Tk()
    app = SAJSSP_GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
