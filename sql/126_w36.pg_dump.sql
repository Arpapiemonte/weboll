CREATE TABLE public.w36 (
    id_w36 bigserial,
    seq_num integer,
    data_emissione date NOT NULL DEFAULT 'now'::text::date,
    status character varying(1) NOT NULL,
    note text,
    last_update timestamp with time zone NOT NULL,
    username character varying(30) NOT NULL,
    id_w36_parent bigint,
    chart_max bytea,
    chart_min bytea,
    internal_note text,
    osservati text,
    debug text,
    primary key (id_w36)
);

CREATE TABLE public.w36_data (
    id_w36_data bigserial,
    id_w36 bigint NOT NULL,
    id_venue integer NOT NULL,
    id_time_layouts integer NOT NULL,
    id_parametro character varying(15) NOT NULL,
    id_aggregazione integer NOT NULL,
    numeric_value double precision,
    locked boolean DEFAULT false,
    primary key (id_w36_data)
);

ALTER TABLE ONLY public.w36_data
    ADD CONSTRAINT w36_data_key UNIQUE (id_w36, id_venue, id_time_layouts, id_parametro, id_aggregazione);
ALTER TABLE ONLY public.w36_data
    ADD CONSTRAINT w36_data_fkey001 FOREIGN KEY (id_w36) REFERENCES public.w36(id_w36) 
    ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY public.w36_data
    ADD CONSTRAINT w36_data_fkey002 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) 
    ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY public.w36_data
    ADD CONSTRAINT w36_data_fkey003 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) 
    ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE ONLY public.w36_data
    ADD CONSTRAINT w36_data_fkey004 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) 
    ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE ONLY public.w36_data
    ADD CONSTRAINT w36_data_fkey005 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) 
    ON UPDATE CASCADE ON DELETE SET NULL;


CREATE TABLE public.w36_percentili (
    id_w36_percentili bigserial,
    id_venue integer NOT NULL,
    mese integer NOT NULL,
    giorno integer NOT NULL,
    id_parametro character varying(15) NOT NULL,
    id_aggregazione integer NOT NULL,
    numeric_value double precision,
    numeric_value_bck double precision,
    primary key (id_w36_percentili)
);

ALTER TABLE ONLY public.w36_percentili
    ADD CONSTRAINT w36_percentili_key UNIQUE (id_venue, mese, giorno, id_parametro, id_aggregazione);
ALTER TABLE public.w36_percentili 
    ADD CONSTRAINT w36_percentili_fkey001 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) 
    ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE public.w36_percentili 
    ADD CONSTRAINT w36_percentili_fkey002 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) 
    ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE public.w36_percentili 
    ADD CONSTRAINT w36_percentili_fkey003 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) 
    ON UPDATE CASCADE ON DELETE SET NULL;

CREATE TABLE public.w36_rolling (
    id_w36_rolling bigserial,
    id_w36_data bigint NOT NULL,
    id_w36 bigint NOT NULL,
    id_venue integer NOT NULL,
    id_time_layouts integer NOT NULL,
    id_parametro character varying(15) NOT NULL,
    id_aggregazione integer NOT NULL,
    numeric_value double precision,
    primary key (id_w36_rolling)
);

ALTER TABLE ONLY public.w36_rolling
    ADD CONSTRAINT w36_rolling_key UNIQUE (id_w36_data, id_venue, id_time_layouts, id_parametro, id_aggregazione);
ALTER TABLE public.w36_rolling 
    ADD CONSTRAINT w36_rolling_fkey001 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) 
    ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE public.w36_rolling 
    ADD CONSTRAINT w36_rolling_fkey002 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) 
    ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE public.w36_rolling 
    ADD CONSTRAINT w36_rolling_fkey003 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) 
    ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE ONLY public.w36_rolling
    ADD CONSTRAINT w36_rolling_fkey004 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) 
    ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE ONLY public.w36_rolling
    ADD CONSTRAINT w36_rolling_fkey005 FOREIGN KEY (id_w36_data) REFERENCES public.w36_data(id_w36_data) 
    ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TABLE public.w36_decessi_attesi (
    id_w36_decessi_attesi bigserial,
    id_venue integer NOT NULL,
    numeric_value double precision,
    mese integer NOT NULL,
    giorno integer NOT NULL,
    primary key (id_w36_decessi_attesi)
);

ALTER TABLE ONLY public.w36_decessi_attesi
    ADD CONSTRAINT w36_decessi_attesi_key UNIQUE (id_venue, mese, giorno);
ALTER TABLE public.w36_decessi_attesi 
    ADD CONSTRAINT w36_decessi_attesi_fkey001 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) 
    ON UPDATE CASCADE ON DELETE SET NULL;

CREATE TABLE public.w36_parametri_equazione (
    id_w36_parametri bigserial,
    parametro_epid character varying(15) NOT NULL,
    stima double precision,
    primary key (id_w36_parametri)
);

ALTER TABLE ONLY public.w36_parametri_equazione
    ADD CONSTRAINT w36_parametri_equazione_key UNIQUE (parametro_epid);

CREATE TABLE public.meteo_real_time (
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

ALTER TABLE public.meteo_real_time OWNER TO weboll;

--
-- Name: meteo_real_time_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.meteo_real_time
    ADD CONSTRAINT meteo_real_time_pkey PRIMARY KEY (codice_istat_comune, progr_punto_com, data, ora, id_parametro, id_aggregazione);


--
-- Name: meteo_real_time_idx001; Type: INDEX; Schema: public; Owner: weboll; Tablespace: 
--

CREATE INDEX meteo_real_time_idx001 ON public.meteo_real_time USING btree (codice_istat_comune, progr_punto_com);


--
-- Name: meteo_real_time_idx002; Type: INDEX; Schema: public; Owner: weboll; Tablespace: 
--

CREATE INDEX meteo_real_time_idx002 ON public.meteo_real_time USING btree (data, ora);


--
-- Name: meteo_real_time_idx003; Type: INDEX; Schema: public; Owner: weboll; Tablespace: 
--

CREATE INDEX meteo_real_time_idx003 ON public.meteo_real_time USING btree (id_parametro, id_aggregazione);


--
-- Name: meteo_real_time_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.meteo_real_time
    ADD CONSTRAINT meteo_real_time_fkey001 FOREIGN KEY (id_rete_monit) REFERENCES public.rete_monitoraggio(id_rete_monit) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: meteo_real_time_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.meteo_real_time
    ADD CONSTRAINT meteo_real_time_fkey002 FOREIGN KEY (codice_istat_comune, progr_punto_com) REFERENCES public.stazione_misura(codice_istat_comune, progr_punto_com) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: meteo_real_time_fkey003; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.meteo_real_time
    ADD CONSTRAINT meteo_real_time_fkey003 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: meteo_real_time_fkey004; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.meteo_real_time
    ADD CONSTRAINT meteo_real_time_fkey004 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) ON UPDATE CASCADE ON DELETE CASCADE;


--------------- Nuove aggregazioni per percentili --------------------------------------
INSERT INTO public.aggregazione
(id_aggregazione, descrizione, id_unita_misura, tipo_aggregazione, data_agg, autore_agg)
VALUES(940, '75° percentile', Null, Null, 'now'::text::timestamp(6) with time zone, 'weboll');
INSERT INTO public.aggregazione
(id_aggregazione, descrizione, id_unita_misura, tipo_aggregazione, data_agg, autore_agg)
VALUES(941, '90° percentile', Null, Null, 'now'::text::timestamp(6) with time zone, 'weboll');
INSERT INTO public.aggregazione
(id_aggregazione, descrizione, id_unita_misura, tipo_aggregazione, data_agg, autore_agg)
VALUES(942, '95° percentile', Null, Null, 'now'::text::timestamp(6) with time zone, 'weboll');
	
--------------- Nuove parametri        --------------------------------------
INSERT INTO public.parametro
(id_parametro, denominazione, id_unita_misura, num_decimali, data_agg, autore_agg)
VALUES('ATMAX', 'Temperatura apparente massima', NULL, 1, 'now'::text::timestamp(6) with time zone, 'weboll');	
INSERT INTO public.parametro
(id_parametro, denominazione, id_unita_misura, num_decimali, data_agg, autore_agg)
VALUES('ATMIN', 'Temperatura apparente minima', NULL, 1, 'now'::text::timestamp(6) with time zone, 'weboll');
INSERT INTO public.parametro
(id_parametro, denominazione, id_unita_misura, num_decimali, data_agg, autore_agg)
VALUES('GGCONS', 'Giorni consecutivi di caldo', NULL, 1, 'now'::text::timestamp(6) with time zone, 'weboll');
INSERT INTO public.parametro
(id_parametro, denominazione, id_unita_misura, num_decimali, data_agg, autore_agg)
VALUES('COD_COLORE', 'Codice Colore', NULL, 1, 'now'::text::timestamp(6) with time zone, 'weboll');
INSERT INTO public.parametro
(id_parametro, denominazione, id_unita_misura, num_decimali, data_agg, autore_agg)
VALUES('COD_COLORE_ORIG', 'Codice Colore Originale', NULL, 1, 'now'::text::timestamp(6) with time zone, 'weboll');
INSERT INTO public.parametro
(id_parametro, denominazione, id_unita_misura, num_decimali, data_agg, autore_agg)
VALUES('ATTESI', 'Decessi attesi', NULL, 1, 'now'::text::timestamp(6) with time zone, 'weboll');
INSERT INTO public.parametro
(id_parametro, denominazione, id_unita_misura, num_decimali, data_agg, autore_agg)
VALUES('COD_SALUTE', 'Codice eccessi sanitari', NULL, 1, 'now'::text::timestamp(6) with time zone, 'weboll');
INSERT INTO public.parametro
(id_parametro, denominazione, id_unita_misura, num_decimali, data_agg, autore_agg)
VALUES('WDA', 'indice Warm Day Alert', NULL, 1, 'now'::text::timestamp(6) with time zone, 'weboll');

--------------- Nuove time_layouts        --------------------------------------
INSERT INTO public.time_layouts
(id_time_layouts, start_day_offset, end_day_offset, start_time, end_time, last_update, username, day_offset)
VALUES(300, -3, -3, '00:00:00', '23:59:59', '2024-01-22 09:00:00.000', 'weboll', NULL);
INSERT INTO public.time_layouts
(id_time_layouts, start_day_offset, end_day_offset, start_time, end_time, last_update, username, day_offset)
VALUES(301, -4, -4, '00:00:00', '23:59:59', '2024-01-22 09:00:00.000', 'weboll', NULL);

\c
\set command `echo "curl $DATA_LOCATION/w36.copy"`
COPY w36 FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
\set command `echo "curl $DATA_LOCATION/w36_data.copy"`
COPY w36_data FROM PROGRAM :'command' CSV HEADER;
\set command `echo "curl $DATA_LOCATION/w36_percentili.copy"`
COPY w36_percentili FROM PROGRAM :'command' CSV HEADER;
\set command `echo "curl $DATA_LOCATION/w36_decessi_attesi.copy"`
COPY w36_decessi_attesi FROM PROGRAM :'command' CSV HEADER;
\set command `echo "curl $DATA_LOCATION/w36_parametri_equazione.copy"`
COPY w36_parametri_equazione FROM PROGRAM :'command' CSV HEADER;
\set command `echo "curl $DATA_LOCATION/meteo_real_time.copy"`
COPY meteo_real_time FROM PROGRAM :'command' CSV HEADER;

SELECT setval('w36_id_w36_seq', max(id_w36)) FROM w36;
SELECT setval('w36_data_id_w36_data_seq', max(id_w36_data)) FROM w36_data;
