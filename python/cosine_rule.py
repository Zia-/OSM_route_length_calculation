import psycopg2
import osgeo.ogr
import math
connection = psycopg2.connect("host='<localhost>' dbname='<database_name>' user='<postgres_user>' password='<postgres_password>'")
cursor1 = connection.cursor()
cursor2 = connection.cursor()
cursor1.execute('select count(*) from kn_ways_new_split')
for i in cursor1:
    count = i[0]
print count
for x in range(count):
    cursor1.execute('select height_st_pt, height_end_pt, angle_earth_center from kn_ways_new_split where n_id=(%s+1)', [x])
    for y in cursor1:
        AB = math.sqrt(abs((6371000+y[0])**2 + (6371000+y[1])**2 - 2*(6371000+y[0])*(6371000+y[1])*(math.cos(y[2]))))
        cursor2.execute('update kn_ways_new_split set length_w_dem = %s where n_id = (%s+1)', [AB, x])
    print 'executed %s again' % (x+1)
connection.commit()
