import psycopg2
import osgeo.ogr
connection = psycopg2.connect("host='localhost' dbname='<database_name>' user='<postgres_user>' password='<postgres_password>'")
cursor1 = connection.cursor()
cursor2 = connection.cursor()
cursor1.execute('select count(*) from ways_new')
for i in cursor1:
    count = i[0]
for x in range(count):
    cursor1.execute("select length_w_dem from ways_new_split where z_id = (%s+1)", [x])
    length = 0
    for y in cursor1:
	length+=y[0]
    cursor2.execute('update ways_new set length_new = %s where z_id = (%s+1)',  [length, x])
    print 'executed %s' % x
connection.commit()
