import icalendar,sys
import pytz
import dataset

with open('smallcal.ics','rb') as f:
    cal = icalendar.Calendar.from_ical(f.read())

for k,v in cal.items():
    print(k,v)

def make_dict(event):
    dept,course,section=item['SUMMARY'].split()
    last=item['RRULE']['UNTIL'][0].strftime('%Y-%m-%dT%H:%M:%S%z')
    frequency=item['RRULE']['FREQ'][0]
    start=item['DTSTART'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    start_utc=item['DTSTART'].dt.astimezone(pytz.utc).timestamp()
    end=item['DTEND'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    end_utc=item['DTEND'].dt.astimezone(pytz.utc).timestamp()
    out=dict(summary=item['SUMMARY'].to_ical(),
             dept=dept,
             course=course,
             section=section,
             location=item['LOCATION'].to_ical(),
             category=item['CATEGORIES'].to_ical(),
             days=repr(item['RRULE']['BYDAY']),
             last=last,
             frequency=frequency,
             start=start,
             start_utc=start_utc,
             end=end,
             end_utc=end_utc)
    return out

dbname='courses.db'
dbstring='sqlite:///{:s}'.format(dbname)
db = dataset.connect(dbstring)

table_name='times'
if table_name in db.tables:
    print('dropping {}'.format(table_name))
    table_raw=db.metadata.tables[table_name]
    table_raw.drop()
    db.engine.connect().close()
    db = dataset.connect(dbstring)

the_table = db.create_table(table_name)
             
count=0
the_list=[]
the_cal=icalendar.Calendar
for item in cal.walk():
    count+=1
    try:
        out=make_dict(item)
        the_table.insert(out)
        print(out)
    except Exception as e:
        print(e)
        pass
    if count > 50000:
        break
