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
-- Name: w31_aree_giorni_livelli; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w31_aree_giorni_livelli (
    id_w31_aree_giorni_livelli integer NOT NULL,
    soglia_superiore double precision NOT NULL,
    id_w31_giorni integer NOT NULL,
    id_w31_livelli integer NOT NULL,
    id_w31_microaree integer NOT NULL
);


ALTER TABLE public.w31_aree_giorni_livelli OWNER TO weboll;

--
-- Name: w31_aree_giorni_livelli_id_w31_aree_giorni_livelli_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w31_aree_giorni_livelli_id_w31_aree_giorni_livelli_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w31_aree_giorni_livelli_id_w31_aree_giorni_livelli_seq OWNER TO weboll;

--
-- Name: w31_aree_giorni_livelli_id_w31_aree_giorni_livelli_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w31_aree_giorni_livelli_id_w31_aree_giorni_livelli_seq OWNED BY public.w31_aree_giorni_livelli.id_w31_aree_giorni_livelli;


--
-- Name: w31_aree_giorni_livelli id_w31_aree_giorni_livelli; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_aree_giorni_livelli ALTER COLUMN id_w31_aree_giorni_livelli SET DEFAULT nextval('public.w31_aree_giorni_livelli_id_w31_aree_giorni_livelli_seq'::regclass);


--
-- Data for Name: w31_aree_giorni_livelli; Type: TABLE DATA; Schema: public; Owner: weboll
--

INSERT INTO public.w31_aree_giorni_livelli (soglia_superiore, id_w31_giorni, id_w31_livelli, id_w31_microaree) SELECT 0.2, id_w31_giorni, 1, id_w31_microaree FROM public.w31_microaree, public.w31_giorni;

INSERT INTO public.w31_aree_giorni_livelli (soglia_superiore, id_w31_giorni, id_w31_livelli, id_w31_microaree) SELECT 5.2, id_w31_giorni, 2, id_w31_microaree FROM public.w31_microaree, public.w31_giorni;

INSERT INTO public.w31_aree_giorni_livelli (soglia_superiore, id_w31_giorni, id_w31_livelli, id_w31_microaree) SELECT 11.2, id_w31_giorni, 3, id_w31_microaree FROM public.w31_microaree, public.w31_giorni;

INSERT INTO public.w31_aree_giorni_livelli (soglia_superiore, id_w31_giorni, id_w31_livelli, id_w31_microaree) SELECT 21.3, id_w31_giorni, 4, id_w31_microaree FROM public.w31_microaree, public.w31_giorni;

--
-- Name: w31_aree_giorni_livelli_id_w31_aree_giorni_livelli_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w31_aree_giorni_livelli_id_w31_aree_giorni_livelli_seq', 68620, true);


--
-- Name: w31_aree_giorni_livelli w31_aree_giorni_livelli_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_aree_giorni_livelli
    ADD CONSTRAINT w31_aree_giorni_livelli_pkey PRIMARY KEY (id_w31_aree_giorni_livelli);


--
-- Name: w31_aree_giorni_livelli_id_w31_giorni_9f670116; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_aree_giorni_livelli_id_w31_giorni_9f670116 ON public.w31_aree_giorni_livelli USING btree (id_w31_giorni);


--
-- Name: w31_aree_giorni_livelli_id_w31_livelli_d7e8388d; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_aree_giorni_livelli_id_w31_livelli_d7e8388d ON public.w31_aree_giorni_livelli USING btree (id_w31_livelli);


--
-- Name: w31_aree_giorni_livelli_id_w31_microaree_b09f34ae; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_aree_giorni_livelli_id_w31_microaree_b09f34ae ON public.w31_aree_giorni_livelli USING btree (id_w31_microaree);


--
-- Name: w31_aree_giorni_livelli w31_aree_giorni_live_id_w31_giorni_9f670116_fk_w31_giorn; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_aree_giorni_livelli
    ADD CONSTRAINT w31_aree_giorni_live_id_w31_giorni_9f670116_fk_w31_giorn FOREIGN KEY (id_w31_giorni) REFERENCES public.w31_giorni(id_w31_giorni) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: w31_aree_giorni_livelli w31_aree_giorni_live_id_w31_livelli_d7e8388d_fk_w31_livel; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_aree_giorni_livelli
    ADD CONSTRAINT w31_aree_giorni_live_id_w31_livelli_d7e8388d_fk_w31_livel FOREIGN KEY (id_w31_livelli) REFERENCES public.w31_livelli(id_w31_livelli) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: w31_aree_giorni_livelli w31_aree_giorni_live_id_w31_microaree_b09f34ae_fk_w31_micro; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_aree_giorni_livelli
    ADD CONSTRAINT w31_aree_giorni_live_id_w31_microaree_b09f34ae_fk_w31_micro FOREIGN KEY (id_w31_microaree) REFERENCES public.w31_microaree(id_w31_microaree) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

