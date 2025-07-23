import sys
import os
from agents import Agent, handoff, OpenAIChatCompletionsModel
from agents import Runner as AgentRunner

# Add tools and agents folders to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

# Import sub-agents
from my_agents.nutrition_expert_agent import nutrition_expert_agent
from my_agents.injury_support_agent import injury_support_agent
from my_agents.escalation_agent import escalation_agent

# Import tools
from tools.goal_analyzer import goal_analyzer
from tools.tracker import tracker
from tools.workout_recommender import workout_recommender
from tools.meal_planner import meal_planner
from tools.scheduler import scheduler


# Basic Runner wrapper (optional but included if needed)
class Runner:
    @staticmethod
    def run_streamed(agent, input, context=None, hooks=None):
        return AgentRunner.run_streamed(
            agent,
            input=input,
            context=context,
            hooks=hooks
        )


# Health & Wellness Triage Agent Builder
class SeparateAgent:
    def __init__(self, history, query):
        self.history = history
        self.query = query
        self.triage_agent = self.build_agent()

    def build_agent(self):
        conversation = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.history]
        )

        return Agent(
            name="TriageAgent",
            instructions=f"""
You are a helpful health and wellness assistant.

You are allowed to use the full chat history provided below to understand the user's needs, recall facts (like user's name), and maintain context.

{conversation}

Based on the query, decide:
- If it's about diet, meal, or food → hand off to NutritionExpert
- If it's about injury, pain, or recovery → hand off to InjurySupport
- For anything else, either answer directly or hand off to EscalationAgent if needed.

If the user asks something simple (like their name or something from earlier), you can answer directly using the chat history.

Use tools (like goal_analyzer) only when applicable.
""",
            handoffs=[
                handoff(nutrition_expert_agent),
                handoff(injury_support_agent),
                handoff(escalation_agent),
            ],
            tools=[
                goal_analyzer,
                meal_planner,
                scheduler,
                tracker,
                workout_recommender,
            ],
        )

# ✅ Export health_wellness_agent
health_wellness_agent = SeparateAgent
