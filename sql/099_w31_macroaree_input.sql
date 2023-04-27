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
-- Name: w31_macroaree_input; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w31_macroaree_input (
    id_w31_macroaree_input integer NOT NULL,
    id_w31_macroaree integer NOT NULL,
    data date NOT NULL,
    deltat integer NOT NULL CHECK (deltat >= -1 AND deltat <= 1),
    rh integer NOT NULL CHECK (rh >= 0 AND rh <= 2),
    ws integer NOT NULL CHECK (ws >= 0 AND ws <= 2), 
    prec integer NOT NULL CHECK (prec >= 0 AND prec <= 2)
);


ALTER TABLE public.w31_macroaree_input OWNER TO weboll;

--
-- Name: w31_macroaree_input_id_w31_macroaree_input_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w31_macroaree_input_id_w31_macroaree_input_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w31_macroaree_input_id_w31_macroaree_input_seq OWNER TO weboll;

--
-- Name: w31_macroaree_input_id_w31_macroaree_input_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w31_macroaree_input_id_w31_macroaree_input_seq OWNED BY public.w31_macroaree_input.id_w31_macroaree_input;


--
-- Name: w31_macroaree_input id_w31_macroaree_input; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_macroaree_input ALTER COLUMN id_w31_macroaree_input SET DEFAULT nextval('public.w31_macroaree_input_id_w31_macroaree_input_seq'::regclass);


--
-- Name: w31_macroaree_input_id_w31_macroaree_input_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w31_macroaree_input_id_w31_macroaree_input_seq', 1, false);


--
-- Name: w31_macroaree_input w31_macroaree_input_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_macroaree_input
    ADD CONSTRAINT w31_macroaree_input_pkey PRIMARY KEY (id_w31_macroaree_input);


--
-- Name: w31_macroaree_input_id_w31_macroaree_666cc076; Type: INDEX; Schema: public; Owner: weboll
--

CREATE INDEX w31_macroaree_input_id_w31_macroaree_666cc076 ON public.w31_macroaree_input USING btree (id_w31_macroaree);


--
-- Name: w31_macroaree_input w31_macroaree_input_id_w31_macroaree_666cc076_fk_w31_macro; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_macroaree_input
    ADD CONSTRAINT w31_macroaree_input_id_w31_macroaree_666cc076_fk_w31_macro FOREIGN KEY (id_w31_macroaree) REFERENCES public.w31_macroaree(id_w31_macroaree) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

