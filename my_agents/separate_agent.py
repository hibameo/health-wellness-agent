# my_agents/separate_agent.py

from agents import Agent
from escalation_agent import escalation_agent  # ya jis bhi file me tumhara agent hai

class SeparateAgent:
    def __init__(self, history, query):
        self.history = history
        self.query = query

        # Use your fallback escalation agent for now
        self.triage_agent = escalation_agent
