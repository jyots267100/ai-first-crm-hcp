# AI-First CRM HCP Module – Log Interaction Screen

An AI-first Customer Relationship Management (CRM) application designed for life-sciences field representatives to log and manage interactions with Healthcare Professionals (HCPs) entirely through a conversational AI assistant.

The application uses a split-screen interface:

- **Left Panel:** AI-controlled, read-only HCP interaction form.
- **Right Panel:** Conversational AI assistant that understands natural-language instructions.

The form is not manually editable. All interaction details are populated and updated exclusively through the AI assistant using **LangGraph tools and a Groq-hosted LLM**.

---

# How to Run the Project

## Prerequisites

Before running the application, make sure you have:

- Python 3.10 or later
- Node.js
- npm
- A valid Groq API key

---

## 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd ai-first-crm-hcp
```

---

## 2. Configure and Run the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` directory:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 3. Configure and Run the Frontend

Open a **second terminal** and navigate to the frontend directory from the project root:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

Open this address in your browser to use the application.

---

## Quick Start Summary

Run the backend in Terminal 1:

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

Run the frontend in Terminal 2:

```bash
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

# Key Features

- AI-controlled HCP interaction form
- Natural-language interaction logging
- Automatic structured data extraction
- AI-powered field-specific editing
- Pharmaceutical sample tracking
- Follow-up action creation
- AI-generated interaction analysis
- Persistent SQL database storage
- Redux-based frontend state management
- Real-time synchronization between AI chat and CRM form

---

# Tech Stack

## Frontend

- React
- Redux Toolkit
- React Redux
- Axios
- Vite
- Google Inter Font

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

## AI and Agent Framework

- LangGraph
- LangChain
- Groq LLM
- `llama-3.3-70b-versatile`

## Database

- SQLite for local development through SQLAlchemy

> The database layer is implemented using SQLAlchemy, allowing migration to PostgreSQL or MySQL by updating the database connection configuration.

---

# Application Architecture

```text
User
  |
  v
React AI Assistant
  |
  v
Redux Toolkit
  |
  v
FastAPI REST API
  |
  v
LangGraph Agent
  |
  v
Groq LLM
  |
  v
Dynamic Tool Selection
  |
  +-----------------------+
  |                       |
  v                       v
Five AI Tools        Current Interaction State
  |                       |
  +-----------+-----------+
              |
              v
       SQLAlchemy Database
              |
              v
      Structured JSON Response
              |
              v
          Redux Update
              |
              v
   AI-Controlled Form Updates
```

---

# LangGraph Agent

The LangGraph agent acts as the orchestration and reasoning layer between the user's natural-language instructions and the CRM application.

The agent:

1. Receives the user's natural-language message.
2. Receives the current HCP interaction state as context.
3. Uses the Groq-hosted LLM to understand the user's intent.
4. Dynamically selects the appropriate tool.
5. Executes the selected tool.
6. Updates only the relevant CRM fields.
7. Persists the resulting interaction state in the SQL database.
8. Returns structured data to the React frontend.
9. Redux updates the read-only interaction form automatically.

No manual form editing is required.

---

# Five LangGraph Tools

## 1. Log Interaction

The `log_interaction` tool captures a new HCP interaction from natural language.

Example:

```text
Today I met with Dr. Smith and discussed Product X efficacy.
The sentiment was positive and I shared brochures.
```

The AI extracts structured information such as:

- HCP name
- Interaction type
- Date and time
- Attendees
- Topics discussed
- Materials shared
- Sentiment
- Outcomes
- Follow-up actions

The extracted information automatically populates the left-side form.

---

## 2. Edit Interaction

The `edit_interaction` tool modifies only the fields explicitly corrected by the user while preserving all other existing information.

Example:

```text
Sorry, the doctor's name was actually Dr. John and the sentiment was negative.
```

Only these fields are changed:

```text
HCP Name: Dr. Smith -> Dr. John
Sentiment: Positive -> Negative
```

All other interaction information remains unchanged.

---

## 3. Add Sample

The `add_sample` tool records pharmaceutical samples distributed during an HCP interaction.

Example:

```text
I also gave Dr. John 2 samples of Product X.
```

Structured result:

```json
{
  "product_name": "Product X",
  "quantity": 2
}
```

---

## 4. Create Follow-up

The `create_follow_up` tool creates a follow-up action based on the user's natural-language request.

Example:

```text
Create a follow-up action to schedule another meeting with Dr. John in two weeks.
```

The follow-up action is automatically added to the CRM form.

---

## 5. Analyze Interaction

The `analyze_interaction` tool uses the current interaction context to identify the key outcome or commercial insight.

Example:

```text
Analyze this interaction and identify the key outcome.
```

The AI considers the full interaction context, including:

- HCP name
- Topics discussed
- Materials shared
- Samples distributed
- Sentiment
- Follow-up actions

It then generates a concise interaction outcome for the field representative.

---

# Project Structure

```text
ai-first-crm-hcp/
|
|-- backend/
|   |-- app/
|   |   |-- agent/
|   |   |   |-- __init__.py
|   |   |   `-- graph.py
|   |   |
|   |   |-- api/
|   |   |   |-- __init__.py
|   |   |   `-- chat.py
|   |   |
|   |   |-- tools/
|   |   |   |-- __init__.py
|   |   |   `-- interaction_tools.py
|   |   |
|   |   |-- __init__.py
|   |   |-- database.py
|   |   |-- db_models.py
|   |   |-- main.py
|   |   `-- schemas.py
|   |
|   |-- .env.example
|   `-- requirements.txt
|
|-- frontend/
|   |-- public/
|   |-- src/
|   |   |-- components/
|   |   |   |-- AIAssistant.jsx
|   |   |   `-- InteractionForm.jsx
|   |   |
|   |   |-- redux/
|   |   |   |-- interactionSlice.js
|   |   |   `-- store.js
|   |   |
|   |   |-- App.css
|   |   |-- App.jsx
|   |   |-- index.css
|   |   `-- main.jsx
|   |
|   |-- package.json
|   `-- vite.config.js
|
|-- .gitignore
`-- README.md
```

---

# How to Test All Five Tools

Use these prompts sequentially in the AI Assistant.

## Tool 1 – Log Interaction

```text
Today I met with Dr. Smith and discussed Product X efficacy.
The sentiment was positive and I shared brochures.
```

**Expected result:** The AI automatically populates the HCP name, interaction type, date, time, topics discussed, materials shared, and sentiment.

---

## Tool 2 – Edit Interaction

```text
Sorry, the doctor's name was actually Dr. John and the sentiment was negative.
```

**Expected result:** Only the HCP name and sentiment are updated. All other information is preserved.

---

## Tool 3 – Add Sample

```text
I also gave Dr. John 2 samples of Product X.
```

**Expected result:** Product X and quantity 2 are added to the Samples Distributed section.

---

## Tool 4 – Create Follow-up

```text
Create a follow-up action to schedule another meeting with Dr. John in two weeks.
```

**Expected result:** A follow-up action is automatically added.

---

## Tool 5 – Analyze Interaction

```text
Analyze this interaction and identify the key outcome.
```

**Expected result:** The LLM analyzes the complete current interaction and automatically populates the Outcomes field.

---

# API Endpoint

## POST `/api/chat`

Example request:

```json
{
  "message": "Today I met with Dr. Smith and discussed Product X efficacy. The sentiment was positive and I shared brochures.",
  "interaction_id": null
}
```

Example response:

```json
{
  "success": true,
  "message": "The interaction has been logged successfully.",
  "tool_used": "log_interaction",
  "form_updates": {
    "hcp_name": "Dr. Smith",
    "interaction_type": "Meeting",
    "topics_discussed": "Product X efficacy",
    "materials_shared": [
      "brochures"
    ],
    "sentiment": "Positive"
  },
  "interaction": {
    "id": 1,
    "hcp_name": "Dr. Smith",
    "interaction_type": "Meeting",
    "topics_discussed": "Product X efficacy",
    "materials_shared": [
      "brochures"
    ],
    "sentiment": "Positive"
  }
}
```

---

# Core Design Principle

The primary requirement of this application is that the HCP interaction form must not be manually filled out.

The left-side form is read-only and controlled entirely through the AI assistant. Users communicate naturally with the assistant, and the LangGraph agent uses the Groq LLM to determine which tool should be called and what structured changes should be applied to the CRM interaction state.

This creates an AI-first experience rather than a traditional form-first CRM workflow.

---

# Security

- The Groq API key is stored only in `backend/.env`.
- `.env` is excluded from Git using `.gitignore`.
- `.env.example` is provided as a safe configuration template.
- No API keys are hard-coded in frontend or backend source files.

---

# Future Enhancements

Potential improvements include:

- PostgreSQL or MySQL deployment
- HCP master-data search
- Authentication and role-based access control
- Conversation persistence
- LangGraph checkpointing
- Multiple interaction sessions
- Audit history for edited fields
- Voice-based interaction logging
- CRM analytics dashboard

---

# Summary

This project demonstrates an AI-first HCP CRM workflow where a pharmaceutical field representative can log, edit, enrich, and analyze healthcare-professional interactions entirely through natural language.

The combination of React, Redux, FastAPI, LangGraph, Groq LLM, SQLAlchemy, and SQL persistence provides an agent-driven architecture in which the AI assistant dynamically invokes specialized tools and synchronizes structured CRM state with a read-only frontend form.