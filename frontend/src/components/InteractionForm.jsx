import { useSelector } from "react-redux";

function DisplayField({ label, value, placeholder = "AI will populate this field" }) {
  return (
    <div className="field-group">
      <label>{label}</label>

      <div className={`readonly-field ${value ? "has-value" : ""}`}>
        {value || placeholder}
      </div>
    </div>
  );
}

function InteractionForm() {
  const interaction = useSelector(
    (state) => state.interaction.currentInteraction
  );

  const materials = interaction.materials_shared || [];
  const samples = interaction.samples_distributed || [];

  return (
    <section className="interaction-panel">
      <div className="panel-header">
        <div>
          <h1>Log HCP Interaction</h1>
          <p>Fields are controlled entirely by the AI Assistant</p>
        </div>

        <span className="ai-controlled-badge">
          AI Controlled
        </span>
      </div>

      <div className="form-content">
        <DisplayField
          label="HCP Name"
          value={interaction.hcp_name}
          placeholder="Waiting for HCP name..."
        />

        <div className="form-row three-columns">
          <DisplayField
            label="Interaction Type"
            value={interaction.interaction_type}
          />

          <DisplayField
            label="Date"
            value={interaction.interaction_date}
          />

          <DisplayField
            label="Time"
            value={interaction.interaction_time}
          />
        </div>

        <DisplayField
          label="Attendees"
          value={interaction.attendees}
        />

        <DisplayField
          label="Topics Discussed"
          value={interaction.topics_discussed}
        />

        <div className="field-group">
          <label>Materials Shared</label>

          <div className="chip-container">
            {materials.length > 0 ? (
              materials.map((material, index) => (
                <span className="chip" key={`${material}-${index}`}>
                  {material}
                </span>
              ))
            ) : (
              <span className="empty-text">
                AI will add shared materials
              </span>
            )}
          </div>
        </div>

        <div className="field-group">
          <label>Samples Distributed</label>

          <div className="samples-container">
            {samples.length > 0 ? (
              samples.map((sample, index) => (
                <div className="sample-card" key={index}>
                  <strong>
                    {sample.product_name || "Product"}
                  </strong>

                  <span>
                    Quantity: {sample.quantity || 1}
                  </span>
                </div>
              ))
            ) : (
              <div className="readonly-field">
                No samples added yet
              </div>
            )}
          </div>
        </div>

        <div className="field-group">
          <label>Sentiment</label>

          <div className="sentiment-options">
            {["Positive", "Neutral", "Negative"].map((option) => (
              <div
                className={`sentiment-option ${
                  interaction.sentiment?.toLowerCase() ===
                  option.toLowerCase()
                    ? "selected"
                    : ""
                }`}
                key={option}
              >
                <span className="radio-circle" />
                {option}
              </div>
            ))}
          </div>
        </div>

        <DisplayField
          label="Outcomes"
          value={interaction.outcomes}
          placeholder="Ask the AI to analyze the interaction"
        />

        <DisplayField
          label="Follow-up Actions"
          value={interaction.follow_up_actions}
          placeholder="Ask the AI to create a follow-up action"
        />
      </div>
    </section>
  );
}

export default InteractionForm;