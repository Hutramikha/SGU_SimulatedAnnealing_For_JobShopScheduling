"""
Tạo file la01.txt tới la40.txt từ OR-Library
"""

import urllib.request
from pathlib import Path

data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

print("Đang tải jobshop1.txt từ OR-Library...\n")

url = "http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/jobshop1.txt"
temp_file = data_folder / "jobshop1_temp.txt"

try:
    urllib.request.urlretrieve(url, temp_file)
    
    # Đọc file toàn bộ
    with open(temp_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Trích xuất tất cả instances
    lines = content.split('\n')
    
    current_instance = None
    current_data = []
    instances = {}
    
    for line in lines:
        line_stripped = line.strip()
        
        # Kiểm tra nếu là bắt đầu instance
        if line_stripped.lower().startswith('instance '):
            # Lưu instance trước nếu có
            if current_instance and current_data:
                instances[current_instance] = current_data
            
            # Lấy tên instance
            parts = line_stripped.split()
            current_instance = parts[-1].lower() if len(parts) > 1 else None
            current_data = []
        elif current_instance:
            # Nếu là dữ liệu (không phải header/separator)
            if line_stripped and not line_stripped.startswith('+++') and not line_stripped.startswith('---'):
                current_data.append(line_stripped)
    
    # Lưu instance cuối cùng
    if current_instance and current_data:
        instances[current_instance] = current_data
    
    # Tạo file LA01-LA40
    print("Đang tạo file LA01-LA40...\n")
    count = 0
    for i in range(1, 41):
        la_name = f"la{i:02d}"
        if la_name in instances:
            file_path = data_folder / f"{la_name}.txt"
            with open(file_path, 'w') as f:
                f.write('\n'.join(instances[la_name]))
            print(f"[OK] {la_name}.txt ({len(instances[la_name])} dòng)")
            count += 1
        else:
            print(f"✗ Không tìm thấy {la_name}")
    
    # Xóa file temp
    temp_file.unlink()
    
    print(f"\n{'='*60}")
    print(f"[OK] Hoàn tất! Đã tạo {count}/40 files")
    print(f"  Lưu tại: {data_folder.absolute()}/")
    print(f"{'='*60}")
    
except Exception as e:
    print(f"✗ Lỗi: {e}")
    if temp_file.exists():
        temp_file.unlink()
