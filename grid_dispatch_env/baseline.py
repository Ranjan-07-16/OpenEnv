from env import GridDispatchEnv
from tasks import TASKS, grade_agent
from models import Action

def run_baseline():
    env = GridDispatchEnv()
    for diff, config in TASKS.items():
        state = env.reset(config)
        total_reward = 0
        done = False
        
        while not done:
            # Simple Heuristic: If load > supply, increase gas
            supply = state.solar_gen + state.gas_gen
            diff_mw = state.current_load - supply
            
            # Action clipping to match constraints
            adj = max(-5.0, min(5.0, diff_mw))
            action = Action(adjust_gas=adj, curtail_load=0.0)
            
            state, reward, done, _ = env.step(action)
            total_reward += reward
            
        score, passed = grade_agent(total_reward, state.step_count, diff)
        print(f"Task: {diff} | Score: {score:.2f} | Passed: {passed}")

if __name__ == "__main__":
    run_baseline()