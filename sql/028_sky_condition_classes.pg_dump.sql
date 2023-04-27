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
-- Name: sky_condition_classes; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.sky_condition_classes (
    id_classes_value smallint NOT NULL,
    id_parametro character varying(15) NOT NULL,
    ordinamento smallint NOT NULL,
    id_sky_condition smallint NOT NULL
);


ALTER TABLE public.sky_condition_classes OWNER TO weboll;

--
-- Data for Name: sky_condition_classes; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.sky_condition_classes (id_classes_value, id_parametro, ordinamento, id_sky_condition) FROM stdin;
1	COP_TOT	1	3
2	COP_TOT	2	22
3	COP_TOT	3	16
4	COP_TOT	4	11
5	COP_TOT	5	2
6	COP_TOT	6	32
7	PLUV	1	8
8	PLUV	2	17
9	PLUV	3	6
10	PLUV	4	25
11	PLUV	5	18
12	SNOW	1	9
13	SNOW	2	21
14	SNOW	3	7
15	SNOW	4	26
16	SNOW	5	44
17	STORM	1	20
18	STORM	2	24
19	STORM	3	23
20	VELV	1	29
21	VELV	2	45
22	VELV	2	46
23	VELV	2	30
24	VELV	3	31
25	VIS_10M	1	5
26	VIS_10M	2	4
\.


--
-- Name: sky_condition_classes_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.sky_condition_classes
    ADD CONSTRAINT sky_condition_classes_pkey PRIMARY KEY (id_classes_value);


--
-- Name: sky_condition_classes_id_parametro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.sky_condition_classes
    ADD CONSTRAINT sky_condition_classes_id_parametro_fkey FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro);


--
-- Name: sky_condition_classes_id_sky_condition_fkey; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.sky_condition_classes
    ADD CONSTRAINT sky_condition_classes_id_sky_condition_fkey FOREIGN KEY (id_sky_condition) REFERENCES public.sky_condition(id_sky_condition);


--
-- Name: TABLE sky_condition_classes; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

