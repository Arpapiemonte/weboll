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

--
-- Name: w23; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w23 (
    id_w23 bigint NOT NULL,
    data_emissione date DEFAULT ('now'::text)::date NOT NULL,
    numero_bollettino character varying(30) DEFAULT public.w23_numero_bollettino() NOT NULL,
    situazione_meteo text,
    status character(1) DEFAULT 0 NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
    fraserisknat text,
    annotazione text,
    last_update_annotazione timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    id_w23_parent integer
);


ALTER TABLE public.w23 OWNER TO weboll;

--
-- Name: COLUMN w23.status; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.w23.status IS '0 = Draft; 1 = Final';


--
-- Name: w23_id_w23_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w23_id_w23_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w23_id_w23_seq OWNER TO weboll;

--
-- Name: w23_id_w23_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w23_id_w23_seq OWNED BY public.w23.id_w23;


--
-- Name: id_w23; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w23 ALTER COLUMN id_w23 SET DEFAULT nextval('public.w23_id_w23_seq'::regclass);


--
-- Name: w23_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w23
    ADD CONSTRAINT w23_pkey PRIMARY KEY (id_w23);


--
-- Name: TABLE w23; Type: ACL; Schema: public; Owner: weboll
--



--
-- Name: SEQUENCE w23_id_w23_seq; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

