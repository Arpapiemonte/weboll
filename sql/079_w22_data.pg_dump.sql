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

--
-- Name: w22_data; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w22_data (
    id_w22 bigint NOT NULL,
    id_w22_zone integer NOT NULL,
    codice1 character varying(10),
    codice2 character varying(10),
    codice3 character varying(10),
    tendenza6hprecedenti character varying(15),
    portata_attesa character varying(15),
    criticita_attesa character varying(15),
    prev_crit12h character varying(15),
    prev_crit24h character varying(15),
    prev_crit36h character varying(15),
    tend48h character varying(15),
    massimo_previsione character varying(15),
    data_massimo_storico character varying(15),
    valore_massimo_storico character varying(15),
    id_w22_data BIGSERIAL
);

ALTER TABLE public.w22_data                                       
ADD CONSTRAINT w22_data_fkey003 
FOREIGN KEY (tendenza6hprecedenti) 
REFERENCES public.w22_tendenza (descrizione) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey004 
FOREIGN KEY (tend48h) 
REFERENCES public.w22_tendenza (descrizione) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey005 
FOREIGN KEY (criticita_attesa) 
REFERENCES public.w22_criticita (id_w22_criticita) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey006
FOREIGN KEY (prev_crit12h) 
REFERENCES public.w22_criticita (id_w22_criticita) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey007
FOREIGN KEY (prev_crit24h) 
REFERENCES public.w22_criticita (id_w22_criticita) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey008
FOREIGN KEY (prev_crit36h) 
REFERENCES public.w22_criticita (id_w22_criticita) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey009
FOREIGN KEY (massimo_previsione) 
REFERENCES public.w22_criticita (id_w22_criticita) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE public.w22_data OWNER TO weboll;

ALTER TABLE ONLY public.w22_data
    ADD CONSTRAINT w22_data_pkey PRIMARY KEY (id_w22_data);


ALTER TABLE ONLY public.w22_data
    ADD CONSTRAINT w22_data_fkey001 FOREIGN KEY (id_w22) REFERENCES public.w22(id_w22) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE ONLY public.w22_data
    ADD CONSTRAINT w22_data_fkey002 FOREIGN KEY (id_w22_zone) REFERENCES public.w22_zone(id_w22_zone) ON UPDATE CASCADE ON DELETE CASCADE;

\c
\set command `echo "curl $DATA_LOCATION/w22.copy"`
COPY w22 FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
\set command `echo "curl $DATA_LOCATION/w22_data.copy"`
COPY w22_data FROM PROGRAM :'command' CSV HEADER;

SELECT setval('public.w22_id_w22_seq', max(id_w22)) FROM public.w22;
SELECT setval('public.w22_data_id_w22_data_seq', max(id_w22_data)) FROM public.w22_data;