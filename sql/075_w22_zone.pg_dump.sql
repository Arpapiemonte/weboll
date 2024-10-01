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
-- Name: w22_zone; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w22_zone (
    id_w22_zone integer NOT NULL,
    codice_istat_comune character varying(6) NOT NULL,
    progr_punto_com integer NOT NULL,
    denominazione_stazione character varying(80) NOT NULL,
    corso_acqua character varying(30) NOT NULL,
    id_parametro character varying(10)
);


ALTER TABLE public.w22_zone OWNER TO weboll;

--
-- Name: w22_zone_id_w22_zone_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w22_zone_id_w22_zone_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w22_zone_id_w22_zone_seq OWNER TO weboll;

--
-- Name: w22_zone_id_w22_zone_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w22_zone_id_w22_zone_seq OWNED BY public.w22_zone.id_w22_zone;


--
-- Name: id_w22_zone; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w22_zone ALTER COLUMN id_w22_zone SET DEFAULT nextval('public.w22_zone_id_w22_zone_seq'::regclass);


--
-- Data for Name: w22_zone; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w22_zone (id_w22_zone, codice_istat_comune, progr_punto_com, denominazione_stazione, corso_acqua, id_parametro) FROM stdin;
1	004179	700	Racconigi	Maira	PORTATA
2	004171	700	Polonghera	Varaita	PORTATA
3	001300	700	Villafranca	Pellice	PORTATA
4	001272	701	Torino	Dora Riparia	PORTATA
5	001272	702	Torino	Stura di Lanzo	PORTATA
6	001236	700	S. Benigno	Orco	PORTATA
7	001271	900	Tavagnasco	Dora Baltea	PORTATA
9	003096	900	Candoglia	Toce	PORTATA
10	004089	901	Fossano	Stura di Demonte	PORTATA
11	005029	900	Castelnuovo	Belbo	PORTATA
13	006012	700	Basaluzzo	Orba	PORTATA
14	004086	900	Farigliano	Tanaro	PORTATA
15	004003	900	Alba	Tanaro	PORTATA
17	006091	900	Masio	Tanaro	PORTATA
18	006105	700	Montecastello	Tanaro	PORTATA
19	006086	700	Guazzora	Scrivia	PORTATA
20	001058	900	Carignano	Po	PORTATA
16	005005	900	Asti	Tanaro	PORT_FIU
22	001253	700	San Sebastiano	Po	PORTATA
23	002049	900	Crescentino	Po	PORTATA
25	006177	900	Valenza	Po	PORTATA
26	006087	700	Isola S. Antonio	Po	PORTATA
27	003156	900	Verbania	Lago Maggiore *	IDRO
21	001272	703	Torino - Murazzi	Po **	PORTATA
8	018107	700	Palestro	Sesia	PORT_FIU
12	006043	900	Cassine	Bormida	PORT_FIU
24	006039	901	Casale Monferrato	Po	PORT_FIU
\.


--
-- Name: w22_zone_id_w22_zone_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w22_zone_id_w22_zone_seq', 27, true);


--
-- Name: w22_zone_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w22_zone
    ADD CONSTRAINT w22_zone_pkey PRIMARY KEY (id_w22_zone);


--
-- Name: w22_zone_idx001; Type: INDEX; Schema: public; Owner: weboll; Tablespace:
--

CREATE UNIQUE INDEX w22_zone_idx001 ON public.w22_zone USING btree (codice_istat_comune, progr_punto_com);


--
-- Name: w22_zone_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w22_zone
    ADD CONSTRAINT w22_zone_fkey001 FOREIGN KEY (codice_istat_comune, progr_punto_com) REFERENCES public.stazione_misura(codice_istat_comune, progr_punto_com) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TABLE w22_zone; Type: ACL; Schema: public; Owner: weboll
--



--
-- Name: SEQUENCE w22_zone_id_w22_zone_seq; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
