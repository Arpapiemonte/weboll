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
-- Name: w16; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w16 (
    id_w16 integer DEFAULT nextval('public.w16_id_seq'::regclass) NOT NULL,
    start_valid_time timestamp without time zone NOT NULL,
    validity integer NOT NULL,
    next_blt_time timestamp without time zone NOT NULL,
    made_by character(1) DEFAULT 0 NOT NULL,
    note text NOT NULL,
    status character(1) DEFAULT 0 NOT NULL,
    last_update timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
    seq_num bigint,
    version bigint,
    id_w16_parent integer
);


ALTER TABLE public.w16 OWNER TO weboll;

--
-- Name: COLUMN w16.made_by; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.w16.made_by IS '0 = Automatic; 1 = Manual';


--
-- Name: COLUMN w16.status; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.w16.status IS '0 = Draft; 1 = Sent';


--
-- Name: w16_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.w16
    ADD CONSTRAINT w16_pkey PRIMARY KEY (id_w16);


--
-- Name: TABLE w16; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

