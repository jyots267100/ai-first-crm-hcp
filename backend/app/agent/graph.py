import json
import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from app.tools.interaction_tools import ALL_TOOLS


load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    current_interaction: dict
    tool_used: str | None
    form_updates: dict


SYSTEM_PROMPT = """
You are an AI assistant inside an AI-first life-sciences CRM for pharmaceutical
field representatives.

The form on the left side of the application cannot be edited manually.
You control the form entirely through tools based on the user's natural-language
messages.

You have exactly five tools:

1. log_interaction:
Use when the user describes a new HCP interaction.

2. edit_interaction:
Use when the user corrects or modifies an existing interaction.
Update only fields explicitly requested by the user.

3. add_sample:
Use when the user says pharmaceutical samples were distributed.

4. create_follow_up:
Use when the user requests a follow-up action.

5. analyze_interaction:
Use when the user asks to analyze, summarize, or identify the key outcome of
the current interaction.

Important rules:

- You MUST use an appropriate tool for requests that modify the CRM form.
- Never invent information that the user did not provide.
- Resolve relative dates such as "today" from the current date given below.
- Preserve existing values when editing unless explicitly changed.
- Sentiment must be Positive, Neutral, or Negative.
- Use the current interaction state as context.
"""


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

llm_with_tools = llm.bind_tools(ALL_TOOLS)

tools_by_name = {
    tool.name: tool
    for tool in ALL_TOOLS
}


def agent_node(state: AgentState):
    from datetime import date

    current_date = date.today().isoformat()

    context = (
        f"\nCurrent date: {current_date}\n"
        f"Current interaction state:\n"
        f"{json.dumps(state.get('current_interaction', {}), indent=2)}"
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT + context),
        *state["messages"]
    ]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


def tool_node(state: AgentState):
    last_message = state["messages"][-1]

    current_interaction = dict(
        state.get("current_interaction", {})
    )

    all_updates = {}
    used_tools = []
    tool_messages = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        selected_tool = tools_by_name[tool_name]
        result = selected_tool.invoke(tool_args)

        parsed = json.loads(result)
        updates = parsed.get("updates", {})

        for key, value in updates.items():
            if key == "samples_distributed":
                existing = current_interaction.get(
                    "samples_distributed",
                    []
                )
                current_interaction[key] = existing + value
            else:
                current_interaction[key] = value

        all_updates.update(updates)
        used_tools.append(tool_name)

        tool_messages.append(
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        )

    return {
        "messages": tool_messages,
        "current_interaction": current_interaction,
        "form_updates": all_updates,
        "tool_used": ", ".join(used_tools)
    }


def should_continue(state: AgentState):
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END


def final_response_node(state: AgentState):
    current_interaction = state.get(
        "current_interaction",
        {}
    )

    prompt = f"""
The requested CRM operation has been completed successfully.

Tool used:
{state.get("tool_used")}

Current interaction:
{json.dumps(current_interaction, indent=2)}

Give the user a brief, friendly confirmation in 1-3 sentences.
Do not mention internal implementation details.
"""

    response = llm.invoke(prompt)

    return {
        "messages": [response]
    }


graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "agent",
    agent_node
)

graph_builder.add_node(
    "tools",
    tool_node
)

graph_builder.add_node(
    "final_response",
    final_response_node
)

graph_builder.add_edge(
    START,
    "agent"
)

graph_builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

graph_builder.add_edge(
    "tools",
    "final_response"
)

graph_builder.add_edge(
    "final_response",
    END
)

crm_graph = graph_builder.compile()