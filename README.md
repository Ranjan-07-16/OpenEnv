# OpenEnv

<div align="center">
  <h1>⚡ GridDispatch-v1</h1>
  <p><b>A Real-World Power Grid OpenEnv Simulation</b></p>
  
  <img src="https://img.shields.io/badge/OpenEnv-v1.0.0-blueviolet" alt="OpenEnv Version">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-Submission--Ready-success" alt="Status">
</div>

---

## 🌍 Motivation & Real-World Utility
Modern power grids are undergoing a radical shift from predictable fossil fuels to volatile renewable sources. As we integrate more solar and wind, the complexity of balancing a grid—where supply must perfectly match demand at every second to avoid catastrophic failure—becomes too fast and multi-faceted for traditional human-operated systems.

**GridDispatch-v1** serves as a critical evaluation environment for AI agents designed to:
* **Manage High-Frequency Volatility:** Automate the balancing of intermittent solar peaks with "spinning reserves" (gas turbines).
* **Navigate Policy-Driven Constraints:** Evaluate how agents respond to economic pressures like carbon taxes and load-shedding mandates.
* **Prevent Infrastructure Failure:** Test the resilience of autonomous systems against "blackout" conditions in a safe, simulated sandbox.

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

> ### 📊 Note on Baseline Scores
> The provided baseline heuristic achieves a score of **~0.37** on the Easy task and **0.00** on Medium/Hard. This is **by design**:
> * **Economic Complexity:** In Medium and Hard scenarios, the reward function incorporates heavy carbon taxes and variable operating costs.
> * **The Optimization Challenge:** A simple proportional-control heuristic (like the one in `baseline.py`) cannot solve the non-linear optimization required to perfectly balance grid stability against high environmental penalties.
> * **Evaluation Intent:** These tasks are specifically designed to move beyond basic logic and require agents (LLMs or RL) to develop sophisticated, multi-objective strategies.

---

## 🚀 Execution & Deployment

### 1. Installation
```bash
git clone [https://github.com/YOUR_USERNAME/grid_dispatch_env.git](https://github.com/YOUR_USERNAME/grid_dispatch_env.git)
cd grid_dispatch_env
pip install -r requirements.txt
```

### 2. Run Baseline Inference
Use the baseline script to verify the environment logic and generate reproducible scores:

```bash
python baseline.py
```

### 3. Deploy with Docker
This environment is fully containerized. Use the following commands to build and run locally:

```bash
# Build the image
docker build -t grid_dispatch_env .

# Run locally on port 7860
docker run -p 7860:7860 grid_dispatch_env
```

<div align="center">
<sub>Built for the Polaris School of Technology OpenEnv Challenge | 2026</sub>
</div>