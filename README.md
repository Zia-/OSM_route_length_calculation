OSM_route_length_calculation


=================================================================
Work-flow to calculate an almost actual length of OpenStreetMap (OSM) linestrings

This repository contains a set of Python and PostgreSQL codes, comprising a work-flow to calculate the length of OpenStreetMaps roads and other linestring features.


==================================================
Requirements

1- You must have a full PostgreSQL database, with PostGIS and pgRouting extensions, installed on your local system for this to work. PgAdmin3 is required as an administration and development platform for PostgreSQL. A full documentation for complete latest installation can be found at http://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS21UbuntuPGSQL93Apt

2- Install psycopg2, osgeo, proj4, gdal, osm2pgrouting packages. 

3- Digital Elevation Model (DEM) of required resolution, covering the area of interest.


==================================================
Procedure

1- Download the OSM XML data from the OSM website (https://www.openstreetmap.org) OR Copy and paste the following URL into the browser (here xmin, ymin, xmax and ymax are the extents of the area of interest (longitude of bottom left, latitude of bottom left, longitude of top right, latitude of top right), provided in decimal degrees ):

http://overpass.osm.rambler.ru/cgi/xapi_meta?*[bbox=xmin,ymin,xmax,ymax] 
 
2- Make a database with a defined superuser, using pgAdmin3.

3- Run the "extensions.sql" SQL code in pgAdmin3 SQL Editor in order to create the PostGIS and pgRouting extensions for our newly created database.

4- Import the downloaded OSM XML file into our newly created db using "osm2pgrouting" tool from Terminal. Here variables are 'full_path_of_osm_xml_file', 'database_name', 'postgres_user' and 'postgres_password', if one has installed the database under normal setup on a local machine.

osm2pgrouting -file 'full_path_of_osm_xml_file' -conf /usr/share/osm2pgrouting/mapconfig.xml -host localhost -port 5432 -dbname <database_name> -user 'postgres_user' -passwd 'postgres_password' -clean

5- Import DEM raster file using "raster2pgsql" programe from Terminal. Here varaibles are 'full_path_of_DEM_raster_image', 'postgres_user' and 'database_name'. Depending upon the extent and resolution of used DEM, its gonna take a while to create dem table inside the database.

raster2pgsql -I -C -Y -t 1x1 -s 4326 'full_path_of_DEM_raster_image' dem | psql -h localhost -p 5432 -U <postgres_user> -d 'database_name'

6- Create some initial tables which will hold the splitted roads by running "table.sql".

7- Create mesh table of desired resolution and extent using OSM_route_splitting_mesh repository (https://github.com/Zia-/OSM_route_splitting_mesh). 

8- Now split the imported line features from OSM XML data, using mesh table, by running the "split.py" python script. Use the newly created mesh table at line 11 (variable 'mesh_table_name').

9- Run the "alter.sql" SQL code to calculate the centroid points of the used DEM.

XXX10- Python code "average_height.py" will then assign the DEM's height values to the nearest centroid point.

10- Use "junction_height.py" script to calculate the height value of all the splitted line junctions using nearest 2 centroid points.

11- To calculate the angle (in radians), an splitted section is making at Earth's center in order to use in Cosine Formula, use "earth_center_angle.py" Python code.

12- Run the "cosine_rule.py" Python code to calculate the lengths of all the splitted line features.

13- Finally assign all new length values to each OSM linestring by running "add.py" Python code.

14- Delete remaining unnecessary table from the database, except the 'ways_new' one. Run SQL code "delete.sql".

15- Table 'ways_new' contains OSM2pgRouting and newly generated more precise length values for each linestring.




