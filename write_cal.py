from __future__ import print_function, unicode_literals
import dataset
from sqlalchemy import and_, or_, join

db_name='old_and_new_courses.db'
dbstring='sqlite:///{:s}'.format(db_name)
db = dataset.connect(dbstring)

print(db.tables)
table_name='times'

time_table=db[table_name]
columns=time_table.columns

query=time_table.table.select(time_table.table.c.id=='300')
print(dict(zip(columns,db.engine.execute(query).first())))

query=time_table.table.select(and_(time_table.table.c.dept=='PHYS',time_table.table.c.course=='203'))
print(query)
phys_courses=db.engine.execute(query)
slots=[]
for item in phys_courses:
    slots.append(dict(zip(columns,item)))
    
print(slots)

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


for course in slots:
    event=defaultdict(dict)
    event['summary']=course['summary']
    event['location']=course['location']
    event['start'] = dict(dateTime=course['start'],
                         timeZone='America/Los_Angeles')
    event['end'] = dict(dateTime=course['end'],
                       timeZone= 'America/Los_Angeles')
    event["recurrence"]= ["RRULE:{}".format(course['rrule_text']),]
    created_event = service.events().insert(calendarId=the_id, body=event).execute()

rule = {
    'scope': {
        'type': 'default',
    },
    'role': 'reader'
}

created_rule = service.acl().insert(calendarId=the_id, body=rule).execute()

uri='https://www.google.com/calendar/embed?'
dates='20150115/20150116'
query= urllib.urlencode({'src':the_id,'ctz':'America/Vancouver','mode':'WEEK','dates':dates})

print('to view: click on: ',uri + query)

## ## print created_rule['id']

## ## print "event: ",created_event['id']

## ## print(service)


