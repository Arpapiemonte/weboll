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
-- Name: w16_conf; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w16_conf (
    id_w16_conf integer NOT NULL,
    id_ozono_aggregazione smallint NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.w16_conf OWNER TO weboll;

--
-- Data for Name: w16_conf; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w16_conf (id_w16_conf, id_ozono_aggregazione, last_update, username) FROM stdin;
1	11	2010-09-14 00:00:00	weboll
\.


--
-- Name: PK_W16_CONF; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.w16_conf
    ADD CONSTRAINT "PK_W16_CONF" PRIMARY KEY (id_w16_conf);


--
-- Name: w16_conf_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w16_conf
    ADD CONSTRAINT w16_conf_fkey001 FOREIGN KEY (id_ozono_aggregazione) REFERENCES public.ozono_aggregazione(id_ozono_aggregazione) ON UPDATE CASCADE DEFERRABLE;


--
-- Name: TABLE w16_conf; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

