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
-- Name: w31_data_microaree_livelli; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w31_data_microaree_livelli (
    id_w31_data_microaree_livelli integer NOT NULL,
    id_time_layouts integer NOT NULL,
    id_w31 integer NOT NULL,
    id_w31_livelli integer NOT NULL,
    id_w31_microaree integer NOT NULL
);


ALTER TABLE public.w31_data_microaree_livelli OWNER TO weboll;

--
-- Name: w31_data_microaree_livelli_id_w31_data_microaree_livelli_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w31_data_microaree_livelli_id_w31_data_microaree_livelli_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w31_data_microaree_livelli_id_w31_data_microaree_livelli_seq OWNER TO weboll;

--
-- Name: w31_data_microaree_livelli_id_w31_data_microaree_livelli_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w31_data_microaree_livelli_id_w31_data_microaree_livelli_seq OWNED BY public.w31_data_microaree_livelli.id_w31_data_microaree_livelli;


--
-- Name: w31_data_microaree_livelli id_w31_data_microaree_livelli; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_data_microaree_livelli ALTER COLUMN id_w31_data_microaree_livelli SET DEFAULT nextval('public.w31_data_microaree_livelli_id_w31_data_microaree_livelli_seq'::regclass);


--
-- Data for Name: w31_data_microaree_livelli; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w31_data_microaree_livelli (id_w31_data_microaree_livelli, id_time_layouts, id_w31, id_w31_livelli, id_w31_microaree) FROM stdin;
\.


--
-- Name: w31_data_microaree_livelli_id_w31_data_microaree_livelli_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w31_data_microaree_livelli_id_w31_data_microaree_livelli_seq', 1, false);


--
-- Name: w31_data_microaree_livelli w31_data_microaree_livelli_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_data_microaree_livelli
    ADD CONSTRAINT w31_data_microaree_livelli_pkey PRIMARY KEY (id_w31_data_microaree_livelli);


--
-- Name: w31_data_microaree_livelli_id_time_layouts_59c3e743; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_data_microaree_livelli_id_time_layouts_59c3e743 ON public.w31_data_microaree_livelli USING btree (id_time_layouts);


--
-- Name: w31_data_microaree_livelli_id_w31_e9cda33a; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_data_microaree_livelli_id_w31_e9cda33a ON public.w31_data_microaree_livelli USING btree (id_w31);


--
-- Name: w31_data_microaree_livelli_id_w31_livelli_d24976f7; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_data_microaree_livelli_id_w31_livelli_d24976f7 ON public.w31_data_microaree_livelli USING btree (id_w31_livelli);


--
-- Name: w31_data_microaree_livelli_id_w31_microaree_8a783b9c; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_data_microaree_livelli_id_w31_microaree_8a783b9c ON public.w31_data_microaree_livelli USING btree (id_w31_microaree);


--
-- Name: w31_data_microaree_livelli w31_data_microaree_l_id_time_layouts_59c3e743_fk_time_layo; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_data_microaree_livelli
    ADD CONSTRAINT w31_data_microaree_l_id_time_layouts_59c3e743_fk_time_layo FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: w31_data_microaree_livelli w31_data_microaree_l_id_w31_livelli_d24976f7_fk_w31_livel; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_data_microaree_livelli
    ADD CONSTRAINT w31_data_microaree_l_id_w31_livelli_d24976f7_fk_w31_livel FOREIGN KEY (id_w31_livelli) REFERENCES public.w31_livelli(id_w31_livelli) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: w31_data_microaree_livelli w31_data_microaree_l_id_w31_microaree_8a783b9c_fk_w31_micro; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_data_microaree_livelli
    ADD CONSTRAINT w31_data_microaree_l_id_w31_microaree_8a783b9c_fk_w31_micro FOREIGN KEY (id_w31_microaree) REFERENCES public.w31_microaree(id_w31_microaree) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: w31_data_microaree_livelli w31_data_microaree_livelli_id_w31_e9cda33a_fk_w31_id_w31; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_data_microaree_livelli
    ADD CONSTRAINT w31_data_microaree_livelli_id_w31_e9cda33a_fk_w31_id_w31 FOREIGN KEY (id_w31) REFERENCES public.w31(id_w31) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

