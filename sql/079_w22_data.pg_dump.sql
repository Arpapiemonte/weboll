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
-- Name: w22_data; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w22_data (
    id_w22 bigint NOT NULL,
    id_w22_zone integer NOT NULL,
    codice1 character varying(10),
    codice2 character varying(10),
    codice3 character varying(10),
    tendenza6hprecedenti character varying(15),
    portata_attesa character varying(15),
    criticita_attesa character varying(15),
    prev_crit12h character varying(15),
    prev_crit24h character varying(15),
    prev_crit36h character varying(15),
    tend48h character varying(15),
    massimo_previsione character varying(15),
    data_massimo_storico character varying(15),
    valore_massimo_storico character varying(15),
    id_w22_data BIGSERIAL
);

ALTER TABLE public.w22_data                                       
ADD CONSTRAINT w22_data_fkey003 
FOREIGN KEY (tendenza6hprecedenti) 
REFERENCES public.w22_tendenza (descrizione) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey004 
FOREIGN KEY (tend48h) 
REFERENCES public.w22_tendenza (descrizione) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey005 
FOREIGN KEY (criticita_attesa) 
REFERENCES public.w22_criticita (id_w22_criticita) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey006
FOREIGN KEY (prev_crit12h) 
REFERENCES public.w22_criticita (id_w22_criticita) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey007
FOREIGN KEY (prev_crit24h) 
REFERENCES public.w22_criticita (id_w22_criticita) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey008
FOREIGN KEY (prev_crit36h) 
REFERENCES public.w22_criticita (id_w22_criticita) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.w22_data                                        
ADD CONSTRAINT w22_data_fkey009
FOREIGN KEY (massimo_previsione) 
REFERENCES public.w22_criticita (id_w22_criticita) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE public.w22_data OWNER TO weboll;

--
-- Data for Name: w22_data; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w22_data (id_w22, id_w22_zone, codice1, codice2, codice3, tendenza6hprecedenti, portata_attesa, criticita_attesa, prev_crit12h, prev_crit24h, prev_crit36h, tend48h, massimo_previsione, data_massimo_storico, valore_massimo_storico, id_w22_data) FROM stdin;
2077	1	100	190	300	stazionario	n.d.	A	A	A	A	stazionario	A	25/11/2016	359	53409
2077	3	300	550	900	stazionario	2	A	A	A	A	stazionario	A	25/11/2016	1310	53410
2077	5	520	730	1400	diminuzione	0.3	A	A	A	A	stazionario	A	25/11/2016	1500	53411
2077	7	540	800	1400	diminuzione	18	A	A	A	A	stazionario	A	15/10/2000	3100	53412
2077	2	150	220	350	stazionario	2	A	A	A	A	stazionario	A	25/11/2016	270	53465
2077	4	160	290	490	diminuzione	1	A	A	A	A	stazionario	A	25/11/2016	550	53466
2077	6	450	700	1200	stazionario	3	A	A	A	A	stazionario	A	14/10/2000	1500	53467
2077	8	910	2000	3200	stazionario	6	A	A	A	A	stazionario	A	15/10/2000	4250	53468
2077	9	750	980	1900	diminuzione	9	A	A	A	A	stazionario	A	15/10/2000	2640	53469
2077	10	250	370	670	stazionario	4	A	A	A	A	stazionario	A	13/06/2000	835	53470
2077	11	160	280	400	crescita	1	A	A	A	A	stazionario	A	27/04/2009	425	53471
2077	12	540	870	1400	diminuzione	1	A	A	A	A	stazionario	A	25/11/2016	2110	53472
2077	13	700	1000	1500	crescita	15	A	A	A	A	stazionario	A	26/11/2002	1280	53473
2077	14	600	850	1500	stazionario	8	A	A	A	A	stazionario	A	25/11/2016	3120	53474
2077	15	850	1300	2000	stazionario	21	A	A	A	A	stazionario	A	06/11/1994	4200	53475
2077	16	900	1400	2100	stazionario	31	A	A	A	A	stazionario	A	25/11/2016	3450	53476
2077	17	1000	1500	2200	stazionario	50	A	A	A	A	stazionario	A	28/04/2009	2000	53477
2077	18	1500	2200	3000	stazionario	42	A	A	A	A	stazionario	A	06/11/1994	4400	53478
2077	19	600	800	1500	stazionario	0.5	A	A	A	A	stazionario	A	26/11/2002	1300	53479
2077	20	440	620	1150	diminuzione	20	A	A	A	A	stazionario	A	25/11/2016	2200	53480
2077	21	680	900	1500	stazionario	26	A	A	A	A	stazionario	A	25/11/2016	2500	53481
2077	22	1000	1800	3200	stazionario	34	A	A	A	A	stazionario	A	25/11/2016	4430	53482
2078	1	100	190	300	stazionario	n.d.	A	A	A	A	stazionario	A	25/11/2016	359	53483
2078	7	540	800	1400	diminuzione	11	A	A	A	A	stazionario	A	15/10/2000	3100	53484
2078	13	700	1000	1500	stazionario	16	A	A	A	A	stazionario	A	26/11/2002	1280	53485
2078	19	600	800	1500	stazionario	0.5	A	A	A	A	stazionario	A	26/11/2002	1300	53486
2078	25	2600	3300	6000	diminuzione	118	A	A	A	A	stazionario	A	26/11/2016	6120	53487
2079	1	100	190	300	stazionario	n.d.	A	A	A	A	stazionario	A	25/11/2016	359	53488
2079	7	540	800	1400	stazionario	20	A	A	A	A	stazionario	A	15/10/2000	3100	53489
2079	13	700	1000	1500	diminuzione	15	A	A	A	A	stazionario	A	26/11/2002	1280	53490
2079	19	600	800	1500	diminuzione	0.3	A	A	A	A	stazionario	A	26/11/2002	1300	53491
2079	25	2600	3300	6000	diminuzione	118	A	A	A	A	stazionario	A	26/11/2016	6120	53492
2080	1	100	190	300	stazionario	n.d.	A	A	A	A	stazionario	A	25/11/2016	359	53493
2080	5	520	730	1400	diminuzione	1	A	A	A	A	stazionario	A	25/11/2016	1500	53494
2080	9	750	980	1900	diminuzione	14	A	A	A	A	stazionario	A	15/10/2000	2640	53495
2080	13	700	1000	1500	crescita	14	A	A	A	A	stazionario	A	26/11/2002	1280	53496
2080	17	1000	1500	2200	stazionario	27	A	A	A	A	stazionario	A	28/04/2009	2000	53497
2080	21	680	900	1500	diminuzione	30	A	A	A	A	stazionario	A	25/11/2016	2500	53498
2080	25	2600	3300	6000	diminuzione	98	A	A	A	A	stazionario	A	26/11/2016	6120	53499
2081	1	100	190	300	stazionario	n.d.	A	A	A	A	stazionario	A	25/11/2016	359	53500
2081	2	150	220	350	diminuzione	1	A	A	A	A	stazionario	A	25/11/2016	270	53501
2081	3	300	550	900	diminuzione	1	A	A	A	A	stazionario	A	25/11/2016	1310	53502
2081	4	160	290	490	diminuzione	7	A	A	A	A	stazionario	A	25/11/2016	550	53503
2081	5	520	730	1400	diminuzione	0.3	A	A	A	A	stazionario	A	25/11/2016	1500	53504
2081	6	450	700	1200	stazionario	3	A	A	A	A	stazionario	A	14/10/2000	1500	53505
2081	7	540	800	1400	diminuzione	16	A	A	A	A	stazionario	A	15/10/2000	3100	53506
2081	8	910	2000	3200	stazionario	6	A	A	A	A	stazionario	A	15/10/2000	4250	53507
2081	9	750	980	1900	diminuzione	15	A	A	A	A	stazionario	A	15/10/2000	2640	53508
2081	10	250	370	670	crescita	5	A	A	A	A	stazionario	A	13/06/2000	835	53509
2081	11	160	280	400	crescita	1	A	A	A	A	stazionario	A	27/04/2009	425	53510
2081	12	540	870	1400	diminuzione	1	A	A	A	A	stazionario	A	25/11/2016	2110	53511
2081	13	700	1000	1500	diminuzione	15	A	A	A	A	stazionario	A	26/11/2002	1280	53512
2081	14	600	850	1500	crescita	11	A	A	A	A	stazionario	A	25/11/2016	3120	53513
2081	15	850	1300	2000	stazionario	20	A	A	A	A	stazionario	A	06/11/1994	4200	53514
2081	16	900	1400	2100	stazionario	30	A	A	A	A	stazionario	A	25/11/2016	3450	53515
2081	17	1000	1500	2200	diminuzione	28	A	A	A	A	stazionario	A	28/04/2009	2000	53516
2081	18	1500	2200	3000	stazionario	43	A	A	A	A	stazionario	A	06/11/1994	4400	53517
2081	19	600	800	1500	stazionario	n.d.	A	A	A	A	stazionario	A	26/11/2002	1300	53518
2081	20	440	620	1150	diminuzione	22	A	A	A	A	stazionario	A	25/11/2016	2200	53519
2081	21	680	900	1500	stazionario	28	A	A	A	A	stazionario	A	25/11/2016	2500	53520
2081	22	1000	1800	3200	stazionario	31	A	A	A	A	stazionario	A	25/11/2016	4430	53521
2081	23	1900	2500	4500	stazionario	62	A	A	A	A	stazionario	A	16/10/2000	8150	53522
2081	24	1900	2500	4500	stazionario	71	A	A	A	A	stazionario	A	25/11/2016	4950	53523
2081	25	2600	3300	6000	diminuzione	89	A	A	A	A	stazionario	A	26/11/2016	6120	53524
2081	26	4000	5400	8000	stazionario	154	A	A	A	A	stazionario	A	16/10/2000	12100	53525
2081	27	4.5	5	6	stazionario	3.02	A	A	A	A	stazionario	A	16/10/2000	7.94	53526
2077	23	1900	2500	4500	crescita	76	A	A	A	A	stazionario	A	16/10/2000	8150	53527
2078	2	150	220	350	stazionario	2	A	A	A	A	stazionario	A	25/11/2016	270	53528
2078	8	910	2000	3200	stazionario	7	A	A	A	A	stazionario	A	15/10/2000	4250	53529
2078	14	600	850	1500	crescita	9	A	A	A	A	stazionario	A	25/11/2016	3120	53530
2078	20	440	620	1150	diminuzione	22	A	A	A	A	stazionario	A	25/11/2016	2200	53531
2078	26	4000	5400	8000	stazionario	165	A	A	A	A	stazionario	A	16/10/2000	12100	53532
2079	2	150	220	350	diminuzione	2	A	A	A	A	stazionario	A	25/11/2016	270	53533
2079	8	910	2000	3200	crescita	8	A	A	A	A	stazionario	A	15/10/2000	4250	53534
2079	14	600	850	1500	stazionario	9	A	A	A	A	stazionario	A	25/11/2016	3120	53535
2079	20	440	620	1150	diminuzione	27	A	A	A	A	stazionario	A	25/11/2016	2200	53536
2079	26	4000	5400	8000	stazionario	174	A	A	A	A	stazionario	A	16/10/2000	12100	53537
2080	2	150	220	350	stazionario	2	A	A	A	A	stazionario	A	25/11/2016	270	53538
2080	6	450	700	1200	stazionario	3	A	A	A	A	stazionario	A	14/10/2000	1500	53539
2080	10	250	370	670	stazionario	6	A	A	A	A	stazionario	A	13/06/2000	835	53540
2080	14	600	850	1500	stazionario	8	A	A	A	A	stazionario	A	25/11/2016	3120	53541
2080	18	1500	2200	3000	stazionario	42	A	A	A	A	stazionario	A	06/11/1994	4400	53542
2080	22	1000	1800	3200	crescita	34	A	A	A	A	stazionario	A	25/11/2016	4430	53543
2080	26	4000	5400	8000	stazionario	157	A	A	A	A	stazionario	A	16/10/2000	12100	53544
2077	24	1900	2500	4500	stazionario	74	A	A	A	A	stazionario	A	25/11/2016	4950	53545
2078	3	300	550	900	crescita	2	A	A	A	A	stazionario	A	25/11/2016	1310	53546
2078	9	750	980	1900	stazionario	10	A	A	A	A	stazionario	A	15/10/2000	2640	53547
2078	15	850	1300	2000	stazionario	21	A	A	A	A	stazionario	A	06/11/1994	4200	53548
2078	21	680	900	1500	diminuzione	24	A	A	A	A	stazionario	A	25/11/2016	2500	53549
2078	27	4.5	5	6	stazionario	2.99	A	A	A	A	stazionario	A	16/10/2000	7.94	53550
2079	3	300	550	900	stazionario	2	A	A	A	A	stazionario	A	25/11/2016	1310	53551
2079	9	750	980	1900	diminuzione	14	A	A	A	A	stazionario	A	15/10/2000	2640	53552
2079	15	850	1300	2000	diminuzione	19	A	A	A	A	stazionario	A	06/11/1994	4200	53553
2079	21	680	900	1500	stazionario	32	A	A	A	A	stazionario	A	25/11/2016	2500	53554
2079	27	4.5	5	6	stazionario	3.0	A	A	A	A	stazionario	A	16/10/2000	7.94	53555
2080	3	300	550	900	stazionario	1	A	A	A	A	stazionario	A	25/11/2016	1310	53556
2080	7	540	800	1400	diminuzione	6	A	A	A	A	stazionario	A	15/10/2000	3100	53557
2080	11	160	280	400	crescita	1	A	A	A	A	stazionario	A	27/04/2009	425	53558
2080	15	850	1300	2000	stazionario	20	A	A	A	A	stazionario	A	06/11/1994	4200	53559
2080	19	600	800	1500	diminuzione	0	A	A	A	A	stazionario	A	26/11/2002	1300	53560
2080	23	1900	2500	4500	crescita	74	A	A	A	A	stazionario	A	16/10/2000	8150	53561
2080	27	4.5	5	6	stazionario	3.0	A	A	A	A	stazionario	A	16/10/2000	7.94	53562
2077	25	2600	3300	6000	diminuzione	93	A	A	A	A	stazionario	A	26/11/2016	6120	53563
2078	4	160	290	490	stazionario	7	A	A	A	A	stazionario	A	25/11/2016	550	53564
2078	10	250	370	670	stazionario	4	A	A	A	A	stazionario	A	13/06/2000	835	53565
2078	16	900	1400	2100	stazionario	31	A	A	A	A	stazionario	A	25/11/2016	3450	53566
2078	22	1000	1800	3200	stazionario	29	A	A	A	A	stazionario	A	25/11/2016	4430	53567
2079	4	160	290	490	diminuzione	6	A	A	A	A	stazionario	A	25/11/2016	550	53568
2079	10	250	370	670	stazionario	5	A	A	A	A	stazionario	A	13/06/2000	835	53569
2079	16	900	1400	2100	stazionario	30	A	A	A	A	stazionario	A	25/11/2016	3450	53570
2079	22	1000	1800	3200	crescita	37	A	A	A	A	stazionario	A	25/11/2016	4430	53571
2080	4	160	290	490	diminuzione	7	A	A	A	A	stazionario	A	25/11/2016	550	53572
2080	8	910	2000	3200	stazionario	6	A	A	A	A	stazionario	A	15/10/2000	4250	53573
2080	12	540	870	1400	diminuzione	1	A	A	A	A	stazionario	A	25/11/2016	2110	53574
2080	16	900	1400	2100	stazionario	32	A	A	A	A	stazionario	A	25/11/2016	3450	53575
2080	20	440	620	1150	diminuzione	21	A	A	A	A	stazionario	A	25/11/2016	2200	53576
2080	24	1900	2500	4500	stazionario	76	A	A	A	A	stazionario	A	25/11/2016	4950	53577
2077	26	4000	5400	8000	stazionario	163	A	A	A	A	stazionario	A	16/10/2000	12100	53578
2078	5	520	730	1400	diminuzione	1	A	A	A	A	stazionario	A	25/11/2016	1500	53579
2078	11	160	280	400	crescita	0	A	A	A	A	stazionario	A	27/04/2009	425	53580
2078	17	1000	1500	2200	stazionario	30	A	A	A	A	stazionario	A	28/04/2009	2000	53581
2078	23	1900	2500	4500	crescita	72	A	A	A	A	stazionario	A	16/10/2000	8150	53582
2079	5	520	730	1400	diminuzione	1	A	A	A	A	stazionario	A	25/11/2016	1500	53583
2079	11	160	280	400	crescita	1	A	A	A	A	stazionario	A	27/04/2009	425	53584
2079	17	1000	1500	2200	stazionario	29	A	A	A	A	stazionario	A	28/04/2009	2000	53585
2079	23	1900	2500	4500	crescita	76	A	A	A	A	stazionario	A	16/10/2000	8150	53586
2077	27	4.5	5	6	stazionario	2.97	A	A	A	A	stazionario	A	16/10/2000	7.94	53587
2078	6	450	700	1200	crescita	4	A	A	A	A	stazionario	A	14/10/2000	1500	53588
2078	12	540	870	1400	diminuzione	2	A	A	A	A	stazionario	A	25/11/2016	2110	53589
2078	18	1500	2200	3000	stazionario	47	A	A	A	A	stazionario	A	06/11/1994	4400	53590
2078	24	1900	2500	4500	diminuzione	68	A	A	A	A	stazionario	A	25/11/2016	4950	53591
2079	6	450	700	1200	stazionario	3	A	A	A	A	stazionario	A	14/10/2000	1500	53592
2079	12	540	870	1400	diminuzione	1	A	A	A	A	stazionario	A	25/11/2016	2110	53593
2079	18	1500	2200	3000	stazionario	43	A	A	A	A	stazionario	A	06/11/1994	4400	53594
2079	24	1900	2500	4500	diminuzione	83	A	A	A	A	stazionario	A	25/11/2016	4950	53595
\.


--
-- Name: w22_data_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w22_data
    ADD CONSTRAINT w22_data_pkey PRIMARY KEY (id_w22_data);


--
-- Name: w22_data_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w22_data
    ADD CONSTRAINT w22_data_fkey001 FOREIGN KEY (id_w22) REFERENCES public.w22(id_w22) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w22_data_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w22_data
    ADD CONSTRAINT w22_data_fkey002 FOREIGN KEY (id_w22_zone) REFERENCES public.w22_zone(id_w22_zone) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TABLE w22_data; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
