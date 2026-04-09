# Job Shop Scheduling Problem Solver using Simulated Annealing

A comprehensive implementation of the **Simulated Annealing (SA)** algorithm for solving the **Job Shop Scheduling Problem (JSSP)** with adaptive mechanisms and benchmark evaluation.

## Overview

This project implements a production-ready SA solver for JSSP with the following features:

- **Adaptive Cooling Schedule**: Dynamically adjusts cooling rate based on solution improvement
- **Metropolis Acceptance Criterion**: Probabilistic acceptance of worse solutions for escape local optima
- **Early Stopping with Reheating**: Prevents premature convergence
- **Operation-based Encoding**: Ensures feasible solutions without repair mechanisms
- **Comprehensive Visualization**: Gantt charts and convergence analysis
- **Standard Benchmarks**: All 40 Lawrence (LA01-LA40) instances from OR-Library

## Problem Definition

**Job Shop Scheduling Problem (JSSP):**
- Schedule **n** jobs across **m** machines
- Each job consists of **m** operations in fixed machine order
- Each operation has fixed processing time
- Constraints:
  - Each operation on each job must execute in order
  - Each machine can process at most one job at a time
- Objective: Minimize **makespan** (C_max) = maximum completion time across all jobs

**Mathematical Formulation:**
```
Minimize: C_max = max{C_j,m | j ∈ [1,n], m ∈ [1,m]}

Subject to:
- C_{i,j} ≥ C_{i-1,j} + p_{i,j}  (precedence constraints)
- C_{i,j} ≥ C_{i,k} + p_{i,k}  (machine conflict avoidance)
```

## Project Structure

```
SAforJSScheduling/
├── config/
│   ├── __init__.py
│   └── config.py           # Configuration management (15+ parameters)
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # OR-Library format parsing
│   ├── jssp_model.py       # JSSP model with Operation-based encoding
│   ├── sa_solver.py        # Main SA algorithm implementation
│   ├── evaluator.py        # Solution evaluation & BKS comparison
│   ├── utils.py            # Helper classes (operators, cooling, acceptance)
│   └── visualizer.py       # Gantt charts and convergence plots
├── data/                   # OR-Library LA01-LA40 instances (40 files)
├── results/                # Output Gantt charts and convergence plots
├── main.py                 # Entry point for single/batch solving
├── LA_BKS.csv             # Best Known Solutions reference
├── requirement.txt         # Python dependencies
└── README.md              # This file
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/SAforJSScheduling.git
cd SAforJSScheduling
```

### 2. Install dependencies
```bash
pip install -r requirement.txt
```

Or manually:
```bash
pip install numpy>=1.21.0 matplotlib>=3.3.0
```

### 3. (Optional) Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

## Usage

### Quick Start: Solve a Single Instance

```bash
python main.py
```

This executes `solve_single_instance("la01")` with default configuration.

**Output:**
- Console: Algorithm progress, final results, execution time
- `/results/gantt_la01.png`: Gantt chart visualization
- `/results/convergence_la01.png`: Temperature and makespan convergence curves
- `/results/la01_result.txt`: Detailed results summary

### Advanced: Batch Processing

Edit `main.py` to run multiple instances:

```python
if __name__ == "__main__":
    # Solve LA01-LA10
    solve_multiple_instances(["la01", "la02", "la03", "la04", "la05", 
                             "la06", "la07", "la08", "la09", "la10"])
```

**Output:**
- 10 Gantt charts in `/results/`
- 10 convergence plots in `/results/`
- `/results/convergence_comparison.png`: Superimposed convergence curves
- `/results/comparison_bar.png`: SA results vs BKS reference

### Programmatic Usage

```python
from config.config import SAConfig
from src.data_loader import DataLoader
from src.jssp_model import JSSPModel
from src.sa_solver import SASolver
from src.evaluator import Evaluator
from src.visualizer import Visualizer

# 1. Configure
config = SAConfig()
config.T0 = 1200.0          # Initial temperature
config.alpha_explore = 0.98 # Slow cooling (exploration)
config.alpha_exploit = 0.95 # Fast cooling (exploitation)

# 2. Load data
loader = DataLoader(config.data_dir)
data = loader.load_instance("la01.txt")

# 3. Create model
model = JSSPModel(data['n_jobs'], data['n_machines'], 
                 data['processing_times'], data['machine_order'])

# 4. Solve
solver = SASolver(model, config)
best_solution, best_makespan, history = solver.solve()

# 5. Evaluate
evaluator = Evaluator(config.bks_file)
evaluation = evaluator.evaluate_solution(best_makespan, "la01")
print(f"Makespan: {best_makespan}, Gap: {evaluation['gap_percent']:.2f}%")

# 6. Visualize
visualizer = Visualizer(config.results_dir)
schedule = solver.get_schedule()
visualizer.plot_gantt_chart(schedule, model, "la01")
visualizer.plot_convergence(history, "la01", evaluator.get_bks("la01"))
```

## Configuration Parameters

Edit `config/config.py` to adjust algorithm behavior. Key parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `T0` | 1000.0 | Initial temperature |
| `T_min` | 0.01 | Stopping temperature threshold |
| `alpha_explore` | 0.98 | Cooling rate in exploration phase |
| `alpha_exploit` | 0.95 | Cooling rate in exploitation phase |
| `L` | 100 | Markov chain length (iterations per temperature) |
| `patience` | 500 | No-improvement iterations before early stop |

## Algorithm Details

### Solution Representation

Operation-based encoding: list of n×m job indices where each job appears m times
- Example: `[1, 3, 1, 2, 3, 1, 2, 3, 2]` for 3 jobs, 3 machines
- Guarantees feasible solutions naturally

### Simulated Annealing Process

1. **Initialization**: Generate random feasible solution
2. **Markov Chain**: Repeat L times:
   - Generate neighbor (50% Swap, 50% Move)
   - Accept if better, or with probability exp(-Δ/T) if worse
3. **Cooling**: Update T_new = α × T_old with adaptive α
4. **Termination**: Stop when T < T_min or no improvement for 500 iterations

### Neighborhood Operators

- **Swap**: Exchange two random positions
- **Move**: Remove element, insert at random position
- **Probabilistic Selection**: 50/50 by default

## Evaluation Metrics

### Best Known Solutions (BKS)
- Lawrence (1984) benchmark: 40 standard instances
- LA01-LA40 with known optimal or best-known makespan values

### Quality Assessment
```
Gap(%) = (Algorithm_Result - BKS) / BKS × 100
```

**Quality Grades:**
- **Optimal ✓**: Gap = 0% 
- **Excellent**: Gap < 5%
- **Good**: 5% ≤ Gap < 10%
- **Fair**: 10% ≤ Gap < 15%
- **Poor**: Gap ≥ 15%

## References

1. Lawrence, S. (1984). Resource constrained project scheduling: An experimental investigation of heuristic scheduling techniques. Carnegie-Mellon University.

2. Kirkpatrick, S., Gelatt Jr, C. D., & Vecchi, M. P. (1983). Optimization by simulated annealing. *Science*, 220(4598), 671-680.

3. Metropolis, N., et al. (1953). Equation of state calculations by fast computing machines. *The Journal of Chemical Physics*, 21(6), 1087-1092.

## License

MIT License

## Status

✅ **Production Ready** - All components implemented and tested with OR-Library benchmarks

