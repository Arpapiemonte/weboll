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
-- Name: w05_data; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.w05_data (
    id_w05 bigint NOT NULL,
    id_venue integer NOT NULL,
    id_parametro character varying(10) NOT NULL,
    id_aggregazione integer NOT NULL,
    numeric_value numeric(7,2),
    id_trend smallint,
    text_value text,
    id_time_layouts integer NOT NULL,
    start_valid_time timestamp(0) without time zone NOT NULL,
    end_valid_time timestamp(0) without time zone NOT NULL,
    id_w05_data integer NOT NULL
);


ALTER TABLE public.w05_data OWNER TO weboll;

--
-- Name: w05_data_id_w05_data_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w05_data_id_w05_data_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w05_data_id_w05_data_seq OWNER TO weboll;

--
-- Name: w05_data_id_w05_data_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w05_data_id_w05_data_seq OWNED BY public.w05_data.id_w05_data;


--
-- Name: id_w05_data; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_data ALTER COLUMN id_w05_data SET DEFAULT nextval('public.w05_data_id_w05_data_seq'::regclass);


--
-- Name: w05_data_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.w05_data
    ADD CONSTRAINT w05_data_pkey PRIMARY KEY (id_w05_data);


--
-- Name: w05_data_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_data
    ADD CONSTRAINT w05_data_fkey001 FOREIGN KEY (id_w05) REFERENCES public.w05(id_w05) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w05_data_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_data
    ADD CONSTRAINT w05_data_fkey002 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) ON UPDATE CASCADE;


--
-- Name: w05_data_fkey003; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_data
    ADD CONSTRAINT w05_data_fkey003 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON UPDATE CASCADE;


--
-- Name: w05_data_fkey004; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_data
    ADD CONSTRAINT w05_data_fkey004 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) ON UPDATE CASCADE;


--
-- Name: w05_data_fkey005; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_data
    ADD CONSTRAINT w05_data_fkey005 FOREIGN KEY (id_trend) REFERENCES public.trend(id_trend) ON UPDATE CASCADE;


--
-- Name: w05_data_fkey006; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w05_data
    ADD CONSTRAINT w05_data_fkey006 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON UPDATE CASCADE;


--
-- Name: TABLE w05_data; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

