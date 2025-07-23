from typing import TypedDict
from pydantic import BaseModel, Field
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

# Input model
class TrackerInput(BaseModel):
    notes: str = Field(
        default="",
        description="Optional user notes related to wellness tracking.",
        examples=["Felt tired", "Skipped lunch", "Went for a walk"]
    )

# Output model
class TrackerOutput(TypedDict):
    message: str

# Function tool
@function_tool
async def tracker(
    ctx: RunContextWrapper[UserSessionContext],
    input: TrackerInput
) -> TrackerOutput:
    ctx.context.tracking_notes = input.notes
    return {"message": f"Note recorded: {input.notes}"}
