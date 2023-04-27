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
-- Name: w29_pericolo; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w29_pericolo (
    id_w29_pericolo character varying(2) NOT NULL,
    descrizione text
);


ALTER TABLE public.w29_pericolo OWNER TO weboll;

--
-- Data for Name: w29_pericolo; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w29_pericolo (id_w29_pericolo, descrizione) FROM stdin;
np	Non pervenuto
-	Nulla da segnalare
1	Inneschi di frane superficiali isolati (1-2/km2)
2	Inneschi di frane superficiali poco o moderatamente diffusi (3-10/km2)
3	Inneschi di frane superficiali diffusi o molto diffusi (>10/km2)
\.


--
-- Name: w29_pericolo_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w29_pericolo
    ADD CONSTRAINT w29_pericolo_pkey PRIMARY KEY (id_w29_pericolo);


--
-- Name: TABLE w29_pericolo; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
