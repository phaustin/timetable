from __future__ import print_function, unicode_literals
import dataset
from sqlalchemy import and_, or_, join
from time import sleep

def find_slots():
    db_name='old_and_new_courses.db'
    dbstring='sqlite:///{:s}'.format(db_name)
    db = dataset.connect(dbstring)

    table_name='times'

    time_table=db[table_name]
    columns=time_table.columns

    query=time_table.table.select(and_(time_table.table.c.dept=='PHYS',time_table.table.c.course=='203'))
    phys_courses=db.engine.execute(query)
    slots=[]
    for item in phys_courses:
        slots.append(dict(zip(columns,item)))
    return slots

def make_calendar(slots):

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

    ## #https://developers.google.com/google-apps/calendar/v3/reference/calendars/insert

    calendar = {
        'summary': 'newphysics',
        'timeZone': 'America/Los_Angeles'
    }

    #created_calendar = service.calendars().insert(body=calendar).execute()


    #
    # clear all physics calendars
    #
    while True:
        sleep(0.5)
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary']=='austin.eoas@gmail.com':
                sleep(0.5)
                the_id=calendar_list_entry['id']
                events = service.events().list(calendarId=the_id, pageToken=page_token).execute()
                for row,item in enumerate(events['items']):
                    service.events().delete(calendarId=the_id, eventId=item['id']).execute()
            page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break




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
        sleep(0.5)
        created_event = service.events().insert(calendarId=the_id, body=event).execute()

    #
    # make the calendar public
    #    
    rule = {
        'scope': {
            'type': 'default',
        },
        'role': 'reader'
    }

    created_rule = service.acl().insert(calendarId=the_id, body=rule).execute()

    uri='https://www.google.com/calendar/embed?'

    dates={'2014T2':'20150115/20150116',
           '2014T1':'20140915/20140916',
           '2013T1':'20130915/20130916',
           '2013T2':'20140115/20140116'}

    out=list()
    for the_week in ['2013T1','2013T2','2014T1','2014T2']:
        week_dates=dates[the_week]    
        query= urllib.urlencode({'src':the_id,'ctz':'America/Vancouver','mode':'WEEK','dates':week_dates})
        out.append('<iframe src={uri:s}{query:s}?useformat=mobile width=800 height=650></iframe>'.format(uri=uri,query=query))
    return out


## text="""<ul>
## <li><a href=http://cafc.ubc.ca target="_blank">CAFC</a></li>
## <li><a href=http://cafc.ubc.ca target="_blank">CAFC</a></li>
## <li><a href=http://cafc.ubc.ca target="_blank">CAFC</a></li>
## <li><a href=http://cafc.ubc.ca target="_blank">CAFC</a></li>
## </ul>
## """

## from IPython.display import HTML
## a=HTML(text);a
## HTML('<iframe src=http://en.mobile.wikipedia.org/?useformat=mobile width=700 height=350></iframe>')

if __name__ == "__main__":

    slots=find_slots()
    out=make_calendar(slots)
    print(out)
