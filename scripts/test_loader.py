#!/usr/bin/env python
"""Quick test for data loader"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader import DataLoader

try:
    loader = DataLoader()
    data = loader.load_instance('la01.txt')
    print(f'[OK] File loaded successfully!')
    print(f'  - Jobs: {data["n_jobs"]}')
    print(f'  - Machines: {data["n_machines"]}')
    print(f'  - Processing times shape: {data["processing_times"].shape}')
    print(f'  - Machine order shape: {data["machine_order"].shape}')
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()
