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

CREATE OR REPLACE FUNCTION public.w26_numero_bollettino()
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
BEGIN
  RETURN
  (SELECT COUNT(data_emissione) + 1 || '/' || date_part('year', current_date)
  FROM w26_numero_bollettino
  WHERE data_emissione >= date_trunc('year', current_date) AND data_emissione < current_date);

END;
$function$
;

--
-- Name: w26; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w26 (
    id_w26 bigint NOT NULL,
    data_emissione date DEFAULT ('now'::text)::date NOT NULL,
    numero_bollettino character varying(30) DEFAULT public.w26_numero_bollettino() NOT NULL,
    status character(1) DEFAULT 0 NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
    data_validita date NOT NULL,
    id_w26_parent integer
);


ALTER TABLE public.w26 OWNER TO weboll;

--
-- Name: COLUMN w26.status; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.w26.status IS '0 = Draft; 1 = Final';


--
-- Name: w26_id_w26_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w26_id_w26_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w26_id_w26_seq OWNER TO weboll;

--
-- Name: w26_id_w26_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w26_id_w26_seq OWNED BY public.w26.id_w26;


--
-- Name: id_w26; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w26 ALTER COLUMN id_w26 SET DEFAULT nextval('public.w26_id_w26_seq'::regclass);


--
-- Data for Name: w26; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w26 (id_w26, data_emissione, numero_bollettino, status, last_update, username, data_validita) FROM stdin;
2736	2023-01-16	15/2023	1	2023-01-16 11:40:19	weboll	2023-01-15
2737	2023-01-17	16/2023	1	2023-01-17 11:51:47	weboll	2023-01-16
2738	2023-01-18	17/2023	1	2023-01-18 11:24:00	weboll	2023-01-17
\.


--
-- Name: w26_id_w26_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w26_id_w26_seq', 506, true);


--
-- Name: w26_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w26
    ADD CONSTRAINT w26_pkey PRIMARY KEY (id_w26);


--
-- Name: TABLE w26; Type: ACL; Schema: public; Owner: weboll
--

REVOKE ALL ON TABLE public.w26 FROM PUBLIC;
REVOKE ALL ON TABLE public.w26 FROM weboll;
GRANT ALL ON TABLE public.w26 TO weboll;
GRANT SELECT ON TABLE public.w26 TO weboll;
GRANT SELECT ON TABLE public.w26 TO weboll;
GRANT ALL ON TABLE public.w26 TO weboll;
GRANT ALL ON TABLE public.w26 TO weboll;


--
-- Name: SEQUENCE w26_id_w26_seq; Type: ACL; Schema: public; Owner: weboll
--

REVOKE ALL ON SEQUENCE public.w26_id_w26_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE public.w26_id_w26_seq FROM weboll;
GRANT ALL ON SEQUENCE public.w26_id_w26_seq TO weboll;
GRANT SELECT ON SEQUENCE public.w26_id_w26_seq TO weboll;
GRANT SELECT ON SEQUENCE public.w26_id_w26_seq TO weboll;
GRANT ALL ON SEQUENCE public.w26_id_w26_seq TO weboll;
GRANT ALL ON SEQUENCE public.w26_id_w26_seq TO weboll;


--
-- PostgreSQL database dump complete
--
