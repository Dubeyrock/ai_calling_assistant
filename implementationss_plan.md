# Implementation Plan: Install and Configure FreeSWITCH for AI Calling

This plan outlines the steps to install FreeSWITCH using Docker on Windows and configure it to work with your AI calling assistant project. This will resolve the "Offline" status and enable inbound/outbound call handling.

## User Review Required

> [!IMPORTANT]
> **Docker Desktop Needed**: We will use Docker to run FreeSWITCH because it is the most stable method for Windows. You have a "Docker Desktop" shortcut on your desktop—please ensure it is installed and running before we proceed.

> [!WARNING]
> **Ports & Networking**: FreeSWITCH uses port 8021 for ESL (Event Socket Layer) and 5060 for SIP. Ensure these ports are not blocked by your Windows Firewall.

## Proposed Changes

### 1. Docker Configuration

#### [MODIFY] [docker-compose.yml](file:///c:/Users/dubey/Desktop/ai_calling_assistant/ai_calling_assistant/docker-compose.yml)
- Update the existing `docker-compose.yml` to include a `freeswitch` service.
- We will use a standard FreeSWITCH image (e.g., `safing/freeswitch`).
- Mount a local volume for configuration files so we can customize ESL passwords and SIP settings.

### 2. FreeSWITCH Configuration

#### [NEW] `fs_config/` directory
- Create a configuration directory in your project containing:
    - `event_socket.conf.xml`: To enable ESL on `0.0.0.0:8021` with a password (for the Python scripts to connect).
    - `vars.xml`: To set the global SIP domain and passwords.

### 3. Python Integration

- Verify that `app.py` can connect to the new FreeSWITCH container.
- Update `config.py` if a specific ESL password is required.

## Open Questions

1. **Do you already have a SIP Trunk provider?** (e.g., Twilio, SignalWire, or a local provider). If not, we can start with local testing using MicroSIP.
2. **Which Python script do you want to use for calls?** You have `fs_server.py` (WebSocket-based) and `sip_bot.py` (File-based). I recommend `fs_server.py` for real-time AI interaction.

## Verification Plan

### Automated Tests
- Run `netstat -ano | findstr :8021` to verify the port is open and listening.
- Use a small python script to test the ESL connection (`python -c "import socket; print(socket.create_connection(('localhost', 8021)))"`).

### Manual Verification
1. Start Docker containers: `docker-compose up -d`.
2. check `app.py` dashboard—The FreeSWITCH status should turn **🟢 Online**.
3. Use **MicroSIP** (which you have on your desktop) to register a test account and place a call to verify the AI responds.
