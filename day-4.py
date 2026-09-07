
import os
import base64
from email.mime.text import MIMEText
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

GMAIL_TOKEN_FILE = os.path.join(
    BASE_DIR,
    "gmail_token.json"
)

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose"
]


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
# GOOGLE GMAIL CONNECTION
# ============================================================

def get_gmail_service():
    """Connect to the Gmail account selected during OAuth."""
    creds = None

    if os.path.exists(GMAIL_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            GMAIL_TOKEN_FILE,
            GMAIL_SCOPES
        )

    # Re-authorize if the saved token does not contain every Gmail scope
    # required by this version of the agent. This prevents the old
    # read-only token from causing a 403 Insufficient Permission error.
    saved_scopes = set(getattr(creds, "scopes", None) or []) if creds else set()
    required_scopes = set(GMAIL_SCOPES)

    if not creds or not creds.valid or not required_scopes.issubset(saved_scopes):
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            GMAIL_SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open(GMAIL_TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


gmail_service = get_gmail_service()


# ============================================================
# GMAIL — ACCOUNT DETAILS
# ============================================================

def get_gmail_account_details():
    """Get the email address of the connected Gmail account."""
    profile = gmail_service.users().getProfile(
        userId="me"
    ).execute()

    email_address = profile.get(
        "emailAddress",
        "Unknown email address"
    )

    return (
        f"Connected Gmail account: {email_address}\n"
        "The Gmail API profile does not provide the account "
        "holder's display name."
    )


# ============================================================
# GMAIL — READ RECENT EMAILS
# ============================================================

def _decode_gmail_body(data):
    """Decode a Gmail message body from base64url format."""
    if not data:
        return ""

    try:
        decoded = base64.urlsafe_b64decode(
            data + "=" * (-len(data) % 4)
        )
        return decoded.decode("utf-8", errors="replace")
    except Exception:
        return ""


def _extract_email_body(payload):
    """Extract readable plain-text content from a Gmail message payload."""
    if not payload:
        return ""

    mime_type = payload.get("mimeType", "")
    body_data = payload.get("body", {}).get("data")

    if body_data and mime_type == "text/plain":
        return _decode_gmail_body(body_data).strip()

    parts = payload.get("parts", [])

    # Prefer plain text when the email is multipart.
    for part in parts:
        if part.get("mimeType") == "text/plain":
            text = _extract_email_body(part)
            if text:
                return text

    # If there is no plain-text part, try any nested parts.
    for part in parts:
        text = _extract_email_body(part)
        if text:
            return text

    return ""


def get_recent_emails():
    """Get recent emails, including sender, subject, date, and body."""
    results = gmail_service.users().messages().list(
        userId="me",
        maxResults=10
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return (
            "You currently have no recent emails in your "
            "connected Gmail account."
        )

    result = []

    for message in messages:
        message_data = gmail_service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        headers = {
            header["name"]: header["value"]
            for header in message_data.get("payload", {}).get(
                "headers", []
            )
        }

        body = _extract_email_body(
            message_data.get("payload", {})
        )

        if not body:
            body = "(No readable plain-text body found.)"

        result.append(
            f"From: {headers.get('From', 'Unknown')}\n"
            f"Subject: {headers.get('Subject', '(No subject)')}\n"
            f"Date: {headers.get('Date', 'Unknown')}\n"
            f"Message:\n{body}"
        )

    return "\n\n".join(result)


# ============================================================
# GMAIL — DRAFT AND SEND REPLIES
# ============================================================

pending_gmail_draft = None

def _create_gmail_message(to: str, subject: str, body: str, reply_to_message_id: str = None):
    """Create a MIME email message and encode it for the Gmail API."""
    message = MIMEText(body, "plain", "utf-8")
    message["To"] = to
    message["Subject"] = subject

    if reply_to_message_id:
        message["In-Reply-To"] = reply_to_message_id
        message["References"] = reply_to_message_id

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode("utf-8")

    return {"raw": raw_message}


def draft_email(to: str, subject: str, body: str):
    """Create a Gmail draft. The draft is NOT sent automatically."""
    global pending_gmail_draft

    message = _create_gmail_message(to, subject, body)

    draft = gmail_service.users().drafts().create(
        userId="me",
        body={"message": message}
    ).execute()

    pending_gmail_draft = {
        "draft_id": draft.get("id"),
        "to": to,
        "subject": subject,
        "body": body
    }

    return (
        f"Draft created successfully.\n"
        f"To: {to}\n"
        f"Subject: {subject}\n"
        f"Message:\n{body}\n\n"
        "I have NOT sent it. Would you like me to send this email?"
    )


def send_pending_gmail_draft():
    """Send the currently pending Gmail draft after explicit user approval."""
    global pending_gmail_draft

    if not pending_gmail_draft:
        return "There is no Gmail draft waiting for approval."

    draft_id = pending_gmail_draft["draft_id"]

    sent = gmail_service.users().drafts().send(
        userId="me",
        body={"id": draft_id}
    ).execute()

    recipient = pending_gmail_draft["to"]
    subject = pending_gmail_draft["subject"]
    pending_gmail_draft = None

    return (
        f"Email sent successfully to {recipient}. "
        f"Subject: {subject}"
    )


def cancel_pending_gmail_draft():
    """Cancel and delete the pending Gmail draft."""
    global pending_gmail_draft

    if not pending_gmail_draft:
        return "There is no Gmail draft waiting for approval."

    draft_id = pending_gmail_draft["draft_id"]

    gmail_service.users().drafts().delete(
        userId="me",
        id=draft_id
    ).execute()

    pending_gmail_draft = None

    return "Okay, I cancelled and deleted the pending Gmail draft."


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
    model="gemini-3.6-flash",

    config={
        "system_instruction": """
You are a helpful personal AI assistant.

You can:
- perform mathematical calculations,
- read Google Calendar,
- search Calendar events,
- create Calendar events,
- update Calendar events,
- delete Calendar events,
- read recent Gmail emails,
- show the connected Gmail account email address,
- create Gmail drafts,
- send an approved Gmail draft.

Important Gmail safety rule:
- Creating a draft is allowed when the user asks for a draft.
- NEVER send an email automatically.
- After creating a draft, clearly show the recipient, subject, and message
  and ask the user for explicit approval before sending.
- Only send after the Python chat loop receives an explicit approval such
  as "yes", "send it", or "send the email".

For Calendar requests, use the appropriate Calendar tool.
For Gmail account requests, use get_gmail_account_details.
For Gmail email requests, use get_recent_emails.

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
            delete_calendar_event,
            get_gmail_account_details,
            get_recent_emails,
            draft_email
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
    # GMAIL DRAFT REJECTION
    # --------------------------------------------------------

    if pending_gmail_draft and (
        lower_input == "no"
        or lower_input.startswith("no ")
        or lower_input.startswith("no,")
        or "don't send" in lower_input
        or "do not send" in lower_input
        or "dont send" in lower_input
        or lower_input == "cancel"
        or lower_input.startswith("cancel ")
    ):

        try:
            print("Agent:", cancel_pending_gmail_draft())
        except Exception as e:
            print("Agent: I couldn't cancel the Gmail draft.")
            print("Error:", e)

        continue

    # --------------------------------------------------------
    # GMAIL DRAFT APPROVAL
    # --------------------------------------------------------

    if pending_gmail_draft and (
        lower_input == "yes"
        or lower_input.startswith("yes ")
        or lower_input.startswith("yes,")
        or lower_input == "send it"
        or lower_input == "send the email"
        or lower_input == "send email"
        or lower_input == "confirm"
        or lower_input == "confirmed"
    ):

        try:
            print("Agent:", send_pending_gmail_draft())
        except Exception as e:
            print("Agent: I couldn't send the approved Gmail draft.")
            print("Error:", e)

        continue

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

