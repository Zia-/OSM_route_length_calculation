import psycopg2
import osgeo.ogr
connection = psycopg2.connect("host='localhost' dbname='<database_name>' user='<postgres_user>' password='<postgres_password>'")
cursor1 = connection.cursor()
cursor1.execute('select count(*) from ways_new_split')
for i in cursor1:
    count = i[0]
for x in range(count):
    cursor1.execute('select val, st_distance(st_transform(n.the_geom_st_pt, 3857), st_transform(r.the_geom_st_centroid, 3857))'+
                    'from dem r, ways_new_split n where n_id=(%s+1)'+
                    'order by st_distance(n.the_geom_st_pt, r.the_geom_st_centroid) ASC limit 2', [x])
    numerator=0
    denomenator=0
    for s in cursor1:
        numerator+= (s[0]/(s[1])**1)
        denomenator+= (1/(s[1])**1)
    height_avg = numerator/denomenator
    cursor1.execute('update ways_new_split set height_st_pt = %s where n_id=(%s+1)', [height_avg, x])
    cursor1.execute('select val, st_distance(st_transform(n.the_geom_end_pt, 3857), st_transform(r.the_geom_st_centroid, 3857))'+
                    'from dem r, ways_new_split n where n_id=(%s+1)'+
                    'order by st_distance(n.the_geom_end_pt, r.the_geom_st_centroid) ASC limit 2', [x])
    numerator=0
    denomenator=0
    for s in cursor1:
        numerator+= (s[0]/(s[1])**1)
        denomenator+= (1/(s[1])**1)
    height_avg = numerator/denomenator
    cursor1.execute('update ways_new_split set height_end_pt = %s where n_id=(%s+1)', [height_avg, x])
    print x
connection.commit()
