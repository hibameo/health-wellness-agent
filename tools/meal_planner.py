from agents import function_tool, RunContextWrapper
from pydantic import BaseModel, Field
from typing import List, TypedDict
from context import UserSessionContext




class MealPlanInput(BaseModel):
    ...

class DailyMeals(TypedDict):
    ...

class MealPlanOutput(TypedDict):
    ...

@function_tool
async def meal_planner(
    ctx: RunContextWrapper[UserSessionContext],
    input: MealPlanInput,
) -> MealPlanOutput:
    ...
