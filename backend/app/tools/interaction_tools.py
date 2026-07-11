import json
from datetime import date, datetime
from typing import Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class LogInteractionInput(BaseModel):
    hcp_name: Optional[str] = Field(
        default=None,
        description="Name of the healthcare professional, for example Dr. Smith"
    )
    interaction_type: Optional[str] = Field(
        default="Meeting",
        description="Type of interaction such as Meeting, Call, Email, or Conference"
    )
    interaction_date: Optional[str] = Field(
        default=None,
        description="Date of the interaction in YYYY-MM-DD format"
    )
    interaction_time: Optional[str] = Field(
        default=None,
        description="Time of the interaction if explicitly mentioned"
    )
    attendees: Optional[str] = Field(
        default=None,
        description="Other attendees involved in the interaction"
    )
    topics_discussed: Optional[str] = Field(
        default=None,
        description="Topics, products, efficacy, safety, or other subjects discussed"
    )
    materials_shared: Optional[list[str]] = Field(
        default=None,
        description="Materials shared, such as brochures, clinical papers, or presentations"
    )
    sentiment: Optional[str] = Field(
        default=None,
        description="HCP sentiment: Positive, Neutral, or Negative"
    )
    outcomes: Optional[str] = Field(
        default=None,
        description="Key outcomes or agreements from the interaction"
    )
    follow_up_actions: Optional[str] = Field(
        default=None,
        description="Any follow-up actions explicitly mentioned"
    )


@tool(args_schema=LogInteractionInput)
def log_interaction(
    hcp_name: Optional[str] = None,
    interaction_type: Optional[str] = "Meeting",
    interaction_date: Optional[str] = None,
    interaction_time: Optional[str] = None,
    attendees: Optional[str] = None,
    topics_discussed: Optional[str] = None,
    materials_shared: Optional[list[str]] = None,
    sentiment: Optional[str] = None,
    outcomes: Optional[str] = None,
    follow_up_actions: Optional[str] = None,
) -> str:
    """
    Log a new HCP interaction from natural-language information.

    Use this tool when the user describes a new meeting, call, email,
    conference, or other interaction with a healthcare professional.
    """

    data = {
        "hcp_name": hcp_name,
        "interaction_type": interaction_type or "Meeting",
        "interaction_date": interaction_date or date.today().isoformat(),
        "interaction_time": interaction_time or datetime.now().strftime("%H:%M"),
        "attendees": attendees,
        "topics_discussed": topics_discussed,
        "materials_shared": materials_shared or [],
        "samples_distributed": [],
        "sentiment": sentiment,
        "outcomes": outcomes,
        "follow_up_actions": follow_up_actions,
    }

    return json.dumps({
        "tool": "log_interaction",
        "updates": data
    })


class EditInteractionInput(BaseModel):
    hcp_name: Optional[str] = Field(
        default=None,
        description="Corrected HCP name. Only provide if user requests this change."
    )
    interaction_type: Optional[str] = Field(
        default=None,
        description="Corrected interaction type"
    )
    interaction_date: Optional[str] = Field(
        default=None,
        description="Corrected date in YYYY-MM-DD format"
    )
    interaction_time: Optional[str] = Field(
        default=None,
        description="Corrected interaction time"
    )
    attendees: Optional[str] = Field(
        default=None,
        description="Corrected attendees"
    )
    topics_discussed: Optional[str] = Field(
        default=None,
        description="Corrected discussion topics"
    )
    materials_shared: Optional[list[str]] = Field(
        default=None,
        description="Corrected list of materials shared"
    )
    sentiment: Optional[str] = Field(
        default=None,
        description="Corrected sentiment: Positive, Neutral, or Negative"
    )
    outcomes: Optional[str] = Field(
        default=None,
        description="Corrected interaction outcomes"
    )
    follow_up_actions: Optional[str] = Field(
        default=None,
        description="Corrected follow-up actions"
    )


@tool(args_schema=EditInteractionInput)
def edit_interaction(
    hcp_name: Optional[str] = None,
    interaction_type: Optional[str] = None,
    interaction_date: Optional[str] = None,
    interaction_time: Optional[str] = None,
    attendees: Optional[str] = None,
    topics_discussed: Optional[str] = None,
    materials_shared: Optional[list[str]] = None,
    sentiment: Optional[str] = None,
    outcomes: Optional[str] = None,
    follow_up_actions: Optional[str] = None,
) -> str:
    """
    Edit specific fields of the current HCP interaction.

    Use this tool when the user corrects or changes previously logged
    information. Preserve every field the user does not explicitly change.
    """

    potential_updates = {
        "hcp_name": hcp_name,
        "interaction_type": interaction_type,
        "interaction_date": interaction_date,
        "interaction_time": interaction_time,
        "attendees": attendees,
        "topics_discussed": topics_discussed,
        "materials_shared": materials_shared,
        "sentiment": sentiment,
        "outcomes": outcomes,
        "follow_up_actions": follow_up_actions,
    }

    updates = {
        key: value
        for key, value in potential_updates.items()
        if value is not None
    }

    return json.dumps({
        "tool": "edit_interaction",
        "updates": updates
    })


class AddSampleInput(BaseModel):
    product_name: str = Field(
        description="Name of the pharmaceutical product or sample"
    )
    quantity: int = Field(
        default=1,
        description="Number of samples distributed"
    )


@tool(args_schema=AddSampleInput)
def add_sample(product_name: str, quantity: int = 1) -> str:
    """
    Add pharmaceutical samples distributed during the current HCP interaction.
    """

    return json.dumps({
        "tool": "add_sample",
        "updates": {
            "samples_distributed": [
                {
                    "product_name": product_name,
                    "quantity": quantity
                }
            ]
        }
    })


class CreateFollowUpInput(BaseModel):
    action: str = Field(
        description="The follow-up action to perform"
    )
    timeframe: Optional[str] = Field(
        default=None,
        description="Timeframe such as tomorrow, next week, or in two weeks"
    )


@tool(args_schema=CreateFollowUpInput)
def create_follow_up(
    action: str,
    timeframe: Optional[str] = None
) -> str:
    """
    Create a follow-up action for the current HCP interaction.
    """

    follow_up = action

    if timeframe:
        follow_up = f"{action} ({timeframe})"

    return json.dumps({
        "tool": "create_follow_up",
        "updates": {
            "follow_up_actions": follow_up
        }
    })


class AnalyzeInteractionInput(BaseModel):
    summary: str = Field(
        description=(
            "A concise LLM-generated analysis of the current interaction, "
            "including the key outcome or commercial insight"
        )
    )


@tool(args_schema=AnalyzeInteractionInput)
def analyze_interaction(summary: str) -> str:
    """
    Analyze the current HCP interaction and identify its key outcome.

    Use the current interaction context to generate a concise, useful outcome
    for the field representative.
    """

    return json.dumps({
        "tool": "analyze_interaction",
        "updates": {
            "outcomes": summary
        }
    })


ALL_TOOLS = [
    log_interaction,
    edit_interaction,
    add_sample,
    create_follow_up,
    analyze_interaction,
]