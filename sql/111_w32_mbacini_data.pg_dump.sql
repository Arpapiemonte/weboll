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
-- Name: w32_mbacini_data; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w32_mbacini_data (
    id_w32 bigint NOT NULL,
    id_w32_mbacini integer NOT NULL,
    livello_criticita_oss character varying(2) NOT NULL,
    livello_criticita_prev_oggi character varying(2) NOT NULL,
    livello_criticita_prev_domani character varying(2) NOT NULL
);


ALTER TABLE public.w32_mbacini_data ADD COLUMN id_w32_mbacini_data BIGSERIAL PRIMARY KEY;
ALTER TABLE public.w32_mbacini_data OWNER TO weboll;

--
-- Data for Name: w32_mbacini_data; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w32_mbacini_data (id_w32, id_w32_mbacini, livello_criticita_oss, livello_criticita_prev_oggi, livello_criticita_prev_domani) FROM stdin;
11	1	-	-	-
11	2	-	-	-
11	3	-	-	-
11	4	-	-	-
11	5	-	-	-
11	6	-	-	-
14	1	-	-	-
14	2	-	-	-
14	3	-	-	-
14	4	-	-	-
14	5	-	-	-
14	6	-	-	-
15	1	-	-	-
15	2	-	-	-
15	3	-	-	-
15	4	-	-	-
15	5	-	-	-
15	6	-	-	-
16	1	-	-	-
16	2	-	-	-
16	3	-	-	-
16	4	-	-	-
16	5	-	-	-
16	6	-	-	-
\.


--
-- Name: w32_data_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

--ALTER TABLE ONLY public.w32_data
--    ADD CONSTRAINT w32_data_pkey PRIMARY KEY (id_w32, id_w32_zone);


--
-- Name: w32_mbacini_data_fk; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w32_mbacini_data
    ADD CONSTRAINT w32_mbacini_data_fk FOREIGN KEY (id_w32_mbacini) REFERENCES public.w32_mbacini(id_w32_mbacini);


--
-- Name: w32_mbacini_data_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w32_mbacini_data
    ADD CONSTRAINT w32_mbacini_data_fkey001 FOREIGN KEY (id_w32) REFERENCES public.w32(id_w32) ON UPDATE CASCADE ON DELETE CASCADE;
