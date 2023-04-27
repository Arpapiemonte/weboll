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
-- Name: meteo_real_time_idro; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.meteo_real_time_idro (
    id_rete_monit character varying(2) NOT NULL,
    codice_istat_comune character varying(6) NOT NULL,
    progr_punto_com integer NOT NULL,
    data date NOT NULL,
    ora time(0) without time zone NOT NULL,
    id_parametro character varying(8) NOT NULL,
    id_aggregazione integer NOT NULL,
    valore_originale numeric(12,3),
    valore_validato numeric(12,3),
    tipologia_validaz character varying(3),
    flag_validaz_autom character varying(1),
    flag_gestore_sistema character varying(1),
    data_agg timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.meteo_real_time_idro OWNER TO weboll;

--
-- Name: meteo_real_time_idro_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.meteo_real_time_idro
    ADD CONSTRAINT meteo_real_time_idro_pkey PRIMARY KEY (codice_istat_comune, progr_punto_com, data, ora, id_parametro, id_aggregazione);


--
-- Name: meteo_real_time_idro_idx001; Type: INDEX; Schema: public; Owner: weboll; Tablespace: 
--

CREATE INDEX meteo_real_time_idro_idx001 ON public.meteo_real_time_idro USING btree (codice_istat_comune, progr_punto_com);


--
-- Name: meteo_real_time_idro_idx002; Type: INDEX; Schema: public; Owner: weboll; Tablespace: 
--

CREATE INDEX meteo_real_time_idro_idx002 ON public.meteo_real_time_idro USING btree (data, ora);


--
-- Name: meteo_real_time_idro_idx003; Type: INDEX; Schema: public; Owner: weboll; Tablespace: 
--

CREATE INDEX meteo_real_time_idro_idx003 ON public.meteo_real_time_idro USING btree (id_parametro, id_aggregazione);


--
-- Name: meteo_real_time_idro_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.meteo_real_time_idro
    ADD CONSTRAINT meteo_real_time_idro_fkey001 FOREIGN KEY (id_rete_monit) REFERENCES public.rete_monitoraggio(id_rete_monit) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: meteo_real_time_idro_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.meteo_real_time_idro
    ADD CONSTRAINT meteo_real_time_idro_fkey002 FOREIGN KEY (codice_istat_comune, progr_punto_com) REFERENCES public.stazione_misura(codice_istat_comune, progr_punto_com) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: meteo_real_time_idro_fkey003; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.meteo_real_time_idro
    ADD CONSTRAINT meteo_real_time_idro_fkey003 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: meteo_real_time_idro_fkey004; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.meteo_real_time_idro
    ADD CONSTRAINT meteo_real_time_idro_fkey004 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TABLE meteo_real_time_idro; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

