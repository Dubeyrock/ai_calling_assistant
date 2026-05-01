# Advanced Streamlit App Features

User wants to add a status dashboard, settings for AI personality and voice, and a robust chat log system.

## User Review Required

> [!IMPORTANT]
> The **System Status Dashboard** will attempt to connect to the FreeSWITCH ESL port (8021) to check status. If your FreeSWITCH is on a different port or host, please let me know.
>
> **TTS Audio**: In the Streamlit app, audio will play through your *browser* (output of `st.audio`), which is essential for AWS deployment.

## Proposed Changes

### Core Logic

#### [MODIFY] [llm.py](file:///c:/Users/dubey/Desktop/ai_calling_assistant/ai_calling_assistant/core/llm.py)
- Update `get_llm_response` to accept an optional `system_prompt`.

### UI Component

#### [MODIFY] [app.py](file:///c:/Users/dubey/Desktop/ai_calling_assistant/ai_calling_assistant/app.py)

- **Sidebar Configuration**:
    - **Settings Section**:
        - `st.text_area` for custom system prompt (defaulting to the job portal assistant).
        - `st.selectbox` for ElevenLabs Voice selection (Rachel, Bella, Antoni, etc.).
        - "Clear Conversation" button.
    - **Dashboard Section**:
        - Visual indicators (🟢/🔴) for FreeSWITCH Connection, Groq API, and ElevenLabs API.
- **Main Chat Interface**:
    - Enhanced transcript display with role-specific icons.
    - Integration of sidebar settings into the logic flow.

## Open Questions

- Should I include a specific list of ElevenLabs voices, or just the default Rachel one for now?
- Is FreeSWITCH running on the same machine as the web app (localhost)?

## Verification Plan

### Automated Tests
- Run `streamlit run app.py` and verify:
    - Sidebar displays correctly.
    - Status indicators update based on simulated/actual connectivity.
    - System prompt changes are reflected in AI responses.
    - Audio uses the selected voice.

### Manual Verification
- Manually record audio via the browser and check if the chat log updates and audio plays back.
