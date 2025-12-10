from __future__ import annotations

from dataclasses import dataclass

from langchain_deepseek.chat_models import ChatDeepSeek
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from src.config.settings import settings
from src.graph.state import ConversationState, ExplanationAgentAnswer
from src.tools.knowledge_tool import lookup
from src.utils.prompts import EXPLANATION_PROMPT


@dataclass
class ExplanationAgent:
    def __init__(self) -> None:
        self.llm_config = {
            "api_base": settings.BASE_URL,
            "base_url": settings.BASE_URL,
            "api_key": settings.API_KEY,
            "model": settings.MODEL_NAME,
            "streaming": False,
            "extra_body": {"reasoning": {"enabled": False}},
        }

    def _create_chain(self, temperature: float):
        llm = ChatDeepSeek(
            **self.llm_config,
            temperature=temperature,
        )
        agent = create_agent(
            model=llm,
            tools=[lookup],
            response_format=ToolStrategy(ExplanationAgentAnswer),
        )
        return EXPLANATION_PROMPT | agent

    def run(self, state: ConversationState) -> ConversationState:
        question = state.get("question", "")

        for attempt in range(settings.MAX_RETRIES + 1):
            temperature = settings.BASE_TEMPERATURE if attempt < 1 else settings.MAX_TEMPERATURE

            chain = self._create_chain(temperature)
            try:
                response = chain.invoke({"question": question})
                answer_text = response['structured_response']["answer_text"]

                history = list(state.get("history", [])) + [question]

                return {**state, "answer": answer_text, "history": history}
            except Exception:
                continue
        raise RuntimeError("ExplanationAgent failed after retries")
