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
-- Name: ozono_livelli; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.ozono_livelli (
    id_ozono_livelli smallint NOT NULL,
    livelli integer NOT NULL,
    soglia_inferiore_mxd integer NOT NULL,
    soglia_superiore_mxd integer NOT NULL,
    soglia_inferiore_mx8 integer NOT NULL,
    soglia_superiore_mx8 integer NOT NULL,
    riferimento_legge text NOT NULL,
    colore character varying(20) NOT NULL,
    rgb text NOT NULL,
    sintesi_raccomandazioni text,
    descrizione text,
    raccomandazione text,
    valid_from timestamp(0) without time zone NOT NULL,
    valid_to timestamp(0) without time zone NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.ozono_livelli OWNER TO weboll;

--
-- Data for Name: ozono_livelli; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.ozono_livelli (id_ozono_livelli, livelli, soglia_inferiore_mxd, soglia_superiore_mxd, soglia_inferiore_mx8, soglia_superiore_mx8, riferimento_legge, colore, rgb, sintesi_raccomandazioni, descrizione, raccomandazione, valid_from, valid_to, last_update, username) FROM stdin;
1	0	0	180	0	110	DGR 27-614 31/07/2000	verde	0:255:0	Non si rendono necessarie particolari raccomandazioni.	Quando i valori di concentrazione\r\ndell'ozono nell'aria sono inferiori a\r\n110 μg/m3 nell'arco delle otto ore\r\noppure a 180 μg/m3 in un'ora.	Non si rendono necessarie particolari raccomandazioni.	2010-05-27 00:00:00	9999-12-30 00:00:00	2010-06-14 07:49:37	weboll
2	1	180	240	110	140	DGR 27-614 31/07/2000	giallo	255:255:0	Le categorie più sensibili, cioè bambini, anziani, asmatici, bronchitici cronici, cardiopatici, devono evitare\r di svolgere attività fisica anche moderata all'aperto, come ad esempio camminare velocemente, in particolare nelle ore più calde e di massima insolazione della giornata.	Quando i valori di concentrazione\r\ndell'ozono nell'aria possono\r\nsuperare i 110 μg /m3 nell'arco\r\ndelle otto ore oppure i 180 μg /m3\r\nnell'ora.	Le categorie più sensibili, cioè bambini, anziani, asmatici, bronchitici cronici,\r cardiopatici, devono evitare di svolgere attività fisica anche moderata all'aperto, come ad esempio camminare velocemente, in particolare nelle ore più calde e di\r massima insolazione della giornata.\r Si consiglia a tutta la popolazione di integrare la propria dieta con cibi contenenti sostanze antiossidanti. Nella tabella che segue sono riportate alcune indicazioni in merito.	2010-05-27 00:00:00	9999-12-30 00:00:00	2010-06-14 07:49:41	weboll
3	2	240	360	140	220	DGR 27-614 31/07/2000	arancione	255:165:0	Le categorie più sensibili devono evitare di svolgere qualsiasi attività fisica all'aperto, specie nelle ore\r di massima insolazione. I soggetti mediamente sensibili devono evitare di svolgere all'aperto attività fisica intensa, specie nelle ore di massima insolazione. Tutta la popolazione deve evitare nelle ore di\r massima insolazione di fare attività fisica molto intensa all'aperto.	Quando i valori di concentrazione\r\ndell'ozono nell'aria possono\r\nsuperare i 140 μg/m3 nell'arco delle\r\notto ore oppure i 240 μg/m3 nell'ora	Le categorie più sensibili, cioè bambini, anziani, asmatici, bronchitici cronici,\r\ncardiopatici, devono evitare di svolgere qualsiasi attività fisica all'aperto, come ad\r\nesempio correre, in particolare nelle ore più calde e di massima insolazione della\r\ngiornata.\r\nI soggetti mediamente sensibili come gli adolescenti, devono evitare di svolgere\r\nall'aperto attività fisica intensa, come ad esempio correre, in particolare nelle ore\r\npiù calde e di massima insolazione della giornata.\r\nTutta la popolazione, quindi anche i soggetti meno sensibili, come gli adulti sani,\r\ndevono evitare nelle ore più calde e di massima insolazione della giornata, di fare\r\nsforzi fisici all'aperto che comportano un attività fisica molto intensa, come ad\r\nesempio correre velocemente.\r\nSi consiglia a tutta la popolazione di integrare la propria dieta con cibi contenenti\r\nsostanze antiossidanti. nella tabella che segue sono riportate alcune indicazioni in\r\nmerito.	2010-05-27 00:00:00	9999-12-30 00:00:00	2010-06-14 07:49:45	weboll
4	3	360	999	220	999	DGR 27-614 31/07/2000	rosso	255.00.00	Le categorie più sensibili devono evitare di uscire di casa, specie nelle ore di massima insolazione. I\r soggetti mediamente sensibili devono evitare di svolgere all'aperto attività fisica anche moderata specie nelle ore di massima insolazione. Tutta la popolazione deve evitare nelle ore più calde di svolgere intensa attività fisica all'aperto.	Quando i valori di concentrazione\r\ndell'ozono nell'aria possono\r\nsuperare i 220 μg/m3 nell'arco delle\r\notto ore oppure i 360 μg/m3 nell'ora	Le categorie più sensibili, cioè bambini, anziani, asmatici, bronchitici cronici,\r\ncardiopatici, devono evitare di uscire di casa e di svolgere qualsiasi attività fisica\r\nall'aperto, in particolare durante le ore più calde e di massima insolazione della\r\ngiornata.\r\nI soggetti mediamente sensibili, come gli adolescenti, devono evitare di svolgere\r\nall'aperto attività fisica anche moderata, come ad esempio camminare\r\nvelocemente, in particolare nelle ore più calde e di massima insolazione della\r\ngiornata.\r\nTutta la popolazione, quindi anche i soggetti meno sensibili, come gli adulti sani,\r\ndevono evitare nelle ore più calde e di massima insolazione della giornata, di fare\r\nsforzi fisici all'aperto che comportano un intensa attività fisica, come ad esempio\r\ncorrere.\r\nSi consiglia a tutta la popolazione di integrare la propria dieta con cibi contenenti\r\nsostanze antiossidanti. nella tabella che segue sono riportate alcune indicazioni in\r\nmerito.	2010-05-27 00:00:00	9999-12-30 00:00:00	2010-06-14 07:49:49	weboll
0	999	0	0	0	0	nessun riferimento	bianco	nessun rgb	\N	\N	\N	2011-03-31 00:00:00	9999-12-30 00:00:00	2011-04-20 14:10:46	weboll
\.


--
-- Name: ozono_livelli_id_ozono_livelli_key; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.ozono_livelli
    ADD CONSTRAINT ozono_livelli_id_ozono_livelli_key UNIQUE (id_ozono_livelli);


--
-- Name: ozono_livelli_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.ozono_livelli
    ADD CONSTRAINT ozono_livelli_pkey PRIMARY KEY (livelli, valid_from, valid_to);


--
-- Name: TABLE ozono_livelli; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

