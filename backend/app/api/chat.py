import json

from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage
from sqlalchemy.orm import Session

from app.agent.graph import crm_graph
from app.database import get_db
from app.db_models import Interaction
from app.schemas import ChatRequest


router = APIRouter(
    prefix="/api",
    tags=["AI Assistant"]
)


def interaction_to_dict(interaction: Interaction) -> dict:
    """Convert a database interaction object into frontend-friendly JSON."""

    def parse_json_list(value):
        if not value:
            return []

        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []

    return {
        "id": interaction.id,
        "hcp_name": interaction.hcp_name,
        "interaction_type": interaction.interaction_type,
        "interaction_date": interaction.interaction_date,
        "interaction_time": interaction.interaction_time,
        "attendees": interaction.attendees,
        "topics_discussed": interaction.topics_discussed,
        "materials_shared": parse_json_list(
            interaction.materials_shared
        ),
        "samples_distributed": parse_json_list(
            interaction.samples_distributed
        ),
        "sentiment": interaction.sentiment,
        "outcomes": interaction.outcomes,
        "follow_up_actions": interaction.follow_up_actions,
    }


@router.post("/chat")
def chat_with_agent(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Send a natural-language message to the LangGraph CRM agent.

    The LLM dynamically selects one or more of the five available tools.
    The resulting structured state is persisted and returned to the frontend.
    """

    try:
        # ---------------------------------------------------------
        # 1. Get existing interaction if an ID was provided.
        # ---------------------------------------------------------
        interaction = None
        current_interaction = {}

        if request.interaction_id is not None:
            interaction = db.query(Interaction).filter(
                Interaction.id == request.interaction_id
            ).first()

            if interaction:
                current_interaction = interaction_to_dict(interaction)

        # ---------------------------------------------------------
        # 2. Send user message and current form state to LangGraph.
        # ---------------------------------------------------------
        initial_state = {
            "messages": [
                HumanMessage(content=request.message)
            ],
            "current_interaction": current_interaction,
            "tool_used": None,
            "form_updates": {},
        }

        result = crm_graph.invoke(initial_state)

        updated_data = result.get(
            "current_interaction",
            current_interaction
        )

        tool_used = result.get("tool_used")

        # ---------------------------------------------------------
        # 3. Save the updated interaction to the database.
        # ---------------------------------------------------------
        if updated_data:
            if interaction is None:
                interaction = Interaction()
                db.add(interaction)

            interaction.hcp_name = updated_data.get("hcp_name")
            interaction.interaction_type = updated_data.get(
                "interaction_type",
                "Meeting"
            )
            interaction.interaction_date = updated_data.get(
                "interaction_date"
            )
            interaction.interaction_time = updated_data.get(
                "interaction_time"
            )
            interaction.attendees = updated_data.get("attendees")
            interaction.topics_discussed = updated_data.get(
                "topics_discussed"
            )

            interaction.materials_shared = json.dumps(
                updated_data.get("materials_shared", [])
            )

            interaction.samples_distributed = json.dumps(
                updated_data.get("samples_distributed", [])
            )

            interaction.sentiment = updated_data.get("sentiment")
            interaction.outcomes = updated_data.get("outcomes")
            interaction.follow_up_actions = updated_data.get(
                "follow_up_actions"
            )

            db.commit()
            db.refresh(interaction)

        # ---------------------------------------------------------
        # 4. Get the final AI message.
        # ---------------------------------------------------------
        ai_message = "Request completed successfully."

        messages = result.get("messages", [])

        if messages:
            last_message = messages[-1]

            if getattr(last_message, "content", None):
                ai_message = last_message.content

        # ---------------------------------------------------------
        # 5. Return everything needed by React + Redux.
        # ---------------------------------------------------------
        return {
            "success": True,
            "message": ai_message,
            "tool_used": tool_used,
            "form_updates": result.get("form_updates", {}),
            "interaction": (
                interaction_to_dict(interaction)
                if interaction
                else updated_data
            ),
        }

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"AI agent error: {str(exc)}"
        )