# 📞 AI-Powered Voice Calling & Assistant System

An end-to-end, autonomous AI Voice Assistant designed for both web-based interaction and direct telephony integration (via FreeSWITCH). This system leverages cutting-edge AI models for Speech-to-Text (STT), Large Language Models (LLM), and Text-to-Speech (TTS) to provide a seamless, low-latency conversational experience.

---

## 🚀 Key Features

- **Omnichannel Support**: Interact via a modern **Streamlit Web UI** or through **Standard Phone Calls** (FreeSWITCH/SIP).
- **Admin Dashboard**: Built-in system status monitoring for FreeSWITCH connectivity and API health.
- **Dynamic Personality**: Real-time adjustment of AI system prompts and voice selection (Rachel, Bella, Antoni, etc.) via the UI.
- **Local & Cloud STT**: Support for local Whisper transcription for privacy and cost-efficiency.
- **Ultra-Fast Responses**: Powered by **Groq** (Llama 3.3) for near-instant text generation.
- **Premium Audio**: High-fidelity voice responses using **ElevenLabs**.

---

## 🏗 System Architecture

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Web interface & Microphone interaction |
| **STT** | OpenAI Whisper | Converts voice to text |
| **LLM** | Groq (Llama 3.3) | Brain of the assistant (logic & reasoning) |
| **TTS** | ElevenLabs | Converts text back to human-like speech |
| **Telephony** | FreeSWITCH | Handles SIP calls and ESL signaling |
| **Storage** | Redis / MongoDB | Conversation history and long-term logging |

---

## 🛠 Prerequisites

- Python 3.10+
- FreeSWITCH (Optional, for telephony features)
- API Keys for:
  - [Groq](https://console.groq.com/)
  - [ElevenLabs](https://elevenlabs.io/)

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai_calling_assistant
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
we   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_key
   ELEVENLABS_API_KEY=your_elevenlabs_key
   # Optional
   REDIS_URL=redis://localhost:6379
   POSTGRES_URL=postgresql://user:pass@localhost/db
   ```

---

## 📈 Running the Application

### 1. Web Assistant (Streamlit)
To start the browser-based voice assistant:
```bash
streamlit run app.py
```

### 2. Telephony Bot (FreeSWITCH)
To handle actual phone calls, ensure FreeSWITCH is running and execute:
```bash
python sip_bot.py
```

---

## ☁️ AWS Deployment Guide

To deploy this system on AWS (EC2 or App Runner), follow these critical steps:

### 1. Security Groups
- Open Port **8501** (Streamlit default).
- Open Port **8021** if you need external ESL access to FreeSWITCH.

### 2. HTTPS Requirement (Crucial)
Web browsers (Chrome, Safari) **block microphone access** on non-secure (HTTP) connections. 
- You **must** set up an SSL certificate (e.g., using Let's Encrypt and Nginx).
- Use Nginx as a reverse proxy to forward traffic from port 443 to 8501.

### 3. Docker Support
You can use the provided `docker-compose.yml` for simplified deployment:
```bash
docker-compose up -d
```

---

## 📁 Project Structure

```text
├── core/               # Core AI modules (STT, TTS, LLM)
├── storage/            # Database configurations (Redis, Mongo)
├── app.py              # Main Streamlit Application
├── sip_bot.py # Telephony/Signal handler
├── config.py           # Configuration manager
└── requirements.txt    # Python dependencies
```

---

## 🤝 Contributing
Feel free to open issues or submit pull requests for any improvements!


## demo 
<img width="1920" height="1080" alt="Screenshot (4458)" src="https://github.com/user-attachments/assets/474393b6-7e1f-4398-9961-8fe0b4bd62b8" />







