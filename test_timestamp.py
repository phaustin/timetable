from __future__ import print_function, unicode_literals
import site,os
home_dir=os.getenv('HOME')
site.addsitedir('{}/repos/pythonlibs'.format(home_dir))
from pyutils.compat import PY2
from dateutil.parser import parse
import time

import datetime, pytz

from math import floor

def build_rfc3339_phrase(datetime_obj):
    #http://stackoverflow.com/questions/15046170/python-and-rfc-3339-timestamps
    datetime_phrase = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S')

    seconds = datetime_obj.utcoffset().total_seconds()

    if seconds is None:
        datetime_phrase += 'Z'
    else:
        # Append: decimal, 6-digit uS, -/+, hours, minutes
        datetime_phrase += ('%s%02d:%02d' % (
                            ('-' if seconds < 0 else '+'),
                            abs(int(floor(seconds / 3600))),
                            abs(seconds % 3600)
                            ))

    return datetime_phrase


if PY2:
    from rfc3339 import rfc3339

EPOCH = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)

def timestamp(dt):
    """
      given datetime object in utc
      return unix timestamp
    """
    if dt.tzinfo is None:
        raise Exception('need a timezone for this datetime')
    dt=dt.astimezone(pytz.utc)
    return (dt - EPOCH).total_seconds()

vancouver=pytz.timezone('America/Vancouver')
test=datetime.datetime.now()
test_van=vancouver.localize(test)
fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'
if PY2:
    print("raw str: ",test)
    print('no timezone rfc3339',rfc3339(test,utc=True))
    test=test.replace(tzinfo=pytz.utc)
    print("raw str utc",test)
    print('rfc3339 utc',rfc3339(test,utc=True))
    print('timestamp: utc',timestamp(test))
    test=test_van.astimezone(vancouver)
    print("raw str vancouver",test)
    print('alternate format: ',test.strftime(fmt))
    print('rfc3339 vancouver',rfc3339(test,utc=False,use_system_timezone=True))
    reparse=parse(rfc3339(test))
    print('dateutil parser for rfc3339',reparse)
    print("alternate format: ",reparse.strftime(fmt))
    recover=datetime.datetime.utcfromtimestamp(timestamp(test)).replace(tzinfo=pytz.utc)
    print('roundtrip utcfromtimestamp raw str vancouver',recover.astimezone(vancouver))
    print('timestamp vancouver',timestamp(recover.astimezone(vancouver)))
    recover=recover.replace(tzinfo=None)
    print(vancouver.localize(recover))
    print("try the alternative method: ",build_rfc3339_phrase(test))
else:
    print(test_van.strftime(fmt))
    time1=timestamp(test_van)
    time2=test_van.timestamp()
    print('timestamp function',time1)
    print('timestamp module',time2)
    rfc_time=build_rfc3339_phrase(test_van)
    print("new rfc3339: ",rfc_time)
    print("parse rfc: ",parse(rfc_time).strftime(fmt))
    recover=datetime.datetime.utcfromtimestamp(time1)
    print("from utc timestamp: ",recover.strftime(fmt))
    tryit=pytz.utc.localize(recover)
    print("from utc timestamp: ",tryit.strftime(fmt))
    print("from utc timestamp: ",tryit.astimezone(vancouver).strftime(fmt))
    
    
    

