# ✅ Path Issues - FIXED

## 🔴 Vấn đề Ban Đầu

Khi chạy GUI từ `gui/` directory:
```bash
cd gui
python gui.py
```

Nó báo lỗi: `data/la01.txt không tồn tại`

**Nguyên nhân:** Các class khởi tạo với relative paths (`data`, `results`, `LA_BKS.csv`), nên:
- Khi chạy từ `gui/` → tìm ở `gui/data/` ❌
- Khi chạy từ root → tìm ở `data/` ✅

---

## 🟢 Giải Pháp

### 1. **DataLoader** (`src/data_loader.py`)
**Trước:**
```python
def __init__(self, data_dir="data"):
    self.data_dir = Path(data_dir)
```

**Sau:**
```python
def __init__(self, data_dir=None):
    if data_dir is None:
        project_root = Path(__file__).parent.parent
        self.data_dir = project_root / "data"
    else:
        self.data_dir = Path(data_dir)
```

### 2. **Evaluator** (`src/evaluator.py`)
**Trước:**
```python
def __init__(self, bks_file: str = "LA_BKS.csv"):
    self.load_bks(bks_file)
```

**Sau:**
```python
def __init__(self, bks_file=None):
    if bks_file is None:
        project_root = Path(__file__).parent.parent
        bks_file = project_root / "data" / "LA_BKS.csv"
    self.load_bks(bks_file)
```

### 3. **Visualizer** (`src/visualizer.py`)
**Trước:**
```python
def __init__(self, output_dir: str = "results"):
    self.output_dir = Path(output_dir)
    self.output_dir.mkdir(exist_ok=True)
```

**Sau:**
```python
def __init__(self, output_dir=None):
    if output_dir is None:
        project_root = Path(__file__).parent.parent
        self.output_dir = project_root / "results"
    else:
        self.output_dir = Path(output_dir)
    self.output_dir.mkdir(exist_ok=True)
```

### 4. **SAConfig** (`config/config.py`)
**Trước:**
```python
self.data_dir = "data"
self.results_dir = "results"
self.bks_file = "LA_BKS.csv"
```

**Sau:**
```python
project_root = Path(__file__).parent.parent
self.data_dir = project_root / "data"
self.results_dir = project_root / "results"
self.bks_file = project_root / "data" / "LA_BKS.csv"
```

---

## ✅ Cách Chạy - Tất Cả Đều Hoạt động

### ✅ Từ Project Root
```bash
cd d:\Github\SAforJSScheduling

# Chạy main
python main.py

# Chạy GUI
python gui/gui.py
# hoặc
python -m gui.gui
```

### ✅ Từ gui/ Directory
```bash
cd d:\Github\SAforJSScheduling\gui

# Chạy GUI trực tiếp
python gui.py
```

### ✅ Từ Scripts Directory
```bash
cd d:\Github\SAforJSScheduling

# Tất cả scripts hoạt động
python scripts/verify_chapter3_features.py
python scripts/test_loader.py
python scripts/test_gui.py
```

---

## 🧪 Verification Results

```
✅ Config paths resolve to project_root:
   - data_dir: D:\Github\SAforJSScheduling\data
   - results_dir: D:\Github\SAforJSScheduling\results
   - bks_file: D:\Github\SAforJSScheduling\data\LA_BKS.csv

✅ DataLoader finds files from any directory:
   - Loaded la01.txt successfully
   - Jobs: 10, Machines: 5

✅ Evaluator loads BKS from any directory:
   - LA01 BKS: 666

✅ Visualizer creates output_dir from any directory:
   - Output: D:\Github\SAforJSScheduling\results

✅ GUI imports work from gui/ directory
✅ main.py runs from project root
```

---

## 📋 Summary

| Issue | Root Cause | Fix Method |
|-------|-----------|-----------|
| Files not found | Relative paths resolve from CWD | Use `Path(__file__).parent.parent` to resolve from source |
| GUI fails from gui/ | DataLoader looks for `data/` relative to CWD | DataLoader now defaults to `project_root/data` |
| Results not saved | Visualizer uses relative `results/` | Visualizer now uses `project_root/results` |
| BKS not loaded | Evaluator uses relative `LA_BKS.csv` | Evaluator now uses `project_root/data/LA_BKS.csv` |
| Config not consistent | SAConfig uses relative paths | SAConfig converts to absolute Path objects |

---

## 🚀 Result

**Trước:** ❌ Chỉ chạy được từ project root  
**Sau:** ✅ Chạy được từ bất kỳ directory nào (root, gui/, scripts/, etc.)

