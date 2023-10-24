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

CREATE OR REPLACE FUNCTION public.w29_numero_bollettino()
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
BEGIN
  RETURN
  (SELECT COUNT(data_emissione) + 1 || '/' || date_part('year', current_date)
  FROM w29
  WHERE data_emissione >= date_trunc('year', current_date) AND data_emissione < current_date);

END;
$function$
;

--
-- Name: w29; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w29 (
    id_w29 bigint NOT NULL,
    data_emissione date DEFAULT ('now'::text)::date NOT NULL,
    ora_emissione character varying(5) NOT NULL,
    ora_simulazione character varying(5),
    numero_bollettino character varying(30) DEFAULT public.w29_numero_bollettino() NOT NULL,
    situazione_evoluzione text,
    status character(1) DEFAULT 0 NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
    data_validita date NOT NULL,
    ora_osservazione character varying(5),
    data_osservazione character varying(20),
    data_simulazione character varying(20),
    note text
);


ALTER TABLE public.w29 OWNER TO weboll;

--
-- Name: COLUMN w29.status; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.w29.status IS '0 = Draft; 1 = Final';


--
-- Name: w29_id_w29_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w29_id_w29_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w29_id_w29_seq OWNER TO weboll;

--
-- Name: w29_id_w29_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w29_id_w29_seq OWNED BY public.w29.id_w29;


--
-- Name: id_w29; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w29 ALTER COLUMN id_w29 SET DEFAULT nextval('public.w29_id_w29_seq'::regclass);


--
-- Data for Name: w29; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w29 (id_w29, data_emissione, ora_emissione, ora_simulazione, numero_bollettino, situazione_evoluzione, status, last_update, username, data_validita, ora_osservazione, data_osservazione, data_simulazione, note) FROM stdin;
502	2023-02-16	12:00	10:20	251/2021		1	2023-02-16 12:01:45	weboll	2021-12-28	10:30	2021-12-27	2021-12-27	-
503	2023-02-17	12:00	10:38	252/2021		1	2023-02-17 12:11:06	weboll	2021-12-29	11:30	2021-12-28	2021-12-28	-
504	2023-02-18	12:00	11:14	253/2021		1	2023-02-18 12:06:42	weboll	2021-12-30	10:50	2021-12-29	2021-12-29	-
505	2023-02-19	12:00	11:20	254/2021		1	2023-02-19 12:06:44	weboll	2021-12-31	10:30	2021-12-30	2021-12-30	-
506	2023-02-20	12:00	10:54	255/2021		1	2023-02-20 12:04:49	weboll	2022-01-03	10:40	2021-12-31	2021-12-31	-
\.


--
-- Name: w29_id_w29_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w29_id_w29_seq', 506, true);


--
-- Name: w29_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w29
    ADD CONSTRAINT w29_pkey PRIMARY KEY (id_w29);


--
-- Name: TABLE w29; Type: ACL; Schema: public; Owner: weboll
--



--
-- Name: SEQUENCE w29_id_w29_seq; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
