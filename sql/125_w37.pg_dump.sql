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
-- Name: w37; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w37 (
    id_w37 bigserial NOT NULL,
    numero_bollettino integer NOT NULL,
    data_emissione timestamp with time zone NOT NULL,
    ora_emissione character varying(5) NOT NULL,
    data_aggiornamento date,
    ora_aggiornamento character varying(5),
    situazione_attuale text,
    previsione_meteo text,
    previsione_idro text,
    status character varying(1) NOT NULL,
    last_update timestamp with time zone NOT NULL,
    username character varying(30) NOT NULL,
    mappa_3h bytea NULL,
	mappa_24h bytea NULL,
    primary key (id_w37)
);

CREATE TABLE public.w37_data (
    id_w37_data bigserial NOT NULL,
    comune character varying(30) NOT NULL,
    area character varying(30) NOT NULL,
    sigla_prov character varying(30) NOT NULL,
    pericolo integer,
    pluvio  integer,
    idro integer,
    temporali integer,
    id_w37 bigint NOT NULL,
    primary key (id_w37_data)
);

ALTER TABLE ONLY public.w37_data
    ADD CONSTRAINT w37_data_fkey001 FOREIGN KEY (id_w37) REFERENCES public.w37(id_w37) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w37 ADD id_w37_parent bigint DEFAULT NULL;

\c
\set command `echo "curl $DATA_LOCATION/w37_last_2_days.copy"`
COPY w37 FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
\set command `echo "curl $DATA_LOCATION/w37_data_last_2_days.copy"`
COPY w37_data FROM PROGRAM :'command' CSV HEADER;

CREATE UNIQUE INDEX w37_data_unique ON public.w37_data USING btree (id_w37, comune);
