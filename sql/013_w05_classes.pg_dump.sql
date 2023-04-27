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
-- Name: w05_classes; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w05_classes (
    id_w05 integer NOT NULL,
    id_venue integer NOT NULL,
    id_parametro character varying(10) NOT NULL,
    id_aggregazione integer NOT NULL,
    id_classes_value smallint NOT NULL,
    id_classes smallint NOT NULL,
    id_time_layouts integer NOT NULL,
    start_valid_time timestamp(0) without time zone NOT NULL,
    end_valid_time timestamp(0) without time zone NOT NULL,
    id_w05_classes integer NOT NULL
);


ALTER TABLE public.w05_classes OWNER TO weboll;

--
-- Name: w05_classes_id_w05_classes_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w05_classes_id_w05_classes_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w05_classes_id_w05_classes_seq OWNER TO weboll;

--
-- Name: w05_classes_id_w05_classes_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w05_classes_id_w05_classes_seq OWNED BY public.w05_classes.id_w05_classes;


--
-- Name: id_w05_classes; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_classes ALTER COLUMN id_w05_classes SET DEFAULT nextval('public.w05_classes_id_w05_classes_seq'::regclass);


--
-- Name: w05_classes_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w05_classes
    ADD CONSTRAINT w05_classes_pkey PRIMARY KEY (id_w05_classes);


--
-- Name: w05_classes_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_classes
    ADD CONSTRAINT w05_classes_fkey001 FOREIGN KEY (id_w05) REFERENCES public.w05(id_w05) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w05_classes_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_classes
    ADD CONSTRAINT w05_classes_fkey002 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) ON UPDATE CASCADE;


--
-- Name: w05_classes_fkey003; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_classes
    ADD CONSTRAINT w05_classes_fkey003 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON UPDATE CASCADE;


--
-- Name: w05_classes_fkey004; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_classes
    ADD CONSTRAINT w05_classes_fkey004 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) ON UPDATE CASCADE;


--
-- Name: w05_classes_fkey005; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_classes
    ADD CONSTRAINT w05_classes_fkey005 FOREIGN KEY (id_classes_value) REFERENCES public.classes_value(id_classes_value) ON UPDATE CASCADE;


--
-- Name: w05_classes_fkey006; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_classes
    ADD CONSTRAINT w05_classes_fkey006 FOREIGN KEY (id_classes) REFERENCES public.classes(id_classes) ON UPDATE CASCADE;


--
-- Name: w05_classes_fkey007; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_classes
    ADD CONSTRAINT w05_classes_fkey007 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON UPDATE CASCADE;


--
-- Name: TABLE w05_classes; Type: ACL; Schema: public; Owner: weboll
--


ALTER TABLE public.w05 ALTER COLUMN id_w05_parent TYPE bigint;
ALTER TABLE public.w05_data ALTER COLUMN id_w05_data TYPE bigint;
ALTER TABLE public.w05_classes ALTER COLUMN id_w05 TYPE bigint;
ALTER TABLE public.w05_classes ALTER COLUMN id_w05_classes TYPE bigint; 

--
-- PostgreSQL database dump complete
--
