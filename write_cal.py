import dataset
from sqlalchemy import and_, or_, join

db_name='old_and_new_courses.db'
dbstring='sqlite:///{:s}'.format(db_name)
db = dataset.connect(dbstring)

print db.tables
table_name='times'

time_table=db[table_name]
columns=time_table.columns

query=time_table.table.select(time_table.table.c.id=='300')
print dict(zip(columns,db.engine.execute(query).first()))

query=time_table.table.select(and_(time_table.table.c.dept=='PHYS',time_table.table.c.course=='203'))
print query
phys_courses=db.engine.execute(query)
slots=[]
for item in phys_courses:
    slots.append(dict(zip(columns,item)))
    

