import asyncio
from agents.orchestrator import Orchestrator

async def main():
    orchestrator = Orchestrator()
    result = await orchestrator.execute_task("Launch Synaptica AI Platform")
    print(result["synthesized"]["final_plan"])

asyncio.run(main())