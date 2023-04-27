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
-- Name: w16_data; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w16_data (
    id_w16_data integer DEFAULT nextval('public.w16_data_id_seq'::regclass) NOT NULL,
    id_w16 integer NOT NULL,
    id_ozono_zone smallint NOT NULL,
    data_emissione timestamp(0) without time zone NOT NULL,
    data_scadenza timestamp(0) without time zone NOT NULL,
    id_scadenza integer NOT NULL,
    id_ozono_livelli smallint NOT NULL
);


ALTER TABLE public.w16_data OWNER TO weboll;

--
-- Name: w16_data_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.w16_data
    ADD CONSTRAINT w16_data_pkey PRIMARY KEY (id_w16_data);


--
-- Name: w16_data_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w16_data
    ADD CONSTRAINT w16_data_fkey001 FOREIGN KEY (id_w16) REFERENCES public.w16(id_w16) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w16_data_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w16_data
    ADD CONSTRAINT w16_data_fkey002 FOREIGN KEY (id_ozono_zone) REFERENCES public.ozono_zone(id_ozono_zone) ON UPDATE CASCADE;


--
-- Name: w16_data_fkey003; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w16_data
    ADD CONSTRAINT w16_data_fkey003 FOREIGN KEY (id_ozono_livelli) REFERENCES public.ozono_livelli(id_ozono_livelli) ON UPDATE CASCADE;


--
-- Name: TABLE w16_data; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

