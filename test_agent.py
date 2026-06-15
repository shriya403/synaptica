import asyncio
from agents.specialist_agents import MarketResearcher

async def main():
    agent = MarketResearcher()
    result = await agent.execute("Analyze AI study planner market")
    print(result)

asyncio.run(main())