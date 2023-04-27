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
-- Name: w23_zone; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w23_zone (
    id_w23_zone integer NOT NULL,
    zona_allerta character varying(2) NOT NULL,
    bacino character varying(40) NOT NULL,
    provincia character varying(20) NOT NULL,
    nome_zona character varying(8)
);


ALTER TABLE public.w23_zone OWNER TO weboll;

--
-- Data for Name: w23_zone; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w23_zone (id_w23_zone, zona_allerta, bacino, provincia, nome_zona) FROM stdin;
12	VA	Val d Aosta	AO	VdAo-A
1	A	Toce	NO-VB	Piem-A
2	B	Chiusella, Cervo, Val Sesia	BI-NO-TO-VC	Piem-B
3	C	Orco, Lanzo, Sangone	TO	Piem-C
4	D	Susa, Chisone, Pellice	CN-TO	Piem-D
5	E	Varaita, Maira, Stura di Demonte	CN	Piem-E
6	F	Tanaro	CN	Piem-F
7	G	Belbo, Bormida	AL-AT-CN	Piem-G
8	H	Scrivia	AL	Piem-H
9	I	Pianura Settentrionale	AL-AT-BI-NO-TO-VC	Piem-I
10	L	Pianura Torinese, Colline	AL-AT-CN-TO	Piem-L
11	M	Pianura Cuneese	CN-TO	Piem-M
\.


--
-- Name: w23_zone_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w23_zone
    ADD CONSTRAINT w23_zone_pkey PRIMARY KEY (id_w23_zone);


--
-- Name: TABLE w23_zone; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

