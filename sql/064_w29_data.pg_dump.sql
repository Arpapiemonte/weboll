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
-- Name: w29_data; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w29_data (
    id_w29 bigint NOT NULL,
    id_w29_zone integer NOT NULL,
    livello_criticita_oss character varying(2) NOT NULL,
    probabilita_criticita_oss character varying(12) NOT NULL,
    livello_criticita_prev_oggi character varying(2) NOT NULL,
    probabilita_criticita_prev_oggi character varying(12) NOT NULL,
    livello_criticita_prev_domani character varying(2) NOT NULL,
    probabilita_criticita_prev_domani character varying(12) NOT NULL
);


ALTER TABLE public.w29_data ADD COLUMN id_w29_data BIGSERIAL PRIMARY KEY;
ALTER TABLE public.w29_data OWNER TO weboll;

--
-- Data for Name: w29_data; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w29_data (id_w29, id_w29_zone, livello_criticita_oss, probabilita_criticita_oss, livello_criticita_prev_oggi, probabilita_criticita_prev_oggi, livello_criticita_prev_domani, probabilita_criticita_prev_domani, id_w29_data) FROM stdin;
502	1	-	nessuna	-	nessuna	-	nessuna	5046
502	4	-	nessuna	-	nessuna	-	nessuna	5047
502	7	-	nessuna	-	nessuna	-	nessuna	5048
502	8	-	nessuna	-	nessuna	-	nessuna	5049
502	11	-	nessuna	-	nessuna	-	nessuna	5050
503	3	-	nessuna	-	nessuna	-	nessuna	5051
503	5	-	nessuna	-	nessuna	-	nessuna	5052
503	8	-	nessuna	-	nessuna	-	nessuna	5053
503	11	-	nessuna	-	nessuna	-	nessuna	5054
504	1	-	nessuna	-	nessuna	-	nessuna	5055
504	4	-	nessuna	-	nessuna	-	nessuna	5056
504	7	-	nessuna	-	nessuna	-	nessuna	5057
504	8	-	nessuna	-	nessuna	-	nessuna	5058
504	11	-	nessuna	-	nessuna	-	nessuna	5059
505	1	-	nessuna	-	nessuna	-	nessuna	5060
505	4	-	nessuna	-	nessuna	-	nessuna	5061
505	11	-	nessuna	-	nessuna	-	nessuna	5062
502	2	-	nessuna	-	nessuna	-	nessuna	5124
502	5	-	nessuna	-	nessuna	-	nessuna	5125
502	9	-	nessuna	-	nessuna	-	nessuna	5126
503	1	-	nessuna	-	nessuna	-	nessuna	5127
503	4	-	nessuna	-	nessuna	-	nessuna	5128
503	6	-	nessuna	-	nessuna	-	nessuna	5129
503	9	-	nessuna	-	nessuna	-	nessuna	5130
504	2	-	nessuna	-	nessuna	-	nessuna	5131
504	5	-	nessuna	-	nessuna	-	nessuna	5132
504	9	-	nessuna	-	nessuna	-	nessuna	5133
505	9	-	nessuna	-	nessuna	-	nessuna	5134
505	2	-	nessuna	-	nessuna	-	nessuna	5135
505	5	-	nessuna	-	nessuna	-	nessuna	5136
505	7	-	nessuna	-	nessuna	-	nessuna	5137
505	8	-	nessuna	-	nessuna	-	nessuna	5138
506	1	-	nessuna	-	nessuna	-	nessuna	5139
506	3	-	nessuna	-	nessuna	-	nessuna	5140
506	6	-	nessuna	-	nessuna	-	nessuna	5141
506	7	-	nessuna	-	nessuna	-	nessuna	5142
506	9	-	nessuna	-	nessuna	-	nessuna	5143
506	11	-	nessuna	-	nessuna	-	nessuna	5144
506	4	-	nessuna	-	nessuna	-	nessuna	5145
502	3	-	nessuna	-	nessuna	-	nessuna	5199
502	6	-	nessuna	-	nessuna	-	nessuna	5200
502	10	-	nessuna	-	nessuna	-	nessuna	5201
503	2	-	nessuna	-	nessuna	-	nessuna	5202
503	7	-	nessuna	-	nessuna	-	nessuna	5203
503	10	-	nessuna	-	nessuna	-	nessuna	5204
504	3	-	nessuna	-	nessuna	-	nessuna	5205
504	6	-	nessuna	-	nessuna	-	nessuna	5206
504	10	-	nessuna	-	nessuna	-	nessuna	5207
505	3	-	nessuna	-	nessuna	-	nessuna	5208
505	6	-	nessuna	-	nessuna	-	nessuna	5209
505	10	-	nessuna	-	nessuna	-	nessuna	5210
506	2	-	nessuna	-	nessuna	-	nessuna	5211
506	5	-	nessuna	-	nessuna	-	nessuna	5212
506	8	-	nessuna	-	nessuna	-	nessuna	5213
506	10	-	nessuna	-	nessuna	-	nessuna	5214
\.

--
-- Name: w29_data_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

--ALTER TABLE ONLY public.w29_data
--    ADD CONSTRAINT w29_data_pkey PRIMARY KEY (id_w29, id_w29_zone);


--
-- Name: w29_data_fk; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w29_data
    ADD CONSTRAINT w29_data_fk FOREIGN KEY (id_w29_zone) REFERENCES public.w29_zone(id_w29_zone);


--
-- Name: w29_data_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w29_data
    ADD CONSTRAINT w29_data_fkey001 FOREIGN KEY (id_w29) REFERENCES public.w29(id_w29) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TABLE w29_data; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
