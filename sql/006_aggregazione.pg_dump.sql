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
-- Name: aggregazione; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.aggregazione (
    id_aggregazione integer NOT NULL,
    descrizione character varying(100) NOT NULL,
    id_unita_misura character varying(2),
    tipo_aggregazione character varying(1),
    data_agg timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone,
    autore_agg character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.aggregazione OWNER TO weboll;

--
-- Data for Name: aggregazione; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.aggregazione (id_aggregazione, descrizione, id_unita_misura, tipo_aggregazione, data_agg, autore_agg) FROM stdin;
293	Valore massimo sui 10 minuti	\N	0	2005-11-14 00:00:00	weboll
912	Dalle 00:00 alle 23:59	\N	\N	2010-02-19 00:00:00	weboll
913	Dalle 00:00 alle 11:59	\N	\N	2010-02-19 00:00:00	weboll
914	Dalle 12:00 alle 23:59	\N	\N	2010-02-19 00:00:00	weboll
911	Totale	99	0	2010-07-23 00:00:00	weboll
904	Minimo su 24 ore	99	0	2010-07-23 00:00:00	weboll
905	Massimo su 3 ore	99	0	2010-07-23 00:00:00	weboll
906	Massimo su 6 ore	99	0	2010-07-23 00:00:00	weboll
907	Massimo su 12 ore	99	0	2010-07-23 00:00:00	weboll
908	Massimo su 24 ore	99	0	2010-07-23 00:00:00	weboll
909	Massimo	99	0	2010-07-23 00:00:00	weboll
910	Minimo	99	0	2010-07-23 00:00:00	weboll
900	Media precipitazioni per periodi di 6 ore consecutive	\N	\N	2010-06-17 00:00:00	weboll
901	Media precipitazioni per periodi di 12 ore consecutive	\N	\N	2010-06-17 00:00:00	weboll
902	Media precipitazioni per periodi di 24 ore consecutive	\N	\N	2010-06-17 00:00:00	weboll
903	Media precipitazioni per periodi di 48 ore consecutive	\N	\N	2010-06-17 00:00:00	weboll
301	Totale mensile dei totali giornalieri dalle 09:00 alle 09:00 del giorno successivo	\N	2	2005-11-14 00:00:00	weboll
302	Totale annuale dei totali giornalieri dalle 09:00 alle 09:00 del giorno successivo	\N	2	2005-11-14 00:00:00	weboll
303	Numero di giorni piovosi nel mese (dalle 09:00 alle 09:00 del giorno successivo)	98	2	2005-11-14 00:00:00	weboll
304	Numero di giorni piovosi nell'anno (dalle 09:00 alle 09:00 del giorno successivo)	98	2	2005-11-14 00:00:00	weboll
305	Valori massimi di precipitazione raggiunti in 5 giorni consecutivi per anno	\N	2	2005-11-14 00:00:00	weboll
306	Valori massimi di precipitazione raggiunti in 10 giorni consecutivi per anno	\N	2	2005-11-14 00:00:00	weboll
307	Valori massimi di precipitazione raggiunti in 20 giorni consecutivi per anno	\N	2	2005-11-14 00:00:00	weboll
308	Valori massimi di precipitazione raggiunti in 30 giorni consecutivi per anno	\N	2	2005-11-14 00:00:00	weboll
362	Valore di portata giornaliera superata nell'anno per 60 giorni	\N	2	2005-11-14 00:00:00	weboll
363	Valore di portata giornaliera superata nell'anno per 91 giorni	\N	2	2005-11-14 00:00:00	weboll
364	Valore di portata giornaliera superata nell'anno per 135 giorni	\N	2	2005-11-14 00:00:00	weboll
365	Valore di portata giornaliera superata nell'anno per 182 giorni	\N	2	2005-11-14 00:00:00	weboll
366	Valore di portata giornaliera superata nell'anno per 274 giorni	\N	2	2005-11-14 00:00:00	weboll
367	Valore di portata giornaliera superata nell'anno per 355 giorni	\N	2	2005-11-14 00:00:00	weboll
378	Totale giornaliero dalle 00:00 alle 23:59	\N	2	2005-11-14 00:00:00	weboll
380	Direzione della massima raffica giornaliera (valore calcolato)	\N	2	2005-11-14 00:00:00	weboll
314	Media giornaliera ((valore max + valore min) / 2)	\N	2	2005-11-14 00:00:00	weboll
320	Tempo di permanenza nel settore prevalente nel giorno (minuti)	20	2	2005-11-14 00:00:00	weboll
321	Tempo di permanenza nel settore prevalente nel mese (minuti)	20	2	2005-11-14 00:00:00	weboll
322	Media annuale delle medie giornaliere ((valore max + valore min) / 2)	\N	2	2005-11-14 00:00:00	weboll
325	Precipitazioni di notevole intensita' e breve durata	\N	2	2005-11-14 00:00:00	weboll
328	Massimo dalle 6 alle 18	\N	2	2005-11-14 00:00:00	weboll
332	Tempo di permanenza del vento nel settore n (minuti)	20	2	2005-11-14 00:00:00	weboll
333	Tempo di permanenza del vento nel settore ne (minuti)	20	2	2005-11-14 00:00:00	weboll
334	Tempo di permanenza del vento nel settore e (minuti)	20	2	2005-11-14 00:00:00	weboll
335	Tempo di permanenza del vento nel settore se (minuti)	20	2	2005-11-14 00:00:00	weboll
336	Tempo di permanenza del vento nel settore s (minuti)	20	2	2005-11-14 00:00:00	weboll
337	Tempo di permanenza del vento nel settore so (minuti)	20	2	2005-11-14 00:00:00	weboll
338	Tempo di permanenza del vento nel settore o (minuti)	20	2	2005-11-14 00:00:00	weboll
339	Tempo di permanenza del vento nel settore no (minuti)	20	2	2005-11-14 00:00:00	weboll
341	Deviazione standard della direzione prevalente sui 10 minuti	\N	2	2005-11-14 00:00:00	weboll
347	Direzione della massima raffica giornaliera (strumentale)	\N	2	2005-11-14 00:00:00	weboll
348	Evapotraspirazione calcolata con la formula di Turc	\N	2	2005-11-14 00:00:00	weboll
349	Evapotraspirazione calcolata con la formula di Penman	\N	2	2005-11-14 00:00:00	weboll
368	Deviazione standard dei massimi	\N	2	2005-11-14 00:00:00	weboll
369	Deviazione standard delle medie	\N	2	2005-11-14 00:00:00	weboll
370	Deviazione standard dei minimi	\N	2	2005-11-14 00:00:00	weboll
371	Massimo dei massimi	\N	2	2005-11-14 00:00:00	weboll
372	Massimo dei minimi	\N	2	2005-11-14 00:00:00	weboll
373	Media dei massimi	\N	2	2005-11-14 00:00:00	weboll
374	Media delle medie	\N	2	2005-11-14 00:00:00	weboll
375	Media dei minimi	\N	2	2005-11-14 00:00:00	weboll
376	Minimo dei massimi	\N	2	2005-11-14 00:00:00	weboll
377	Minimo dei minimi	\N	2	2005-11-14 00:00:00	weboll
379	Contatore di precipitazione (da DVD CAE)	\N	9	2005-11-14 00:00:00	weboll
212	Percentuale di osservazioni giornaliere per settore sw di provenienza	\N	2	2005-11-14 00:00:00	weboll
213	Percentuale di osservazioni giornaliere per settore w di provenienza	\N	2	2005-11-14 00:00:00	weboll
214	Percentuale di osservazioni giornaliere per settore nw di provenienza	\N	2	2005-11-14 00:00:00	weboll
215	Percentuale giornaliera di dati mancanti	\N	2	2005-11-14 00:00:00	weboll
216	Media mensile per settore n di provenienza	\N	2	2005-11-14 00:00:00	weboll
217	Media mensile per settore ne di provenienza	\N	2	2005-11-14 00:00:00	weboll
218	Media mensile per settore e di provenienza	\N	2	2005-11-14 00:00:00	weboll
219	Media mensile per settore se di provenienza	\N	2	2005-11-14 00:00:00	weboll
220	Media mensile per settore s di provenienza	\N	2	2005-11-14 00:00:00	weboll
221	Media mensile per settore sw di provenienza	\N	2	2005-11-14 00:00:00	weboll
222	Media mensile per settore w di provenienza	\N	2	2005-11-14 00:00:00	weboll
223	Media mensile per settore nw di provenienza	\N	2	2005-11-14 00:00:00	weboll
224	Percentuale di osservazioni mensili di vento variabile	\N	2	2005-11-14 00:00:00	weboll
225	Percentuale di osservazioni mensili di calma di vento	\N	2	2005-11-14 00:00:00	weboll
511	Escursione termica totale mensile (E+M) - °C	\N	\N	2006-03-16 00:00:00	weboll
226	Percentuale di osservazioni mensili per settore n di provenienza	\N	2	2005-11-14 00:00:00	weboll
227	Percentuale di osservazioni mensili per settore ne di provenienza	\N	2	2005-11-14 00:00:00	weboll
228	Percentuale di osservazioni mensili per settore e di provenienza	\N	2	2005-11-14 00:00:00	weboll
229	Percentuale di osservazioni mensili per settore se di provenienza	\N	2	2005-11-14 00:00:00	weboll
230	Percentuale di osservazioni mensili per settore s di provenienza	\N	2	2005-11-14 00:00:00	weboll
231	Percentuale di osservazioni mensili per settore sw di provenienza	\N	2	2005-11-14 00:00:00	weboll
232	Percentuale di osservazioni mensili per settore w di provenienza	\N	2	2005-11-14 00:00:00	weboll
233	Percentuale di osservazioni mensili per settore nw di provenienza	\N	2	2005-11-14 00:00:00	weboll
234	Percentuale mensile di dati mancanti	\N	2	2005-11-14 00:00:00	weboll
236	Media su 8 ore	\N	1	2005-11-14 00:00:00	weboll
253	95° percentile delle concentrazioni medie giornaliere rilevate da 1/4 a 31/3	\N	2	2006-03-16 00:00:00	weboll
255	Media annuale delle medie giornaliere	\N	2	2005-11-14 00:00:00	weboll
280	Totale al minuto	\N	1	2005-11-14 00:00:00	weboll
281	max annuale delle medie di 8 ore	\N	2	2005-11-14 00:00:00	weboll
286	50° percentile annuale delle medie giornaliere	\N	2	2006-03-16 00:00:00	weboll
290	max annuale delle medie giornaliere	\N	2	2005-11-14 00:00:00	weboll
291	media annuale delle medie di orarie	\N	2	2005-11-14 00:00:00	weboll
292	95° percentile annuale delle medie orarie	\N	2	2006-03-16 00:00:00	weboll
311	Numero di giorni nevosi nel mese	98	2	2005-11-14 00:00:00	weboll
315	Massimo mensile delle medie giornaliere ((valore max + valore min) / 2)	\N	2	2005-11-14 00:00:00	weboll
316	Minimo mensile delle medie giornaliere ((valore max + valore min) / 2)	\N	2	2005-11-14 00:00:00	weboll
317	Media mensile delle medie giornaliere ((valore max + valore min) / 2)	\N	2	2005-11-14 00:00:00	weboll
318	Massima raffica giornaliera	\N	2	2005-11-14 00:00:00	weboll
319	Massimo mensile delle massime raffiche giornaliere	\N	2	2005-11-14 00:00:00	weboll
323	Massimo giornaliero dei valori rilevati	\N	2	2005-11-14 00:00:00	weboll
324	Minimo giornaliero dei valori rilevati	\N	2	2005-11-14 00:00:00	weboll
326	Totale sulle 6 ore precedenti	\N	1	2005-11-14 00:00:00	weboll
327	Minimo dalle 18 alle 6	\N	2	2005-11-14 00:00:00	weboll
329	Minimo orario	28	1	2005-11-14 00:00:00	weboll
330	Massimo orario	\N	1	2005-11-14 00:00:00	weboll
331	Vento filato giornaliero (km)	12	2	2005-11-14 00:00:00	weboll
340	Massimo annuale delle medie orarie	\N	2	2005-11-14 00:00:00	weboll
342	Durata giornaliera della calma di vento (minuti)	20	2	2005-11-14 00:00:00	weboll
343	Totale ogni 30 minuti	\N	0	2005-11-14 00:00:00	weboll
344	Durata oraria della calma di vento (minuti)	20	2	2005-11-14 00:00:00	weboll
345	Prima direzione prevalente giornaliera	\N	2	2005-11-14 00:00:00	weboll
346	Seconda direzione prevalente giornaliera	\N	2	2005-11-14 00:00:00	weboll
288	98° percentile annuale delle medie giornaliere	\N	2	2006-03-16 00:00:00	weboll
300	Totale giornaliero dalle 09:00 alle 09:00 del giorno successivo	\N	2	2005-11-14 00:00:00	weboll
0	Valore puntuale	\N	0	2005-11-14 00:00:00	weboll
3	98° percentile annuale	\N	2	2006-03-16 00:00:00	weboll
25	Massimo giornaliero (strumentale)	\N	2	2005-11-14 00:00:00	weboll
27	Massimo mensile dei massimi giornalieri (calcolati)	\N	2	2005-11-14 00:00:00	weboll
28	Massimo mensile dei minimi giornalieri	\N	2	2005-11-14 00:00:00	weboll
29	Valore massimo mensile	\N	2	2005-11-14 00:00:00	weboll
30	Massimo mensile delle escursioni giornaliere	\N	2	2005-11-14 00:00:00	weboll
31	Massimo mensile delle medie giornaliere	\N	2	2005-11-14 00:00:00	weboll
32	Media annuale	\N	2	2005-11-14 00:00:00	weboll
33	Media annuale dei massimi giornalieri	\N	2	2005-11-14 00:00:00	weboll
34	Media annuale dei minimi giornalieri	\N	2	2005-11-14 00:00:00	weboll
35	Media annuale delle escursioni giornaliere	\N	2	2005-11-14 00:00:00	weboll
47	Media giornaliera	\N	2	2005-11-14 00:00:00	weboll
49	Media mensile	\N	2	2005-11-14 00:00:00	weboll
50	Media mensile dei massimi giornalieri (calcolati)	\N	2	2005-11-14 00:00:00	weboll
51	Media mensile dei minimi giornalieri (calcolati)	\N	2	2005-11-14 00:00:00	weboll
52	Media mensile delle escursioni giornaliere	\N	2	2005-11-14 00:00:00	weboll
53	Media mensile delle medie giornaliere	\N	2	2005-11-14 00:00:00	weboll
54	Media oraria	\N	1	2005-11-14 00:00:00	weboll
68	Minimo mensile dei massimi giornalieri	\N	2	2005-11-14 00:00:00	weboll
69	Minimo mensile dei minimi giornalieri (calcolati)	\N	2	2005-11-14 00:00:00	weboll
70	Valore minimo mensile	\N	2	2005-11-14 00:00:00	weboll
71	Minimo mensile delle escursioni giornaliere	\N	2	2005-11-14 00:00:00	weboll
72	Minimo mensile delle medie giornaliere	\N	2	2005-11-14 00:00:00	weboll
77	Numero di giorni piovosi nell'anno	98	2	2005-11-14 00:00:00	weboll
78	Numero di giorni piovosi nel mese (dalle 00:00 alle 23:59)	98	2	2005-11-14 00:00:00	weboll
82	Totale mensile del numero di giorni con neve al suolo	98	2	2005-11-14 00:00:00	weboll
84	Numero di giorni al mese con raffica >= 30 km/h	98	2	2005-11-14 00:00:00	weboll
130	Settore prevalente nel giorno (sedicesimi + calma di vento)	21	2	2005-11-14 00:00:00	weboll
131	Settore prevalente nel mese (sedicesimi + calma di vento)	21	2	2005-11-14 00:00:00	weboll
135	Totale mensile	\N	2	2005-11-14 00:00:00	weboll
137	Totale annuale	\N	2	2005-11-14 00:00:00	weboll
143	Totale giornaliero	\N	2	2005-11-14 00:00:00	weboll
163	Massime precipitazioni dell'anno per periodi di 1 giorno (dalle 9 alle 9)	\N	2	2008-09-18 00:00:00	weboll
165	Massime precipitazioni dell'anno per periodi di 2 giorni (dalle 9 alle 9)	\N	2	2008-09-18 00:00:00	weboll
167	Massime precipitazioni dell'anno per periodi di 3 giorni (dalle 9 alle 9)	\N	2	2008-09-18 00:00:00	weboll
169	Massime precipitazioni dell'anno per periodi di 4 giorni (dalle 9 alle 9)	\N	2	2008-09-18 00:00:00	weboll
171	Massime precipitazioni dell'anno per periodi di 5 giorni (dalle 9 alle 9)	\N	2	2008-09-18 00:00:00	weboll
173	Massime precipitazioni dell'anno per periodi di 12 ore consecutive	\N	2	2005-11-14 00:00:00	weboll
176	Massime precipitazioni dell'anno per periodi di 24 ore consecutive	\N	2	2005-11-14 00:00:00	weboll
178	Massime precipitazioni dell'anno per periodi di 3 ore consecutive	\N	2	2005-11-14 00:00:00	weboll
183	Massime precipitazioni dell'anno per periodi di 6 ore consecutive	\N	2	2005-11-14 00:00:00	weboll
184	Massime precipitazioni dell'anno per periodi di 1 ora	\N	2	2005-11-14 00:00:00	weboll
185	valori guida - media aritm. annuale medie 24 ore	\N	2	2005-11-14 00:00:00	weboll
192	Totale orario	\N	1	2005-11-14 00:00:00	weboll
194	Media ogni dieci minuti	\N	1	2005-11-14 00:00:00	weboll
197	Media giornaliera per settore n di provenienza	\N	2	2005-11-14 00:00:00	weboll
198	Media giornaliera per settore ne di provenienza	\N	2	2005-11-14 00:00:00	weboll
199	Media giornaliera per settore e di provenienza	\N	2	2005-11-14 00:00:00	weboll
200	Media giornaliera per settore se di provenienza	\N	2	2005-11-14 00:00:00	weboll
201	Media giornaliera per settore s di provenienza	\N	2	2005-11-14 00:00:00	weboll
202	Media giornaliera per settore sw di provenienza	\N	2	2005-11-14 00:00:00	weboll
203	Media giornaliera per settore w di provenienza	\N	2	2005-11-14 00:00:00	weboll
204	Media giornaliera per settore nw di provenienza	\N	2	2005-11-14 00:00:00	weboll
205	Percentuale di osservazioni giornaliere di vento variabile	\N	2	2005-11-14 00:00:00	weboll
206	Percentuale di osservazioni giornaliere di calma di vento	\N	2	2005-11-14 00:00:00	weboll
207	Percentuale di osservazioni giornaliere per settore n di provenienza	\N	2	2005-11-14 00:00:00	weboll
18	Escursione giornaliera	\N	2	2005-11-14 00:00:00	weboll
36	Media decadica	\N	2	2005-11-14 00:00:00	weboll
67	Minimo giornaliero (strumentale)	\N	2	2005-11-14 00:00:00	weboll
86	Totale stagionale del numero di giorni con neve al suolo	98	2	2005-11-14 00:00:00	weboll
155	Totale stagionale	\N	2	2005-11-14 00:00:00	weboll
193	Totale ogni 10 minuti	\N	0	2005-11-14 00:00:00	weboll
195	Direzione prevalente (calcolo su dieci minuti)	\N	1	2005-11-14 00:00:00	weboll
245	98° percentile delle concentrazioni medie di 1 ora rilevate nell'anno solare	\N	2	2006-03-16 00:00:00	weboll
246	50° percentile delle concentrazioni medie di 1 ora rilevate nell'anno solare	\N	2	2006-03-16 00:00:00	weboll
278	50° percentile delle concentrazioni medie di 24 ore rilevate nel periodo 1/4 - 31/3	\N	2	2006-03-16 00:00:00	weboll
279	50° percentile delle concentrazioni medie di 24 ore rilevate nel periodo 1/10 - 31/3	\N	2	2006-03-16 00:00:00	weboll
282	50° percentile delle medie di 8 ore	\N	2	2006-03-16 00:00:00	weboll
283	98° percentile delle medie di 8 ore	\N	2	2006-03-16 00:00:00	weboll
284	99.9° percentile delle medie di 8 ore	\N	2	2006-03-16 00:00:00	weboll
285	99.9° percentile delle medie orarie	\N	2	2006-03-16 00:00:00	weboll
287	95° percentile annuale delle medie giornaliere	\N	2	2006-03-16 00:00:00	weboll
312	Numero di giorni nevosi nella stagione	98	2	2005-11-14 00:00:00	weboll
313	Altezza della neve al suolo alle ore 07:00 gmt	\N	2	2005-11-14 00:00:00	weboll
208	Percentuale di osservazioni giornaliere per settore ne di provenienza	\N	2	2005-11-14 00:00:00	weboll
209	Percentuale di osservazioni giornaliere per settore e di provenienza	\N	2	2005-11-14 00:00:00	weboll
210	Percentuale di osservazioni giornaliere per settore se di provenienza	\N	2	2005-11-14 00:00:00	weboll
211	Percentuale di osservazioni giornaliere per settore s di provenienza	\N	2	2005-11-14 00:00:00	weboll
350	Minimo orario di radiazione diretta (calorie / centimetro quadro al minuto)	28	1	2005-11-14 00:00:00	weboll
351	Massimo orario di radiazione diretta (calorie / centimetro quadro al minuto)	28	1	2005-11-14 00:00:00	weboll
352	Minimo giornaliero di radiazione diretta (calorie / centimetro quadro al minuto)	28	2	2005-11-14 00:00:00	weboll
353	Massimo giornaliero di radiazione diretta (calorie / centimetro quadro al minuto)	28	2	2005-11-14 00:00:00	weboll
354	Media giornaliera dei valori rilevati alle 8, alle 19, del minimo e del massimo	\N	2	2005-11-14 00:00:00	weboll
355	Media giornaliera dei valori rilevati alle 8, alle 14 e alle 19	\N	2	2005-11-14 00:00:00	weboll
356	Valore mensile	98	2	2005-11-14 00:00:00	weboll
357	Valore annuale	98	2	2005-11-14 00:00:00	weboll
358	Media annuale delle medie mensili	\N	2	2005-11-14 00:00:00	weboll
359	Minimo annuale delle medie giornaliere	\N	2	2005-11-14 00:00:00	weboll
360	Valore di portata giornaliera superata nell'anno per 10 giorni	\N	2	2005-11-14 00:00:00	weboll
361	Valore di portata giornaliera superata nell'anno per 30 giorni	\N	2	2005-11-14 00:00:00	weboll
123	Massime precipitazioni del giorno per periodi di 1 ora	\N	2	2007-10-18 00:00:00	weboll
267	Massime precipitazioni dell'anno per periodi di 3 giorni (dalle 0 alle 0)	\N	2	2008-09-18 00:00:00	weboll
269	Massime precipitazioni dell'anno per periodi di 4 giorni (dalle 0 alle 0)	\N	2	2008-09-18 00:00:00	weboll
271	Massime precipitazioni dell'anno per periodi di 5 giorni (dalle 0 alle 0)	\N	2	2008-09-18 00:00:00	weboll
382	Media mensile dei massimi giornalieri (strumentali)	\N	2	2005-06-10 00:00:00	weboll
383	Media mensile dei minimi giornalieri (strumentali)	\N	2	2005-06-10 00:00:00	weboll
384	Massimo mensile dei massimi giornalieri (strumentali)	\N	2	2005-06-10 00:00:00	weboll
385	Minimo mensile dei minimi giornalieri (strumentali)	\N	2	2005-06-10 00:00:00	weboll
386	Direzione della massima raffica mensile (strumentale)	\N	2	2006-03-03 00:00:00	weboll
387	Totale mensile dei totali giornalieri dalle 00:00 alle 23:59	\N	2	2005-06-10 00:00:00	weboll
388	Durata mensile della calma di vento (minuti)	20	2	2006-03-03 00:00:00	weboll
389	Direzione della massima raffica mensile (valore calcolato)	\N	2	2006-03-03 00:00:00	weboll
501	Temperatura media mensile (E) - °C	\N	\N	2006-03-16 00:00:00	weboll
502	Temperatura media mensile (M) - °C	\N	\N	2006-03-16 00:00:00	weboll
503	Temperatura media mensile (E+M) - °C	\N	\N	2006-03-16 00:00:00	weboll
504	Temperatura minima mensile (E+M) - °C	\N	\N	2006-03-16 00:00:00	weboll
505	Temperatura massima mensile (E+M) - °C	\N	\N	2006-03-16 00:00:00	weboll
506	Temperatura minima media mensile (E+M) - °C	\N	\N	2006-03-16 00:00:00	weboll
507	Temperatura massima media mensile (E+M) - °C	\N	\N	2006-03-16 00:00:00	weboll
510	Escursione termica media mensile (E+M) - °C	\N	\N	2006-03-16 00:00:00	weboll
514	Somma termica mensile con soglia 0°C (E+M)  - °C*d	33	\N	2006-03-16 00:00:00	weboll
515	Somma termica mensile con soglia 4°C (E+M)  - °C*d	33	\N	2006-03-16 00:00:00	weboll
516	Somma termica mensile con soglia 10°C (E+M)  - °C*d	33	\N	2006-03-16 00:00:00	weboll
517	Precipitazione totale mensile (E+M) - mm	\N	\N	2005-04-19 00:00:00	weboll
518	Precipitazione giornaliera massima (E+M) - mm	\N	\N	2005-04-19 00:00:00	weboll
521	Bagnatura fogliare totale mensile (E) - minuti	\N	\N	2005-04-19 00:00:00	weboll
522	Radiazione media giornaliera (E) - MJ/m^2	\N	\N	2005-09-01 00:00:00	weboll
523	Radiazione totale mensile (E) - MJ/m^2	\N	\N	2005-09-01 00:00:00	weboll
524	Umidita media mensile (E)  - %	\N	\N	2005-04-19 00:00:00	weboll
525	Umidita media mensile (M)  - %	\N	\N	2005-04-19 00:00:00	weboll
526	Umidita minima media mensile (E)  - %	\N	\N	2005-04-19 00:00:00	weboll
527	Umidita massima media mensile (E)  - %	\N	\N	2005-04-19 00:00:00	weboll
528	Velocita media mensile del vento (E) - km/h	\N	\N	2005-04-19 00:00:00	weboll
529	Massima velocita del vento mensile (E) - km/h	\N	\N	2005-04-19 00:00:00	weboll
530	Km di vento filato medi giornalieri (E) - km 	12	\N	2005-04-19 00:00:00	weboll
531	Km di vento filato totali mensili (E) - km 	12	\N	2005-04-19 00:00:00	weboll
532	Indice di Huglin MENSILE (E)  - °C*d	33	\N	2006-03-16 00:00:00	weboll
533	Indice di Huglin MENSILE (E+M)  - °C*d	33	\N	2006-03-16 00:00:00	weboll
535	Massimo giornaliero delle medie mobili di 8 ore	\N	\N	2006-03-16 00:00:00	weboll
381	Totale ogni 15 minuti	\N	0	2005-11-14 00:00:00	weboll
508	Temperatura minima piu alta (E+M) - °C	\N	\N	2006-03-16 00:00:00	weboll
509	Temperatura massima piu bassa (E+M) - °C	\N	\N	2006-03-16 00:00:00	weboll
512	Giorni di gelo (E+M) - n° gg	98	\N	2006-03-16 00:00:00	weboll
513	Giorni senza disgelo - n° gg	98	\N	2006-03-16 00:00:00	weboll
519	Numero di giorni di pioggia (prec.>=1mm) (E+M) - n° gg	98	\N	2006-03-16 00:00:00	weboll
520	Numero di giorni di prec. tra 0 e 1mm (E+M) - n° gg	98	\N	2006-03-16 00:00:00	weboll
534	Media invernale (1 ottobre - 31 marzo)	\N	\N	2006-03-16 00:00:00	weboll
700	Stima	\N	\N	2005-11-14 00:00:00	weboll
701	Stima - Massimo	\N	\N	2005-11-14 00:00:00	weboll
120	Massime precipitazioni del giorno per periodi di 10 minuti consecutivi	\N	2	2007-10-18 00:00:00	weboll
121	Massime precipitazioni del giorno per periodi di 20 minuti consecutivi	\N	2	2007-10-18 00:00:00	weboll
122	Massime precipitazioni del giorno per periodi di 30 minuti consecutivi	\N	2	2007-10-18 00:00:00	weboll
124	Massime precipitazioni del giorno per periodi di 3 ore consecutive	\N	2	2007-10-18 00:00:00	weboll
125	Massime precipitazioni del giorno per periodi di 6 ore consecutive	\N	2	2007-10-18 00:00:00	weboll
126	Massime precipitazioni del giorno per periodi di 12 ore consecutive	\N	2	2007-10-18 00:00:00	weboll
127	Massime precipitazioni del giorno per periodi di 24 ore consecutive	\N	2	2007-10-18 00:00:00	weboll
187	Massime precipitazioni dell'anno per periodi di 10 minuti consecutivi	\N	2	2007-10-18 00:00:00	weboll
188	Massime precipitazioni dell'anno per periodi di 20 minuti consecutivi	\N	2	2007-10-18 00:00:00	weboll
189	Massime precipitazioni dell'anno per periodi di 30 minuti consecutivi	\N	2	2007-10-18 00:00:00	weboll
87	Altezza della neve fresca	\N	2	2007-02-12 00:00:00	weboll
88	Massima altezza della neve	\N	2	2007-02-12 00:00:00	weboll
263	Massime precipitazioni dell'anno per periodi di 1 giorno (dalle 0 alle 0)	\N	2	2008-09-18 00:00:00	weboll
265	Massime precipitazioni dell'anno per periodi di 2 giorni (dalle 0 alle 0)	\N	2	2008-09-18 00:00:00	weboll
390	Massima portata al colmo annuale (Q colmo)	14	2	2010-12-30 00:00:00	weboll
391	Altezza idrometrica in corrispondenza della massima portata al colmo annuale (H colmo)	13	2	2010-12-30 00:00:00	weboll
392	Massima delle portate medie giornaliere (Q giorno)	14	2	2010-12-30 00:00:00	weboll
177	Massime precipitazioni dell'anno per periodi di 2 ore consecutive	01	2	2010-12-29 00:00:00	weboll
186	Massime precipitazioni dell'anno per periodi di 5 minuti consecutivi	01	2	2010-12-29 00:00:00	weboll
190	Massime precipitazioni dell'anno per periodi di 15 minuti consecutivi	01	2	2010-12-29 00:00:00	weboll
191	Massime precipitazioni dell'anno per periodi di 45 minuti consecutivi	01	2	2010-12-29 00:00:00	weboll
915	Valore di riferimento dell'intervallo di 6 ore	\N	\N	2011-10-10 00:00:00	weboll
916	Valore di riferimento dell'intervallo di 12 ore	\N	\N	2011-10-10 00:00:00	weboll
917	Valore di riferimento dell'intervallo di 24 ore	\N	\N	2011-10-10 00:00:00	weboll
918	Totale sulle 3 ore precedenti (ex ID 123)	\N	1	2012-01-30 00:00:00	weboll
402	Sommatoria termica semestrale (15 ottobre - 15 aprile) dei gradi giorno da riscaldamento	\N	\N	2018-10-08 00:00:00	weboll
403	Sommatoria termica annuale dei gradi giorno da riscaldamento	\N	\N	2018-10-22 00:00:00	weboll
401	Sommatoria termica mensile dei gradi giorno da riscaldamento	\N	\N	2018-10-08 00:00:00	weboll
400	Grado giorno da riscaldamento (20°C - Tmedia, solo se > 0)	\N	\N	2018-10-08 00:00:00	weboll
294	Valore minimo sui 10 minuti	\N	0	2020-02-05 16:32:04	weboll
295	Valore massimo sui 30 minuti	\N	0	2020-02-05 16:32:00	weboll
296	Valore minimo sui 30 minuti	\N	0	2020-02-05 16:32:25	weboll
406	Sommatoria termica annuale dei gradi giorno da raffrescamento	\N	\N	2020-06-30 09:48:29	weboll
404	Gradi giorno da raffrescamento giornaliero	\N	\N	2020-06-30 09:48:29	weboll
405	Sommatoria termica mensile dei gradi giorno da raffrescamento	\N	\N	2020-06-30 09:48:29	weboll
89	Altezza della neve fresca 	\N	0	2013-01-17 11:40:48	weboll
164	Massime precipitazioni dell'anno per periodi di 25 minuti consecutivi	\N	2	2013-03-07 13:54:41	weboll
166	Massime precipitazioni dell'anno per periodi di 35 minuti consecutivi	\N	2	2013-03-07 13:56:54	weboll
168	Massime precipitazioni dell'anno per periodi di 40 minuti consecutivi	\N	2	2013-03-07 13:57:13	weboll
170	Massime precipitazioni dell'anno per periodi di 50 minuti consecutivi	\N	2	2013-03-07 13:57:39	weboll
929	Media precipitazioni per periodi di 36 ore consecutive	\N	\N	2016-05-04 15:05:45	weboll
\.


--
-- Name: aggregazione_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.aggregazione
    ADD CONSTRAINT aggregazione_pkey PRIMARY KEY (id_aggregazione);


--
-- Name: aggregazione_idx001; Type: INDEX; Schema: public; Owner: weboll; Tablespace:
--

CREATE INDEX aggregazione_idx001 ON public.aggregazione USING btree (id_unita_misura);


--
-- Name: aggregazione_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.aggregazione
    ADD CONSTRAINT aggregazione_fkey001 FOREIGN KEY (id_unita_misura) REFERENCES public.unita_misura(id_unita_misura) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TABLE aggregazione; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
