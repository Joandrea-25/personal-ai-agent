# AZRIEL 🤖

AZRIEL is a Personal AI Agent built using Python and Google's Gemini API.

I built this project to understand how an AI Agent can do more than just respond to questions. Instead of only generating a response like a normal chatbot, AZRIEL can use different tools to perform actions based on what the user asks.

Currently, AZRIEL can perform mathematical calculations, manage Google Calendar events, help with daily planning, and interact with Gmail.

## What AZRIEL Can Do

### AI Agent

AZRIEL uses Gemini to understand the user's request.

Based on the request, it can decide whether a tool is needed and call the appropriate function. For example, if the user asks to create a calendar event, AZRIEL can use the Calendar functionality instead of just explaining how to create one.

It can also perform basic mathematical operations such as:

- Addition
- Subtraction
- Multiplication
- Division

The agent runs through a command-line interface where the user can interact with it using normal language.

## Google Calendar Integration

AZRIEL is connected to Google Calendar and can:

- View upcoming events
- Search for events
- Create new events
- Update existing events
- Delete events
- Help plan a daily schedule

For daily planning, AZRIEL checks the calendar and suggests a schedule based on the request. Before adding the suggested events to Google Calendar, it asks for user approval.

The events are only added if the user accepts the plan.

## Gmail Integration

AZRIEL is also connected to Gmail.

The agent can read recent emails and help the user interact with their email account.

For actions that can affect the user's account, AZRIEL is designed to ask for user approval before performing them.

## How It Works

When a user gives AZRIEL a request, Gemini is used to understand what the user is asking for.

If the request requires an action, the agent checks the available tools and uses the appropriate one.

For example, if the user asks about upcoming events, AZRIEL uses the Google Calendar functionality to get the information and returns the result.

If the user asks to create or modify an event, the agent uses the Calendar API to perform the requested action.

The main thing I wanted to understand while building this project was how an AI model can work together with Python functions and external APIs.

## Technologies Used

- Python
- Google Gemini API
- Google GenAI SDK
- Google Calendar API
- Gmail API
- Google OAuth 2.0
- google-api-python-client
- google-auth
- google-auth-oauthlib
- python-dotenv

## Project Structure
AZRIEL-AI-AGENT/
│
├── azriel.py
├── requirements.txt
├── README.md
└── .gitignore
Sensitive files such as API keys, OAuth credentials, and authentication tokens are not included in the repository.

Setup
1. Clone the repository
git clone https://github.com/Joandrea-25/AZRIEL-AI-AGENT.git
cd AZRIEL-AI-AGENT
2. Create a virtual environment
python -m venv .venv
3. Activate the virtual environment

For Windows PowerShell:

.venv\Scripts\Activate.ps1
4. Install the required packages
pip install -r requirements.txt
Gemini API Key

Create a file named:

key.env

Add your Gemini API key:

GEMINI_API_KEY=your_api_key_here
Google OAuth Setup

To use the Google Calendar and Gmail features, Google OAuth needs to be configured.

The required steps are:

Create a project in Google Cloud Console.
Enable Google Calendar API.
Enable Gmail API.
Configure the OAuth Consent Screen.
Create OAuth credentials for a Desktop Application.
Download the credentials JSON file.
Place the credentials file inside the project folder.
Run the program and complete the Google authentication process.

Authentication tokens created during this process are stored locally and are not uploaded to GitHub.

Running the Project

After completing the setup, run:

python azriel.py

The agent will start in the terminal.

Example Interactions
Mathematical Calculation
You: What is 25 multiplied by 8?

AZRIEL: 200
Checking Calendar Events
You: What events do I have coming up?

AZRIEL: Here are your upcoming events...
Creating an Event
You: Create an event for tomorrow at 7 PM.

AZRIEL: Event created successfully.
Planning the Day
You: Help me plan my day tomorrow.

AZRIEL: Here is the schedule I suggest...

AZRIEL: Do you want me to add these events to your Google Calendar?

The events are only added after the user gives approval.

Security

The following types of files are excluded from GitHub:

Gemini API keys
OAuth credentials
Google authentication tokens
Gmail authentication tokens

These files contain sensitive information and should not be uploaded to a public repository.

What I Learned:

This project helped me understand the difference between using an LLM and building an AI Agent.

An LLM can understand a prompt and generate a response. While building AZRIEL, I learned how an AI model can also be connected to tools and functions to perform actions.

I also learned about:

AI Agent tool calling
Connecting Python functions with an AI model
API integration
Google Calendar API
Gmail API
OAuth authentication
Authentication tokens and permission scopes
Environment variables
Debugging API and integration issues

One of the main things I learned from this project is that building an AI Agent involves connecting multiple parts together. The AI model understands the request, but APIs, functions, and authentication are needed to allow the agent to actually perform actions.

Future Improvements

Some features I would like to add to AZRIEL in the future are:

Better daily schedule planning
Recurring tasks and reminders
Email summarization
Email drafting with user approval
Task and to-do list management
More integrations with other applications
Better planning based on calendar availability
A web interface
More advanced AI Agent workflows
About the Project

I built AZRIEL to learn more about AI Agents by actually creating one.

I wanted to understand what happens when an AI model is connected with tools and external services instead of only being used to generate text.

Starting with simple tools helped me understand how tool calling works. I then expanded the project by connecting Google Calendar and Gmail.

AZRIEL is something I want to continue improving, and building it helped me get practical experience with AI models, APIs, authentication, and AI Agent workflows.

Author

Joan Andrea

B.E. Computer Science Engineering
Artificial Intelligence and Robotics
