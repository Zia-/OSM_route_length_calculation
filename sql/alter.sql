alter table dem add column the_geom_st_centroid geometry;
update dem set the_geom_st_centroid = st_centroid(the_geom_st_envelope);
create index the_geom_st_centroid_idx on dem using gist(the_geom_st_centroid);
alter table dem add column val double precision;
update dem set val = x.val from (select val, rid from (select (ST_PixelAsCentroids(rast)).*, rid from dem) as foo) as x where dem.rid = x.rid
--create table dem_pixelascentroid as
--select val, geom as the_geom from (select (ST_PixelAsCentroids(rast)).* from dem) foo;
--create index the_geom_idx on dem_pixelascentroid using gist(the_geom);
--alter table ways_new_split add column avg_height double precision;
alter table ways_new_split add column angle_earth_center double precision;
alter table ways_new_split add column length_w_dem double precision;
alter table ways_new_split add column the_geom_st_pt geometry;
alter table ways_new_split add column the_geom_end_pt geometry;
alter table ways_new_split add column height_st_pt double precision;
alter table ways_new_split add column height_end_pt double precision;
alter table ways_new_split add column n_id bigserial;
alter table ways_new_split add column long_st_pt double precision;
alter table ways_new_split add column lat_st_pt double precision;
alter table ways_new_split add column long_end_pt double precision;
alter table ways_new_split add column lat_end_pt double precision;
update ways_new_split set long_st_pt = (select st_x(the_geom_st_pt));
update ways_new_split set lat_st_pt = (select st_y(the_geom_st_pt));
update ways_new_split set long_end_pt = (select st_x(the_geom_end_pt));
update ways_new_split set lat_end_pt = (select st_y(the_geom_end_pt));
update ways_new_split set the_geom_st_pt = st_startpoint(the_geom);
update ways_new_split set the_geom_end_pt = st_endpoint(the_geom);
create index the_geom_st_pt_idx on ways_new_split using gist(the_geom_st_pt);
create index the_geom_end_pt_idx on ways_new_split using gist(the_geom_end_pt);


