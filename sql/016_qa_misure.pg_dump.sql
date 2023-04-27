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
-- Name: qa_misure; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.qa_misure (
    id_venue integer NOT NULL,
    data_emissione timestamp(0) without time zone NOT NULL,
    data_scadenza timestamp(0) without time zone NOT NULL,
    id_scadenza integer,
    id_strumentazione smallint NOT NULL,
    id_qa_aggregazione smallint NOT NULL,
    id_qa_parametro character varying(10) NOT NULL,
    valore_originale_num numeric(7,2),
    valore_validato_num numeric(7,2),
    valore_originale_classe integer,
    valore_validato_classe integer,
    valore_originale_txt text,
    valore_validato_txt text,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
    id_qa_misure integer NOT NULL
);


ALTER TABLE public.qa_misure OWNER TO weboll;

--
-- Name: qa_misure_id_qa_misure_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.qa_misure_id_qa_misure_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qa_misure_id_qa_misure_seq OWNER TO weboll;

--
-- Name: qa_misure_id_qa_misure_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.qa_misure_id_qa_misure_seq OWNED BY public.qa_misure.id_qa_misure;


--
-- Name: id_qa_misure; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.qa_misure ALTER COLUMN id_qa_misure SET DEFAULT nextval('public.qa_misure_id_qa_misure_seq'::regclass);


--
-- Name: qa_misure_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.qa_misure
    ADD CONSTRAINT qa_misure_pkey PRIMARY KEY (id_qa_misure);


--
-- Name: TABLE qa_misure; Type: ACL; Schema: public; Owner: weboll
--



--
-- Name: SEQUENCE qa_misure_id_qa_misure_seq; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

