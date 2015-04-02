alter table kn_dem_clip_finer add column the_geom_st_centroid geometry;
update kn_dem_clip_finer set the_geom_st_centroid = st_centroid(the_geom_st_envelope);
create index the_geom_st_centroid_idx on kn_dem_clip_finer using gist(the_geom_st_centroid);
create table kn_dem_clip_finer_pixelascentroid as
select val, geom as the_geom from (select (ST_PixelAsCentroids(rast)).* from kn_dem_clip_finer) foo;
create index the_geom_idx on kn_dem_clip_finer_pixelascentroid using gist(the_geom);
alter table kn_dem_clip_finer add column avg_height double precision;
alter table kn_ways_new_split add column angle_earth_center double precision;
alter table kn_ways_new_split add column length_w_dem double precision;
