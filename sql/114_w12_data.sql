--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: w12_data; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w12_data (
    id_w12 bigint NOT NULL,
    id_venue integer NOT NULL,
    id_time_layouts integer NOT NULL,
    sky_condition smallint,
    cloud_amount smallint,
    precipitation_class smallint,
    cumulated_snow integer,
    freezing_level integer,
    snow_level integer,
    temperature_below_zero boolean,
    risk_freezing_rain boolean,
    vis_inf_1000 boolean,
    vis_inf_1000_reason smallint,
    wind_class smallint
);


ALTER TABLE public.w12_data OWNER TO weboll;

--
-- Data for Name: w12_data; Type: TABLE DATA; Schema: public; Owner: weboll
--


--
-- Name: w12_data_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w12_data
    ADD CONSTRAINT w12_data_fkey001 FOREIGN KEY (id_w12) REFERENCES public.w12(id_w12) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w12_data_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w12_data
    ADD CONSTRAINT w12_data_fkey002 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w12_data_fkey003; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w12_data
    ADD CONSTRAINT w12_data_fkey003 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON UPDATE CASCADE ON DELETE CASCADE;



ALTER TABLE ONLY public.w12_data ADD COLUMN id_w12_data SERIAL PRIMARY KEY;


\set command `echo "curl $DATA_LOCATION/w12_data.copy"`
COPY public.w12_data
  FROM PROGRAM :'command' CSV HEADER;

SELECT setval('public.w12_id_w12_seq', max(id_w12)) FROM public.w12;
SELECT setval('public.w12_data_id_w12_data_seq', max(id_w12_data)) FROM public.w12_data;