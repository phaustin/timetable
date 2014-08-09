from __future__ import print_function, unicode_literals
from oauth2client.client import Credentials
from apiclient.discovery import build
import urllib

import httplib2

def __create_service():
    with open('credentials', 'rw') as f:
        credentials = Credentials.new_from_json(f.read())

    http = httplib2.Http()
    http = credentials.authorize(http)

    return build('calendar', 'v3', http=http)

service = __create_service()

#
# first clear all calendars
#

page_token = None

#
# clear all physics calendars
#
while True:
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
        if calendar_list_entry['summary']=='physics':
            print(calendar_list_entry['summary'])
            print(calendar_list_entry['id'])
            print('found physics will delete')
            service.calendars().delete(calendarId=calendar_list_entry['id']).execute()
        page_token = calendar_list.get('nextPageToken')
    if not page_token:
        break


## #https://developers.google.com/google-apps/calendar/v3/reference/calendars/insert

calendar = {
    'summary': 'physics',
    'timeZone': 'America/Los_Angeles'
}
    
created_calendar = service.calendars().insert(body=calendar).execute()

the_id=created_calendar['id']


from collections import defaultdict

event=defaultdict(dict)

event['summary']='Appointment'
event['location']='Somewhere'
event['start'] = dict(dateTime='2014-09-03T10:00:00-07:00',
                     timeZone='America/Los_Angeles')
event['end'] = dict(dateTime='2014-09-03T10:25:00-07:00',
                   timeZone= 'America/Los_Angeles')

event["recurrence"]= ["RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20150410T230000Z",]

    
created_event = service.events().insert(calendarId=the_id, body=event).execute()

rule = {
    'scope': {
        'type': 'default',
    },
    'role': 'reader'
}

created_rule = service.acl().insert(calendarId=the_id, body=rule).execute()

uri='https://www.google.com/calendar/embed?'
query= urllib.urlencode({'src':the_id,'ctz':'America/Vancouver'})

print('to view: click on: ',uri + query)

## ## print created_rule['id']

## ## print "event: ",created_event['id']

## ## print(service)


