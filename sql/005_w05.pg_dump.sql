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
-- Name: w05; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w05 (
    id_w05 bigint DEFAULT nextval('public.w05_id_seq'::regclass) NOT NULL,
    start_valid_time timestamp(0) without time zone NOT NULL,
    validity integer NOT NULL,
    next_blt_time timestamp(0) without time zone NOT NULL,
    situation text,
    status character(1) DEFAULT 0 NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
    seq_num bigint,
    version bigint,
    id_w05_parent integer,
    situation_image bytea
);


ALTER TABLE public.w05 OWNER TO weboll;

--
-- Name: COLUMN w05.status; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.w05.status IS '0 = Draft; 1 = Sent';


--
-- Name: w05_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.w05
    ADD CONSTRAINT w05_pkey PRIMARY KEY (id_w05);


--
-- Name: TABLE w05; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

