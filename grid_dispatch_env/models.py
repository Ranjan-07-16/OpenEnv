from pydantic import BaseModel, Field

class Observation(BaseModel):
    current_load: float = Field(..., description="Megawatts demanded")
    solar_gen: float = Field(..., description="Megawatts from solar")
    gas_gen: float = Field(..., description="Megawatts from gas")
    grid_stability: float = Field(..., ge=0.0, le=1.0)
    step_count: int

class Action(BaseModel):
    adjust_gas: float = Field(..., ge=-5.0, le=5.0)
    curtail_load: float = Field(..., ge=0.0, le=2.0)

class TaskConfig(BaseModel):
    id: str
    solar_multiplier: float
    load_variance: float
    carbon_penalty_weight: float