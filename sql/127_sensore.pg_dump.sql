CREATE TABLE public.sensore (    codice_istat_comune character varying(6) NOT NULL,    progr_punto_com integer NOT NULL,    id_parametro character varying(8) NOT NULL,    codice_sensore_das integer,    num_decimale_cae integer,    tempo_campionamento integer,    tempo_registrazione integer,    altezza_sensore numeric(6,2),    data_installazione date,    data_agg timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,    autore_agg character varying(30) DEFAULT "current_user"() NOT NULL);
COMMENT ON TABLE public.sensore IS 'Descrive le caratteristiche di un sensore';
ALTER TABLE ONLY public.sensore    ADD CONSTRAINT sensore_pkey PRIMARY KEY (codice_istat_comune, progr_punto_com, id_parametro);
CREATE INDEX sensore_idx001 ON public.sensore USING btree (id_parametro);
ALTER TABLE ONLY public.sensore    ADD CONSTRAINT sensore_fkey001 FOREIGN KEY (codice_istat_comune, progr_punto_com) REFERENCES public.stazione_misura(codice_istat_comune, progr_punto_com) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY public.sensore    ADD CONSTRAINT sensore_fkey002 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON UPDATE CASCADE ON DELETE CASCADE;

\set command `echo "curl $DATA_LOCATION/sensore.copy"`
COPY sensore 
  FROM PROGRAM :'command' CSV HEADER;

create view sensore_stazione_misura as select codice_istat_comune,progr_punto_com,cod_staz_meteo,denominazione,id_parametro from stazione_misura join sensore using (codice_istat_comune,progr_punto_com);


