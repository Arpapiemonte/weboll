--
-- PostgreSQL database dump
--

-- Dumped from database version 13.7 (Debian 13.7-1.pgdg110+1)
-- Dumped by pg_dump version 13.7 (Debian 13.7-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: w31; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w31 (
    id_w31 integer NOT NULL,
    start_valid_time timestamp with time zone NOT NULL,
    validity integer NOT NULL,
    next_blt_time timestamp with time zone NOT NULL,
    status character varying(1) NOT NULL,
    last_update timestamp with time zone NOT NULL,
    username character varying(30) NOT NULL,
    seq_num bigint,
    version bigint,
    algoritmo character varying(6) NOT NULL,
    id_w31_parent integer,
    annotazione text
);


ALTER TABLE public.w31 OWNER TO weboll;

--
-- Name: w31_id_w31_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w31_id_w31_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w31_id_w31_seq OWNER TO weboll;

--
-- Name: w31_id_w31_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w31_id_w31_seq OWNED BY public.w31.id_w31;


--
-- Name: w31 id_w31; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31 ALTER COLUMN id_w31 SET DEFAULT nextval('public.w31_id_w31_seq'::regclass);


--
-- Data for Name: w31; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w31 (id_w31, start_valid_time, validity, next_blt_time, status, last_update, username, seq_num, version, algoritmo, id_w31_parent, annotazione) FROM stdin;
\.


--
-- Name: w31_id_w31_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w31_id_w31_seq', 1, false);


--
-- Name: w31 w31_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31
    ADD CONSTRAINT w31_pkey PRIMARY KEY (id_w31);


--
-- PostgreSQL database dump complete
--

