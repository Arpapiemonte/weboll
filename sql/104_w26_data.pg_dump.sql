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

CREATE TABLE public.w26_data (
    id_w26 bigint NOT NULL,
    id_w26_zone bigint NOT NULL,
    --localita character varying(100) NOT NULL,
    --corsoacqua character varying(100) NOT NULL,
    hmin character varying(8),
    hmax character varying(8),
    hmed character varying(8),
    qmin character varying(8),
    qmax character varying(8),
    qmed character varying(8),
    nota character varying(2000),
    idnota character varying(70)
    --numero integer NOT NULL
);


ALTER TABLE public.w26_data ADD COLUMN id_w26_data BIGSERIAL PRIMARY KEY;
ALTER TABLE public.w26_data OWNER TO weboll;

--COPY public.w26_data (id_w26, localita, corsoacqua, hmin, hmax, hmed, qmin, qmax, qmed, nota, idnota, numero) FROM stdin;
COPY public.w26_data (id_w26, id_w26_zone, hmin, hmax, hmed, qmin, qmax, qmed, nota, idnota) FROM stdin;
2736	2	0.83	0.86	0.84	0.1	1.2	0.5	\N	
2736	8	0.06	0.10	0.08	3.1	5.3	4.4	\N	
2736	14	1.04	1.07	1.05	21.5	24.9	22.9	\N	
2736	20	-0.08	0.11	0.01	18.9	31.5	24.7	\N	
2736	26	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(6)
2736	32	-0.02	0.08	0.05	2.1	3.9	3.4	\N	
2736	38	-0.11	-0.08	-0.09	0.4	0.6	0.5	\N	
2736	44	-1.24	-1.17	-1.19	7.9	12.1	10.7	\N	
2736	50	0.17	0.19	0.18	134.0	139.0	137.0	\N	
2736	3	0.02	0.04	0.03	0.3	0.4	0.4	\N	
2736	9	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(6)
2736	15	0.70	0.72	0.71	0.7	0.9	0.8	\N	
2736	21	0.40	0.42	0.42	0.8	0.9	0.9	\N	
2736	27	0.27	0.31	0.30	0.1	0.1	0.1	\N	
2736	33	0.84	0.87	0.85	0.8	1.2	0.9	\N	
2736	39	0.73	0.74	0.74	0.8	0.9	0.9	\N	
2736	45	0.29	0.33	0.31	7.1	9.3	8.2	\N	
2736	4	-0.10	-0.07	-0.08	0.2	0.3	0.2	\N	
2736	10	-1.01	-0.80	-0.97	3.3	4.9	3.4	\N	
2736	16	0.04	0.07	0.05	0.8	1.3	1.0	\N	
2736	22	-0.53	-0.49	-0.51	1.0	1.4	1.2	\N	
2736	28	0.59	0.61	0.60	1.5	1.8	1.7	\N	
2736	34	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(6)
2736	40	0.54	0.56	0.55	0.8	1.0	0.9	\N	
2736	46	-0.05	0.27	0.10	3.7	33.3	16.0	\N	
2736	5	0.22	0.28	0.24	3.7	4.8	4.1	\N	
2736	11	0.52	0.54	0.53	2.0	2.4	2.3	\N	
2736	17	-0.45	-0.42	-0.43	7.3	8.5	8.1	\N	
2736	23	0.13	0.15	0.14	-999.9	-999.9	-999.9	\N	(2)
2736	29	0.50	0.52	0.51	1.0	1.2	1.1	\N	
2736	35	-1.33	-1.25	-1.31	18.2	23.8	19.4	\N	
2736	41	0.42	0.47	0.44	0.5	0.8	0.6	\N	
2736	47	0.95	1.07	0.99	23.5	38.7	27.7	\N	
2736	6	1.14	1.38	1.22	5.6	17.7	9.0	\N	
2736	12	-0.21	-0.17	-0.18	0.1	0.5	0.4	\N	
2736	18	0.50	0.59	0.53	6.1	6.2	6.2	\N	
2736	24	0.13	0.33	0.22	1.1	5.1	2.3	\N	
2736	30	-0.16	0.05	-0.10	2.8	7.5	4.1	\N	
2736	36	0.51	0.53	0.52	22.6	25.3	24.4	\N	
2736	42	-0.31	-0.25	-0.27	1.2	1.2	1.2	\N	
2736	48	-2.00	-1.97	-1.99	47.0	57.0	53.0	\N	
2736	1	-0.63	-0.59	-0.61	2.6	3.4	3.0	\N	
2736	7	-0.27	-0.23	-0.25	4.4	5.3	4.8	\N	
2736	13	0.51	0.68	0.58	15.4	33.5	22.0	\N	
2736	19	1.92	1.94	1.93	16.0	16.8	16.5	\N	
2736	25	0.03	0.05	0.05	0.7	0.8	0.8	\N	
2736	31	0.04	0.16	0.10	2.9	5.4	4.1	\N	
2736	37	-0.53	-0.50	-0.51	36.1	39.3	37.7	\N	
2736	43	0.75	0.77	0.76	8.8	11.1	10.4	\N	
2736	49	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(2)
2737	2	0.83	0.86	0.84	0.1	1.2	0.5	\N	
2737	8	0.06	0.10	0.08	3.1	5.3	4.4	\N	
2737	14	1.04	1.07	1.05	21.5	24.9	22.9	\N	
2737	20	-0.08	0.11	0.01	18.9	31.5	24.7	\N	
2737	26	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(6)
2737	32	-0.02	0.08	0.05	2.1	3.9	3.4	\N	
2737	38	-0.11	-0.08	-0.09	0.4	0.6	0.5	\N	
2737	44	-1.24	-1.17	-1.19	7.9	12.1	10.7	\N	
2737	50	0.17	0.19	0.18	134.0	139.0	137.0	\N	
2737	3	0.02	0.04	0.03	0.3	0.4	0.4	\N	
2737	9	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(6)
2737	15	0.70	0.72	0.71	0.7	0.9	0.8	\N	
2737	21	0.40	0.42	0.42	0.8	0.9	0.9	\N	
2737	27	0.27	0.31	0.30	0.1	0.1	0.1	\N	
2737	33	0.84	0.87	0.85	0.8	1.2	0.9	\N	
2737	39	0.73	0.74	0.74	0.8	0.9	0.9	\N	
2737	45	0.29	0.33	0.31	7.1	9.3	8.2	\N	
2737	4	-0.10	-0.07	-0.08	0.2	0.3	0.2	\N	
2737	10	-1.01	-0.80	-0.97	3.3	4.9	3.4	\N	
2737	16	0.04	0.07	0.05	0.8	1.3	1.0	\N	
2737	22	-0.53	-0.49	-0.51	1.0	1.4	1.2	\N	
2737	28	0.59	0.61	0.60	1.5	1.8	1.7	\N	
2737	34	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(6)
2737	40	0.54	0.56	0.55	0.8	1.0	0.9	\N	
2737	46	-0.05	0.27	0.10	3.7	33.3	16.0	\N	
2737	5	0.22	0.28	0.24	3.7	4.8	4.1	\N	
2737	11	0.52	0.54	0.53	2.0	2.4	2.3	\N	
2737	17	-0.45	-0.42	-0.43	7.3	8.5	8.1	\N	
2737	23	0.13	0.15	0.14	-999.9	-999.9	-999.9	\N	(2)
2737	29	0.50	0.52	0.51	1.0	1.2	1.1	\N	
2737	35	-1.33	-1.25	-1.31	18.2	23.8	19.4	\N	
2737	41	0.42	0.47	0.44	0.5	0.8	0.6	\N	
2737	47	0.95	1.07	0.99	23.5	38.7	27.7	\N	
2737	6	1.14	1.38	1.22	5.6	17.7	9.0	\N	
2737	12	-0.21	-0.17	-0.18	0.1	0.5	0.4	\N	
2737	18	0.50	0.59	0.53	6.1	6.2	6.2	\N	
2737	24	0.13	0.33	0.22	1.1	5.1	2.3	\N	
2737	30	-0.16	0.05	-0.10	2.8	7.5	4.1	\N	
2737	36	0.51	0.53	0.52	22.6	25.3	24.4	\N	
2737	42	-0.31	-0.25	-0.27	1.2	1.2	1.2	\N	
2737	48	-2.00	-1.97	-1.99	47.0	57.0	53.0	\N	
2737	1	-0.63	-0.59	-0.61	2.6	3.4	3.0	\N	
2737	7	-0.27	-0.23	-0.25	4.4	5.3	4.8	\N	
2737	13	0.51	0.68	0.58	15.4	33.5	22.0	\N	
2737	19	1.92	1.94	1.93	16.0	16.8	16.5	\N	
2737	25	0.03	0.05	0.05	0.7	0.8	0.8	\N	
2737	31	0.04	0.16	0.10	2.9	5.4	4.1	\N	
2737	37	-0.53	-0.50	-0.51	36.1	39.3	37.7	\N	
2737	43	0.75	0.77	0.76	8.8	11.1	10.4	\N	
2737	49	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(2)
2738	2	0.83	0.86	0.84	0.1	1.2	0.5	\N	
2738	8	0.06	0.10	0.08	3.1	5.3	4.4	\N	
2738	14	1.04	1.07	1.05	21.5	24.9	22.9	\N	
2738	20	-0.08	0.11	0.01	18.9	31.5	24.7	\N	
2738	26	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(6)
2738	32	-0.02	0.08	0.05	2.1	3.9	3.4	\N	
2738	38	-0.11	-0.08	-0.09	0.4	0.6	0.5	\N	
2738	44	-1.24	-1.17	-1.19	7.9	12.1	10.7	\N	
2738	50	0.17	0.19	0.18	134.0	139.0	137.0	\N	
2738	3	0.02	0.04	0.03	0.3	0.4	0.4	\N	
2738	9	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(6)
2738	15	0.70	0.72	0.71	0.7	0.9	0.8	\N	
2738	21	0.40	0.42	0.42	0.8	0.9	0.9	\N	
2738	27	0.27	0.31	0.30	0.1	0.1	0.1	\N	
2738	33	0.84	0.87	0.85	0.8	1.2	0.9	\N	
2738	39	0.73	0.74	0.74	0.8	0.9	0.9	\N	
2738	45	0.29	0.33	0.31	7.1	9.3	8.2	\N	
2738	4	-0.10	-0.07	-0.08	0.2	0.3	0.2	\N	
2738	10	-1.01	-0.80	-0.97	3.3	4.9	3.4	\N	
2738	16	0.04	0.07	0.05	0.8	1.3	1.0	\N	
2738	22	-0.53	-0.49	-0.51	1.0	1.4	1.2	\N	
2738	28	0.59	0.61	0.60	1.5	1.8	1.7	\N	
2738	34	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(6)
2738	40	0.54	0.56	0.55	0.8	1.0	0.9	\N	
2738	46	-0.05	0.27	0.10	3.7	33.3	16.0	\N	
2738	5	0.22	0.28	0.24	3.7	4.8	4.1	\N	
2738	11	0.52	0.54	0.53	2.0	2.4	2.3	\N	
2738	17	-0.45	-0.42	-0.43	7.3	8.5	8.1	\N	
2738	23	0.13	0.15	0.14	-999.9	-999.9	-999.9	\N	(2)
2738	29	0.50	0.52	0.51	1.0	1.2	1.1	\N	
2738	35	-1.33	-1.25	-1.31	18.2	23.8	19.4	\N	
2738	41	0.42	0.47	0.44	0.5	0.8	0.6	\N	
2738	47	0.95	1.07	0.99	23.5	38.7	27.7	\N	
2738	6	1.14	1.38	1.22	5.6	17.7	9.0	\N	
2738	12	-0.21	-0.17	-0.18	0.1	0.5	0.4	\N	
2738	18	0.50	0.59	0.53	6.1	6.2	6.2	\N	
2738	24	0.13	0.33	0.22	1.1	5.1	2.3	\N	
2738	30	-0.16	0.05	-0.10	2.8	7.5	4.1	\N	
2738	36	0.51	0.53	0.52	22.6	25.3	24.4	\N	
2738	42	-0.31	-0.25	-0.27	1.2	1.2	1.2	\N	
2738	48	-2.00	-1.97	-1.99	47.0	57.0	53.0	\N	
2738	1	-0.63	-0.59	-0.61	2.6	3.4	3.0	\N	
2738	7	-0.27	-0.23	-0.25	4.4	5.3	4.8	\N	
2738	13	0.51	0.68	0.58	15.4	33.5	22.0	\N	
2738	19	1.92	1.94	1.93	16.0	16.8	16.5	\N	
2738	25	0.03	0.05	0.05	0.7	0.8	0.8	\N	
2738	31	0.04	0.16	0.10	2.9	5.4	4.1	\N	
2738	37	-0.53	-0.50	-0.51	36.1	39.3	37.7	\N	
2738	43	0.75	0.77	0.76	8.8	11.1	10.4	\N	
2738	49	-999.90	-999.90	-999.90	-999.9	-999.9	-999.9	\N	(2)
\.


ALTER TABLE ONLY public.w26_data
    ADD CONSTRAINT w26_data_fkey001 FOREIGN KEY (id_w26) REFERENCES public.w26(id_w26) ON UPDATE CASCADE ON DELETE CASCADE;


REVOKE ALL ON TABLE public.w26_data FROM PUBLIC;
REVOKE ALL ON TABLE public.w26_data FROM weboll;
GRANT ALL ON TABLE public.w26_data TO weboll;
GRANT SELECT ON TABLE public.w26_data TO weboll;
GRANT SELECT ON TABLE public.w26_data TO weboll;
GRANT ALL ON TABLE public.w26_data TO weboll;
GRANT ALL ON TABLE public.w26_data TO weboll;


--
-- PostgreSQL database dump complete
--