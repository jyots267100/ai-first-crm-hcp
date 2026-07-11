import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/chat";

const emptyInteraction = {
  id: null,
  hcp_name: "",
  interaction_type: "",
  interaction_date: "",
  interaction_time: "",
  attendees: "",
  topics_discussed: "",
  materials_shared: [],
  samples_distributed: [],
  sentiment: "",
  outcomes: "",
  follow_up_actions: "",
};

export const sendMessage = createAsyncThunk(
  "interaction/sendMessage",
  async (message, { getState, rejectWithValue }) => {
    try {
      const state = getState();

      const response = await axios.post(API_URL, {
        message,
        interaction_id: state.interaction.currentInteraction.id || null,
      });

      return response.data;
    } catch (error) {
      return rejectWithValue(
        error.response?.data?.detail ||
          error.message ||
          "Unable to communicate with the AI assistant."
      );
    }
  }
);

const interactionSlice = createSlice({
  name: "interaction",

  initialState: {
    currentInteraction: emptyInteraction,

    messages: [
      {
        role: "assistant",
        content:
          "Hello! I'm your AI assistant. Describe an HCP interaction, and I'll automatically populate the form for you.",
      },
    ],

    loading: false,
    error: null,
    lastToolUsed: null,
  },

  reducers: {},

  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state, action) => {
        state.loading = true;
        state.error = null;

        state.messages.push({
          role: "user",
          content: action.meta.arg,
        });
      })

      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false;

        if (action.payload.interaction) {
          state.currentInteraction = {
            ...emptyInteraction,
            ...action.payload.interaction,
          };
        }

        state.lastToolUsed = action.payload.tool_used || null;

        state.messages.push({
          role: "assistant",
          content:
            action.payload.message ||
            "Your request was completed successfully.",
          toolUsed: action.payload.tool_used || null,
        });
      })

      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;

        state.error =
          action.payload || "Something went wrong. Please try again.";

        state.messages.push({
          role: "assistant",
          content: `Error: ${
            action.payload || "Something went wrong."
          }`,
          isError: true,
        });
      });
  },
});

export default interactionSlice.reducer;