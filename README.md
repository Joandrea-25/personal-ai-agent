Personal AI Agent 🤖

A Python-based Personal AI Agent that uses Google's Gemini API along with Google Calendar and Gmail integrations to understand user requests and perform real actions.

The goal of this project is to move beyond a traditional chatbot. Instead of only generating responses, the agent can use connected tools and services to perform tasks such as managing calendar events and interacting with emails.

✨ Features
🤖 AI Agent
Understands user requests using Google's Gemini AI
Uses tools to perform actions instead of only generating responses
Handles basic mathematical calculations
Provides conversational interaction through a command-line interface
📅 Google Calendar Integration

The agent can:

View upcoming Google Calendar events
Search calendar events
Create new calendar events
Update existing calendar events
Delete calendar events
Plan a daily schedule
Ask for user approval before adding proposed events to Google Calendar
📧 Gmail Integration

The AI Agent is also connected with Gmail functionality, allowing it to interact with the user's email account as part of the agent system.

🧠 How It Works

The AI agent receives a request from the user and determines whether a connected tool is needed.

Example: Checking Calendar Events
User: What events do I have coming up?

        ↓

Gemini AI Agent

        ↓

Calendar Tool

        ↓

Google Calendar API

        ↓

Agent returns the result
Example: Daily Planning
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
🛠️ Technologies Used
Python
Google Gemini API
Google GenAI SDK
Google Calendar API
Gmail API
Google OAuth 2.0
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
python-dotenv

📁 Project Structure
AI_AGENT/
│
├── day-4.py
├── README.md
├── .gitignore
│
├── key.env
│   └── Stores the Gemini API key
│
├── token.json
│   └── Google Calendar authentication token
│
├── gmail_token.json
│   └── Gmail authentication token
│
└── client_secret_*.json
    └── Google OAuth client credentials

⚠️ Sensitive files such as API keys, OAuth credentials, and authentication tokens are excluded from GitHub.

⚙️ Setup
1. Clone the Repository
git clone <your-repository-url>
cd AI_AGENT
2. Create a Virtual Environment
python -m venv .venv
3. Activate the Virtual Environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
4. Install Dependencies
pip install google-genai google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv
🔑 Add Your Gemini API Key

Create a file named:

key.env

Add your API key:

GEMINI_API_KEY=your_api_key_here
🔐 Google OAuth Setup

To connect the agent with Google services:

Create a project in Google Cloud Console.
Enable the required APIs:
Google Calendar API
Gmail API
Configure the OAuth Consent Screen.
Create OAuth credentials for a Desktop Application.
Download the OAuth credentials JSON file.
Place the credentials file inside the project folder.
Run the application and complete Google authentication.

Authentication tokens generated during this process are stored locally and should never be uploaded to GitHub.

▶️ Run the Project
python day-4.py

The AI Agent will start in the terminal.

💬 Example Interactions
Mathematical Calculation
You: 25 * 8

Agent: 200
Check Upcoming Events
You: What events do I have coming up?

Agent: Here are your upcoming events...
Plan a Day
You: Plan my day tomorrow.

Agent: Here is your proposed schedule.

Agent: Would you like me to add these events to your Google Calendar?

If approved:

You: Yes

Agent: Done! I added the events to your Google Calendar.
🔒 Security

The following sensitive files are excluded from GitHub using .gitignore:

key.env
token.json
gmail_token.json
client_secret_*.json

These files may contain:

API keys
OAuth credentials
Access tokens
Authentication information

Never upload these files to a public GitHub repository.

🚧 Current Status

The current Personal AI Agent prototype includes:

✅ Gemini-powered AI interaction
✅ Tool-based AI Agent architecture
✅ Mathematical tools
✅ Google Calendar integration
✅ View Calendar events
✅ Search Calendar events
✅ Create Calendar events
✅ Update Calendar events
✅ Delete Calendar events
✅ Daily schedule planning
✅ User approval before Calendar changes
✅ Gmail integration
🚀 Future Improvements
Improved email automation
Email drafting with user approval before sending
Smarter schedule planning
Task and to-do list management
Multiple tool integrations
Real-time information capabilities
Web interface
Persistent memory for user preferences
More advanced AI Agent workflows
🎯 Project Goal

This project was built to understand how modern AI Agents work.

An LLM can generate responses, but an AI Agent can use tools and take actions.

By connecting Gemini with tools such as Google Calendar and Gmail, this project explores how an AI model can move beyond conversation and interact with real-world applications.

👩‍💻 Author

Joan Andrea

B.E. Computer Science Engineering
Artificial Intelligence and Robotics
