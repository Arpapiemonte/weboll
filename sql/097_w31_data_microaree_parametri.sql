--
-- PostgreSQL database dump
--

-- Dumped from database version 13.7 (Debian 13.7-1.pgdg110+1)
-- Dumped by pg_dump version 13.7 (Debian 13.7-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: w31_data_microaree_parametri; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w31_data_microaree_parametri (
    id_w31_data_microaree_parametri integer NOT NULL,
    numeric_value double precision NOT NULL,
    id_parametro character varying(15) NOT NULL,
    id_w31_data_microaree_livelli integer NOT NULL
);


ALTER TABLE public.w31_data_microaree_parametri OWNER TO weboll;

--
-- Name: w31_data_microaree_parametri_id_w31_data_microaree_parametr_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w31_data_microaree_parametri_id_w31_data_microaree_parametr_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w31_data_microaree_parametri_id_w31_data_microaree_parametr_seq OWNER TO weboll;

--
-- Name: w31_data_microaree_parametri_id_w31_data_microaree_parametr_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w31_data_microaree_parametri_id_w31_data_microaree_parametr_seq OWNED BY public.w31_data_microaree_parametri.id_w31_data_microaree_parametri;


--
-- Name: w31_data_microaree_parametri id_w31_data_microaree_parametri; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_data_microaree_parametri ALTER COLUMN id_w31_data_microaree_parametri SET DEFAULT nextval('public.w31_data_microaree_parametri_id_w31_data_microaree_parametr_seq'::regclass);


--
-- Data for Name: w31_data_microaree_parametri; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w31_data_microaree_parametri (id_w31_data_microaree_parametri, numeric_value, id_parametro, id_w31_data_microaree_livelli) FROM stdin;
\.


--
-- Name: w31_data_microaree_parametri_id_w31_data_microaree_parametr_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w31_data_microaree_parametri_id_w31_data_microaree_parametr_seq', 1, false);


--
-- Name: w31_data_microaree_parametri w31_data_microaree_parametri_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_data_microaree_parametri
    ADD CONSTRAINT w31_data_microaree_parametri_pkey PRIMARY KEY (id_w31_data_microaree_parametri);


--
-- Name: w31_data_microaree_paramet_id_w31_data_microaree_live_b9b50b39; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_data_microaree_paramet_id_w31_data_microaree_live_b9b50b39 ON public.w31_data_microaree_parametri USING btree (id_w31_data_microaree_livelli);


--
-- Name: w31_data_microaree_parametri_id_parametro_93bb3451; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_data_microaree_parametri_id_parametro_93bb3451 ON public.w31_data_microaree_parametri USING btree (id_parametro);


--
-- Name: w31_data_microaree_parametri_id_parametro_93bb3451_like; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_data_microaree_parametri_id_parametro_93bb3451_like ON public.w31_data_microaree_parametri USING btree (id_parametro varchar_pattern_ops);


--
-- Name: w31_data_microaree_parametri w31_data_microaree_p_id_parametro_93bb3451_fk_parametro; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_data_microaree_parametri
    ADD CONSTRAINT w31_data_microaree_p_id_parametro_93bb3451_fk_parametro FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: w31_data_microaree_parametri w31_data_microaree_p_id_w31_data_microare_b9b50b39_fk_w31_data_; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_data_microaree_parametri
    ADD CONSTRAINT w31_data_microaree_p_id_w31_data_microare_b9b50b39_fk_w31_data_ FOREIGN KEY (id_w31_data_microaree_livelli) REFERENCES public.w31_data_microaree_livelli(id_w31_data_microaree_livelli) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

