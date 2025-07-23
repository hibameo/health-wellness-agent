from pydantic import BaseModel, Field
from agents import function_tool

# ✅ Step 1: Define your input schema properly
class GoalInput(BaseModel):
    quantity: float = Field(..., gt=0, description="Goal amount (e.g. 5)")
    metric: str = Field(..., description="Measurement unit (e.g. kg or pounds)")

    model_config = {
        "extra": "forbid"  # 🚫 Disallow additional fields to avoid schema errors
    }

# ✅ Step 2: Create the function tool
@function_tool
def goal_analyzer(input: GoalInput) -> str:
    return f"You want to lose {input.quantity} {input.metric}. Great start!"
