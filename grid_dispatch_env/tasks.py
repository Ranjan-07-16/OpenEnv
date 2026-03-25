from models import TaskConfig

TASKS = {
    "easy": TaskConfig(id="easy", solar_multiplier=1.2, load_variance=0.05, carbon_penalty_weight=0.05),
    "medium": TaskConfig(id="medium", solar_multiplier=0.5, load_variance=0.2, carbon_penalty_weight=0.1),
    "hard": TaskConfig(id="hard", solar_multiplier=0.2, load_variance=0.5, carbon_penalty_weight=0.5),
}

def grade_agent(cumulative_reward, steps, difficulty):
    # Normalized grading: Max theoretical reward is ~48 (24 steps * 2.0)
    max_score = 48.0
    score = max(0.0, min(1.0, cumulative_reward / max_score))
    
    # Harder tasks have a lower bar for "passing"
    thresholds = {"easy": 0.8, "medium": 0.6, "hard": 0.4}
    passed = score >= thresholds[difficulty]
    return score, passed