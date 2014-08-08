import icalendar,sys

with open('allcourses.ics','rb') as f:
    cal = icalendar.Calendar.from_ical(f.read())

for k,v in cal.items():
    print(k,v)

        
count=0
the_list=[]
with open('smallcal.ics','w') as f:
    the_cal=icalendar.Calendar()
    for item in cal.walk():
        count+=1
        print(count,type(item))
        try:
            print(item['SUMMARY'])
            print(item['DTSTART'].to_ical())
            print(item['DTEND'].to_ical())
            the_list.append(item['SUMMARY'])
            the_cal.add_component(item)
        except:
            pass
        if count > 1000:
            break
    f.write(the_cal.to_ical().decode('utf-8'))
