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
-- Name: w24_data; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w24_data (
    id_w24 bigint NOT NULL,
    id_allertamento character varying(6) NOT NULL,
    id_time_layouts integer NOT NULL,
    id_parametro character varying(10) NOT NULL,
    numeric_value numeric(7,2) NOT NULL
);


ALTER TABLE public.w24_data OWNER TO weboll;

--
-- Name: w24_data_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w24_data
    ADD CONSTRAINT w24_data_fkey001 FOREIGN KEY (id_w24) REFERENCES public.w24(id_w24) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w24_data_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w24_data
    ADD CONSTRAINT w24_data_fkey002 FOREIGN KEY (id_allertamento) REFERENCES public.aree_allertamento(id_allertamento) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w24_data_fkey003; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w24_data
    ADD CONSTRAINT w24_data_fkey003 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w24_data_fkey004; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w24_data
    ADD CONSTRAINT w24_data_fkey004 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TABLE w24_data; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

