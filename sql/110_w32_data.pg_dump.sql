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
-- Name: w32_data; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w32_data (
    id_w32 bigint NOT NULL,
    id_w32_zone integer NOT NULL,
    livello_criticita_oss character varying(2) NOT NULL,
    livello_criticita_prev_oggi character varying(2) NOT NULL,
    livello_criticita_prev_domani character varying(2) NOT NULL
);


ALTER TABLE public.w32_data ADD COLUMN id_w32_data BIGSERIAL PRIMARY KEY;
ALTER TABLE public.w32_data OWNER TO weboll;

--
-- Data for Name: w32_data; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w32_data (id_w32, id_w32_zone, livello_criticita_oss, livello_criticita_prev_oggi, livello_criticita_prev_domani) FROM stdin;
11	1	A	A	A
11	2	A	A	A
11	3	A	A	A
11	4	A	A	A
11	5	A	A	A
11	6	A	A	A
14	1	A	A	A
14	2	A	A	A
14	3	A	A	A
14	4	A	A	A
14	5	A	A	A
14	6	A	A	A
15	1	A	A	A
15	2	A	A	A
15	3	A	A	A
15	4	A	A	A
15	5	A	A	A
15	6	A	A	A
16	1	A	A	A
16	2	A	A	A
16	3	A	A	A
16	4	A	A	A
16	5	A	A	A
16	6	A	A	A
\.


--
-- Name: w32_data_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

--ALTER TABLE ONLY public.w32_data
--    ADD CONSTRAINT w32_data_pkey PRIMARY KEY (id_w32, id_w32_zone);


--
-- Name: w32_data_fk; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w32_data
    ADD CONSTRAINT w32_data_fk FOREIGN KEY (id_w32_zone) REFERENCES public.w32_zone(id_w32_zone);


--
-- Name: w32_data_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w32_data
    ADD CONSTRAINT w32_data_fkey001 FOREIGN KEY (id_w32) REFERENCES public.w32(id_w32) ON UPDATE CASCADE ON DELETE CASCADE;
