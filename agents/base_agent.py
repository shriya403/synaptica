"""
Synaptica Base Agent
Fast prototype mode.
"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from langchain_ollama import ChatOllama


@dataclass
class AgentState:
    task: str
    context: Dict[str, Any] = field(default_factory=dict)
    memory: List[Dict[str, Any]] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    performance_score: float = 0.0
    feedback: Optional[str] = None
    self_improvement_log: List[Dict[str, Any]] = field(default_factory=list)


class BaseAgent(ABC):
    def __init__(
        self,
        name: str,
        role: str,
        llm_model: str = "llama3.2",
        temperature: float = 0.7,
    ):
        self.name = name
        self.role = role
        self.llm = ChatOllama(model=llm_model, temperature=temperature)
        self.state = AgentState(task="")
        self.tools: Dict[str, Any] = {}
        self.memory_store: List[Dict[str, Any]] = []

    def set_tools(self, tools: Dict[str, Any]) -> None:
        self.tools = tools

    async def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        context = context or {}

        self.state.task = task
        self.state.context = context

        # Fast prototype mode: skip slow planning and critique LLM calls
        plan = {
            "steps": [task],
            "raw_plan": task,
        }

        result = await self._execute(plan, context)

        critique = {
            "score": 8.0,
            "needs_improvement": False,
            "suggestions": [],
            "raw_critique": "Skipped for fast prototype mode.",
        }

        self._log_learning(task, result, critique)

        return {
            "agent": self.name,
            "role": self.role,
            "task": task,
            "plan": plan,
            "result": result,
            "critique": critique,
            "performance_score": self.state.performance_score,
        }

    @abstractmethod
    async def _execute(
        self,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Any:
        pass

    def _log_learning(
        self,
        task: str,
        result: Any,
        critique: Dict[str, Any],
    ) -> None:
        self.state.self_improvement_log.append(
            {
                "task": task,
                "result": str(result),
                "critique_score": critique["score"],
                "timestamp": asyncio.get_event_loop().time(),
            }
        )

        self.state.performance_score = (
            self.state.performance_score * 0.7 + critique["score"] * 0.3
        )

    def __repr__(self) -> str:
        return (
            f"BaseAgent(name='{self.name}', "
            f"role='{self.role}', "
            f"score={self.state.performance_score:.2f})"
        )