from env import GridDispatchEnv
from tasks import TASKS, grade_agent
from models import Action

def run_baseline():
    env = GridDispatchEnv()
    for diff, config in TASKS.items():
        state = env.reset(config)
        total_reward = 0
        done = False
        
        print(f"\n--- Starting Task: {diff} ---")
        
        while not done:
            # 1. Calculate the current power gap
            supply = state.solar_gen + state.gas_gen
            diff_mw = state.current_load - supply
            
            # 2. P-Control: React 20% more aggressively to close gaps faster
            # This prevents the initial Stability drop we saw in your logs
            adj = max(-5.0, min(5.0, diff_mw * 1.2))
            
            # 3. Emergency Logic: If stability is failing, shed 1.5MW of load
            # This is a "Smart" move for the Medium/Hard tasks
            curtail = 0.0
            if state.grid_stability < 0.85:
                curtail = 1.5
            
            action = Action(adjust_gas=adj, curtail_load=curtail)
            
            # 4. Execute step
            state, reward, done, _ = env.step(action)
            total_reward += reward

            # Clean logging
            print(f"Step: {state.step_count:02d} | Load: {state.current_load:.2f} | Stability: {state.grid_stability:.2f} | Reward: {reward:.2f}")
            
        # 5. Final Grade
        score, passed = grade_agent(total_reward, state.step_count, diff)
        print(f">>> FINAL RESULT - Task: {diff} | Score: {score:.2f} | Passed: {passed}")

if __name__ == "__main__":
    run_baseline()