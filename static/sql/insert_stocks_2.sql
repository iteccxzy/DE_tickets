-- PROCEDURE: public.insert_stock_2(integer, integer, integer)

-- DROP PROCEDURE public.insert_stock_2(integer, integer, integer);

CREATE OR REPLACE PROCEDURE public.insert_stock_2(
	office integer,
	plan integer,
	cantidad integer)
LANGUAGE 'sql'
AS $BODY$
INSERT INTO public.entry_stocks(
	st_date, st_time, office_id, plan_id, qt)  

	  select now() + interval '1 day', 
	  to_char(generate_series(9, 16) * interval '1 hour' + '2020-01-01 00:00:00'::timestamp, 'HH24:MI')::time,
	 office, 
	 plan, 
	 cantidad
	 where (select extract(dow from now() + interval '1 day')<> 0);
	 INSERT INTO public.entry_stocks(
	st_date, st_time, office_id, plan_id, qt)  

	  select now() + interval '2 day', 
	  to_char(generate_series(9, 16) * interval '1 hour' + '2020-01-01 00:00:00'::timestamp, 'HH24:MI')::time,
	 office, 
	 plan, 
	 cantidad
	 where (select extract(dow from now() + interval '2 day')<> 0);
	 INSERT INTO public.entry_stocks(
	st_date, st_time, office_id, plan_id, qt)  

	  select now() + interval '3 day', 
	  to_char(generate_series(9, 16) * interval '1 hour' + '2020-01-01 00:00:00'::timestamp, 'HH24:MI')::time,
	 office, 
	 plan, 
	 cantidad
	 where (select extract(dow from now() + interval '3 day')<> 0);
	 INSERT INTO public.entry_stocks(
	st_date, st_time, office_id, plan_id, qt)  

	  select now() + interval '4 day', 
	  to_char(generate_series(9, 16) * interval '1 hour' + '2020-01-01 00:00:00'::timestamp, 'HH24:MI')::time,
	 office, 
	 plan, 
	 cantidad
	 where (select extract(dow from now() + interval '4 day')<> 0);
	 INSERT INTO public.entry_stocks(
	st_date, st_time, office_id, plan_id, qt)  

	  select now() + interval '5 day', 
	  to_char(generate_series(9, 16) * interval '1 hour' + '2020-01-01 00:00:00'::timestamp, 'HH24:MI')::time,
	 office, 
	 plan, 
	 cantidad
	 where (select extract(dow from now() + interval '5 day')<> 0);
	 INSERT INTO public.entry_stocks(
	st_date, st_time, office_id, plan_id, qt)  

	  select now() + interval '6 day', 
	  to_char(generate_series(9, 16) * interval '1 hour' + '2020-01-01 00:00:00'::timestamp, 'HH24:MI')::time,
	 office, 
	 plan, 
	 cantidad
	 where (select extract(dow from now() + interval '6 day')<> 0);
	 INSERT INTO public.entry_stocks(
	st_date, st_time, office_id, plan_id, qt)  

	  select now() + interval '7 day', 
	  to_char(generate_series(9, 16) * interval '1 hour' + '2020-01-01 00:00:00'::timestamp, 'HH24:MI')::time,
	 office, 
	 plan, 
	 cantidad
	 where (select extract(dow from now() + interval '7 day')<> 0);
$BODY$;
