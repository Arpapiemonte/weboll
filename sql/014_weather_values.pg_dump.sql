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
-- Name: weather_values; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.weather_values (
    id_venue integer NOT NULL,
    start_time timestamp(0) without time zone NOT NULL,
    end_time timestamp(0) without time zone NOT NULL,
    id_time_layouts integer NOT NULL,
    id_parametro character varying(10) NOT NULL,
    id_aggregazione integer NOT NULL,
    original_numeric_values numeric(7,2),
    validated_numeric_values numeric(7,2),
    original_text_values text,
    validated_text_values text,
    original_trend integer,
    validated_trend integer,
    id_query_numeric bigint,
    id_query_text bigint,
    cod_staz_meteo character varying(5),
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"(),
    id_weather_values integer NOT NULL
);


ALTER TABLE public.weather_values OWNER TO weboll;

--
-- Name: weather_values_id_weather_values_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.weather_values_id_weather_values_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.weather_values_id_weather_values_seq OWNER TO weboll;

--
-- Name: weather_values_id_weather_values_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.weather_values_id_weather_values_seq OWNED BY public.weather_values.id_weather_values;


--
-- Name: id_weather_values; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.weather_values ALTER COLUMN id_weather_values SET DEFAULT nextval('public.weather_values_id_weather_values_seq'::regclass);

--
-- Name: weather_values_id_weather_values_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.weather_values_id_weather_values_seq', 146848, true);


--
-- Name: weather_values_key; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.weather_values
    ADD CONSTRAINT weather_values_key UNIQUE (id_venue, start_time, end_time, id_time_layouts, id_parametro, id_aggregazione);


--
-- Name: weather_values_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.weather_values
    ADD CONSTRAINT weather_values_pkey PRIMARY KEY (id_weather_values);


--
-- Name: weather_values_tr; Type: TRIGGER; Schema: public; Owner: weboll
--

-- è da riattivare in produzione
-- CREATE TRIGGER weather_values_tr AFTER UPDATE ON public.weather_values FOR EACH ROW EXECUTE PROCEDURE public.weather_values_fn();


--
-- Name: weather_values_aggregazione_fk; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.weather_values
    ADD CONSTRAINT weather_values_aggregazione_fk FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) ON DELETE CASCADE;


--
-- Name: weather_values_original_trend_fk; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.weather_values
    ADD CONSTRAINT weather_values_original_trend_fk FOREIGN KEY (original_trend) REFERENCES public.trend(id_trend) ON DELETE CASCADE;


--
-- Name: weather_values_parametro_fk; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.weather_values
    ADD CONSTRAINT weather_values_parametro_fk FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON DELETE CASCADE;


--
-- Name: weather_values_time_layouts_fk; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.weather_values
    ADD CONSTRAINT weather_values_time_layouts_fk FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON DELETE CASCADE;


--
-- Name: weather_values_validated_trend_fk; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.weather_values
    ADD CONSTRAINT weather_values_validated_trend_fk FOREIGN KEY (validated_trend) REFERENCES public.trend(id_trend) ON DELETE CASCADE;


--
-- Name: TABLE weather_values; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
