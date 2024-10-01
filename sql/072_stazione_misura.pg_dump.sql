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
-- Name: stazione_misura; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.stazione_misura (
    codice_istat_comune character varying(6) NOT NULL,
    progr_punto_com integer NOT NULL,
    codice_stazione character varying(6),
    nazione character varying(30),
    indirizzo_localita character varying(80),
    denominazione character varying(80) NOT NULL,
    latitudine_n numeric(10,8),
    longitudine_e numeric(10,8),
    latitudine_mm numeric(8,2),
    longitudine_mm numeric(8,2),
    utm_x integer,
    utm_y integer,
    quota_stazione numeric(6,2),
    quota_sito numeric(6,2),
    cod_staz_meteo character varying(5),
    proprietario character varying(100),
    idtab_allertamento_2 character varying(6),
    data_agg timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    autore_agg character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.stazione_misura OWNER TO weboll;

--
-- Name: TABLE stazione_misura; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON TABLE public.stazione_misura IS 'Contiene i dati delle stazioni di misura';

--
-- Name: stazione_misura_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.stazione_misura
    ADD CONSTRAINT stazione_misura_pkey PRIMARY KEY (codice_istat_comune, progr_punto_com);


--
-- Name: stazione_misura_idx001; Type: INDEX; Schema: public; Owner: weboll; Tablespace: 
--

CREATE INDEX stazione_misura_idx001 ON public.stazione_misura USING btree (codice_istat_comune);


--
-- Name: stazione_misura_idx002; Type: INDEX; Schema: public; Owner: weboll; Tablespace: 
--

CREATE UNIQUE INDEX stazione_misura_idx002 ON public.stazione_misura USING btree (denominazione);


--
-- Name: stazione_misura_idx003; Type: INDEX; Schema: public; Owner: weboll; Tablespace: 
--

CREATE UNIQUE INDEX stazione_misura_idx003 ON public.stazione_misura USING btree (cod_staz_meteo);


--
-- Name: stazione_misura_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.stazione_misura
    ADD CONSTRAINT stazione_misura_fkey001 FOREIGN KEY (codice_istat_comune) REFERENCES public.comune(codice_istat_comune) ON UPDATE CASCADE ON DELETE CASCADE;


\c
\set command `echo "curl $DATA_LOCATION/stazione_misura.copy"`
COPY stazione_misura FROM PROGRAM :'command' CSV HEADER;
