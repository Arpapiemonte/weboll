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
-- Name: ozono_zone; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.ozono_zone (
    id_ozono_zone smallint NOT NULL,
    zone character(1) NOT NULL,
    descrizione character varying(60) NOT NULL,
    valid_from timestamp(0) without time zone NOT NULL,
    valid_to timestamp without time zone DEFAULT 'infinity'::timestamp without time zone NOT NULL,
    last_update timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.ozono_zone OWNER TO weboll;

--
-- Data for Name: ozono_zone; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.ozono_zone (id_ozono_zone, zone, descrizione, valid_from, valid_to, last_update, username) FROM stdin;
1	A	Alpi Settentrionali	2010-05-28 00:00:00	9999-12-30 00:00:00	2010-05-21 14:29:38	weboll
2	B	Alpi Occidentali	2010-05-28 00:00:00	9999-12-30 00:00:00	2010-05-21 14:29:38	weboll
3	C	Piemonte centro-meridionale	2010-05-28 00:00:00	9999-12-30 00:00:00	2010-05-21 14:29:38	weboll
4	D	Piemonte centro-settentrionale	2010-05-28 00:00:00	9999-12-30 00:00:00	2010-05-21 14:29:38	weboll
\.


--
-- Name: ozono_zone_id_ozono_zone_key; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.ozono_zone
    ADD CONSTRAINT ozono_zone_id_ozono_zone_key UNIQUE (id_ozono_zone);


--
-- Name: ozono_zone_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.ozono_zone
    ADD CONSTRAINT ozono_zone_pkey PRIMARY KEY (zone, valid_from, valid_to);


--
-- Name: TABLE ozono_zone; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

