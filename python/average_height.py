import psycopg2
import osgeo.ogr
connection = psycopg2.connect("host='<localhost>' dbname='<database_name>' user='<postgres_user>' password='<postgres_password>'")
cursor1 = connection.cursor()
cursor1.execute('select count(*) from kn_dem_clip_finer')
for y in cursor1:
    len1 = y[0]
for i in range(len1):
    height=0
    count=0
    cursor1.execute("with x as (select the_geom_st_envelope from kn_dem_clip_finer where rid = (%s+1)) select p.val from kn_dem_clip_finer_pixelascentroid p, x where st_dwithin(x.the_geom_st_envelope, the_geom, 0)", [i])
    for x in cursor1:
        height+=x[0]
        count+=1
    height=height/count
    cursor1.execute("update kn_dem_clip_finer set avg_height = %s where rid = (%s+1)", [height, i]) # We have made a height double precision column for the st_cent_env table already which is empty. Thats why we are using update command rather than insert command.
    print 'row %s done' % (i+1)
    connection.commit()
