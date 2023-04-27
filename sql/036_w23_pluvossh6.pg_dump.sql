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
-- Name: w23_pluvossh6; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w23_pluvossh6 (
    data date NOT NULL,
    ora time(0) without time zone NOT NULL,
    area character varying(7) NOT NULL,
    valore character varying(20)
);


ALTER TABLE public.w23_pluvossh6 OWNER TO weboll;

--
-- Data for Name: w23_pluvossh6; Type: TABLE DATA; Schema: public; Owner: weboll
--
--
-- Name: w23_pluvossh6_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w23_pluvossh6
    ADD CONSTRAINT w23_pluvossh6_pkey PRIMARY KEY (data, ora, area);


--
-- Name: TABLE w23_pluvossh6; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

