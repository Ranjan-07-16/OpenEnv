# OpenEnv

<div align="center">
  <h1>⚡ GridDispatch-v1</h1>
  <p><b>A Real-World Power Grid OpenEnv Simulation</b></p>
  
  <img src="https://img.shields.io/badge/OpenEnv-v1.0.0-blueviolet" alt="OpenEnv Version">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-Submission--Ready-success" alt="Status">
</div>

---

## 📖 Overview
**GridDispatch-v1** is a high-fidelity environment designed for AI agents to master energy management. Unlike toy environments, this simulates a regional microgrid where an agent balances volatile **Solar Energy** and carbon-heavy **Gas Turbines** to meet urban demand without causing a blackout.

### 🏗️ Project Architecture
The environment follows the strict **OpenEnv** specification:
- **Typed Models:** Pydantic-validated `Observation` and `Action` objects.
- **API:** Standard `step()`, `reset()`, and `state()` loop.
- **Manifest:** Machine-readable `openenv.yaml` for agent discovery.

---

## 🛠️ Environment Specification

### 📡 Observation Space (The State)
| Feature | Type | Description |
| :--- | :--- | :--- |
| `current_load` | `float32` | Total Megawatts (MW) demanded by the city. |
| `solar_gen` | `float32` | MW currently produced by renewable solar arrays. |
| `gas_gen` | `float32` | MW produced by controllable gas turbines. |
| `grid_stability` | `float32` | Health metric (1.0 = Perfect, <0.2 = Blackout). |
| `step_count` | `int32` | Current hour in the 24-hour cycle. |

### 🕹️ Action Space
| Action | Range | Description |
| :--- | :--- | :--- |
| `adjust_gas` | `[-5.0, 5.0]` | Increase or decrease gas output. |
| `curtail_load` | `[0.0, 2.0]` | Strategic demand reduction to save the grid. |

---

## 📊 Task Scenarios & Grading
The environment includes three built-in tasks evaluated by automated graders (Scores: 0.0 – 1.0).

| Task ID | Difficulty | Target | Description |
| :--- | :--- | :--- | :--- |
| `sunny_day_baseline` | <kbd>Easy</kbd> | **0.9** | High solar; maintain stability with minimal gas. |
| `stormy_night_fluctuation` | <kbd>Medium</kbd> | **0.8** | Zero solar + high volatility; tests precision. |
| `carbon_tax_crunch` | <kbd>Hard</kbd> | **0.7** | High carbon penalties; requires load curtailment. |

---

## 🚀 Execution & Deployment

### 1. Installation
```bash
git clone [https://github.com/YOUR_USERNAME/grid_dispatch_env.git](https://github.com/YOUR_USERNAME/grid_dispatch_env.git)
cd grid_dispatch_env
pip install -r requirements.txt