# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
target="https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=3&dept=ATSC&course=301"
target="https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=ATSC&course=301&section=101"
target="https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=3&dept=PHYS&course=203"
r = requests.get(target)
out=BeautifulSoup(r.text)
times=out.findAll('table')[1].findAll('tr')
headers=times[0].findAll('th')
for count,cell_head in enumerate(headers):
    print(count,cell_head.text.strip())
for rownum,the_row in enumerate(times):
    cells=the_row.findAll('td')
    print("***row {} ***".format(rownum))
    for cellnum,the_cell in enumerate(cells):
        print(cellnum,the_cell.text.strip())

