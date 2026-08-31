# Personal AI Agent 🤖

A Python-based AI agent that uses Google's Gemini API and Google Calendar API to interact with users and perform real actions.

## Features

* Perform basic mathematical calculations
* View upcoming Google Calendar events
* Search calendar events
* Create new calendar events
* Update existing calendar events
* Delete calendar events
* Plan a daily schedule
* Ask for user approval before adding proposed events to Google Calendar

## How It Works

The agent receives a user's request and decides whether a tool is needed.

For example:

```text
User: What events do I have coming up?
        ↓
Gemini AI Agent
        ↓
Calendar Tool
        ↓
Google Calendar API
        ↓
Agent returns the result
```

For daily planning:

```text
User asks to plan their day
        ↓
Agent checks Google Calendar
        ↓
Creates a proposed schedule
        ↓
Waits for user approval
        ↓
If approved → Events are added to Google Calendar
If rejected → No changes are made
```

## Technologies Used

* Python
* Google Gemini API
* Google Calendar API
* Google GenAI SDK
* Google OAuth 2.0
* python-dotenv

## Project Structure

```text
AI_AGENT/
│
├── day-4.py
├── README.md
├── .gitignore
├── key.env                 # Not uploaded to GitHub
├── token.json              # Not uploaded to GitHub
└── client_secret_*.json    # Not uploaded to GitHub
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI_AGENT
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install google-genai google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv
```

### 5. Add your Gemini API key

Create a `key.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

### 6. Add Google OAuth credentials

Create a Google Cloud project, enable the Google Calendar API, and download your OAuth client credentials.

Place the downloaded JSON credentials file in the project folder.

Update the `CLIENT_SECRET_FILE` name in `day-4.py` if necessary.

### 7. Run the project

```bash
python day-4.py
```

## Example Interactions

```text
You: 25 * 8
Agent: 200
```

```text
You: What events do I have coming up?
Agent: Here are your upcoming events...
```

```text
You: Plan my day tomorrow.
Agent: Would you like me to add these events to your Google Calendar?

You: Yes
Agent: Done! I added 2 events to your Google Calendar.
```

## Current Status

The Google Calendar integration is complete for the current prototype.

Email integration and additional agent capabilities are planned as future improvements.

## Important

Sensitive files such as API keys, OAuth credentials, and authentication tokens are excluded from GitHub using `.gitignore`.
