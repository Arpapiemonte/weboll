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
-- Name: w24_soglie; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w24_soglie (
    id_allertamento character varying(6) NOT NULL,
    id_parametro character varying(10) NOT NULL,
    id_aggregazione integer NOT NULL,
    soglia1 numeric(7,2) NOT NULL,
    soglia2 numeric(7,2) NOT NULL,
    classe_intensita integer NOT NULL,
    last_update timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.w24_soglie OWNER TO weboll;

--
-- Data for Name: w24_soglie; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w24_soglie (id_allertamento, id_parametro, id_aggregazione, soglia1, soglia2, classe_intensita, last_update, username) FROM stdin;
Piem-I	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-I	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-I	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-I	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-L	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-L	VELV	0	15.00	20.00	1	2017-08-01 14:11:07	weboll
Piem-L	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-L	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-L	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-L	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-L	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-L	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-L	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-L	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-L	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-L	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-L	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-L	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-L	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-L	PLUV	901	1.00	9.00	1	2018-01-24 15:31:39	weboll
Piem-L	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-L	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-L	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-L	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-L	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-L	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-L	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-L	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-L	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-L	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-L	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-L	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-L	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-L	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-L	VELV	0	0.00	15.00	0	2017-08-01 14:10:54	weboll
Piem-L	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-E	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-L	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-L	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-L	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-L	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-L	SNOW	902	1.00	14.00	1	2017-09-11 15:25:15	weboll
Piem-L	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-L	VELV	0	20.00	999.00	2	2017-08-01 14:11:07	weboll
Piem-L	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-L	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-L	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-M	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-M	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-M	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-F	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-M	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-M	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-M	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-M	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-M	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-M	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-M	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-M	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-M	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-M	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-M	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-M	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-M	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-M	SNOW	902	1.00	14.00	1	2017-09-11 15:25:15	weboll
Piem-M	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-M	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-M	PLUV	901	1.00	9.00	1	2018-01-24 15:31:39	weboll
Piem-M	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-M	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-M	VELV	0	20.00	999.00	2	2017-08-01 14:11:07	weboll
Piem-M	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-M	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-M	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-M	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-M	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-M	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-M	VELV	0	15.00	20.00	1	2017-08-01 14:11:07	weboll
Piem-M	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-M	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-M	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-M	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-M	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-M	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-M	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-M	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-M	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-M	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-M	VELV	0	0.00	15.00	0	2017-08-01 14:11:07	weboll
Piem-M	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-A	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-A	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-A	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-A	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-A	VELV	0	0.00	17.00	0	2017-08-01 14:08:42	weboll
Piem-A	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-A	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-G	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-L	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-M	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-A	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-A	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-A	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-A	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-A	VELV	0	25.00	999.00	2	2017-08-01 14:08:42	weboll
Piem-A	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-A	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-A	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-A	VELV	0	17.00	25.00	1	2017-08-01 14:08:42	weboll
Piem-A	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-A	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-A	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-A	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-A	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-A	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-A	SNOW	902	1.00	14.00	1	2017-09-14 15:08:11	weboll
Piem-A	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-A	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-A	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-A	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-A	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-A	PLUV	901	1.00	9.00	1	2018-01-24 15:30:21	weboll
Piem-A	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-A	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-A	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-A	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-A	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-A	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-A	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-A	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-A	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-A	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-A	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-A	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-A	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-B	PLUV	901	1.00	9.00	1	2018-01-24 15:31:39	weboll
Piem-B	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-B	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-B	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-B	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-B	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-B	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-B	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-B	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-B	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-B	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-B	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-B	SNOW	902	1.00	14.00	1	2017-09-11 15:25:15	weboll
Piem-B	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-B	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-H	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-B	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-B	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-B	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-B	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-B	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-I	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-B	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-B	VELV	0	25.00	999.00	2	2017-08-01 14:11:07	weboll
Piem-B	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-B	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-B	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-B	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-B	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-B	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-B	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-B	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-B	VELV	0	17.00	25.00	1	2017-08-01 14:11:07	weboll
Piem-B	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-B	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-B	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-B	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-B	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-B	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-B	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-B	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-B	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-B	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-B	VELV	0	0.00	17.00	0	2017-08-01 14:09:34	weboll
Piem-C	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-C	VELV	0	17.00	25.00	1	2017-08-01 14:11:07	weboll
Piem-C	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-C	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-C	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-C	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-C	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-C	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-C	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-C	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-C	SNOW	902	1.00	14.00	1	2017-09-11 15:25:15	weboll
Piem-C	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-C	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-C	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-C	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-C	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-C	PLUV	901	1.00	9.00	1	2018-01-24 15:31:39	weboll
Piem-C	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-C	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-C	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-A	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-B	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-C	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-C	VELV	0	0.00	17.00	0	2017-08-01 14:09:52	weboll
Piem-C	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-C	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-C	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-C	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-C	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-C	VELV	0	25.00	999.00	2	2017-08-01 14:11:07	weboll
Piem-C	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-C	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-C	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-C	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-C	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-C	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-C	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-C	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-C	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-C	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-C	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-C	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-C	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-L	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-C	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-D	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-D	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-D	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-D	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-D	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-D	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-D	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-D	VELV	0	25.00	999.00	2	2017-08-01 14:11:07	weboll
Piem-D	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-D	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-D	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-D	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-D	SNOW	902	1.00	14.00	1	2017-09-11 15:25:15	weboll
Piem-D	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-D	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-D	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-D	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-D	VELV	0	0.00	17.00	0	2017-08-01 14:09:57	weboll
Piem-D	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-D	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-D	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-D	PLUV	901	1.00	9.00	1	2018-01-24 15:31:39	weboll
Piem-D	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-D	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-D	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-D	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-D	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-D	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-D	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-D	VELV	0	17.00	25.00	1	2017-08-01 14:11:07	weboll
Piem-D	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-D	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-D	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-D	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-D	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-D	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-D	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-D	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-D	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-D	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-D	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-D	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-M	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-E	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-E	VELV	0	25.00	999.00	2	2017-08-01 14:11:07	weboll
Piem-E	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-E	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-E	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-E	SNOW	902	1.00	14.00	1	2017-09-11 15:25:15	weboll
Piem-E	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-E	VELV	0	0.00	17.00	0	2017-08-01 14:10:12	weboll
Piem-E	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-E	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-E	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-E	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-A	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-E	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-E	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-E	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-E	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-E	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-E	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-E	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-E	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-E	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-E	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-E	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-E	VELV	0	17.00	25.00	1	2017-08-01 14:11:07	weboll
Piem-E	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-E	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-E	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-E	PLUV	901	1.00	9.00	1	2018-01-24 15:31:39	weboll
Piem-E	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-E	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-C	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-D	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-E	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-E	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-E	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-E	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-E	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-E	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-E	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-E	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-E	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-E	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-E	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-E	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-E	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-F	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-F	VELV	0	15.00	20.00	1	2017-08-01 14:11:07	weboll
Piem-F	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-F	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-F	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-F	SNOW	902	1.00	14.00	1	2017-09-11 15:25:15	weboll
Piem-F	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-F	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-F	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-F	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-F	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-F	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-F	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-F	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-F	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-F	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-F	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-F	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-F	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-F	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-F	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-F	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-F	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-F	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-F	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-C	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-F	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-F	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-F	VELV	0	0.00	15.00	0	2017-08-01 14:10:18	weboll
Piem-F	VELV	0	20.00	999.00	2	2017-08-01 14:11:07	weboll
Piem-F	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-F	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-F	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-F	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-F	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-F	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-F	PLUV	901	1.00	9.00	1	2018-01-24 15:31:39	weboll
Piem-F	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-F	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-F	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-F	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-F	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-F	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-G	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-G	VELV	0	0.00	15.00	0	2017-08-01 14:10:23	weboll
Piem-G	VELV	0	15.00	20.00	1	2017-08-01 14:11:07	weboll
Piem-G	VELV	0	20.00	999.00	2	2017-08-01 14:11:07	weboll
Piem-G	SNOW	902	1.00	14.00	1	2017-09-11 15:25:15	weboll
Piem-G	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-D	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-G	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-G	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-G	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-G	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-G	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-G	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-G	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-G	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-G	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-G	PLUV	901	1.00	9.00	1	2018-01-24 15:31:39	weboll
Piem-G	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-G	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-G	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-G	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-G	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-G	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-G	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-G	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-G	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-G	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-G	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-G	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-G	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-G	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-G	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-G	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-G	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-G	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-G	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-G	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-G	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-G	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-G	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-G	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-G	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-G	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-F	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-G	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-H	VELV	0	15.00	20.00	1	2017-08-01 14:11:07	weboll
Piem-H	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-H	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-H	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-H	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-H	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-H	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-H	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-H	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-H	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-H	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-H	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-H	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-H	VELV	0	0.00	15.00	0	2017-08-01 14:10:43	weboll
Piem-H	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-H	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-H	SNOW_1000	901	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-H	VELV	0	20.00	999.00	2	2017-08-01 14:11:07	weboll
Piem-H	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-H	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-H	SNOW_400	902	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-H	PLUV	901	1.00	9.00	1	2018-01-24 15:31:39	weboll
Piem-H	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-H	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-H	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-H	PLUV	901	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-H	SNOW	902	1.00	14.00	1	2017-09-11 15:25:15	weboll
Piem-H	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-H	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-H	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-H	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-H	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-H	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-H	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-H	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-H	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-H	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-H	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-H	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-H	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-H	SNOW_700	901	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-H	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-I	VELV	0	20.00	999.00	2	2017-08-01 14:11:07	weboll
Piem-I	PLUV	902	1.00	14.00	1	2018-01-24 15:32:33	weboll
Piem-I	SNOW_400	902	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-I	SNOW_1000	901	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-I	PLUV	901	1.00	9.00	1	2018-01-24 15:31:39	weboll
Piem-I	SNOW_700	902	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-I	SNOW_400	902	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-I	SNOW	901	1.00	9.00	1	2017-09-11 15:25:15	weboll
Piem-I	VELV	0	15.00	20.00	1	2017-08-01 14:11:07	weboll
Piem-I	PLUV	901	10.00	29.00	2	2018-01-24 15:33:50	weboll
Piem-I	SNOW_1000	901	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-I	PLUV	901	60.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-I	SNOW_700	902	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-I	SNOW	902	15.00	39.00	2	2017-09-11 15:25:15	weboll
Piem-I	SNOW_400	901	40.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-I	SNOW_700	901	20.00	39.00	1	2017-09-18 12:00:00	weboll
Piem-I	SNOW_1000	902	100.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-I	SNOW	902	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-I	SNOW	901	0.00	0.00	0	2017-09-11 15:25:15	weboll
Piem-I	PLUV	902	0.00	0.00	0	2018-01-24 15:42:00	weboll
Piem-I	SNOW_700	901	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-I	SNOW_1000	902	40.00	69.00	1	2017-09-18 12:00:00	weboll
Piem-I	PLUV	902	90.00	999.00	4	2018-01-24 15:37:07	weboll
Piem-I	PLUV	902	15.00	44.00	2	2018-01-24 15:33:50	weboll
Piem-I	SNOW_400	901	20.00	39.00	2	2017-09-18 12:00:00	weboll
Piem-I	SNOW_700	902	60.00	999.00	3	2017-09-18 12:00:00	weboll
Piem-I	VELV	0	0.00	15.00	0	2017-08-01 14:10:48	weboll
Piem-I	SNOW	902	1.00	14.00	1	2017-09-11 15:25:15	weboll
Piem-I	SNOW_400	901	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-I	PLUV	902	45.00	89.00	3	2018-01-24 15:35:02	weboll
Piem-I	SNOW_1000	901	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-I	SNOW_700	901	40.00	59.00	2	2017-09-18 12:00:00	weboll
Piem-I	SNOW_400	902	0.00	9.00	0	2017-09-18 12:00:00	weboll
Piem-I	SNOW_1000	902	70.00	99.00	2	2017-09-18 12:00:00	weboll
Piem-I	SNOW_400	901	10.00	19.00	1	2017-09-18 12:00:00	weboll
Piem-I	SNOW_700	902	0.00	19.00	0	2017-09-18 12:00:00	weboll
Piem-I	PLUV	901	30.00	59.00	3	2018-01-24 15:35:02	weboll
Piem-I	SNOW_1000	902	0.00	39.00	0	2017-09-18 12:00:00	weboll
Piem-G	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-B	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-H	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-I	SNOW	902	40.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-L	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-M	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-A	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-B	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-C	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-D	SNOW	901	10.00	29.00	2	2017-09-11 15:25:15	weboll
Piem-H	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-I	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-E	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
Piem-F	SNOW	901	30.00	999.00	3	2017-09-11 15:25:15	weboll
\.


--
-- Name: w24_soglie_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.w24_soglie
    ADD CONSTRAINT w24_soglie_pkey PRIMARY KEY (id_allertamento, id_parametro, id_aggregazione, classe_intensita);


--
-- Name: w24_soglie_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w24_soglie
    ADD CONSTRAINT w24_soglie_fkey001 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w24_soglie_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w24_soglie
    ADD CONSTRAINT w24_soglie_fkey002 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

