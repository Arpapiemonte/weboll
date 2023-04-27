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

--SET default_with_oids = true;

--
-- Name: w29_probabilita; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w29_probabilita (
    id_w29_probabilita character varying(12) NOT NULL,
    descrizione text
);


ALTER TABLE public.w29_probabilita OWNER TO weboll;

--
-- Data for Name: w29_probabilita; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w29_probabilita (id_w29_probabilita, descrizione) FROM stdin;
bassa	Raggiungimento e superamento del 10% del valore soglia
media	Superamento del valore soglia dall'11% al 30%
alta	Superamento del valore soglia dall'31% al 50%
molto alta	Superamento del valore soglia maggiore del 50%
nessuna	Nessun superamento del 10% del valore soglia
\.


--
-- Name: w29_probabilita_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w29_probabilita
    ADD CONSTRAINT w29_probabilita_pkey PRIMARY KEY (id_w29_probabilita);


--
-- Name: TABLE w29_probabilita; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
