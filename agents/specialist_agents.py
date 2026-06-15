from typing import Dict, Any
from agents.base_agent import BaseAgent


class MarketResearcher(BaseAgent):

    def __init__(self):
        super().__init__(
            name="MarketResearcher",
            role="Market Research Analyst",
            temperature=0.5
        )

    async def _execute(self, plan, context) -> Dict[str, Any]:
        return {
            "market_size": "$2.3B by 2028",
            "competitors": ["Company A", "Company B", "Company C"],
            "trends": ["AI-powered", "Mobile-first", "Privacy-focused"],
            "user_pain_points": [
                "Complexity",
                "Price",
                "Limited features"
            ]
        }


class ContentCreator(BaseAgent):

    def __init__(self):
        super().__init__(
            name="ContentCreator",
            role="Content Creator",
            temperature=0.8
        )

    async def _execute(self, plan, context) -> Dict[str, Any]:
        return {
            "taglines": [
                "Revolutionize your workflow",
                "AI-powered simplicity"
            ],
            "social_posts": [
                "🚀 Exciting news coming soon!"
            ]
        }


class TimelinePlanner(BaseAgent):

    def __init__(self):
        super().__init__(
            name="TimelinePlanner",
            role="Project Manager",
            temperature=0.3
        )

    async def _execute(self, plan, context) -> Dict[str, Any]:
        return {
            "phases": [
                {
                    "name": "Research",
                    "duration": "2 weeks"
                },
                {
                    "name": "Development",
                    "duration": "6 weeks"
                },
                {
                    "name": "Launch",
                    "duration": "2 weeks"
                }
            ]
        }


class RiskAnalyst(BaseAgent):

    def __init__(self):
        super().__init__(
            name="RiskAnalyst",
            role="Risk Analyst",
            temperature=0.4
        )

    async def _execute(self, plan, context) -> Dict[str, Any]:
        return {
            "risks": [
                {
                    "risk": "Competition",
                    "probability": "High"
                },
                {
                    "risk": "Technical Debt",
                    "probability": "Medium"
                }
            ]
        }


class BudgetOptimizer(BaseAgent):

    def __init__(self):
        super().__init__(
            name="BudgetOptimizer",
            role="Financial Analyst",
            temperature=0.3
        )

    async def _execute(self, plan, context) -> Dict[str, Any]:
        return {
            "budget": "$50,000",
            "roi": "3.5x"
        }


def create_agent_team():
    return {
        "market_researcher": MarketResearcher(),
        "content_creator": ContentCreator(),
        "timeline_planner": TimelinePlanner(),
        "risk_analyst": RiskAnalyst(),
        "budget_optimizer": BudgetOptimizer(),
    }