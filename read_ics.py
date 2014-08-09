import icalendar,sys,datetime
import pytz
import dataset
import rfc3339


EPOCH = datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)

def timestamp(dt):
    """
      given datetime object in utc
      return unix timestamp
    """
    dt=dt.astimezone(datetime.timezone.utc)
    return (dt - EPOCH).total_seconds()


#with open('old_and_new.ics','rb') as f:
with open('smallcal.ics','rb') as f:
    cal = icalendar.Calendar.from_ical(f.read())

## with open('smallcal.ics','rb') as f:
##     cal = icalendar.Calendar.from_ical(f.read())
    
    
for k,v in cal.items():
    print(k,v)

def make_dict(event):
    dept,course,section=item['SUMMARY'].split()
    last=rfc3339(item['RRULE']['UNTIL'][0])
    frequency=item['RRULE']['FREQ'][0]
    #format fo ical
    #start=item['DTSTART'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    start=rfc3339(item['DTSTART'].dt)
    start_utc=item['DTSTART'].dt.astimezone(pytz.utc).timestamp()
    end=rfc3339(item['DTEND'].dt)
    end_utc=item['DTEND'].dt.astimezone(pytz.utc).timestamp()
    rrule_text=item['RRULE'].to_ical().decode('utf-8')
    if 'BYDAY' in item['RRULE']:
        days=repr(item['RRULE']['BYDAY'])
    else:
        print('no BYDAY in {}'.format(event['SUMMARY'].to_ical().decode('utf-8')))
        days='NaN'
    out=dict(summary=item['SUMMARY'].to_ical().decode('utf-8'),
             dept=dept,
             course=course,
             section=section,
             location=item['LOCATION'].to_ical().decode('utf-8'),
             category=item['CATEGORIES'].to_ical().decode('utf-8'),
             rrule_text=rrule_text,
             last=last,
             frequency=frequency,
             days=days,
             start=start,
             start_utc=start_utc,
             end=end,
             end_utc=end_utc)
    return out

dbname='old_and_new_courses.db'
dbname='old_and_new_courses.db'
dbname='all_courses.db'
dbstring='sqlite:///{:s}'.format(dbname)
db = dataset.connect(dbstring)

table_name='times'
if table_name in db.tables:
    print("dropping table {}".format(table_name))
    db[table_name].drop()
    db.engine.connect().close()
    db = dataset.connect(dbstring)

the_table = db.create_table(table_name)
             
count=0
the_list=[]
the_cal=icalendar.Calendar
for item in cal.walk():
    count+=1
    if isinstance(item,icalendar.cal.Event):
        try:
            out=make_dict(item)
            the_table.insert(out)
            print(count)
        except Exception as e:
            print("caught exception: ",type(e),e.args,e)
            raise e
    ## if count > 50000:
    ##     break
