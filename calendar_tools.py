from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import logging
from datetime import datetime
import pickle

class CalendarManager:
    def __init__(self):
        """Initialize Google Calendar API client."""
        self.service = self._get_calendar_service()

    def _get_calendar_service(self):
        """Get or create Google Calendar API service."""
        creds = None
        
        # Check if token exists
        if os.path.exists('credentials/token.pickle'):
            with open('credentials/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If credentials are invalid, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials/credentials.json',
                    ['https://www.googleapis.com/auth/calendar.events']
                )
                creds = flow.run_local_server(port=0)
            
            # Save the credentials
            with open('credentials/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return build('calendar', 'v3', credentials=creds)

    def create_event(self, event_details: dict) -> str:
        """
        Create a new calendar event.
        
        Args:
            event_details: Dictionary containing event details
            {
                'summary': 'Event title',
                'start': datetime,
                'end': datetime,
                'description': 'Optional description'
            }
            
        Returns:
            Response message
        """
        try:
            event = {
                'summary': event_details['summary'],
                'start': {
                    'dateTime': event_details['start'].isoformat(),
                    'timeZone': 'Asia/Kolkata'
                },
                'end': {
                    'dateTime': event_details['end'].isoformat(),
                    'timeZone': 'Asia/Kolkata'
                }
            }
            
            if 'description' in event_details:
                event['description'] = event_details['description']
            
            created_event = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            return f"Event created successfully: {created_event['summary']}"
            
        except Exception as e:
            logging.error(f"Error creating event: {str(e)}")
            return "Failed to create event. Please try again."

    def get_upcoming_events(self, max_results: int = 10) -> str:
        """
        Get upcoming events from calendar.
        
        Args:
            max_results: Maximum number of events to return
            
        Returns:
            Formatted string of upcoming events
        """
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            if not events:
                return "No upcoming events found."
                
            response = "Upcoming events:\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                response += f"\n{event['summary']} at {start}"
            
            return response
            
        except Exception as e:
            logging.error(f"Error fetching events: {str(e)}")
            return "Failed to fetch events. Please try again."
