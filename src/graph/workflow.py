from langgraph.graph import START, END, StateGraph

from src.agents.explanation_agent import ExplanationAgent
from src.agents.problem_solving_agent import ProblemSolvingAgent
from src.agents.router_agent import RouterAgent
from src.graph.state import ConversationState

def build_workflow() -> StateGraph:
    """Create a LangGraph workflow connecting router and specialized agents."""

    router = RouterAgent()
    explainer = ExplanationAgent()
    solver = ProblemSolvingAgent()

    graph = StateGraph(ConversationState)
    graph.add_node("router", router.run)
    graph.add_node("explanation", explainer.run)
    graph.add_node("problem_solving", solver.run)

    graph.add_edge(START, "router")
    graph.add_edge("explanation", END)
    graph.add_edge("problem_solving", END)

    graph.add_conditional_edges(
        "router",
        lambda state: state.get("intent", "unknown"),
        {
            "explanation": "explanation",
            "problem_solving": "problem_solving",
            "unknown": END,
        },
    )
    return graph