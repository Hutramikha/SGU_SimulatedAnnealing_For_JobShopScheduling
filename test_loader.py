#!/usr/bin/env python
"""Quick test for data loader"""

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
