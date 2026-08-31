
import os
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from google import genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ============================================================
# CONFIGURATION
# ============================================================

SCOPES = ["https://www.googleapis.com/auth/calendar"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CLIENT_SECRET_FILE = os.path.join(
    BASE_DIR,
    "client_secret_1062398998705-tcakpmm78sprppvvn0vqqkmjcvud8av6.apps.googleusercontent.com.json"
)

TOKEN_FILE = os.path.join(
    BASE_DIR,
    "token.json"
)


# ============================================================
# GOOGLE CALENDAR CONNECTION
# ============================================================

def get_calendar_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build(
        "calendar",
        "v3",
        credentials=creds
    )


# ============================================================
# MATH TOOLS
# ============================================================

def addition(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def subtraction(a: int, b: int) -> int:
    """Subtract the second number from the first."""
    return a - b


def multiplication(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


def division(a: int, b: int) -> float:
    """Divide the first number by the second."""

    if b == 0:
        return "I cannot divide by zero."

    return a / b


# ============================================================
# CALENDAR — READ EVENTS
# ============================================================

def get_calendar_events():
    """Get upcoming Google Calendar events."""

    events_result = calendar_service.events().list(
        calendarId="primary",
        timeMin=datetime.now(timezone.utc).isoformat(),
        maxResults=20,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return "There are no upcoming events."

    result = []

    for event in events:
        start = event["start"].get(
            "dateTime",
            event["start"].get("date")
        )

        summary = event.get(
            "summary",
            "Untitled event"
        )

        event_id = event.get("id")

        result.append(
            f"ID: {event_id} | {start} - {summary}"
        )

    return "\n".join(result)


# ============================================================
# CALENDAR — CREATE EVENT
# ============================================================

def create_calendar_event(
    summary: str,
    start_time: str,
    end_time: str
):
    """Create an event in the user's primary calendar."""

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Kolkata"
        }
    }

    created_event = calendar_service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return (
        f"Event created successfully: "
        f"{created_event.get('summary')}"
    )


# ============================================================
# CALENDAR — SEARCH EVENTS
# ============================================================

def search_calendar_events(search_text: str):
    """Search upcoming calendar events."""

    events_result = calendar_service.events().list(
        calendarId="primary",
        timeMin=datetime.now(timezone.utc).isoformat(),
        maxResults=20,
        singleEvents=True,
        orderBy="startTime",
        q=search_text
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return (
            f"No upcoming events found matching "
            f"'{search_text}'."
        )

    result = []

    for event in events:
        start = event["start"].get(
            "dateTime",
            event["start"].get("date")
        )

        summary = event.get(
            "summary",
            "Untitled event"
        )

        event_id = event.get("id")

        result.append(
            f"ID: {event_id} | {start} - {summary}"
        )

    return "\n".join(result)


# ============================================================
# CALENDAR — UPDATE EVENT
# ============================================================

def update_calendar_event(
    event_id: str,
    summary: str = None,
    start_time: str = None,
    end_time: str = None
):
    """Update an existing calendar event."""

    event = calendar_service.events().get(
        calendarId="primary",
        eventId=event_id
    ).execute()

    if summary is not None:
        event["summary"] = summary

    if start_time is not None:
        event["start"] = {
            "dateTime": start_time,
            "timeZone": "Asia/Kolkata"
        }

    if end_time is not None:
        event["end"] = {
            "dateTime": end_time,
            "timeZone": "Asia/Kolkata"
        }

    updated_event = calendar_service.events().update(
        calendarId="primary",
        eventId=event_id,
        body=event
    ).execute()

    return (
        f"Event updated successfully: "
        f"{updated_event.get('summary')}"
    )


# ============================================================
# CALENDAR — DELETE EVENT
# ============================================================

def delete_calendar_event(event_id: str):
    """Delete an existing calendar event."""

    calendar_service.events().delete(
        calendarId="primary",
        eventId=event_id
    ).execute()

    return "Event deleted successfully."


# ============================================================
# DAILY PLANNER
# ============================================================

pending_events = []


def plan_my_day():
    """
    Check tomorrow's calendar and create a proposed schedule.

    The proposed events are stored temporarily and are only
    added to Google Calendar after user approval.
    """

    pending_events.clear()

    india_timezone = timezone(
        timedelta(hours=5, minutes=30)
    )

    tomorrow = (
        datetime.now(india_timezone).date()
        + timedelta(days=1)
    )

    start_of_day = datetime.combine(
        tomorrow,
        datetime.min.time()
    ).replace(
        tzinfo=india_timezone
    )

    end_of_day = start_of_day + timedelta(days=1)

    # Check tomorrow's existing events
    events_result = calendar_service.events().list(
        calendarId="primary",
        timeMin=start_of_day.astimezone(
            timezone.utc
        ).isoformat(),
        timeMax=end_of_day.astimezone(
            timezone.utc
        ).isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    existing_events = events_result.get(
        "items",
        []
    )

    # Proposed schedule
    python_start = start_of_day.replace(
        hour=9
    )

    python_end = python_start + timedelta(
        hours=2
    )

    agent_start = python_end

    agent_end = agent_start + timedelta(
        hours=1
    )

    pending_events.extend([
        {
            "summary": "Study Python",
            "start_time": python_start.strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),
            "end_time": python_end.strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
        },
        {
            "summary": "Work on AI Agent",
            "start_time": agent_start.strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),
            "end_time": agent_end.strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
        }
    ])

    if existing_events:
        print(
            "Agent: I found these events "
            "already scheduled tomorrow:"
        )

        for event in existing_events:
            start = event["start"].get(
                "dateTime",
                event["start"].get("date")
            )

            summary = event.get(
                "summary",
                "Untitled event"
            )

            print(
                f"- {start} — {summary}"
            )
    else:
        print(
            "Agent: Your calendar is clear tomorrow."
        )

    print()
    print("📅 Proposed Schedule for Tomorrow")
    print()
    print(
        "09:00 AM – 11:00 AM : Study Python"
    )
    print(
        "11:00 AM – 12:00 PM : Work on AI Agent"
    )
    print()

    print(
        "Agent: Would you like me to add these "
        "events to your Google Calendar?"
    )


# ============================================================
# GEMINI SETUP
# ============================================================

load_dotenv(
    os.path.join(BASE_DIR, "key.env")
)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in key.env."
    )

client = genai.Client(
    api_key=api_key
)


# ============================================================
# GOOGLE CALENDAR SERVICE
# ============================================================

calendar_service = get_calendar_service()


# ============================================================
# AI AGENT
# ============================================================

chat = client.chats.create(
    model="gemini-3.5-flash",

    config={
        "system_instruction": """
You are a helpful personal AI assistant.

You can:
- perform mathematical calculations,
- read Google Calendar,
- search Calendar events,
- create Calendar events,
- update Calendar events,
- delete Calendar events.

For Calendar requests, use the appropriate
Calendar tool.

Never claim that a Calendar operation succeeded
unless the operation actually succeeded.

When the user asks to plan their day, the Python
daily planner handles the planning workflow.
""",

        "tools": [
            addition,
            subtraction,
            multiplication,
            division,

            get_calendar_events,
            create_calendar_event,
            search_calendar_events,
            update_calendar_event,
            delete_calendar_event
        ]
    }
)


# ============================================================
# CHAT LOOP
# ============================================================

while True:

    user_input = input("You: ").strip()
    lower_input = user_input.lower()

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    if lower_input == "stop":
        print("Agent: Okay, goodbye!")
        break

    # --------------------------------------------------------
    # REJECTION
    # --------------------------------------------------------

    if pending_events and (
        lower_input == "no"
        or lower_input.startswith("no ")
        or lower_input.startswith("no,")
        or "don't add" in lower_input
        or "do not add" in lower_input
        or "dont add" in lower_input
        or lower_input == "cancel"
        or lower_input.startswith("cancel ")
    ):

        pending_events.clear()

        print(
            "Agent: Okay, I won't add the "
            "proposed events to your calendar."
        )

        continue

    # --------------------------------------------------------
    # APPROVAL
    # --------------------------------------------------------

    if pending_events and (
        lower_input == "yes"
        or lower_input.startswith("yes ")
        or lower_input.startswith("yes,")
        or lower_input == "add them"
        or lower_input == "add these events"
        or lower_input == "confirm"
        or lower_input == "confirmed"
    ):

        try:
            created_count = 0

            for event in pending_events:
                create_calendar_event(
                    event["summary"],
                    event["start_time"],
                    event["end_time"]
                )

                created_count += 1

            pending_events.clear()

            print(
                f"Agent: Done! I added "
                f"{created_count} events "
                f"to your Google Calendar."
            )

        except Exception as e:
            print(
                "Agent: I couldn't add the "
                "approved events to your "
                "Google Calendar."
            )

            print("Error:", e)

        continue

    # --------------------------------------------------------
    # DAILY PLANNING
    # --------------------------------------------------------

    if (
        "plan my day" in lower_input
        or "plan tomorrow" in lower_input
        or "schedule my day" in lower_input
        or "make a schedule" in lower_input
    ):

        try:
            plan_my_day()

        except Exception as e:
            print(
                "Agent: I couldn't check "
                "your calendar right now."
            )

            print("Error:", e)

        continue

    # --------------------------------------------------------
    # NORMAL AI REQUEST
    # --------------------------------------------------------

    try:
        response = chat.send_message(
            user_input
        )

        print(
            "Agent:",
            response.text
        )

    except Exception as e:
        print(
            "Agent: Sorry, the AI service "
            "is temporarily unavailable. "
            "Please try again later."
        )

        print("Error:", e)

