from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv()
#gemini_api_key = os.getenv("GEMINI_API_KEY")


# OpenAI setup
# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider
# )

# config = RunConfig(
#     model=model,
#     model_provider=provider,
#     tracing_disabled=True,
# )

assistant = Agent(
    name= "Assistant",
    instructions= "You are a helpful assistant that can answer questions and help with tasks.",
    
)

result = Runner.run_sync(
    assistant,
    "Who is salman khan",
    
)

print(result)