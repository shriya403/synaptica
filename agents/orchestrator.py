"""
Synaptica Orchestrator
Coordinates all specialist agents.
"""

import asyncio
from typing import Any, Dict, List

from .specialist_agents import create_agent_team


class Orchestrator:
    def __init__(self):
        self.agents = create_agent_team()

    async def execute_task(self, user_request: str) -> Dict[str, Any]:
        subtasks = await self._decompose_task(user_request)
        assignments = await self._assign_agents(subtasks)
        results = await self._execute_parallel(assignments)
        synthesized = await self._synthesize(results)
        critique = await self._orchestrator_critique(synthesized)

        return {
            "user_request": user_request,
            "subtasks": subtasks,
            "results": results,
            "synthesized": synthesized,
            "critique": critique,
        }

    async def _decompose_task(self, task: str) -> List[Dict[str, Any]]:
        return [
            {"id": 1, "task": "Research market opportunities", "agent": "market_researcher"},
            {"id": 2, "task": "Create marketing content", "agent": "content_creator"},
            {"id": 3, "task": "Build execution timeline", "agent": "timeline_planner"},
            {"id": 4, "task": "Analyze project risks", "agent": "risk_analyst"},
            {"id": 5, "task": "Optimize budget allocation", "agent": "budget_optimizer"},
        ]

    async def _assign_agents(self, subtasks: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        assignments = {}

        for subtask in subtasks:
            agent_name = subtask["agent"]

            if agent_name not in assignments:
                assignments[agent_name] = []

            assignments[agent_name].append(subtask)

        return assignments

    async def _execute_parallel(self, assignments: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        tasks = []
        agent_names = []

        for agent_name, subtasks in assignments.items():
            agent = self.agents[agent_name]
            prompt = " + ".join([subtask["task"] for subtask in subtasks])

            tasks.append(agent.execute(prompt, {}))
            agent_names.append(agent_name)

        outputs = await asyncio.gather(*tasks)

        return {name: output for name, output in zip(agent_names, outputs)}

    async def _synthesize(self, results: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "market_insights": results["market_researcher"]["result"],
            "content": results["content_creator"]["result"],
            "timeline": results["timeline_planner"]["result"],
            "risks": results["risk_analyst"]["result"],
            "budget": results["budget_optimizer"]["result"],
            "final_plan": self._create_final_plan(results),
        }

    def _create_final_plan(self, results: Dict[str, Any]) -> str:
        return f"""
==============================
SYNAPTICA EXECUTION REPORT
==============================

MARKET INSIGHTS
--------------
{results["market_researcher"]["result"]}

CONTENT STRATEGY
----------------
{results["content_creator"]["result"]}

PROJECT TIMELINE
----------------
{results["timeline_planner"]["result"]}

RISK ANALYSIS
-------------
{results["risk_analyst"]["result"]}

BUDGET PLAN
-----------
{results["budget_optimizer"]["result"]}

==============================
END REPORT
==============================
"""

    async def _orchestrator_critique(self, synthesized: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "overall_score": 8.5,
            "strengths": ["Comprehensive planning", "Parallel execution", "Multi-agent collaboration"],
            "improvements": ["Add KPI tracking", "Integrate real APIs", "Add memory persistence"],
        }