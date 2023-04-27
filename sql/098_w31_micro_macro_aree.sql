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
-- Name: w31_micro_macro_aree; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w31_micro_macro_aree (
    id_w31_micro_macro_aree integer NOT NULL,
    id_w31_macroaree integer NOT NULL,
    id_w31_microaree integer NOT NULL
);


ALTER TABLE public.w31_micro_macro_aree OWNER TO weboll;

--
-- Name: w31_micro_macro_aree_id_w31_micro_macro_aree_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w31_micro_macro_aree_id_w31_micro_macro_aree_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w31_micro_macro_aree_id_w31_micro_macro_aree_seq OWNER TO weboll;

--
-- Name: w31_micro_macro_aree_id_w31_micro_macro_aree_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w31_micro_macro_aree_id_w31_micro_macro_aree_seq OWNED BY public.w31_micro_macro_aree.id_w31_micro_macro_aree;


--
-- Name: w31_micro_macro_aree id_w31_micro_macro_aree; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_micro_macro_aree ALTER COLUMN id_w31_micro_macro_aree SET DEFAULT nextval('public.w31_micro_macro_aree_id_w31_micro_macro_aree_seq'::regclass);


--
-- Data for Name: w31_micro_macro_aree; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w31_micro_macro_aree (id_w31_micro_macro_aree, id_w31_macroaree, id_w31_microaree) FROM stdin;
1	5	1
2	5	2
3	5	3
4	5	4
5	5	5
6	1	6
7	1	7
8	1	8
9	1	9
10	1	10
11	6	11
12	6	12
13	6	13
14	6	14
15	2	15
16	2	16
17	2	17
18	2	18
19	2	19
20	2	21
21	2	23
22	4	25
23	4	26
24	4	28
25	4	29
26	4	30
27	3	32
28	3	33
29	3	34
30	3	36
31	2	38
32	2	41
33	2	44
34	2	45
35	5	51
36	5	52
37	5	53
38	5	54
39	6	55
40	1	56
41	4	57
42	3	58
43	3	59
44	2	60
45	2	61
46	2	62
47	5	63
\.


--
-- Name: w31_micro_macro_aree_id_w31_micro_macro_aree_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w31_micro_macro_aree_id_w31_micro_macro_aree_seq', 47, true);


--
-- Name: w31_micro_macro_aree w31_micro_macro_aree_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_micro_macro_aree
    ADD CONSTRAINT w31_micro_macro_aree_pkey PRIMARY KEY (id_w31_micro_macro_aree);


--
-- Name: w31_micro_macro_aree_id_w31_macroaree_8bead4e9; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_micro_macro_aree_id_w31_macroaree_8bead4e9 ON public.w31_micro_macro_aree USING btree (id_w31_macroaree);


--
-- Name: w31_micro_macro_aree_id_w31_microaree_2ffe2557; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_micro_macro_aree_id_w31_microaree_2ffe2557 ON public.w31_micro_macro_aree USING btree (id_w31_microaree);


--
-- Name: w31_micro_macro_aree w31_micro_macro_aree_id_w31_macroaree_8bead4e9_fk_w31_macro; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_micro_macro_aree
    ADD CONSTRAINT w31_micro_macro_aree_id_w31_macroaree_8bead4e9_fk_w31_macro FOREIGN KEY (id_w31_macroaree) REFERENCES public.w31_macroaree(id_w31_macroaree) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: w31_micro_macro_aree w31_micro_macro_aree_id_w31_microaree_2ffe2557_fk_w31_micro; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_micro_macro_aree
    ADD CONSTRAINT w31_micro_macro_aree_id_w31_microaree_2ffe2557_fk_w31_micro FOREIGN KEY (id_w31_microaree) REFERENCES public.w31_microaree(id_w31_microaree) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

