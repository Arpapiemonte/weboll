--
-- PostgreSQL database dump
--

-- Dumped from database version 13.7 (Debian 13.7-1.pgdg110+1)
-- Dumped by pg_dump version 13.7 (Debian 13.7-1.pgdg110+1)

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
-- Name: w31_microaree; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w31_microaree (
    id_w31_microaree integer NOT NULL,
    nome_microarea_forestale character varying(100) NOT NULL,
    ettari_forestali double precision NOT NULL
);


ALTER TABLE public.w31_microaree OWNER TO weboll;

--
-- Data for Name: w31_microaree; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w31_microaree (id_w31_microaree, nome_microarea_forestale, ettari_forestali) FROM stdin;
1	Valli Curone, Grue e Ossona	30970.3
2	Val Borbera e Valle Spinti	37620.3
3	Alta Val Lemme e Alto Ovadese	35755
4	Alta Valle Orba e Valle Erro	42004.6
5	Langa Astigiana-Val Bormida	18959.9
6	VALLI PO, BRONDA E INFERNOTTO	48180.4
7	VALLE VARAITA	48282.7
8	Valle Maira	63278.7
9	Valle Grana	23931.2
10	Valle Stura	60771.2
11	Valli Gesso Vermenagna e Pesio	72792.1
12	Valli Monregalesi	51284.2
13	Alta Valle Tanaro, Valli Mongia e Cevetta, Langa c	67291.4
14	Alta Langa e Langa est	81032.5
15	Valli Antigorio e Formazza	61017.8
16	Valle Vigezzo	21222
17	Valle Antrona	15997.9
18	Valle Anzasca	30165.1
19	Valle Ossola	32260
21	VALLE STRONA, CUSIO, MOTTARONE E ORTA	27645.9
23	Valle Grande - Alto Verbano - Val Cannobina	37108.6
25	Valle Pellice	29447.1
26	Valli Chisone e Germanasca	55864.8
28	Pinerolese Pedemontano - Val Sangone	48284.2
29	Bassa Valle Susa e Val Cenischia	47985.4
30	Alta Valle Susa	64063.5
32	Valli di Lanzo	69640.2
33	Val Ceronda Castern., Alto Can. e Pian. T.se Sett.	75522.2
34	Valli Orco e Soana	61628
36	Valle Sacra-Val Chiusella-Dora Baltea Canavesana	30815.2
38	Val Sesia	76269.8
41	Alta e bassa Valle Cervo, Valle Mosso, Val Sessera	46777.8
44	Alto Novarese	32426.9
45	Alta Valle Elvo - Bassa Valle Elvo	19692.2
51	MONFERRATO ALESSANDRINO	37871.9
52	Pianura Alessandrina settentrionale	87311.3
53	BASSO MONFERRATO ASTIGIANO	71792.3
54	ALTO MONFERRATO ASTIGIANO	60018.6
55	Roero	40657.1
56	PIANURA CUNEESE	132204
57	PIANURA TORINESE MERIDIONALE	91579.8
58	Collina e fascia fluviale del Po	60825
59	Canavese-Serra d' Ivrea	47402.6
60	PIANURA VERCELLESE	130278
61	Pianura biellese	27061.6
62	PIANURA NOVARESE	101496
63	Pianura alessandrina meridionale	84166.5
\.


--
-- Name: w31_microaree w31_microaree_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_microaree
    ADD CONSTRAINT w31_microaree_pkey PRIMARY KEY (id_w31_microaree);


--
-- PostgreSQL database dump complete
--

