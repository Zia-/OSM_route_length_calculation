import psycopg2
import osgeo.ogr
connection = psycopg2.connect("host='<localhost>' dbname='<database_name>' user='<postgres_user>' password='<postgres_password>'")
cursor1 = connection.cursor()
cursor2 = connection.cursor()
cursor1.execute('select count(*) from kn_ways_new')
for i in cursor1:
    count = i[0]
for x in range(count):
    cursor1.execute("select (st_dump(st_intersection(w.the_geom, e.the_geom_st_envelope))).geom as the_geom, z_id from " +
                    "kn_ways_new w, kn_dem_clip_finer e where w.z_id=(%s+1) and " + 
                    "st_dwithin(w.the_geom, e.the_geom_st_envelope, 0)", [x])
    print 'executed %s' % x
    for y in cursor1:
        cursor2.execute('insert into kn_ways_new_split (the_geom, z_id) values (%s, %s)',  [y[0], y[1]])
        print 'inserted %s' % y[1]
connection.commit()
