--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-1.pgdg120+1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: w15; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w15 (
    id_w15 serial NOT NULL,
    seq_num bigint,
    id_w15_parent bigint,
    data_emissione timestamp with time zone NOT NULL,
    status character varying(1) NOT NULL,
    last_update timestamp with time zone NOT NULL,
    username character varying(30) NOT NULL,
    primary key(id_w15)
);

--
-- Name: w15_data; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w15_data (
    id_w15_data serial NOT NULL,
    numeric_value integer,
    id_aggregazione integer NOT NULL,
    id_venue integer,
    id_parametro character varying(15) NOT NULL,
    id_time_layouts integer NOT NULL,
    id_w15 bigint NOT NULL,
    id_trend integer,
    primary key(id_w15_data)
);

ALTER TABLE ONLY public.w15_data
    ADD CONSTRAINT w15_data_unique UNIQUE (id_w15, id_venue, id_time_layouts, id_parametro, id_aggregazione);

ALTER TABLE ONLY public.w15_data
    ADD CONSTRAINT w15_data_id_aggregazione_fk_aggregazi FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE ONLY public.w15_data
    ADD CONSTRAINT w15_data_id_venue_fk_venue FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE ONLY public.w15_data
    ADD CONSTRAINT w15_data_id_parametro_fk_parametro_id_parametro FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE ONLY public.w15_data
    ADD CONSTRAINT w15_data_id_time_layouts_fk_time_layo FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE ONLY public.w15_data
    ADD CONSTRAINT w15_data_id_w15_fk_w15_id_w15 FOREIGN KEY (id_w15) REFERENCES public.w15(id_w15) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;

INSERT INTO public.venue (id_venue, description, altitude, last_update, username) VALUES (157, 'Nichelino', 229.00, '2013-07-04 12:15:00', 'weboll');
INSERT INTO public.venue (id_venue, description, altitude, last_update, username) VALUES (158, 'Candiolo', 237.00, '2013-07-04 12:15:00', 'weboll');
INSERT INTO public.venue (id_venue, description, altitude, last_update, username) VALUES (159, 'Orbassano', 273.00, '2013-07-04 12:15:00', 'weboll');
INSERT INTO public.venue (id_venue, description, altitude, last_update, username) VALUES (165, 'Venaria Reale', 264.00, '2013-07-08 09:15:00', 'weboll');
INSERT INTO public.venue (id_venue, description, altitude, last_update, username) VALUES (166, 'Parco naturale di Stupinigi', NULL, '2013-07-08 09:15:00', 'weboll');
INSERT INTO public.venue (id_venue, description, altitude, last_update, username) VALUES (170, 'Parco naturale La Mandria', NULL, '2013-07-09 09:40:00', 'weboll');

\c
\set command `echo "curl $DATA_LOCATION/w15_last_2_days.copy"`
COPY w15 FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
\set command `echo "curl $DATA_LOCATION/w15_data_last_2_days.copy"`
COPY w15_data FROM PROGRAM :'command' CSV HEADER;