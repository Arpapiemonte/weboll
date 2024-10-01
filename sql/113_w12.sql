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
-- Name: w12; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w12 (
    id_w12 serial NOT NULL,
    start_valid_time timestamp(0) without time zone NOT NULL,
    validity integer NOT NULL,
    next_blt_time timestamp(0) without time zone NOT NULL,
    status character(1) DEFAULT 0 NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    id_w12_parent integer,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.w12 OWNER TO weboll;

--
-- Name: COLUMN w12.status; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.w12.status IS '0 = Draft; 1 = Final';

ALTER TABLE public.w12_id_w12_seq OWNER TO weboll;

--
-- Name: w12_id_w12_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w12_id_w12_seq OWNED BY public.w12.id_w12;


--
-- Name: id_w12; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w12 ALTER COLUMN id_w12 SET DEFAULT nextval('public.w12_id_w12_seq'::regclass);


--
-- Data for Name: w12; Type: TABLE DATA; Schema: public; Owner: weboll
--


SELECT pg_catalog.setval('public.w12_id_w12_seq', 2013, true);

--
-- Name: w12_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.w12
    ADD CONSTRAINT w12_pkey PRIMARY KEY (id_w12);


\set command `echo "curl $DATA_LOCATION/w12.copy"`
COPY public.w12
  FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
