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
-- Name: w31_input; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w31_input (
    id_w31_input integer NOT NULL,
    temp double precision NOT NULL,
    umid double precision NOT NULL,
    velv double precision NOT NULL,
    prec double precision NOT NULL,
    data date NOT NULL,
    id_w31_microaree integer NOT NULL
);


ALTER TABLE public.w31_input OWNER TO weboll;

--
-- Name: w31_input_id_w31_input_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w31_input_id_w31_input_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w31_input_id_w31_input_seq OWNER TO weboll;

--
-- Name: w31_input_id_w31_input_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w31_input_id_w31_input_seq OWNED BY public.w31_input.id_w31_input;


--
-- Name: w31_input id_w31_input; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_input ALTER COLUMN id_w31_input SET DEFAULT nextval('public.w31_input_id_w31_input_seq'::regclass);


--
-- Name: w31_input_id_w31_input_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w31_input_id_w31_input_seq', 1, false);


--
-- Name: w31_input w31_input_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_input
    ADD CONSTRAINT w31_input_pkey PRIMARY KEY (id_w31_input);


--
-- Name: w31_input_id_w31_microaree_666cc076; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_input_id_w31_microaree_666cc076 ON public.w31_input USING btree (id_w31_microaree);


--
-- Name: w31_input w31_input_id_w31_microaree_666cc076_fk_w31_micro; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_input
    ADD CONSTRAINT w31_input_id_w31_microaree_666cc076_fk_w31_micro FOREIGN KEY (id_w31_microaree) REFERENCES public.w31_microaree(id_w31_microaree) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

