# 📁 CẤU TRÚC DỰ ÁN - SA for Job Shop Scheduling

## 🎯 Tổng Quan Cấu Trúc

```
SAforJSScheduling/
├── config/                          # ⚙️ Cấu hình & tham số
│   ├── __init__.py
│   └── config.py                    # SAConfig class
│
├── src/                             # 💻 Mã nguồn chính
│   ├── __init__.py
│   ├── data_loader.py               # Đọc file dữ liệu
│   ├── jssp_model.py                # Mô hình JSSP (Operation-based encoding)
│   ├── sa_solver.py                 # Thuật toán SA (4 giai đoạn)
│   ├── evaluator.py                 # Đánh giá kết quả vs BKS
│   ├── utils.py                     # Hàm hỗ trợ (cooling, operators, etc.)
│   └── visualizer.py                # Vẽ biểu đồ Gantt & Convergence
│
├── data/                            # 📚 Dữ liệu nhập vào
│   ├── la01.txt to la40.txt         # 40 instances từ OR-Library
│   └── LA_BKS.csv                   # Best Known Solutions (benchmark)
│
├── results/                         # 📊 Kết quả đầu ra
│   ├── gantt_*.png                  # Biểu đồ Gantt cho mỗi instance
│   ├── convergence_*.png            # Biểu đồ hội tụ cho mỗi instance
│   └── *_result.txt                 # Tệp kết quả chi tiết
│
├── gui/                             # 🖥️ Giao diện người dùng
│   ├── __init__.py
│   └── gui.py                       # Tkinter GUI (Tab: Config + Results)
│
├── docs/                            # 📖 Tài liệu & Báo cáo
│   ├── __init__.py
│   ├── README_ARCHITECTURE.md       # Kiến trúc chi tiết
│   ├── GUIDE_GUI.md                 # Hướng dẫn sử dụng GUI
│   ├── PARAMETERS_NOTES.md          # Ghi chú tham số
│   ├── CODE_REVIEW_CHAPTER3.md      # Kiểm tra code Chapter 3
│   ├── CHAPTER3_VERIFICATION_REPORT.md  # Báo cáo xác minh
│   ├── INDEX_CHAPTER3_VERIFICATION.md   # Chỉ mục xác minh
│   ├── FINAL_CHAPTER3_VERDICT.txt   # Kết luận cuối cùng
│   └── GUI_ENHANCEMENT_REPORT.md    # Báo cáo cải tiến GUI
│
├── scripts/                         # 🔧 Script hỗ trợ & kiểm tra
│   ├── __init__.py
│   ├── verify_chapter3_features.py  # Xác minh 8 tính mới Chapter 3
│   ├── test_loader.py               # Test data loader
│   ├── test_gui.py                  # Test GUI methods
│   ├── create_la_files.py           # Tạo/cập nhật LA files
│   └── download_la_datasets.py      # Download datasets từ OR-Library
│
├── main.py                          # 🚀 Entry point chính
├── README.md                        # 📝 Hướng dẫn tổng quan (GitHub)
└── requirement.txt                  # 📦 Thư viện phụ thuộc

```

---

## 📖 HƯỚNG DẪN SỬ DỤNG CẤU TRÚC

### 🏃 Chạy Ứng Dụng

#### **Option 1: GUI Mode**
```bash
# Mở giao diện graphical
python main.py
# Hoặc chạy trực tiếp GUI
python gui/gui.py
```

#### **Option 2: Command Line Mode**
```bash
# Chạy thuật toán từ terminal
python main.py
# Lựa chọn: 1 (Single) hoặc 2 (Batch)
```

#### **Option 3: Script Mode**
```bash
# Chạy script kiểm chứng
python scripts/verify_chapter3_features.py

# Tạo/cập nhật data files
python scripts/create_la_files.py

# Download datasets
python scripts/download_la_datasets.py
```

---

## 🔧 IMPORT PATHS

### **Từ main.py**
```python
from config import SAConfig             # Import từ config/
from src.data_loader import DataLoader  # Import từ src/
from src.jssp_model import JSSPModel
# ...
```

### **Từ gui/gui.py**
```python
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))
sys.path.insert(0, str(project_root / 'config'))

from config import SAConfig
from src.data_loader import DataLoader
# ...
```

### **Từ scripts/**
```python
# Cần add parent paths
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'config'))

from config import SAConfig
from src.data_loader import DataLoader
# ...
```

---

## 📊 MODULE RELATIONSHIPS

```
main.py
├─→ config/config.py (SAConfig)
├─→ src/data_loader.py (DataLoader)
├─→ src/jssp_model.py (JSSPModel)
├─→ src/sa_solver.py (SASolver) ← Điều khiển chính
│   ├─→ src/utils.py (Operators, Cooling, etc.)
│   └─→ src/jssp_model.py (Tính Makespan)
├─→ src/evaluator.py (Evaluator - BKS comparison)
└─→ src/visualizer.py (Gantt & Convergence charts)

gui/gui.py
├─→ All of above + Tkinter UI
└─→ Results management

scripts/
├─→ verify_chapter3_features.py
│   └─→ Kiểm chứng 8 tính mới Chapter 3
├─→ test_loader.py
├─→ test_gui.py
└─→ create_la_files.py, download_la_datasets.py
```

---

## 📝 QUYỀN SỬ DỤNG FILES

| Thư Mục | Quyền | Ghi Chú |
|---------|------|--------|
| **config/** | Read-only | Không chỉnh sửa (khác thử nghiệm) |
| **src/** | Read-only | Core algorithm (production) |
| **data/** | Write | Chứa datasets & benchmark data |
| **results/** | Write | Output files (tự động tạo) |
| **gui/** | Run | Gọi từ main.py hoặc trực tiếp |
| **docs/** | Read | Tài liệu tham khảo |
| **scripts/** | Run | Chạy cho testing/verification |
| **main.py** | Run | Entry point chính |

---

## 🔍 HỖTỢ KIỂM TRA CẤU TRÚC

```bash
# Kiểm tra xem cấu trúc đã đúng chưa
ls -la config/          # Xem config files
ls -la src/             # Xem source files
ls -la data/            # Xem data files
ls -la results/         # Xem output files
ls -la gui/             # Xem GUI files
ls -la docs/            # Xem documentation
ls -la scripts/         # Xem scripts
```

---

## 🎯 FLOW QUÁ TRÌNH

### **1. Initialization (Khởi động)**
```
main.py → SAConfig (config/) → DataLoader (src/)
```

### **2. Problem Setup (Chuẩn bị)**
```
DataLoader → JSSPModel (src/) → Load data from data/
```

### **3. Optimization (Tối ưu hóa)**
```
SASolver (src/) ← Metropolis + Adaptive Cooling + Early Stopping
   ↓
   ├─→ NeighborhoodOperators (Swap/Move)
   ├─→ CoolingSchedule (Adaptive α)
   ├─→ MetropolisAcceptance (Accept/Reject)
   └─→ EarlyStoppingChecker (Convergence check)
```

### **4. Evaluation (Đánh giá)**
```
SASolver → Evaluator (src/) → Compare with BKS (data/LA_BKS.csv)
```

### **5. Output (Xuất kết quả)**
```
Visualizer (src/) → results/ (Gantt + Convergence)
                 → *_result.txt
```

### **6. UI Display (Hiển thị)**
```
gui.py → Load results/ → Display in Tkinter
      ├─→ Tab 1: Configuration
      └─→ Tab 2: Results (with list view & charts)
```

---

## 💾 CÁCH BACKUP & RESTORE

### **Backup**
```bash
# Backup entire project
robocopy . backup_folder /S /E

# Backup chỉ results
robocopy results backup_results /S /E

# Backup chỉ data
robocopy data backup_data /S /E
```

### **Restore**
```bash
# Restore từ backup
robocopy backup_folder . /S /E
```

---

## 🚨 TROUBLESHOOTING

### **Import Error: No module named 'config'**
```
→ Kiểm tra sys.path.insert() trong script
→ Đảm bảo config/__init__.py tồn tại
→ Chạy từ project root, không từ subfolder
```

### **FileNotFoundError: data/la01.txt**
```
→ Kiểm tra data folder có files không
→ Chạy: python scripts/create_la_files.py
→ Hoặc: python scripts/download_la_datasets.py
```

### **GUI không hiển thị**
```
→ Đảm bảo PIL/Pillow được cài: pip install Pillow
→ Kiểm tra gui/gui.py imports
→ Chạy: python gui/gui.py trực tiếp
```

---

## 📚 TÀI LIỆU LIÊN QUAN

- **GUIDE_GUI.md** → Hướng dẫn GUI từng bước
- **PARAMETERS_NOTES.md** → Giải thích tất cả tham số
- **CODE_REVIEW_CHAPTER3.md** → Kiểm tra 8 tính mới
- **CHAPTER3_VERIFICATION_REPORT.md** → Báo cáo chi tiết
- **README.md** → Tổng quan dự án (cho GitHub)

---

**Cập nhật lần cuối**: April 9, 2025  
**Version**: 1.0 - Reorganized Structure  
**Status**: ✅ Ready
