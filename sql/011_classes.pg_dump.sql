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
-- Name: classes; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.classes (
    id_classes smallint DEFAULT nextval('public.classes_id_classes_seq'::regclass) NOT NULL,
    id_parametro character varying(10) NOT NULL,
    description character varying(50),
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
    version bigint
);


ALTER TABLE public.classes OWNER TO weboll;

--
-- Data for Name: classes; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.classes (id_classes, id_parametro, description, last_update, username, version) FROM stdin;
1	COP_TOT	Classe di Appartenenza	2010-03-23 09:00:00	weboll	\N
2	COP_TOT	Evoluzione	2010-03-23 09:00:00	weboll	\N
3	COP_TOT	Localizzazione	2010-03-23 09:00:00	weboll	\N
4	COP_TOT	Visibilita	2010-03-23 09:00:00	weboll	\N
5	PLUV	Classe di Appartenenza su Area vasta	2010-03-23 09:00:00	weboll	\N
6	PLUV	Classe di Appartenenza su Area ridotta	2010-03-23 09:00:00	weboll	\N
7	PLUV	Classe di Appartenenza del valore massimo	2010-03-23 09:00:00	weboll	\N
9	TERMA	Valore di riferimento min	2010-03-23 09:00:00	weboll	\N
10	TERMA	Valore di riferimento max	2010-03-23 09:00:00	weboll	\N
11	FRZLVL	Valore dalle 00 alle 12	2010-03-23 09:00:00	weboll	\N
12	FRZLVL	Valore dalle 12 alle 24	2010-03-23 09:00:00	weboll	\N
13	FRZLVL	Valore dalle 00 alle 24	2010-03-23 09:00:00	weboll	\N
14	SNOW_LEV	Valore di riferimento min	2010-03-23 09:00:00	weboll	\N
15	SNOW_LEV	Valore di riferimento max	2010-03-23 09:00:00	weboll	\N
16	VELV	Intensita in pianura	2010-03-23 09:00:00	weboll	\N
17	VELV	Andamento in pianura	2010-03-23 09:00:00	weboll	\N
18	VELV	Intensita in montagna	2010-03-23 09:00:00	weboll	\N
19	VELV	Andamento in montagna	2010-03-23 09:00:00	weboll	\N
20	VELV	Rinforzi	2010-03-23 09:00:00	weboll	\N
21	VELV	Foehn	2010-03-23 09:00:00	weboll	\N
8	PLUV	Evoluzione	2010-03-23 09:00:00	weboll	\N
\.


--
-- Name: classes_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.classes
    ADD CONSTRAINT classes_pkey PRIMARY KEY (id_classes);


--
-- Name: classes_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.classes
    ADD CONSTRAINT classes_fkey001 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON UPDATE CASCADE;


--
-- Name: TABLE classes; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

