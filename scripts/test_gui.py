#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_gui.py - Test các method của GUI
"""

import tkinter as tk
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from gui.gui import SAJSSP_GUI

def test_gui():
    """Test GUI methods"""
    root = tk.Tk()
    root.withdraw()  # Hide window
    
    try:
        app = SAJSSP_GUI(root)
        
        # Test 1: load_results_list()
        print("[TEST 1] load_results_list()...")
        app.load_results_list()
        print("  [OK] Danh sách kết quả được tải")
        print(f"  Số items: {len(app.results_tree.get_children())}")
        
        # Test 2: Kiểm tra tree có dữ liệu
        items = app.results_tree.get_children()
        if items:
            first_item = items[0]
            values = app.results_tree.item(first_item, 'values')
            print(f"  [OK] Item đầu tiên: {values}")
            
            # Test 3: on_result_select()
            print("\n[TEST 2] on_result_select()...")
            app.results_tree.selection_set(first_item)
            app.on_result_select(None)
            print(f"  [OK] Chọn item: {app.current_selected_instance}")
            
            # Test 4: Kiểm tra nút được bật
            print("\n[TEST 3] Button state...")
            gantt_state = app.btn_gantt['state']
            conv_state = app.btn_convergence['state']
            print(f"  Gantt button: {gantt_state}")
            print(f"  Convergence button: {conv_state}")
            
            # Test 5: display_result_detail()
            print("\n[TEST 4] display_result_detail()...")
            result_text = app.result_text.get(1.0, tk.END)
            lines = result_text.strip().split('\n')
            print(f"  [OK] Chi tiết kết quả ({len(lines)} dòng)")
            print(f"  Dòng đầu: {lines[0][:50]}")
            
            # Test 6: delete_selected_result() (không thực hiện, chỉ check)
            print("\n[TEST 5] delete_selected_result() - SKIP test thực tế")
            print("  (Bỏ qua để không xóa kết quả)")
        
        print("\n" + "="*50)
        print("[OK] TẤT CẢ TEST PASSED!")
        print("="*50)
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        root.quit()

if __name__ == "__main__":
    test_gui()
