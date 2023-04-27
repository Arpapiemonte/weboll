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

CREATE OR REPLACE FUNCTION public.w32_numero_bollettino()
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
BEGIN
  RETURN
  (SELECT COUNT(data_emissione) + 1 || '/' || date_part('year', current_date)
  FROM w32
  WHERE data_emissione >= date_trunc('year', current_date) AND data_emissione < current_date);

END;
$function$
;

--
-- Name: w32; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w32 (
    id_w32 bigint NOT NULL,
    data_emissione date DEFAULT ('now'::text)::date NOT NULL,
    ora_emissione character varying(8) NOT NULL,
    ora_simulazione character varying(8),
    numero_bollettino character varying(30) DEFAULT public.w32_numero_bollettino() NOT NULL,
    situazione_evoluzione text,
    status character(1) DEFAULT 0 NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
    data_validita date NOT NULL,
    ora_osservazione character varying(8),
    data_osservazione character varying(20),
    data_simulazione character varying(20),
    note text
);


ALTER TABLE public.w32 OWNER TO weboll;

--
-- Name: COLUMN w32.status; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.w32.status IS '0 = Draft; 1 = Final';


--
-- Name: w32_id_w32_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w32_id_w32_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w32_id_w32_seq OWNER TO weboll;

--
-- Name: w32_id_w32_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w32_id_w32_seq OWNED BY public.w32.id_w32;


--
-- Name: id_w32; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w32 ALTER COLUMN id_w32 SET DEFAULT nextval('public.w32_id_w32_seq'::regclass);


--
-- Data for Name: w32; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w32 (id_w32, data_emissione, ora_emissione, ora_simulazione, numero_bollettino, situazione_evoluzione, status, last_update, username, data_validita, ora_osservazione, data_osservazione, data_simulazione, note) FROM stdin;
11	2020-03-03	16:00	11:40	1/2020		1	2020-03-03 16:21:28	weboll	2020-03-04	15:30	03/03/2020	03/03/2020	-
14	2020-03-04	12:00	12:22	2/2020		1	2020-03-04 12:09:44	weboll	2020-03-05	11:40	04/03/2020	04/03/2020	-
15	2020-03-05	12:00	11:02	3/2020		1	2020-03-05 12:10:52	weboll	2020-03-06	11:40	05/03/2020	05/03/2020	-
16	2020-03-06	12:00	10:56	4/2020		1	2020-03-06 12:08:50	weboll	2020-03-09	11:40	06/03/2020	06/03/2020	-
\.


--
-- Name: w32_id_w32_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w32_id_w32_seq', 1, true);


--
-- Name: w32_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w32
    ADD CONSTRAINT w32_pkey PRIMARY KEY (id_w32);
