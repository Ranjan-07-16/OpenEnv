import numpy as np
from models import Observation, Action, TaskConfig

class GridDispatchEnv:
    def __init__(self):
        self.max_steps = 24
        self.current_task = None
        self.reset()

    def reset(self, task: TaskConfig = None):
        self.current_task = task or TaskConfig(
            id="default", solar_multiplier=1.0, load_variance=0.1, carbon_penalty_weight=0.1
        )
        self._state = Observation(
            current_load=20.0,
            solar_gen=0.0,
            gas_gen=10.0,
            grid_stability=1.0,
            step_count=0
        )
        return self._state

    def state(self) -> Observation:
        return self._state

    def step(self, action: Action):
        # 1. Update Energy Levels
        self._state.gas_gen = max(0.0, min(50.0, self._state.gas_gen + action.adjust_gas))
        
        # Solar Cycle (Sine wave) modified by task difficulty
        solar_base = 15.0 * np.sin(np.pi * self._state.step_count / 12.0)
        self._state.solar_gen = max(0.0, solar_base * self.current_task.solar_multiplier)
        
        # Load Cycle (Busy at day, low at night)
        load_base = 25.0 + 5.0 * np.sin(np.pi * (self._state.step_count - 6) / 12.0)
        noise = np.random.normal(0, self.current_task.load_variance)
        self._state.current_load = max(10.0, load_base + noise)

        # 2. Physics & Stability
        total_supply = self._state.solar_gen + self._state.gas_gen
        effective_demand = self._state.current_load - action.curtail_load
        imbalance = abs(total_supply - effective_demand)
        
        # Stability decays faster with higher imbalance
        stability_loss = (imbalance / 10.0) ** 2
        self._state.grid_stability = max(0.0, 1.0 - stability_loss)

        # 3. Reward Function (Partial Progress)
        # Components: Stability (primary), Carbon (secondary), Curtailment (penalty)
        reward = (self._state.grid_stability * 2.0) \
                 - (self._state.gas_gen * self.current_task.carbon_penalty_weight) \
                 - (action.curtail_load * 0.5)
        
        self._state.step_count += 1
        done = self._state.step_count >= self.max_steps or self._state.grid_stability < 0.2
        
        return self._state, float(reward), done, {}