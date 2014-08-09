from oauth2client.client import Credentials
from apiclient.discovery import build

import httplib2

def __create_service():
    with open('credentials', 'rw') as f:
        credentials = Credentials.new_from_json(f.read())

    http = httplib2.Http()
    http = credentials.authorize(http)

    return build('calendar', 'v3', http=http)

service = __create_service()

page_token = None
while True:
  calendar_list = service.calendarList().list(pageToken=page_token).execute()
  for calendar_list_entry in calendar_list['items']:
    print calendar_list_entry['summary']
    print calendar_list_entry
  page_token = calendar_list.get('nextPageToken')
  if not page_token:
    break


event = {
  'summary': 'Appointment',
  'location': 'Somewhere',
  'start': {
    'dateTime': '2014-08-09T10:00:00.000-07:00'
  },
  'end': {
    'dateTime': '2014-08-09T10:25:00.000-07:00'
  }
}

created_event = service.events().insert(calendarId=u'mugk2r6qf2perahuvn2h7vptgc@group.calendar.google.com', body=event).execute()

print "event: ",created_event['id']

print(service)

## #https://developers.google.com/google-apps/calendar/v3/reference/calendars/insert

## calendar = {
##     'summary': 'physics',
##     'timeZone': 'America/Los_Angeles'
## }

    
## created_calendar = service.calendars().insert(body=calendar).execute()

## print created_calendar['id']

