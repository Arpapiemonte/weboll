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

--SET default_with_oids = false;

--
-- Name: parametro; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.parametro (
    id_parametro character varying(15) NOT NULL,
    denominazione character varying NOT NULL,
    id_unita_misura character varying(2),
    num_decimali integer,
    data_agg timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    autore_agg character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.parametro OWNER TO weboll;

--
-- Name: TABLE parametro; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON TABLE public.parametro IS 'Contiene l''elenco dei parametri';


--
-- Data for Name: parametro; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.parametro (id_parametro, denominazione, id_unita_misura, num_decimali, data_agg, autore_agg) FROM stdin;
PORTATAV	Portata ottenuta dalla misurazione della velocità	14	3	2010-07-20 00:00:00	weboll
VELQ	Velocità superficiale del corso d'acqua	22	1	2010-07-20 00:00:00	weboll
IDROL	Livello idrometrico - Idrometro sul lago che compare nei bollettini di allerta per il quale si effettua il controllo delle anomalie	13	2	2011-06-09 00:00:00	weboll
IDROL1	Livello idrometrico - Idrometro sul lago che non compare nei bollettini di allerta ma per il quale si effettua il controllo delle anomalie	13	2	2011-06-09 00:00:00	weboll
COR_CELL	Corrente cella	11	2	2011-11-10 00:00:00	weboll
CAL_SPAN	Cal span (calibrazione dell'analizzatore di ozono)	98	\N	2011-05-25 00:00:00	weboll
GAMMA	Radiazione Gamma (media di Gamma1 e/o Gamma2)	40	1	2006-02-17 00:00:00	weboll
GAMMA3	Radiazioni Gamma 3	42	0	2007-05-17 00:00:00	weboll
RADD_UVE	Radiometro UV-E	10	3	2007-11-22 00:00:00	weboll
NIVOBARO	Pressione del manto nevoso	43	\N	2009-01-26 00:00:00	weboll
TERM_UVE	Temperatura Radiometro UV-E	02	3	2007-11-22 00:00:00	weboll
CAL_ZERO	Cal zero (calibrazione dell'analizzatore di ozono)	98	\N	2011-05-25 00:00:00	weboll
OZONO	Ozono	31	\N	2011-05-25 00:00:00	weboll
RETE_KO	Mancanza corrente elettrica	98	\N	2011-05-25 00:00:00	weboll
SYS_OK	System OK (funzionamento dell'analizzatore di ozono)	98	\N	2011-05-25 00:00:00	weboll
TERMA1	Temperatura dell'aria 1	02	1	2011-05-25 00:00:00	weboll
TERMA2	Temperatura dell'aria 2	02	1	2011-05-25 00:00:00	weboll
TERMN1	Temperatura della neve a 0 cm	02	1	2011-05-25 00:00:00	weboll
TERMN4	Temperatura della neve a 60 cm	02	1	2011-05-25 00:00:00	weboll
VBATT	Tensione batteria	10	1	2011-05-25 00:00:00	weboll
IGRO	Umidita' dell'aria	05	0	2006-11-17 00:00:00	weboll
IDRO1	Livello idrometrico - Idrometro che non compare nei bollettini di allerta ma per il quale si effettua il controllo delle anomalie	13	2	2010-10-04 00:00:00	weboll
CUM_NIVO	Cumulative snow sum	01	\N	2002-11-15 00:00:00	weboll
CUM_PLUV	Cumulative water sum	01	\N	2002-11-15 00:00:00	weboll
HW_ERR	Hardware error	98	\N	2002-11-15 00:00:00	weboll
PLUV_15M	Livello pioggia sui 15 minuti	01	1	2004-09-20 00:00:00	weboll
PLUV_30M	Livello pioggia sui 30 minuti	01	1	2001-10-15 00:00:00	weboll
BARO	Pressione atmosferica	07	0	2006-11-17 00:00:00	weboll
VIS_1M	Visibility one minute average (max 50 km)	30	\N	2002-11-15 00:00:00	weboll
VIS_ALA	Visibility alarm	98	\N	2002-11-15 00:00:00	weboll
DIRV	Direzione vento (vettoriale)	03	0	2006-11-17 00:00:00	weboll
DIRVR	Direzione vento riscaldato (vettoriale)	03	0	1999-03-17 00:00:00	weboll
PLUV_01M	Livello pioggia al minuto	01	1	2001-10-15 00:00:00	weboll
COP_NUV1	Copertura primo strato di nuvole	19	\N	2003-03-21 00:00:00	weboll
IDRO	Livello idrometrico - Idrometro che compare nei bollettini di allerta per il quale si effettua il controllo delle anomalie	13	2	2006-11-17 00:00:00	weboll
COP_NUV2	Copertura secondo strato di nuvole	19	\N	2003-03-21 00:00:00	weboll
COP_NUV3	Copertura terzo strato di nuvole	19	\N	2003-03-21 00:00:00	weboll
COP_NUV4	Copertura quarto strato di nuvole	19	\N	2003-03-21 00:00:00	weboll
GAMDQB	Data Quality Bits delle Radiazioni Gamma	98	0	2005-11-23 00:00:00	weboll
NIVO	Altezza neve	13	2	2006-11-17 00:00:00	weboll
GAMMA1	Radiazioni Gamma 1	40	0	2005-11-23 00:00:00	weboll
GAMMA2	Radiazioni Gamma 2	40	0	2005-11-23 00:00:00	weboll
PLUV	Livello pioggia sui 10 minuti	01	1	2006-11-17 00:00:00	weboll
PLUVR	Livello pioggia riscaldato	01	1	1999-03-17 00:00:00	weboll
RADD	Radiazione solare diretta (globale)	09	0	2006-11-17 00:00:00	weboll
TERMA	Temperatura dell'aria	02	1	2006-11-17 00:00:00	weboll
RADR	Radiazione solare riflessa	09	0	2009-01-23 00:00:00	weboll
RISCP	Riscaldatore pluviometro	99	0	2009-01-26 00:00:00	weboll
VELV	Velocita' vento (vettoriale)	22	1	2006-11-17 00:00:00	weboll
VELV1	Velocita' vento 1 (vettoriale)	22	1	2006-11-17 00:00:00	weboll
VELV2	Velocita' vento 2 (vettoriale)	22	1	2006-11-17 00:00:00	weboll
VELVR	Velocita' vento riscaldato (vettoriale)	22	1	1999-03-17 00:00:00	weboll
DIRV1	Direzione vento 1 (vettoriale)	03	0	2006-11-17 00:00:00	weboll
DIRV2	Direzione vento 2 (vettoriale)	03	0	2006-11-17 00:00:00	weboll
RISCA	Riscaldatore anemometro	99	\N	1999-05-07 00:00:00	weboll
VIS_ORIZ	Visibilita' orizzontale	13	\N	2001-03-06 00:00:00	weboll
BARO_LM	Pressione al livello del mare	07	0	2001-03-06 00:00:00	weboll
COP_NB	Copertura nubi basse	19	\N	2001-03-06 00:00:00	weboll
IDRO2	Livello idrometrico (2) - Idrometro che non compare nei bollettini di allerta ma per il quale si effettua il controllo delle anomalie	13	2	2002-07-25 00:00:00	weboll
IDROS	Livello idrometrico - Idrometro che non compare nei bollettini di allerta e per il quale non si effettua il controllo delle anomalie	13	2	2002-07-25 00:00:00	weboll
VELS	Velocita' vento (scalare)	22	1	2006-11-17 00:00:00	weboll
VELR	Velocita' vento (raffica)	22	1	2006-11-17 00:00:00	weboll
DIRR	Direzione vento (raffica)	03	0	2006-11-17 00:00:00	weboll
VIS_10M	Visibility 10 minutes average (max 50 km)	30	\N	2002-11-15 00:00:00	weboll
WTH_INS	Instant present weather (NWS codes)	99	\N	2002-11-15 00:00:00	weboll
WTH_INS1	Instant present weather (WMO codes)	99	\N	2002-11-15 00:00:00	weboll
WTH_15M	15 minutes present weather (WMO codes)	99	\N	2002-11-15 00:00:00	weboll
WTH_1H	1 hour present weather (WMO codes)	99	\N	2002-11-15 00:00:00	weboll
PLUV_FD	Precipitation (volume) intensity mm/h	01	\N	2002-11-15 00:00:00	weboll
VELVMX10	Velocita' vento (max sui 10 minuti)	22	1	2004-04-13 00:00:00	weboll
DIRVMX10	Direzione vento (direzione della massima raffica sui 10 minuti)	03	0	2004-04-13 00:00:00	weboll
PCUM	Contatore precipitazioni (da DVD CAE, max 4096)	98	\N	2004-04-23 00:00:00	weboll
RADN	Radiazione solare netta	09	0	2004-09-20 00:00:00	weboll
VELU	Velocita' vento ultrasonica	22	1	2004-09-20 00:00:00	weboll
DIRU	Direzione vento ultrasonica	03	0	2004-09-20 00:00:00	weboll
VELW	Velocita' vento verticale	22	1	2004-09-20 00:00:00	weboll
FRZLVL	Zero Termico - Freezing Level	\N	\N	2010-05-21 00:00:00	weboll
FOG_INDEX	Indice di nebbia	\N	\N	2007-03-02 00:00:00	weboll
FWI_INDEX	Fire bulletin FWI	\N	1	2007-05-04 00:00:00	weboll
FFMC_INDEX	Fire bulletin FFMC	\N	1	2007-05-04 00:00:00	weboll
DMC_INDEX	Fire bulletin DMC	\N	1	2007-05-04 00:00:00	weboll
HAZE_INDEX	Indice di foschia	\N	\N	2007-03-02 00:00:00	weboll
ISI_INDEX	Fire bulletin ISI	\N	1	2007-05-04 00:00:00	weboll
RISK_FOG	Rischio di nebbia (Vigilanza)	\N	\N	2011-10-10 00:00:00	weboll
RISK_RAIN	Rischio di pioggia (Vigilanza)	\N	\N	2011-10-10 00:00:00	weboll
RISK_SNOW	Rischio di neve (Vigilanza)	\N	\N	2011-10-10 00:00:00	weboll
RISK_STORM	Rischio di temporali (Vigilanza)	\N	\N	2011-10-10 00:00:00	weboll
RISK_TCOLD	Rischio anomalia temperatura minima (Vigilanza)	\N	\N	2011-10-10 00:00:00	weboll
RISK_THOT	Rischio anomalia temperatura massima (Vigilanza)	\N	\N	2011-10-10 00:00:00	weboll
RISK_WIND	Rischio di vento (Vigilanza)	\N	\N	2011-10-10 00:00:00	weboll
RS	Rain State (IceCast)	\N	\N	2010-03-12 00:00:00	weboll
SKY_CONDIT	Stato del cielo (tempo prevalente)	\N	\N	2005-03-03 00:00:00	weboll
SNOW_LEV	Quota neve	\N	\N	2010-02-26 00:00:00	weboll
SKY_06	Tipo di tempo su 6 ore (Algoritmo tipo di tempo)	\N	\N	2011-10-10 00:00:00	weboll
SKY_12	Tipo di tempo su 12 ore (Algoritmo tipo di tempo)	\N	\N	2011-10-10 00:00:00	weboll
SKY_24	Tipo di tempo su 24 ore (Algoritmo tipo di tempo)	\N	\N	2011-10-10 00:00:00	weboll
TC	Total Cloud Amount (IceCast)	\N	\N	2010-03-12 00:00:00	weboll
TD	Dew Point Temperature (IceCast)	\N	\N	2010-03-12 00:00:00	weboll
TERMA_1500	Temperatura dell'aria a 1500m	02	\N	2010-02-26 00:00:00	weboll
TERMA_2000	Temperatura dell'aria a 2000m	02	\N	2010-02-26 00:00:00	weboll
TERMA_700	Temperatura dell'aria a 700m	02	\N	2010-02-26 00:00:00	weboll
BUI_INDEX	Fire bulletin BUI	\N	1	2007-05-04 00:00:00	weboll
COP_TOT	Copertura nuvolosa totale	19	\N	2005-03-03 00:00:00	weboll
CT	Cloud Type (IceCast)	\N	\N	2010-03-12 00:00:00	weboll
DC_INDEX	Fire bulletin DC	\N	1	2007-05-04 00:00:00	weboll
ZERO	Zero Termico	\N	\N	2005-03-03 00:00:00	weboll
WINDCHILL	Wind chill	\N	\N	2005-03-03 00:00:00	weboll
WINDGUSTS	Raffica di vento	\N	\N	2005-03-03 00:00:00	weboll
REINF	Rinforzi	\N	\N	2007-06-25 00:00:00	weboll
FOEHN	Foehn	\N	\N	2007-06-25 00:00:00	weboll
VIS	Visibilita'	\N	\N	2007-06-25 00:00:00	weboll
TERMA_MAX	Temperatura massima dell'aria	02	1	2006-10-31 00:00:00	weboll
TERMA_MIN	Temperatura minima dell'aria	02	1	2006-10-31 00:00:00	weboll
WFOP	Altri fenomeni	\N	\N	2010-01-28 00:00:00	weboll
WFR	Previsione meteo	\N	\N	2010-01-28 00:00:00	weboll
CUM_NIVO_L400	Cumulative snow sum < 400m	01	\N	2012-02-16 00:00:00	weboll
CUM_NIVO_L700	Cumulative snow sum < 700m	01	\N	2012-02-16 00:00:00	weboll
CUM_NIVO_L1000	Cumulative snow sum < 1000m	01	\N	2012-02-16 00:00:00	weboll
SNOW	Neve	\N	\N	2021-04-21 11:13:44	weboll
STORM	Classe temporali	\N	\N	2021-04-21 11:13:44	weboll
WIND_CLASS	WIND_CLASS	\N	\N	2021-04-14 11:50:43	weboll
DIRV_CLASS	DIRV_CLASS	\N	\N	2021-04-14 11:50:57	weboll
PREC_CLASS	PREC_CLASS	\N	\N	2021-04-14 11:51:08	weboll
VELR_1500	VELR_1500	\N	\N	2021-04-14 11:51:23	weboll
VELR_2000	VELR_2000	\N	\N	2021-04-14 11:51:32	weboll
VELR_700	VELR_700	\N	\N	2021-04-14 11:51:42	weboll
VELV_1500	VELV_1500	\N	\N	2021-04-14 11:51:57	weboll
VELV_2000	VELV_2000	\N	\N	2021-04-14 11:52:06	weboll
VELV_700	VELV_700	\N	\N	2021-04-14 11:52:14	weboll
WIND_BEAUF	WIND_BEAUF	\N	\N	2021-04-14 11:52:27	weboll
PARAT	Posizione Paratoia 	98	0	2020-03-04 00:00:00	weboll
RISK_FROST	Rischio di gelate	\N	\N	2016-11-11 15:48:30	weboll
PLUV1	Livello pioggia generico	01	1	2017-07-18 11:47:24	weboll
PARAT1	Posizione Paratoia 1 	98	0	2020-03-04 00:00:00	weboll
TRAVSTAT	Stato della Traversa  	98	0	2020-05-14 00:00:00	weboll
LIV_SF	Livello sfioro traversa/paratoia	13	2	2020-07-20 00:00:00	weboll
PORT_SF	Portata sfioro traversa/paratoia	14	1	2020-07-20 00:00:00	weboll
LIVMTRAV	Livello monte traversa	13	2	2020-07-20 00:00:00	weboll
PORT_TUR	Portata turbinata	32	3	2015-04-09 00:00:00	weboll
PARAPER	Apertura paratoria	05	0	2020-07-20 00:00:00	weboll
PARAPER1	Apertura paratoria 1	05	0	2020-07-20 00:00:00	weboll
PORTATA	Portata	14	3	2013-07-19 00:00:00	weboll
SNOW_400	Neve (cm) da 0 a 400 m	06	1	2014-06-17 10:51:13	weboll
SNOW_700	Neve (cm) da 400 a 700 m	06	1	2014-06-17 10:51:45	weboll
PLUV_OTT	Precipitazione pluviometro a peso	01	2	2014-07-07 00:00:00	weboll
SNOW_1000	Neve (cm) da 700 a 1000 m	06	1	2014-06-17 10:52:07	weboll
PORT_AFF	Portata affluente	14	3	2014-12-18 00:00:00	weboll
PARAGONF	Paratoia Gonfiabile	98	0	2015-11-12 00:00:00	weboll
STATOP	Stato della stazione	98	0	2016-05-10 00:00:00	weboll
TERMA_F1	Temperatura dell'aria anomalia termica	02	1	2017-05-30 11:54:28	weboll
TERMA_F2	Temperatura dell'aria anomalia termica	02	1	2017-05-30 11:55:03	weboll
TERMAMAX	Temperatura massima dell'aria	02	1	2019-01-14 00:00:00	weboll
TERMA_F	Temperatura dell'aria anomalia termica	02	1	2017-07-10 14:41:58	weboll
PARASTA	Stato paratorie (aperto / chiuso)	98	0	2020-07-20 00:00:00	weboll
PORT_CUM	Portata totale turbinata e sfioro traversa/paratoia	32	3	2020-08-31 00:00:00	weboll
PORT_T	Portata totale al netto di derivazioni	14	3	2007-09-21 00:00:00	weboll
RISK_VAL	Rischio pericolo valanghe	\N	\N	2018-09-04 15:06:41	weboll
TERMAMIN	Temperatura minima dell'aria	02	1	2019-01-14 00:00:00	weboll
IGROMAX	Umidita' massima dell'aria	05	0	2019-01-15 00:00:00	weboll
IGROMIN	Umidita' minima dell'aria	05	0	2019-01-15 00:00:00	weboll
SNOW_2000	Neve (cm) in quota	06	1	2014-06-17 10:49:18	weboll
PORTATA1	Portata 1	14	3	2014-10-21 08:49:30	weboll
ORARHMAX	offset alle ore 00 dell'umidità relativa massima giornaliera	26	0	2020-10-07 00:00:00	weboll
ORARHMIN	offset alle ore 00 dell'umidità relativa minima giornaliera	26	0	2020-10-07 00:00:00	weboll
ORATMAX	offset alle ore 00 della temperatura massima giornaliera	26	0	2020-09-29 00:00:00	weboll
ORATMIN	offset alle ore 00 della temperatura minima giornaliera	26	0	2020-09-29 00:00:00	weboll
ORAVRMAX	offset alle ore 00 della velocita'  massima raffica giornaliera	26	0	2020-11-09 00:00:00	weboll
VELRMAX	Velocita' vento (massima raffica giornaliera)	22	1	2020-11-09 00:00:00	weboll
NIVO1	Altezza neve 1	13	2	2006-11-17 00:00:00	weboll
IDROCC	Livello idrometrico - Idrometro in centro alveo che compare nei bollettini di allerta per il quale si effettua il controllo delle anomalie	13	2	2021-03-16 00:00:00	weboll
IDRODX	Livello idrometrico - Idrometro in sponda destra  che compare nei bollettini di allerta per il quale si effettua il controllo delle anomalie	13	2	2021-03-16 00:00:00	weboll
IDROSX	Livello idrometrico - Idrometro in sponda sinistra  che compare nei bollettini di allerta per il quale si effettua il controllo delle anomalie	13	2	2021-03-16 00:00:00	weboll
IDRODER	Livello idrometrico - Idrometro su canale di derivazione	13	2	2021-04-07 00:00:00	weboll
PORTDER	Portata derivata (da canaledi derivazione centrale)	14	3	2021-04-07 00:00:00	weboll
PARALIV	Livello altezza apertura paratoia in metri	13	3	2021-09-06 00:00:00	weboll
PARALIV1	Livello altezza apertura paratoia 1 in metri	13	3	2021-09-06 00:00:00	weboll
RETE1_KO	Mancanza corrente elettrica 1	98	\N	2021-10-27 00:00:00	weboll
RETE2_KO	Mancanza corrente elettrica 2	98	\N	2021-10-27 00:00:00	weboll
PORT_FIU	Portata fiume: totale portate al netto di derivazioni	14	3	2020-09-18 10:11:30	weboll
PORT_NAT	Portata naturale: totale portate fiume e derivazioni	14	3	2020-09-18 10:11:34	weboll
ORAT1MAX	offset alle ore 00 della temperatura massima 1 giornaliera	26	0	2024-07-16 00:00:00	weboll
TERM1MAX	Temperatura massima dell'aria terma1	02	1	2024-07-16 00:00:00	weboll
BAROMAX	Pressione atmosferica massima	07	1	2020-11-18 00:00:00	weboll
ORABMAX	offset alle ore 00 della pressione massima giornaliera	26	1	2020-11-18 00:00:00	weboll
ORAT1MIN	offset alle ore 00 della temperatura minima 1 giornaliera	26	0	2024-07-16 00:00:00	weboll
TERM1MIN	Temperatura minima dell'aria terma1	02	1	2024-07-16 00:00:00	weboll
BAROMIN	Pressione atmosferica minima	07	1	2020-11-18 00:00:00	weboll
ORABMIN	offset alle ore 00 della pressione minima giornaliera	26	1	2020-11-18 00:00:00	weboll
VELR1	Velocità vento 1 (raffica)	22	1	2023-02-08 00:00:00	weboll
VELS1	Velocita' vento 1 (scalare)	22	1	2023-02-08 00:00:00	weboll
TERMN10	Temperatura della neve a 180 cm	02	1	2017-10-09 07:51:25	weboll
TERMN11	Temperatura della neve a 200 cm	02	1	2017-10-09 07:51:25	weboll
TERMN12	Temperatura della neve a 220 cm	02	1	2017-10-09 07:51:25	weboll
TERMN13	Temperatura della neve a 240 cm	02	1	2017-10-09 07:51:25	weboll
TERMN14	Temperatura della neve a 260 cm	02	1	2017-10-09 07:51:25	weboll
TERMN15	Temperatura della neve 280 cm	02	1	2017-10-09 07:51:25	weboll
TERMN16	Temperatura della neve 300 cm	02	1	2017-10-09 07:51:25	weboll
TERMN17	Temperatura della neve 320 cm	02	1	2017-10-09 07:51:25	weboll
TERMN18	Temperatura della neve a 340 cm	02	1	2017-10-09 07:51:25	weboll
TERMN19	Temperatura della neve a 360 cm	02	1	2017-10-09 07:51:25	weboll
TERMN2	Temperatura della neve a 20 cm	02	1	2017-10-09 07:51:25	weboll
TERMN20	Temperatura della neve a 380 cm	02	1	2017-10-09 07:51:25	weboll
TERMN21	Temperatura della neve a 400 cm	02	1	2017-10-09 07:51:25	weboll
TERMN22	Temperatura della neve a 420 cm	02	1	2017-10-09 07:51:25	weboll
TERMN23	Temperatura della neve a 440 cm	02	1	2017-10-09 07:51:25	weboll
TERMN24	Temperatura della neve a 460 cm	02	1	2017-10-09 07:51:25	weboll
TERMN3	Temperatura della neve a 40 cm	02	1	2017-10-09 07:51:25	weboll
TERMN5	Temperatura della neve a 80 cm	02	1	2017-10-09 07:51:25	weboll
TERMN6	Temperatura della neve a 100 cm	02	1	2017-10-09 07:51:25	weboll
TERMN7	Temperatura della neve a 120 cm	02	1	2017-10-09 07:51:25	weboll
TERMN8	Temperatura della neve a 140 cm	02	1	2017-10-09 07:51:25	weboll
TERMN9	Temperatura della neve a 160 cm	02	1	2017-10-09 07:51:25	weboll
TERMN30	Temperatura della neve a 30 cm	02	1	2019-09-25 14:22:33	weboll
TERMN90	Temperatura della neve a 90 cm	02	1	2019-09-25 14:23:16	weboll
TERMNI	Termometro neve ad infrarossi	02	1	2019-09-25 14:23:28	weboll
UVICS	UV Index cielo sereno	02	0	2019-09-25 14:23:28	weboll
\.

--
-- Name: parametro_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.parametro
    ADD CONSTRAINT parametro_pkey PRIMARY KEY (id_parametro);


--
-- Name: parametro_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--


ALTER TABLE ONLY public.parametro
    ADD CONSTRAINT parametro_fkey001 FOREIGN KEY (id_unita_misura) REFERENCES public.unita_misura(id_unita_misura) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: TABLE parametro; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
