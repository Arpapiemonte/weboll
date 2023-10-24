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
-- Name: w12_data; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w12_data (
    id_w12 bigint NOT NULL,
    id_venue integer NOT NULL,
    id_time_layouts integer NOT NULL,
    sky_condition smallint,
    cloud_amount smallint,
    precipitation_class smallint,
    cumulated_snow integer,
    freezing_level integer,
    snow_level integer,
    temperature_below_zero boolean,
    risk_freezing_rain boolean,
    vis_inf_1000 boolean,
    vis_inf_1000_reason smallint,
    wind_class smallint
);


ALTER TABLE public.w12_data OWNER TO weboll;

--
-- Data for Name: w12_data; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w12_data (id_w12, id_venue, id_time_layouts, sky_condition, cloud_amount, precipitation_class, cumulated_snow, freezing_level, snow_level, temperature_below_zero, risk_freezing_rain, vis_inf_1000, vis_inf_1000_reason, wind_class) FROM stdin;
2011	99	45	29	2	0	\N	3000	2700	f	f	f	\N	2
2011	103	63	22	2	0	\N	2200	2000	f	f	f	\N	2
2011	104	63	22	2	0	\N	2100	1800	f	f	f	\N	1
2011	105	63	22	2	0	\N	2100	1800	f	f	f	\N	2
2011	99	81	29	2	0	\N	2100	1900	f	f	f	\N	2
2011	100	81	29	2	0	\N	2100	1900	f	f	f	\N	3
2011	101	81	29	2	0	\N	2100	1900	f	f	f	\N	3
2011	102	81	22	2	0	\N	2000	1800	f	f	f	\N	2
2011	103	81	22	2	0	\N	2000	1800	f	f	f	\N	1
2011	104	81	22	2	0	\N	1900	1700	f	f	f	\N	1
2011	105	81	22	2	0	\N	1900	1700	f	f	f	\N	2
2011	99	82	29	2	0	\N	2100	1900	f	f	f	\N	2
2011	100	82	29	2	0	\N	2200	1900	f	f	f	\N	3
2011	101	82	29	2	0	\N	2100	1900	f	f	f	\N	3
2011	102	82	22	2	0	\N	2100	1900	f	f	f	\N	2
2011	103	82	22	2	0	\N	2100	1900	f	f	f	\N	2
2011	100	45	29	2	0	\N	3000	2700	f	f	f	\N	3
2011	101	45	29	2	0	\N	3000	2600	f	f	f	\N	4
2011	102	45	11	6	0	\N	2900	2500	f	f	f	\N	3
2011	103	45	11	6	0	\N	2800	2400	f	f	f	\N	2
2011	104	45	11	6	0	\N	2500	2000	f	f	f	\N	2
2011	105	45	11	6	0	\N	2400	1900	f	f	f	\N	1
2011	99	46	29	4	0	\N	3000	2700	f	f	f	\N	2
2011	100	46	29	4	0	\N	3000	2700	f	f	f	\N	2
2011	101	46	29	2	0	\N	2900	2600	f	f	f	\N	3
2011	102	46	16	2	0	\N	2900	2500	f	f	f	\N	2
2011	103	46	11	6	0	\N	2800	2400	f	f	f	\N	2
2011	104	46	11	6	0	\N	2500	2100	f	f	f	\N	1
2011	105	46	8	6	5	\N	2400	2000	f	f	f	\N	1
2011	100	62	29	2	0	\N	2700	2400	f	f	f	\N	3
2011	101	62	29	2	0	\N	2700	2300	f	f	f	\N	4
2011	102	62	22	2	0	\N	2500	2300	f	f	f	\N	2
2011	103	62	22	2	0	\N	2500	2200	f	f	f	\N	2
2011	104	62	22	2	0	\N	2300	2000	f	f	f	\N	1
2011	105	62	22	2	0	\N	2200	1900	f	f	f	\N	1
2011	99	63	22	2	0	\N	2400	2100	f	f	f	\N	2
2011	100	63	22	2	0	\N	2400	2100	f	f	f	\N	3
2011	101	63	22	2	0	\N	2400	2100	f	f	f	\N	3
2011	102	63	22	2	0	\N	2300	2000	f	f	f	\N	2
2011	104	82	22	2	0	\N	2000	1800	f	f	f	\N	2
2011	105	82	22	2	0	\N	2000	1800	f	f	f	\N	2
2011	99	60	11	6	0	\N	3100	2700	f	f	f	\N	2
2011	100	60	11	6	0	\N	3100	2700	f	f	f	\N	2
2011	101	60	11	6	0	\N	3000	2600	f	f	f	\N	3
2011	102	60	11	6	0	\N	2900	2500	f	f	f	\N	2
2011	103	60	11	6	0	\N	2800	2300	f	f	f	\N	1
2011	104	60	11	6	0	\N	2500	1900	f	f	f	\N	1
2011	105	60	8	6	5	\N	2300	1800	f	f	f	\N	1
2011	99	61	29	4	0	\N	2900	2600	f	f	f	\N	3
2011	100	61	29	6	0	\N	2900	2600	f	f	f	\N	2
2011	101	61	29	2	0	\N	2800	2500	f	f	f	\N	4
2011	102	61	11	6	0	\N	2700	2400	f	f	f	\N	2
2011	103	61	11	6	0	\N	2600	2300	f	f	f	\N	2
2011	104	61	8	6	5	\N	2300	1900	f	f	f	\N	1
2011	105	61	8	8	1	\N	2100	1700	f	f	f	\N	2
2011	99	62	29	2	0	\N	2700	2400	f	f	f	\N	2
2012	103	63	22	2	0	\N	2100	1900	f	f	f	\N	2
2012	103	82	22	2	0	\N	2000	1800	f	f	f	\N	2
2012	104	82	22	2	0	\N	2000	1800	f	f	f	\N	2
2012	105	82	22	2	0	\N	2000	1800	f	f	f	\N	2
2012	104	62	22	2	0	\N	2000	1800	f	f	f	\N	2
2012	105	62	22	2	0	\N	2000	1800	f	f	f	\N	2
2012	99	63	22	2	0	\N	2100	1900	f	f	f	\N	2
2012	100	63	22	2	0	\N	2100	1900	f	f	f	\N	3
2012	101	63	22	2	0	\N	2100	1900	f	f	f	\N	3
2012	102	63	22	2	0	\N	2100	1900	f	f	f	\N	2
2012	104	63	22	2	0	\N	2100	1900	f	f	f	\N	3
2012	105	63	22	2	0	\N	2100	1800	f	f	f	\N	3
2012	99	81	22	2	0	\N	2000	1800	f	f	f	\N	2
2012	100	81	3	0	0	\N	2000	1700	f	f	f	\N	2
2012	101	81	3	0	0	\N	2000	1700	f	f	f	\N	2
2012	102	81	3	0	0	\N	2000	1700	f	f	f	\N	2
2012	103	81	3	0	0	\N	1900	1700	f	f	f	\N	1
2012	104	81	22	2	0	\N	2000	1700	f	f	f	\N	2
2012	105	81	22	2	0	\N	1900	1700	f	f	f	\N	2
2012	99	45	16	4	0	\N	2700	2400	f	f	f	\N	3
2012	100	45	16	4	0	\N	2700	2400	f	f	f	\N	3
2012	101	45	16	4	0	\N	2600	2300	f	f	f	\N	5
2012	102	45	16	4	0	\N	2500	2200	f	f	f	\N	2
2012	103	45	16	4	0	\N	2400	2100	f	f	f	\N	2
2012	104	45	20	6	1	\N	2200	1900	f	f	f	\N	2
2012	105	45	20	6	1	\N	2100	1700	f	f	f	\N	1
2012	99	46	22	2	0	\N	2300	2100	f	f	f	\N	2
2012	100	46	22	2	0	\N	2300	2000	f	f	f	\N	3
2012	101	46	22	2	0	\N	2300	2000	f	f	f	\N	3
2012	102	46	22	2	0	\N	2200	2000	f	f	t	3	2
2012	103	46	22	2	0	\N	2200	1900	f	f	f	\N	2
2012	104	46	16	4	0	\N	2100	1800	f	f	f	\N	1
2012	105	46	16	4	0	\N	2000	1800	f	f	f	\N	2
2012	99	60	3	0	0	\N	2100	1900	f	f	f	\N	3
2012	100	60	3	0	0	\N	2100	1800	f	f	f	\N	3
2012	101	60	3	0	0	\N	2100	1900	f	f	f	\N	3
2012	102	60	3	0	0	\N	2100	1800	f	f	f	\N	2
2012	103	60	3	0	0	\N	2100	1800	f	f	t	3	2
2012	104	60	3	0	0	\N	2000	1700	f	f	f	\N	2
2012	105	60	3	0	0	\N	1900	1700	f	f	f	\N	2
2012	99	61	3	0	0	\N	2100	1900	f	f	f	\N	2
2012	100	61	3	0	0	\N	2100	1800	f	f	f	\N	3
2012	101	61	3	0	0	\N	2100	1800	f	f	f	\N	3
2012	102	61	3	0	0	\N	2100	1800	f	f	f	\N	2
2012	103	61	3	0	0	\N	2100	1800	f	f	f	\N	2
2012	104	61	3	0	0	\N	1900	1700	f	f	f	\N	2
2012	105	61	3	0	0	\N	1900	1700	f	f	f	\N	2
2012	99	62	22	2	0	\N	2200	1900	f	f	f	\N	3
2012	100	62	22	2	0	\N	2200	2000	f	f	f	\N	4
2012	101	62	22	2	0	\N	2100	1900	f	f	f	\N	4
2012	102	62	22	2	0	\N	2100	1900	f	f	f	\N	2
2012	103	62	22	2	0	\N	2100	1900	f	f	f	\N	2
2012	99	82	22	2	0	\N	2000	1700	f	f	f	\N	2
2012	100	82	22	2	0	\N	2000	1700	f	f	f	\N	2
2012	101	82	22	2	0	\N	2000	1700	f	f	f	\N	2
2012	102	82	22	2	0	\N	2000	1800	f	f	f	\N	2
2013	99	45	16	4	0	\N	2800	2500	f	f	f	\N	2
2013	100	45	16	4	0	\N	2800	2500	f	f	f	\N	3
2013	101	45	16	4	0	\N	2800	2500	f	f	f	\N	4
2013	100	61	11	6	0	\N	2800	2500	f	f	f	\N	1
2013	101	61	11	6	0	\N	2700	2400	f	f	f	\N	2
2013	102	61	11	6	0	\N	2600	2200	f	f	f	\N	2
2013	103	61	11	6	0	\N	2500	2100	f	f	f	\N	2
2013	104	61	11	6	0	\N	2300	1800	f	f	f	\N	1
2013	105	61	11	6	0	\N	2200	1800	f	f	f	\N	1
2013	99	62	20	8	1	\N	2800	2500	f	f	f	\N	2
2013	100	62	20	8	1	\N	2800	2500	f	f	f	\N	3
2013	99	63	20	8	1	\N	2600	2200	f	f	f	\N	2
2013	100	63	20	8	1	\N	2600	2200	f	f	f	\N	2
2013	101	63	20	8	1	\N	2500	2100	f	f	f	\N	4
2013	102	63	20	8	1	\N	2400	2100	f	f	f	\N	2
2013	103	63	20	8	1	\N	2400	2000	f	f	f	\N	2
2013	104	63	20	8	1	\N	2200	1800	f	f	f	\N	2
2013	105	63	20	8	1	\N	2100	1800	f	f	f	\N	1
2013	99	81	24	8	1	\N	2000	1600	f	f	f	\N	1
2013	100	81	24	8	1	\N	2000	1600	f	f	f	\N	2
2013	101	81	24	8	1	\N	1900	1600	f	f	f	\N	3
2013	102	81	24	8	1	\N	1900	1600	f	f	f	\N	2
2013	103	81	24	8	1	\N	1900	1600	f	f	f	\N	2
2013	104	81	24	8	1	\N	1800	1500	f	f	f	\N	2
2013	105	81	24	8	1	\N	1800	1500	f	f	f	\N	2
2013	99	82	29	0	0	\N	1600	1300	f	f	f	\N	2
2013	100	82	29	0	0	\N	1600	1400	f	f	f	\N	2
2013	101	82	3	0	0	\N	1600	1300	f	f	f	\N	3
2013	102	82	3	0	0	\N	1600	1400	f	f	f	\N	2
2013	102	45	16	4	0	\N	2700	2400	f	f	f	\N	3
2013	103	45	16	4	0	\N	2600	2300	f	f	f	\N	2
2013	104	45	16	4	0	\N	2500	2200	f	f	f	\N	2
2013	105	45	16	4	0	\N	2400	2100	f	f	f	\N	2
2013	99	46	11	6	0	\N	2800	2500	f	f	f	\N	2
2013	100	46	11	6	0	\N	2800	2500	f	f	f	\N	2
2013	101	46	16	4	0	\N	2800	2500	f	f	f	\N	3
2013	102	46	16	4	0	\N	2700	2400	f	f	f	\N	3
2013	103	46	16	4	0	\N	2700	2400	f	f	f	\N	2
2013	104	46	16	4	0	\N	2500	2200	f	f	f	\N	1
2013	105	46	16	4	0	\N	2500	2200	f	f	f	\N	2
2013	99	60	11	6	0	\N	2800	2400	f	f	f	\N	1
2013	100	60	11	6	0	\N	2800	2400	f	f	f	\N	1
2013	101	60	11	6	0	\N	2700	2400	f	f	f	\N	1
2013	102	60	11	6	0	\N	2600	2200	f	f	f	\N	2
2013	103	60	11	6	0	\N	2500	2100	f	f	f	\N	1
2013	104	60	11	6	0	\N	2400	2000	f	f	f	\N	2
2013	105	60	11	6	0	\N	2400	2000	f	f	f	\N	1
2013	99	61	11	6	0	\N	2800	2400	f	f	f	\N	1
2013	101	62	20	8	1	\N	2700	2400	f	f	f	\N	3
2013	102	62	20	8	1	\N	2600	2200	f	f	f	\N	2
2013	103	62	20	8	1	\N	2500	2100	f	f	f	\N	2
2013	104	62	20	8	1	\N	2300	1900	f	f	f	\N	2
2013	105	62	20	8	1	\N	2200	1800	f	f	f	\N	1
2013	103	82	3	0	0	\N	1700	1400	f	f	f	\N	2
2013	104	82	29	0	0	\N	1600	1400	f	f	f	\N	3
2013	105	82	29	0	0	\N	1600	1400	f	f	f	\N	3
\.

--
-- Name: w12_data_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w12_data
    ADD CONSTRAINT w12_data_fkey001 FOREIGN KEY (id_w12) REFERENCES public.w12(id_w12) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w12_data_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w12_data
    ADD CONSTRAINT w12_data_fkey002 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w12_data_fkey003; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w12_data
    ADD CONSTRAINT w12_data_fkey003 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON UPDATE CASCADE ON DELETE CASCADE;



ALTER TABLE ONLY public.w12_data ADD COLUMN id_w12_data SERIAL PRIMARY KEY;
