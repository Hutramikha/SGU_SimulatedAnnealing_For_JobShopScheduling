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
        columns = ("Instance", "Makespan", "BKS", "Gap(%)")
        self.results_tree = ttk.Treeview(frame_list, columns=columns, height=15, show="tree headings")
        self.results_tree.column("#0", width=0)
        self.results_tree.column("Instance", anchor=tk.W, width=80)
        self.results_tree.column("Makespan", anchor=tk.CENTER, width=80)
        self.results_tree.column("BKS", anchor=tk.CENTER, width=60)
        self.results_tree.column("Gap(%)", anchor=tk.CENTER, width=60)
        
        self.results_tree.heading("Instance", text="Instance")
        self.results_tree.heading("Makespan", text="Makespan")
        self.results_tree.heading("BKS", text="BKS")
        self.results_tree.heading("Gap(%)", text="Gap(%)")
        
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
        
        ttk.Button(frame_charts, text="Mo Folder Results",
                  command=self.open_results_folder).pack(side=tk.LEFT, padx=3)
        
        # Lưu instance hiện tại
        self.current_selected_instance = None
        
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
        
        # Chạy trong thread riêng
        self.is_running = True
        self.btn_run.config(state=tk.DISABLED)
        self.progress.start()
        self.status_var.set(f"Dang chay {instance_name.upper()}...")
        
        thread = threading.Thread(target=self._solve_thread, args=(instance_name,))
        thread.daemon = True
        thread.start()
    
    def _solve_thread(self, instance_name):
        """Thread chạy thuật toán"""
        try:
            # Reset ALL objects mỗi lần chạy để tránh cache issues
            # ← Đây là nguyên nhân lỗi: LA07 rồi LA06, state bị cache!
            self.evaluator = Evaluator()
            self.data_loader = DataLoader()  # ← Reset DataLoader
            print(f"[DEBUG] All objects reset. Instance: {instance_name}")
            
            # Load dữ liệu
            try:
                data = self.data_loader.load_instance(f"{instance_name}.txt")
                print(f"[DEBUG] Data loaded. Jobs: {data['n_jobs']}, Machines: {data['n_machines']}")
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
                solver = SASolver(model, self.config)
                best_solution, best_makespan, history = solver.solve()
                print(f"[DEBUG] SA solve done. Best makespan: {best_makespan}")
            except Exception as e:
                raise Exception(f"SA solver failed: {e}")
            
            # Đánh giá
            try:
                bks = self.evaluator.get_bks(instance_name)
                print(f"[DEBUG] Got BKS: {bks}")
                
                evaluation = self.evaluator.evaluate_solution(best_makespan, instance_name)
                print(f"[DEBUG] Evaluation: gap={evaluation.get('gap_percent', 'ERROR')}")
            except Exception as e:
                raise Exception(f"Evaluation failed: {e}")
            
            # Lưu biểu đồ
            try:
                visualizer = Visualizer(self.config.results_dir)
                schedule = solver.get_schedule()
                visualizer.plot_gantt_chart(schedule, model, instance_name)
                bks = self.evaluator.get_bks(instance_name)
                visualizer.plot_convergence(history, instance_name, bks)
            except Exception as e:
                print(f"[WARNING] Visualization failed: {e}")
            
            # Hiển thị kết quả
            try:
                result_text = self._format_result(instance_name, evaluation, history)
            except Exception as e:
                raise Exception(f"Format result failed: {e}")
            
            # Lưu kết quả vào file (cùng format như main.py)
            try:
                result_file = self.config.results_dir / f"{instance_name}_result.txt"
                with open(result_file, 'w', encoding='utf-8') as f:
                    f.write(f"Instance: {instance_name.upper()}\n")
                    f.write(f"Makespan: {best_makespan}\n")
                    f.write(f"BKS: {evaluation['bks']}\n")
                    # Check "is not None" để tránh 0 bị xem là False
                    gap_str = f"{evaluation['gap_percent']:.2f}" if evaluation['gap_percent'] is not None else 'N/A'
                    f.write(f"Gap (%): {gap_str}\n")
                    f.write(f"Quality: {evaluation['quality']}\n\n")
                    f.write(f"Schedule:\n{model.get_schedule_info(best_solution)}\n")
            except Exception as e:
                raise Exception(f"Save result failed: {e}")
            
            # Cập nhật UI (thread-safe)
            self.root.after(0, self._update_result_ui, result_text)
            
        except Exception as e:
            # Capture exception trong default argument để tránh closure issue
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"[ERROR] _solve_thread: {error_msg}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda err=error_msg: messagebox.showerror("Loi", f"Loi: {err}"))
        
        finally:
            self.is_running = False
            self.root.after(0, self._finish_run)
    
    def _format_result(self, instance_name, evaluation, history):
        """Format kết quả"""
        # Tính gap_display trước để tránh syntax error trong f-string format specifier
        # Check "is not None" để tránh 0 bị xem là False
        gap_display = f"{evaluation['gap_percent']:.2f}" if evaluation['gap_percent'] is not None else 'N/A'
        
        result = f"""
========== KET QUA ==========
Instance:        {instance_name.upper()}
Makespan:        {evaluation['makespan']}
BKS:             {evaluation['bks']}
Gap (%):         {gap_display}
Chat Luong:      {evaluation['quality']}

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
        return result
    
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
    
    def show_gantt(self):
        """Hiển thị Gantt chart"""
        if not self.current_selected_instance:
            messagebox.showwarning("Canh Bao", "Hay chon mot ket qua truoc!")
            return
        
        instance_name = self.current_selected_instance
        gantt_file = Path(self.config.results_dir) / f"gantt_{instance_name}.png"
        
        if not gantt_file.exists():
            messagebox.showwarning("Canh Bao", f"File khong ton tai!\n{gantt_file}")
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
        convergence_file = Path(self.config.results_dir) / f"convergence_{instance_name}.png"
        
        if not convergence_file.exists():
            messagebox.showwarning("Canh Bao", f"File khong ton tai!\n{convergence_file}")
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
        
        # Tìm tất cả file gantt_*.txt hoặc convergence_*.txt
        result_files = sorted(results_dir.glob("*_result.txt"))
        
        if not result_files:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, "Khong co ket qua nao.\nHay chay thuat toan de tao ket qua!")
            self.btn_gantt.config(state=tk.DISABLED)
            self.btn_convergence.config(state=tk.DISABLED)
            return
        
        # Duyệt qua từng file kết quả
        for result_file in result_files:
            instance_name = result_file.stem.replace("_result", "")
            
            # Đọc file kết quả để lấy Makespan, BKS, Gap
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Parse básico
                    makespan = "N/A"
                    bks = "N/A"
                    gap = "N/A"
                    
                    for line in content.split('\n'):
                        if line.startswith("Makespan:"):
                            makespan = line.split()[-1]
                        elif line.startswith("BKS:"):
                            bks = line.split()[-1]
                        elif line.startswith("Gap"):
                            gap = line.split()[-1].replace("%", "")
                    
                    # Thêm vào tree
                    self.results_tree.insert("", "end", 
                                            values=(instance_name.upper(), makespan, bks, gap),
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
            self.current_selected_instance = instance_name
            
            # Load kết quả chi tiết
            self.display_result_detail(instance_name)
            
            # Bật nút xem biểu đồ
            self.btn_gantt.config(state=tk.NORMAL)
            self.btn_convergence.config(state=tk.NORMAL)
    
    def display_result_detail(self, instance_name):
        """Hiển thị chi tiết kết quả"""
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
        
        # Xác nhận xóa
        if messagebox.askyesno("Xac Nhan", f"Ban chac chan muon xoa ket qua {instance_name.upper()}?"):
            try:
                # Xóa các file liên quan
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
                
                messagebox.showinfo("Thong Bao", f"Da xoa ket qua {instance_name.upper()}")
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
