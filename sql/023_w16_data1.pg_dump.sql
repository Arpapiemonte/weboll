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
-- Name: w16_data1; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w16_data1 (
    id_w16_data integer NOT NULL,
    id_qa_parametro character varying(10) NOT NULL,
    id_ozono_aggregazione smallint NOT NULL,
    valore_num numeric(7,2),
    valore_classe integer,
    id_w16_data1 integer,
    id_strumentazione smallint
);


ALTER TABLE public.w16_data1 OWNER TO weboll;

--
-- Name: w16_data1_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w16_data1
    ADD CONSTRAINT w16_data1_fkey001 FOREIGN KEY (id_w16_data) REFERENCES public.w16_data(id_w16_data) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w16_data1_fkey003; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w16_data1
    ADD CONSTRAINT w16_data1_fkey003 FOREIGN KEY (id_ozono_aggregazione) REFERENCES public.ozono_aggregazione(id_ozono_aggregazione) ON UPDATE CASCADE;


--
-- Name: TABLE w16_data1; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

