from __future__ import annotations

from langchain_deepseek.chat_models import ChatDeepSeek
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from src.config.settings import settings
from src.graph.state import ConversationState, RouterAnswer
from src.utils.prompts import ROUTER_PROMPT

class RouterAgent:
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
            tools=[],
            response_format=ToolStrategy(RouterAnswer),
        )
        return ROUTER_PROMPT | agent
    
    def run(self, state: ConversationState) -> ConversationState:
        question = state.get("question", "")

        for attempt in range(settings.MAX_RETRIES + 1):
            temperature = settings.BASE_TEMPERATURE if attempt < 1 else settings.MAX_TEMPERATURE

            chain = self._create_chain(temperature)

            try:
                response = chain.invoke({"question": question})

                updated = ConversationState(
                    intent=response['structured_response']["intent"],
                    subject=response['structured_response']["subject"],
                    level=state.get("level"),
                    history=state.get("history", []),
                    question=question,
                )
                return {**state, **updated}
            except Exception:
                continue
        raise RuntimeError("Router failed after retries")
