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
-- Name: w24; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w24 (
    id_w24 bigint DEFAULT nextval('public.w24_id_w24_seq'::regclass) NOT NULL,
    numero_bollettino character varying(30) DEFAULT public.w24_numero_bollettino() NOT NULL,
    data_emissione date DEFAULT ('now'::text)::date NOT NULL,
    next_blt_time date NOT NULL,
    sintesi_meteo text,
    status character(1) DEFAULT 0 NOT NULL,
    last_update timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
    tipo_anomalia_termica character varying(1),
    forzante_0 character(1) NOT NULL,
    forzante_1 character(1) NOT NULL,
    forzante_2 character(1) NOT NULL,
    id_w24_parent integer
);


ALTER TABLE public.w24 OWNER TO weboll;

--
-- Name: w24_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.w24
    ADD CONSTRAINT w24_pkey PRIMARY KEY (id_w24);


--
-- Name: TABLE w24; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

