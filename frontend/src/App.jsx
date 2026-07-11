import "./App.css";

import InteractionForm from "./components/InteractionForm";
import AIAssistant from "./components/AIAssistant";

function App() {
  return (
    <main className="app-shell">
      <header className="top-header">
        <div>
          <div className="brand">
            <span className="brand-icon">✦</span>
            HCP CRM
          </div>

          <span className="brand-subtitle">
            AI-First Life Sciences CRM
          </span>
        </div>

        <div className="technology-badges">
          <span>LangGraph</span>
          <span>Groq LLM</span>
          <span>FastAPI</span>
          <span>Redux</span>
        </div>
      </header>

      <div className="split-layout">
        <InteractionForm />
        <AIAssistant />
      </div>
    </main>
  );
}

export default App;