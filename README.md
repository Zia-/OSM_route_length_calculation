OSM_route_length_calculation


=================================================================
Work-flow to calculate an almost actual length of OSM linestrings

This repository contains a set of Python and PostgreSQL codes, comprising a work-flow, to calculate the length of OpenStreetMaps roads and other line features.


==================================================
Requirements

1- You must have a full PostgreSQL with PostGIS and pgRouting extensions installed for this to work. PgAdmin3 is required as an administration and development platform for PostgreSQL. A full documentation for complete installation can be found at http://trac.osgeo.org. 

2- Install psycopg2, osgeo, proj4, gdal, osm2pgrouting packages. 

3- Digital Elevation Model (DEM) of certain resolution one is desiring to use, covering the area of interest.


==================================================
Procedure

1- Download the OSM XML data from the OSM website. Copy and paste the following URL into the browser (here xmin, ymin, xmax and ymax are the extents of the area of interest, provided in decimal degrees ):

http://overpass.osm.rambler.ru/cgi/xapi_meta?*[bbox=xmin,ymin,xmax,ymax] 
 
2- Make a database with a defined superuser, using pgAdmin3.

3- Run the "extensions.sql" SQL code in pgAdmin3 SQL Editor in order to create the PostGIS and pgRouting extensions for our newly created database.

4- Import the OSM file into our newly created db using the "osm2pgrouting" command from Terminal:

osm2pgrouting -file <full_path_of_osm_xml_file> -conf /usr/share/osm2pgrouting/mapconfig.xml -host <localhost> -port 5432 -dbname <database_name> -user <postgres_user> -passwd <postgres_password> -prefixtables kn_ -clean

5- Import DEM raster file using "raster2pgsql" programe from Terminal:

raster2pgsql -I -C -Y -t 1x1 -s 4326 <full_path_of_DEM_raster_image> kn_dem_clip_finer | psql -h <localhost> -p 5432 -U <postgres_user> -d <database_name>

6- Create some initial tables which will hold the splitted roads by running "table.sql".

7- Now split the imported line features from OSM XML data, using mesh table, by running the "split.py" python script.

8- Run the "alter.sql" SQL code to calculate the centroid points of the mesh used.

9- Python code "average_height.py" will then assign the DEM's height values to the nearest centroid point.

10- Use "junction_height.py" script to calculate the height value of all the splitted line junctions using nearest 2 centroid points.

11- To calculate the angle (in radians) an splitted section is making at Earth's center, in order to use in Cosine Formula, use "earth_center_angle.py" Python code.

12- Finally run the "cosine_rule.py" Python code to calculate the lengths of all the splitted line features.






