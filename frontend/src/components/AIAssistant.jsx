import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import { sendMessage } from "../redux/interactionSlice";

const TOOL_LABELS = {
  log_interaction: "Log Interaction",
  edit_interaction: "Edit Interaction",
  add_sample: "Add Sample",
  create_follow_up: "Create Follow-up",
  analyze_interaction: "Analyze Interaction",
};

function AIAssistant() {
  const [input, setInput] = useState("");

  const dispatch = useDispatch();

  const { messages, loading, lastToolUsed } = useSelector(
    (state) => state.interaction
  );

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const handleSubmit = (event) => {
    event.preventDefault();

    const cleanMessage = input.trim();

    if (!cleanMessage || loading) {
      return;
    }

    dispatch(sendMessage(cleanMessage));

    setInput("");
  };

  return (
    <section className="assistant-panel">
      <div className="assistant-header">
        <div className="assistant-title">
          <div className="bot-icon">✦</div>

          <div>
            <h2>AI Assistant</h2>
            <span>
              <span className="online-dot" />
              Online · Powered by LangGraph + Groq
            </span>
          </div>
        </div>

        {lastToolUsed && (
          <div className="last-tool">
            Last tool:{" "}
            <strong>
              {TOOL_LABELS[lastToolUsed] || lastToolUsed}
            </strong>
          </div>
        )}
      </div>

      <div className="chat-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message-row ${message.role}`}
          >
            <div
              className={`message-bubble ${
                message.isError ? "error-message" : ""
              }`}
            >
              {message.content}

              {message.toolUsed && (
                <div className="tool-badge">
                  ✦ {TOOL_LABELS[message.toolUsed] || message.toolUsed}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-row assistant">
            <div className="message-bubble typing-bubble">
              <span />
              <span />
              <span />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="prompt-suggestions">
        <button
          onClick={() =>
            setInput(
              "Today I met with Dr. Smith and discussed Product X efficacy. The sentiment was positive and I shared brochures."
            )
          }
        >
          Log interaction
        </button>

        <button
          onClick={() =>
            setInput(
              "Actually, the doctor's name was Dr. John and the sentiment was negative."
            )
          }
        >
          Edit details
        </button>

        <button
          onClick={() =>
            setInput(
              "I also gave Dr. John 2 samples of Product X."
            )
          }
        >
          Add sample
        </button>
      </div>

      <form className="chat-input-area" onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Describe an HCP interaction or ask the AI to update the form..."
          rows="3"
          disabled={loading}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              handleSubmit(event);
            }
          }}
        />

        <button
          className="send-button"
          type="submit"
          disabled={!input.trim() || loading}
        >
          {loading ? "Thinking..." : "Send ➤"}
        </button>
      </form>
    </section>
  );
}

export default AIAssistant;