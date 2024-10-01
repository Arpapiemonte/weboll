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
-- Name: venue; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.comune_aree_allertamento (
	denominazione varchar(40) NULL,
	codice_comune varchar(6) NULL,
	id_allertamento varchar(6) NULL
);


ALTER TABLE public.comune_aree_allertamento OWNER TO weboll;

--
-- Data for Name: venue; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.comune_aree_allertamento (denominazione, codice_comune, id_allertamento) FROM stdin delimiter ',';
Parella,001179,Piem-I
Porte,001200,Piem-D
Salassa,001231,Piem-L
Villanova Canavese,001301,Piem-L
Venasca,004237,Piem-E
Villar San Costanzo,004247,Piem-E
Tarantasca,004225,Piem-M
Arignano,001012,Piem-L
Villaromagnano,006186,Piem-H
Bricherasio,001035,Piem-D
Bricherasio,001035,Piem-M
Brusasco,001039,Piem-I
Brozolo,001037,Piem-I
Cascinette d''Ivrea,001061,Piem-I
Burolo,001042,Piem-I
Cercenasco,001071,Piem-L
Castiglione Torinese,001068,Piem-L
Ciconio,001083,Piem-L
Castagnole Piemonte,001065,Piem-L
Forno Canavese,001107,Piem-C
Foglizzo,001106,Piem-L
Alpette,001007,Piem-C
Sala Biellese,096057,Piem-I
Gifflenga,096027,Piem-I
Reano,001211,Piem-L
Piobesi Torinese,001193,Piem-L
Albaretto della Torre,004004,Piem-F
Romano Canavese,001223,Piem-I
San Giusto Canavese,001246,Piem-L
San Gillio,001243,Piem-L
San Ponso,001251,Piem-L
Settimo Vittone,001266,Piem-B
Monasterolo di Savigliano,004128,Piem-M
Arborio,002006,Piem-I
Volpiano,001314,Piem-L
San Giacomo Vercellese,002035,Piem-I
Lamporo,002067,Piem-I
Asigliano Vercellese,002007,Piem-I
Cavallirio,003047,Piem-I
Pella,003115,Piem-A
Orta San Giulio,003112,Piem-A
Beinette,004016,Piem-F
Bagnasco,004008,Piem-F
Castelletto Stura,004049,Piem-M
Cavallerleone,004058,Piem-M
Cervasca,004064,Piem-M
Cervasca,004064,Piem-E
Roaschia,004183,Piem-E
Gargallo,003070,Piem-I
Margarita,004118,Piem-F
Frabosa Soprana,004090,Piem-F
Grinzane Cavour,004100,Piem-F
Martiniana Po,004121,Piem-D
Montelupo Albese,004137,Piem-F
Ostana,004156,Piem-D
Feisoglio,004088,Piem-G
Priero,004175,Piem-F
Piozzo,004169,Piem-F
Rittana,004182,Piem-E
Mango,004115,Piem-G
San Michele Mondovì,004210,Piem-F
Santa Vittoria d''Alba,004212,Piem-F
Belveglio,005008,Piem-G
Villafalletto,004244,Piem-M
Vezza d''Alba,004241,Piem-L
Terzo,006172,Piem-G
Villanova Solaro,004246,Piem-M
Vicoforte,004242,Piem-F
Viola,004249,Piem-F
Celle Enomondo,005034,Piem-G
Mombercelli,005066,Piem-G
Acqui Terme,006001,Piem-G
Roccasparvera,004191,Piem-E
Salmour,004202,Piem-M
Volpeglino,006189,Piem-H
Castelletto Monferrato,006051,Piem-G
Cella Monte,006056,Piem-I
Cassinelle,006044,Piem-G
Frascaro,006071,Piem-G
Frassinello Monferrato,006072,Piem-I
Denice,006065,Piem-G
Moncestino,006099,Piem-I
Moasca,005063,Piem-G
Mirabello Monferrato,006094,Piem-I
Molino dei Torti,006096,Piem-H
Orsara Bormida,006119,Piem-G
Paderna,006124,Piem-H
Pozzol Groppo,006137,Piem-H
Valmacca,006178,Piem-I
Cereseto,006057,Piem-I
Castelletto d''Erro,006048,Piem-G
Benna,096003,Piem-I
Bruzolo,001040,Piem-C
Buriasco,001041,Piem-L
Carema,001057,Piem-B
Cafasse,001046,Piem-L
Cafasse,001046,Piem-C
Torrazzo,096069,Piem-I
Andezeno,001009,Piem-L
Balangero,001016,Piem-L
Balangero,001016,Piem-C
Dorzano,096025,Piem-I
Zimone,096081,Piem-I
Airasca,001002,Piem-L
Strona,096065,Piem-B
Strona,096065,Piem-I
Bee,103009,Piem-A
Portula,096048,Piem-B
Ronco Biellese,096053,Piem-B
Verrone,096076,Piem-I
Nomaglio,001167,Piem-B
Pertusio,001187,Piem-L
Pertusio,001187,Piem-C
Bruino,001038,Piem-L
Anzola d''Ossola,103002,Piem-A
Casale Corte Cerro,103019,Piem-A
Trontano,103068,Piem-A
Ternengo,096067,Piem-I
Spineto Scrivia,006166,Piem-H
Dusino San Michele,005052,Piem-L
Olmo Gentile,005081,Piem-G
Rifreddo,004181,Piem-D
Novello,004152,Piem-F
Camino,006027,Piem-I
Montalto Dora,001160,Piem-I
Casapinta,096014,Piem-I
Cossano Canavese,001095,Piem-I
Castellazzo Novarese,003042,Piem-I
Settimo Rottaro,001264,Piem-I
Perosa Canavese,001185,Piem-I
Castagnito,004046,Piem-G
Gambasca,004094,Piem-D
Cervatto,002041,Piem-B
San Giorgio Monferrato,006153,Piem-I
Pila,002096,Piem-B
Santa Maria Maggiore,103062,Piem-A
Bossolasco,004027,Piem-G
Bossolasco,004027,Piem-F
Roccavione,004192,Piem-E
Viguzzolo,006181,Piem-H
Polonghera,004171,Piem-M
Rocchetta Palafea,005095,Piem-G
Mombello di Torino,001153,Piem-L
Viale,005114,Piem-L
Trezzo Tinella,004231,Piem-G
Mercenasco,001150,Piem-I
San Giorio di Susa,001245,Piem-C
Gurro,103036,Piem-A
Quagliuzzo,001208,Piem-I
Casalvolone,003041,Piem-I
Villata,002164,Piem-I
Sandigliano,096059,Piem-I
Albugnano,005002,Piem-L
Meina,003095,Piem-I
Claviere,001087,Piem-D
Alice Castello,002004,Piem-I
Premosello-Chiovenda,103057,Piem-A
Borgo San Martino,006020,Piem-I
Macello,001142,Piem-L
Vignolo,004243,Piem-M
Vignolo,004243,Piem-E
Bozzole,006023,Piem-I
Argentera,004006,Piem-E
Aurano,103005,Piem-A
Viverone,096080,Piem-I
Barbania,001021,Piem-L
Castelnuovo Calcea,005030,Piem-G
Mandello Vitta,003090,Piem-I
Collobiano,002045,Piem-I
Usseaux,001281,Piem-D
Montemagno,005077,Piem-G
Belgirate,103010,Piem-A
Priocca,004176,Piem-L
Clavesana,004071,Piem-F
Sampeyre,004205,Piem-E
Azeglio,001014,Piem-I
Fossano,004089,Piem-M
Coassolo Torinese,001088,Piem-C
Ponti,006134,Piem-G
Vallanzengo,096072,Piem-I
Vallanzengo,096072,Piem-B
Curino,096023,Piem-I
Curino,096023,Piem-B
Brignano-Frascata,006024,Piem-H
Carmagnola,001059,Piem-L
Divignano,003060,Piem-I
Cortandone,005045,Piem-L
Cartosio,006036,Piem-G
Tagliolo Monferrato,006169,Piem-G
Coggiola,096019,Piem-B
Balmuccia,002008,Piem-B
Monastero di Lanzo,001155,Piem-C
Valgioie,001285,Piem-C
Ornavasso,103051,Piem-A
Trisobbio,006176,Piem-G
Cuceglio,001096,Piem-L
Isolabella,001123,Piem-L
Torre Pellice,001275,Piem-D
Montemale di Cuneo,004138,Piem-E
Castelspina,006054,Piem-G
Prasco,006139,Piem-G
Rivalta Bormida,006144,Piem-G
Castelletto Uzzone,004050,Piem-G
Gabiano,006077,Piem-I
Mombaldone,005064,Piem-G
Riva presso Chieri,001215,Piem-L
Mergozzo,103044,Piem-A
Casal Cermelli,006037,Piem-G
Marmora,004119,Piem-E
Pontecurone,006132,Piem-H
Rocchetta Ligure,006148,Piem-H
Ferrere,005053,Piem-L
Cardè,004042,Piem-M
San Marzano Oliveto,005100,Piem-G
Tortona,006174,Piem-H
Scopello,002135,Piem-B
Serravalle Scrivia,006160,Piem-H
San Giorgio Canavese,001244,Piem-L
Varzo,103071,Piem-A
Valenza,006177,Piem-I
Borgo Ticino,003025,Piem-I
Vaie,001283,Piem-C
Torresina,004229,Piem-F
Sinio,004220,Piem-F
Bobbio Pellice,001026,Piem-D
Niella Tanaro,004151,Piem-F
Castiglione Tinella,004056,Piem-G
Cerano,003049,Piem-I
Dronero,004082,Piem-E
San Damiano Macra,004207,Piem-E
Greggio,002065,Piem-I
San Giorgio Scarampi,005098,Piem-G
Masio,006091,Piem-G
Borgosesia,002016,Piem-B
Lesa,003084,Piem-A
Fabbrica Curone,006067,Piem-H
Nichelino,001164,Piem-L
Grugliasco,001120,Piem-L
Campiglia Cervo,096086,Piem-B
Rocca Canavese,001221,Piem-L
Rocca Canavese,001221,Piem-C
Pont Canavese,001199,Piem-C
Bellinzago Novarese,003016,Piem-I
Mezzomerico,003097,Piem-I
Gattico-Veruno,003166,Piem-I
Quaregna Cerreto,096087,Piem-I
Magnano,096030,Piem-I
Alagna Valsesia,002002,Piem-B
Monforte d''Alba,004132,Piem-F
Cartignano,004044,Piem-E
Gravere,001117,Piem-D
Chivasso,001082,Piem-L
Castelnuovo Nigra,001067,Piem-C
Bannio Anzino,103007,Piem-A
Cassine,006043,Piem-G
Altavilla Monferrato,006007,Piem-G
Costigliole d''Asti,005050,Piem-G
Ponderano,096047,Piem-I
Pinerolo,001191,Piem-C
Pinerolo,001191,Piem-L
Moncrivello,002079,Piem-I
Desana,002054,Piem-I
Frassinetto,001108,Piem-C
Giaveno,001115,Piem-C
Giaveno,001115,Piem-L
Alba,004003,Piem-F
Albano Vercellese,002003,Piem-I
Santena,001257,Piem-L
Isola d''Asti,005059,Piem-G
Rivalba,001213,Piem-L
Pisano,003119,Piem-A
Brandizzo,001034,Piem-L
Caravino,001056,Piem-I
Pontechianale,004172,Piem-E
Mollia,002078,Piem-B
Frossasco,001110,Piem-L
Frossasco,001110,Piem-C
San Sebastiano da Po,001253,Piem-L
Casaleggio Novara,003039,Piem-I
Carrosio,006035,Piem-G
Voltaggio,006190,Piem-G
Pralormo,001203,Piem-L
Noasca,001165,Piem-C
Portacomaro,005087,Piem-G
Basaluzzo,006012,Piem-G
Borgomale,004024,Piem-G
None,001168,Piem-L
Cortemilia,004073,Piem-G
Ticineto,006173,Piem-I
Visone,006187,Piem-G
Front,001109,Piem-L
Busano,001043,Piem-L
Isola Sant''Antonio,006087,Piem-I
Isola Sant''Antonio,006087,Piem-H
Cellarengo,005033,Piem-L
Boves,004028,Piem-F
Ameno,003002,Piem-A
Oncino,004154,Piem-D
La Loggia,001127,Piem-L
Borghetto di Borbera,006018,Piem-H
Montegrosso d''Asti,005076,Piem-G
Candelo,096012,Piem-I
Dogliani,004081,Piem-F
Cantalupo Ligure,006028,Piem-H
Mondovì,004130,Piem-F
Bistagno,006017,Piem-G
Montecastello,006105,Piem-G
Alfiano Natta,006004,Piem-L
Mombarcaro,004124,Piem-G
Ailoche,096001,Piem-B
Paesana,004157,Piem-D
Intragna,103037,Piem-A
San Pietro Val Lemina,001250,Piem-C
Macra,004112,Piem-E
Traversella,001278,Piem-B
Maglione,001143,Piem-I
Garbagna,006079,Piem-H
Vauda Canavese,001290,Piem-L
Albera Ligure,006002,Piem-H
Fobello,002057,Piem-B
Postua,002102,Piem-B
Serralunga di Crea,006159,Piem-I
Vinovo,001309,Piem-L
Morbello,006110,Piem-G
Belforte Monferrato,006014,Piem-G
Piea,005084,Piem-L
Valdieri,004233,Piem-E
Camburzano,096010,Piem-B
San Didero,001239,Piem-C
Agliè,001001,Piem-L
Pomaretto,001198,Piem-D
Coazze,001089,Piem-C
Rovasenda,002122,Piem-I
Roure,001227,Piem-D
Revello,004180,Piem-M
Vernante,004239,Piem-E
Pettinengo,096042,Piem-B
Peveragno,004163,Piem-F
Niella Belbo,004150,Piem-G
Quattordio,006142,Piem-G
Ceres,001072,Piem-C
Vische,001311,Piem-I
Quarona,002107,Piem-B
Bosia,004026,Piem-G
Santhià,002133,Piem-I
Grognardo,006084,Piem-G
Villanova Monferrato,006185,Piem-I
Cavour,001070,Piem-M
Baldichieri d''Asti,005007,Piem-L
Massello,001145,Piem-D
Berzano di Tortona,006016,Piem-H
Quaranti,005088,Piem-G
Barengo,003012,Piem-I
Pocapaglia,004170,Piem-M
Lignana,002070,Piem-I
Capriglio,005019,Piem-L
Moncalieri,001156,Piem-L
Rivarossa,001218,Piem-L
Rueglio,001230,Piem-B
Roppolo,096054,Piem-I
Cesana Torinese,001074,Piem-D
Pomaro Monferrato,006131,Piem-I
Marene,004117,Piem-M
Limone Piemonte,004110,Piem-E
Oglianico,001170,Piem-L
Muzzano,096038,Piem-B
Montanaro,001161,Piem-L
Roletto,001222,Piem-C
Roletto,001222,Piem-L
Odalengo Grande,006116,Piem-I
Demonte,004079,Piem-E
Montaldo Roero,004135,Piem-M
Montaldeo,006103,Piem-G
Veglio,096075,Piem-B
Toceno,103065,Piem-A
Nucetto,004153,Piem-F
Cherasco,004067,Piem-M
Cherasco,004067,Piem-F
Scarnafigi,004217,Piem-M
San Paolo Solbrito,005101,Piem-L
Caltignaga,003030,Piem-I
Briga Novarese,003026,Piem-I
Salbertrand,001232,Piem-D
Cossato,096020,Piem-I
Bra,004029,Piem-M
Trofarello,001280,Piem-L
Druogno,103029,Piem-A
Roccabruna,004187,Piem-E
Santo Stefano Roero,004214,Piem-L
Villarboit,002163,Piem-I
Isasca,004103,Piem-E
Casale Monferrato,006039,Piem-I
San Colombano Belmonte,001238,Piem-C
Formigliana,002059,Piem-I
Borgiallo,001029,Piem-C
Baceno,103006,Piem-A
Brusnengo,096007,Piem-I
Cerreto Grue,006058,Piem-H
Pezzolo Valle Uzzone,004164,Piem-G
Piossasco,001194,Piem-L
Murazzano,004145,Piem-F
Valfenera,005112,Piem-L
Torre Bormida,004226,Piem-G
Guazzora,006086,Piem-H
Omegna,103050,Piem-A
Tricerro,002147,Piem-I
Castelletto d''Orba,006049,Piem-G
Casteldelfino,004047,Piem-E
Sant''Agata Fossili,006156,Piem-H
Pray,096050,Piem-B
Alzano Scrivia,006008,Piem-H
Bosco Marengo,006021,Piem-G
Vinadio,004248,Piem-E
Monasterolo Casotto,004127,Piem-F
Garbagna Novarese,003069,Piem-I
Quarna Sotto,103059,Piem-A
La Cassa,001126,Piem-L
La Cassa,001126,Piem-C
Mattie,001147,Piem-C
Govone,004099,Piem-G
Gaglianico,096026,Piem-I
Villadossola,103075,Piem-A
Serravalle Sesia,002137,Piem-B
Cerretto Langhe,004063,Piem-F
Cerretto Langhe,004063,Piem-G
Briaglia,004030,Piem-F
Calosso,005015,Piem-G
Cossombrato,005049,Piem-L
Mompantero,001154,Piem-C
Roasio,002116,Piem-I
Grignasco,003079,Piem-I
Lessona,096085,Piem-I
Trarego Viggiona,103066,Piem-A
Beura-Cardezza,103011,Piem-A
Narzole,004147,Piem-F
Rocchetta Tanaro,005096,Piem-G
Salussola,096058,Piem-I
Montacuto,006102,Piem-H
Vercelli,002158,Piem-I
Castelnuovo Belbo,005029,Piem-G
Givoletto,001116,Piem-L
Givoletto,001116,Piem-C
Albiano d''Ivrea,001004,Piem-I
Avigliana,001013,Piem-L
Ghiffa,103033,Piem-A
Borgomanero,003024,Piem-I
Maggiora,003088,Piem-I
Sparone,001267,Piem-C
Villafranca d''Asti,005117,Piem-L
Canelli,005017,Piem-G
Montezemolo,004141,Piem-G
Montezemolo,004141,Piem-F
Casasco,006041,Piem-H
Mappano,001316,Piem-L
Baldissero Canavese,001017,Piem-I
Stroppo,004224,Piem-E
Fontanetto Po,002058,Piem-I
Guardabosone,002066,Piem-B
Valdengo,096071,Piem-I
San Benedetto Belbo,004206,Piem-G
Alessandria,006003,Piem-G
Borgaro Torinese,001028,Piem-L
Canischio,001052,Piem-C
Chiusa di Pesio,004068,Piem-F
Perosa Argentina,001184,Piem-D
Carrega Ligure,006034,Piem-H
Crescentino,002049,Piem-I
Valstrona,103069,Piem-A
Momperone,006098,Piem-H
Murisengo,006113,Piem-L
Refrancore,005089,Piem-G
Rorà,001226,Piem-D
Cavaglià,096016,Piem-I
Vocca,002166,Piem-B
Castagnole delle Lanze,005022,Piem-G
Cantarana,005018,Piem-L
Roatto,005091,Piem-L
Montiglio Monferrato,005121,Piem-L
Pradleves,004173,Piem-E
Maranzana,005061,Piem-G
Bardonecchia,001022,Piem-D
Felizzano,006068,Piem-G
Andorno Micca,096002,Piem-B
Rivarolo Canavese,001217,Piem-L
Cerreto d''Asti,005035,Piem-L
Ponzano Monferrato,006135,Piem-I
Castellamonte,001066,Piem-C
Castellamonte,001066,Piem-L
Moiola,004123,Piem-E
Collegno,001090,Piem-L
Condove,001093,Piem-C
Mongardino,005071,Piem-G
Centallo,004061,Piem-M
Cavaglietto,003044,Piem-I
Passerano Marmorito,005082,Piem-L
Domodossola,103028,Piem-A
Carcoforo,002029,Piem-B
Piscina,001195,Piem-L
Vigliano d''Asti,005116,Piem-G
Monteu da Po,001162,Piem-I
Rimella,002113,Piem-B
Cervere,004065,Piem-M
Gozzano,003076,Piem-I
Castelnuovo Don Bosco,005031,Piem-L
Druento,001099,Piem-L
Penango,005083,Piem-L
Scurzolengo,005103,Piem-G
Biandrate,003018,Piem-I
Cavagnolo,001069,Piem-I
Belvedere Langhe,004018,Piem-F
Briga Alta,004031,Piem-F
Oviglio,006122,Piem-G
Olivola,006118,Piem-I
Stazzano,006167,Piem-H
Coazzolo,005041,Piem-G
Caselette,001062,Piem-C
Caselette,001062,Piem-L
Aisone,004002,Piem-E
Stroppiana,002142,Piem-I
Envie,004085,Piem-M
Envie,004085,Piem-D
San Germano Chisone,001242,Piem-D
Exilles,001100,Piem-D
Sagliano Micca,096056,Piem-B
Caresanablot,002031,Piem-I
Tassarolo,006170,Piem-G
Sale,006151,Piem-H
Baldissero d''Alba,004010,Piem-M
Busca,004034,Piem-E
Busca,004034,Piem-M
Moncenisio,001157,Piem-C
Caluso,001047,Piem-L
Borgo d''Ale,002015,Piem-I
Mornese,006111,Piem-G
Fontaneto d''Agogna,003066,Piem-I
Camerano Casasco,005016,Piem-L
Cortiglione,005048,Piem-G
Rosta,001228,Piem-L
Buttigliera Alta,001045,Piem-L
Magliano Alfieri,004113,Piem-G
Cureggio,003058,Piem-I
Canale,004037,Piem-L
Montabone,005072,Piem-G
Monticello d''Alba,004142,Piem-F
Tornaco,003146,Piem-I
Revigliasco d''Asti,005090,Piem-G
Premeno,103055,Piem-A
Berzano di San Pietro,005009,Piem-L
Bruno,005010,Piem-G
Montaldo Bormida,006104,Piem-G
Gaiola,004093,Piem-E
Nizza Monferrato,005080,Piem-G
Castelmagno,004053,Piem-E
Loazzolo,005060,Piem-G
Torre San Giorgio,004228,Piem-M
Novi Ligure,006114,Piem-H
Novi Ligure,006114,Piem-G
Bergamasco,006015,Piem-G
Scopa,002134,Piem-B
Favria,001101,Piem-L
Bollengo,001027,Piem-I
Arona,003008,Piem-I
Cabella Ligure,006025,Piem-H
Quargnento,006141,Piem-G
Tonco,005109,Piem-L
Monterosso Grana,004139,Piem-E
Cannobio,103017,Piem-A
San Raffaele Cimena,001252,Piem-L
Bassignana,006013,Piem-I
Novara,003106,Piem-I
Pramollo,001204,Piem-D
Pietraporzio,004167,Piem-E
Vigliano Biellese,096077,Piem-I
Antrona Schieranco,103001,Piem-A
Castelnuovo Scrivia,006053,Piem-H
Ronco Canavese,001224,Piem-C
Melazzo,006092,Piem-G
Occimiano,006115,Piem-I
Vistrorio,001312,Piem-B
Salasco,002126,Piem-I
Valgrana,004234,Piem-E
Genola,004096,Piem-M
San Nazzaro Sesia,003134,Piem-I
Cocconato,005042,Piem-L
Vinzaglio,003164,Piem-I
Montanera,004136,Piem-M
Perlo,004162,Piem-F
Verduno,004238,Piem-F
San Carlo Canavese,001237,Piem-L
Macugnaga,103039,Piem-A
Bosio,006022,Piem-G
Aramengo,005004,Piem-L
Carezzano,006032,Piem-H
Meana di Susa,001149,Piem-C
Corio,001094,Piem-C
Camerana,004035,Piem-G
Sala Monferrato,006150,Piem-I
Guarene,004101,Piem-F
Crevoladossola,103025,Piem-A
Calasca-Castiglione,103014,Piem-A
Quinto Vercellese,002108,Piem-I
Castagneto Po,001064,Piem-L
Garzigliana,001111,Piem-M
Ceresole Alba,004062,Piem-L
Mongrando,096035,Piem-I
Calamandrana,005013,Piem-G
Mottalciata,096037,Piem-I
Lauriano,001129,Piem-I
Carpeneto,006033,Piem-G
Malesco,103041,Piem-A
Rossa,002121,Piem-B
Robassomero,001220,Piem-L
Pertengo,002091,Piem-I
Bolzano Novarese,003022,Piem-I
Carignano,001058,Piem-L
Casalbeltrame,003037,Piem-I
Castellero,005026,Piem-L
Battifollo,004015,Piem-F
Cavatore,006055,Piem-G
Tavagnasco,001271,Piem-B
Scagnello,004216,Piem-F
Grazzano Badoglio,005057,Piem-I
Sizzano,003139,Piem-I
Mathi,001146,Piem-L
Mathi,001146,Piem-C
Fresonara,006074,Piem-G
Scarmagno,001261,Piem-I
Pozzolo Formigaro,006138,Piem-G
Pozzolo Formigaro,006138,Piem-H
San Salvatore Monferrato,006154,Piem-I
Graglia,096028,Piem-B
Verolengo,001293,Piem-I
Montechiaro d''Asti,005075,Piem-L
Ozzano Monferrato,006123,Piem-I
Groscavallo,001118,Piem-C
Invorio,003082,Piem-I
Caselle Torinese,001063,Piem-L
Sommariva del Bosco,004222,Piem-M
Lozzolo,002072,Piem-I
Asti,005005,Piem-G
Asti,005005,Piem-L
Mombasiglio,004125,Piem-F
Perletto,004161,Piem-G
Recetto,003129,Piem-I
Settime,005106,Piem-L
Vignone,103074,Piem-A
Gamalero,006078,Piem-G
Cortazzone,005047,Piem-L
Premia,103056,Piem-A
Ivrea,001125,Piem-I
Boccioleto,002014,Piem-B
Villanova d''Asti,005118,Piem-L
Ormea,004155,Piem-F
Caprile,096013,Piem-B
Ghemme,003073,Piem-I
Sozzago,003141,Piem-I
Locana,001134,Piem-C
Rive,002115,Piem-I
Volvera,001315,Piem-L
Palazzo Canavese,001177,Piem-I
Venaria Reale,001292,Piem-L
Vespolate,003158,Piem-I
Montaldo Torinese,001158,Piem-L
Gottasecca,004098,Piem-G
Comignago,003052,Piem-I
Pino d''Asti,005085,Piem-L
Buronzo,002021,Piem-I
Settimo Torinese,001265,Piem-L
Perrero,001186,Piem-D
Pietra Marazzi,006129,Piem-G
Sommariva Perno,004223,Piem-M
Pagno,004158,Piem-D
Monchiero,004129,Piem-F
Lequio Tanaro,004107,Piem-F
Madonna del Sasso,103040,Piem-A
Villette,103076,Piem-A
Ceva,004066,Piem-F
Orbassano,001171,Piem-L
Vignole Borbera,006180,Piem-H
Prazzo,004174,Piem-E
Moncucco Torinese,005070,Piem-L
Campertogno,002025,Piem-B
Varisella,001289,Piem-L
Varisella,001289,Piem-C
Pontestura,006133,Piem-I
Castellazzo Bormida,006047,Piem-G
Bagnolo Piemonte,004009,Piem-M
Bagnolo Piemonte,004009,Piem-D
Bastia Mondovì,004014,Piem-F
Verbania,103072,Piem-A
Cremolino,006063,Piem-G
Rassa,002110,Piem-B
Montegioco,006107,Piem-H
Vignale Monferrato,006179,Piem-I
Caraglio,004040,Piem-M
La Morra,004105,Piem-F
Miazzina,103045,Piem-A
Marentino,001144,Piem-L
Grondona,006085,Piem-H
Cuneo,004078,Piem-M
Piovà Massaia,005086,Piem-L
Sessame,005105,Piem-G
Sauze d''Oulx,001259,Piem-D
Crissolo,004077,Piem-D
Villafranca Piemonte,001300,Piem-M
Borgo Vercelli,002017,Piem-I
Almese,001006,Piem-C
Almese,001006,Piem-L
Bene Vagienna,004019,Piem-F
Bene Vagienna,004019,Piem-M
Cossogno,103023,Piem-A
Tollegno,096068,Piem-B
Mazzè,001148,Piem-I
Villarbasse,001302,Piem-L
Cambiano,001048,Piem-L
Galliate,003068,Piem-I
Cressa,003055,Piem-I
Vanzone con San Carlo,103070,Piem-A
Levice,004109,Piem-G
Piode,002097,Piem-B
Ozegna,001176,Piem-L
Bogogno,003021,Piem-I
Cravanzana,004076,Piem-G
Soriso,003140,Piem-I
Sambuco,004204,Piem-E
Campiglione Fenile,001049,Piem-M
Bernezzo,004022,Piem-M
Bernezzo,004022,Piem-E
Pecetto Torinese,001183,Piem-L
Occhieppo Superiore,096041,Piem-B
Villar Focchiardo,001305,Piem-C
Coniolo,006060,Piem-I
Castelletto Cervo,096015,Piem-I
Canosio,004038,Piem-E
Avolasca,006010,Piem-H
Susa,001270,Piem-C
Gremiasco,006083,Piem-H
Caprezzo,103018,Piem-A
Armeno,003006,Piem-A
Trasquera,103067,Piem-A
Trinità,004232,Piem-M
Trinità,004232,Piem-F
Traves,001279,Piem-C
Prunetto,004178,Piem-G
Castellar Guidobono,006046,Piem-H
Barone Canavese,001023,Piem-L
Cortanze,005046,Piem-L
Camagna Monferrato,006026,Piem-I
Romentino,003131,Piem-I
Rivara,001216,Piem-C
Rivara,001216,Piem-L
Netro,096039,Piem-B
Occhieppo Inferiore,096040,Piem-B
Germagno,103032,Piem-A
Frassino,004092,Piem-E
Valduggia,002152,Piem-B
Barolo,004013,Piem-F
Donato,096024,Piem-B
Valperga,001287,Piem-L
Valperga,001287,Piem-C
Garessio,004095,Piem-F
Beinasco,001024,Piem-L
Valloriate,004235,Piem-E
Livorno Ferraris,002071,Piem-I
Cerrina Monferrato,006059,Piem-I
Rivalta di Torino,001214,Piem-L
Paruzzaro,003114,Piem-I
Cumiana,001097,Piem-L
Cumiana,001097,Piem-C
San Germano Vercellese,002131,Piem-I
Pecetto di Valenza,006128,Piem-I
Strambino,001269,Piem-I
Motta de Conti,002082,Piem-I
Bairo,001015,Piem-L
Benevello,004020,Piem-G
Rubiana,001229,Piem-C
Feletto,001102,Piem-L
Sciolze,001262,Piem-L
Montà,004133,Piem-L
Fraconalto,006069,Piem-G
Fraconalto,006069,Piem-H
Torrazza Piemonte,001273,Piem-I
Torre Canavese,001274,Piem-I
Quassolo,001209,Piem-B
Roascio,004184,Piem-F
Sant''Ambrogio di Torino,001255,Piem-C
Antignano,005003,Piem-G
San Maurizio Canavese,001248,Piem-L
Ronsecco,002118,Piem-I
Palazzolo Vercellese,002090,Piem-I
Entracque,004084,Piem-E
Crevacuore,096021,Piem-B
Crova,002052,Piem-I
Sillavengo,003138,Piem-I
Pianfei,004165,Piem-F
Bonvicino,004023,Piem-F
Vicolungo,003159,Piem-I
Vinchio,005120,Piem-G
Montechiaro d''Acqui,006106,Piem-G
San Damiano d''Asti,005097,Piem-L
Candiolo,001051,Piem-L
Castellinaldo d''Alba,004051,Piem-L
Borgomasino,001031,Piem-I
Oggebbio,103049,Piem-A
Neviglie,004149,Piem-G
Azzano d''Asti,005006,Piem-G
Nebbiuno,003103,Piem-A
Banchette,001020,Piem-I
Miagliano,096034,Piem-B
Salza di Pinerolo,001234,Piem-D
Mezzenile,001152,Piem-C
Rivoli,001219,Piem-L
Magliano Alpi,004114,Piem-F
Roburent,004186,Piem-F
Verrua Savoia,001294,Piem-I
Luserna San Giovanni,001139,Piem-D
Osasio,001174,Piem-L
Pessinetto,001188,Piem-C
Piobesi d''Alba,004168,Piem-F
Oulx,001175,Piem-D
Moncalvo,005069,Piem-I
Rosignano Monferrato,006149,Piem-I
Baldissero Torinese,001018,Piem-L
Casalnoceto,006040,Piem-H
Roddino,004195,Piem-F
Lequio Berria,004106,Piem-G
Pavarolo,001180,Piem-L
Ricaldone,006143,Piem-G
Prato Sesia,003122,Piem-I
Marano Ticino,003091,Piem-I
Issiglio,001124,Piem-B
Ceppo Morelli,103021,Piem-A
Roccaforte Ligure,006146,Piem-H
Solero,006163,Piem-G
Val della Torre,001284,Piem-C
Val della Torre,001284,Piem-L
Zubiena,096082,Piem-I
Casalborgone,001060,Piem-L
Sant''Antonino di Susa,001256,Piem-C
Cavaglio d''Agogna,003045,Piem-I
Brossasco,004033,Piem-E
Odalengo Piccolo,006117,Piem-L
Frabosa Sottana,004091,Piem-F
Capriata d''Orba,006029,Piem-G
Lombardore,001135,Piem-L
Faule,004087,Piem-M
Castello di Annone,005028,Piem-G
Giaglione,001114,Piem-D
Cavallermaggiore,004059,Piem-M
Sardigliano,006157,Piem-H
Conzano,006061,Piem-I
Lombriasco,001136,Piem-M
Borgomezzavalle,103078,Piem-A
Strambinello,001268,Piem-I
Barge,004012,Piem-D
Barge,004012,Piem-M
Nibbiola,003104,Piem-I
Massino Visconti,003093,Piem-A
Villalvernia,006183,Piem-H
Spigno Monferrato,006165,Piem-G
Gassino Torinese,001112,Piem-L
Massazza,096031,Piem-I
Caramagna Piemonte,004041,Piem-M
Trino,002148,Piem-I
Viù,001313,Piem-C
Cinaglio,005039,Piem-L
Lagnasco,004104,Piem-M
Momo,003100,Piem-I
Casanova Elvo,002033,Piem-I
Castellino Tanaro,004052,Piem-F
Ruffia,004198,Piem-M
Castiglione Falletto,004055,Piem-F
Rivarone,006145,Piem-G
Quincinetto,001210,Piem-B
Brondello,004032,Piem-D
Vaglio Serra,005111,Piem-G
Vogogna,103077,Piem-A
Crodo,103026,Piem-A
Baveno,103008,Piem-A
Monleale,006101,Piem-H
Manta,004116,Piem-M
Sauze di Cesana,001258,Piem-D
Cassinasco,005021,Piem-G
Sordevolo,096063,Piem-B
Sarezzano,006158,Piem-H
Trana,001276,Piem-L
Ponzone,006136,Piem-G
Quarna Sopra,103058,Piem-A
Pareto,006125,Piem-G
Sostegno,096064,Piem-B
Sostegno,096064,Piem-I
Costigliole Saluzzo,004075,Piem-E
Costigliole Saluzzo,004075,Piem-M
Virle Piemonte,001310,Piem-L
Solonghello,006164,Piem-I
Sestriere,001263,Piem-D
Chialamberto,001075,Piem-C
Terdobbiate,003144,Piem-I
Rocca Grimalda,006147,Piem-G
Massiola,103043,Piem-A
Chiusa di San Michele,001081,Piem-C
Piedimulera,103053,Piem-A
Paroldo,004160,Piem-F
Vottignasco,004250,Piem-M
Prali,001202,Piem-D
Tigliole,005108,Piem-L
Rondissone,001225,Piem-I
Pino Torinese,001192,Piem-L
Cossano Belbo,004074,Piem-G
Landiona,003083,Piem-I
San Pietro Mosezzo,003135,Piem-I
Somano,004221,Piem-F
Borgo San Dalmazzo,004025,Piem-M
Borgo San Dalmazzo,004025,Piem-E
San Bernardino Verbano,103061,Piem-A
Saluggia,002128,Piem-I
Scalenghe,001260,Piem-L
Maretto,005062,Piem-L
Robella,005092,Piem-I
Cravagliana,002048,Piem-B
Oleggio,003108,Piem-I
Gattinara,002061,Piem-I
Ottiglio,006120,Piem-I
Ingria,001121,Piem-C
San Benigno Canavese,001236,Piem-L
Morozzo,004144,Piem-F
Casalgrasso,004045,Piem-M
Pamparato,004159,Piem-F
Andrate,001010,Piem-B
Roccaverano,005094,Piem-G
Cerrione,096018,Piem-I
Suno,003143,Piem-I
Usseglio,001282,Piem-C
Craveggia,103024,Piem-A
Racconigi,004179,Piem-M
Villar Pellice,001306,Piem-D
Morano sul Po,006109,Piem-I
Civiasco,002043,Piem-B
Serravalle Langhe,004219,Piem-G
Serravalle Langhe,004219,Piem-F
Mongiardino Ligure,006100,Piem-H
Roccaforte Mondovì,004190,Piem-F
Piverone,001196,Piem-I
Corsione,005044,Piem-L
Castelletto Molina,005027,Piem-G
Carentino,006031,Piem-G
Balocco,002009,Piem-I
Cantalupa,001053,Piem-C
Bussoleno,001044,Piem-C
Agrate Conturbia,003001,Piem-I
Formazza,103031,Piem-A
Robilante,004185,Piem-E
Camandona,096009,Piem-B
Prarolo,002104,Piem-I
Saluzzo,004203,Piem-M
Strevi,006168,Piem-G
Villar Dora,001303,Piem-C
Santo Stefano Belbo,004213,Piem-G
Castelletto sopra Ticino,003043,Piem-I
San Martino Alfieri,005099,Piem-G
Arquata Scrivia,006009,Piem-H
Gavi,006081,Piem-G
Fubine Monferrato,006076,Piem-G
Cambiasca,103015,Piem-A
Vidracco,001298,Piem-B
Cesara,103022,Piem-A
Colleretto Giacosa,001092,Piem-I
Samone,001235,Piem-I
Villareggia,001304,Piem-I
Frinco,005055,Piem-L
Miasino,003098,Piem-A
Stresa,103064,Piem-A
Briona,003027,Piem-I
Marsaglia,004120,Piem-F
Cintano,001084,Piem-C
Pianezza,001189,Piem-L
Olcenengo,002088,Piem-I
Casalino,003040,Piem-I
Pieve Vergonte,103054,Piem-A
Costanzana,002047,Piem-I
Pogno,003120,Piem-A
Oleggio Castello,003109,Piem-I
Varallo Pombia,003154,Piem-I
Agliano Terme,005001,Piem-G
Murello,004146,Piem-M
Chiomonte,001080,Piem-D
Malvicino,006090,Piem-G
Zumaglia,096083,Piem-B
Montescheno,103047,Piem-A
Loreglia,103038,Piem-A
Caprauna,004039,Piem-F
Grana Monferrato,005056,Piem-L
Chiesanuova,001079,Piem-C
Incisa Scapaccino,005058,Piem-G
Pralungo,096049,Piem-B
Pollone,096046,Piem-B
Predosa,006140,Piem-G
Caresana,002030,Piem-I
Castelletto Merli,006050,Piem-I
Ribordone,001212,Piem-C
Biella,096004,Piem-B
Brovello-Carpugnino,103013,Piem-A
Castell''Alfero,005025,Piem-L
San Cristoforo,006152,Piem-G
Bibiana,001025,Piem-D
Bibiana,001025,Piem-M
Frassineto Po,006073,Piem-I
Diano d''Alba,004080,Piem-F
Cisterna d''Asti,005040,Piem-L
Mezzana Mortigliengo,096033,Piem-B
Mezzana Mortigliengo,096033,Piem-I
Valle San Nicolao,096074,Piem-B
Valle San Nicolao,096074,Piem-I
Parodi Ligure,006126,Piem-G
Sale San Giovanni,004200,Piem-F
Acceglio,004001,Piem-E
Poirino,001197,Piem-L
Borgoratto Alessandrino,006019,Piem-G
Tronzano Vercellese,002150,Piem-I
Verzuolo,004240,Piem-D
Verzuolo,004240,Piem-M
Masserano,096032,Piem-I
Angrogna,001011,Piem-D
Sanfront,004209,Piem-D
Dernice,006066,Piem-H
Lanzo Torinese,001128,Piem-C
Cuorgnè,001098,Piem-C
Borgofranco d''Ivrea,001030,Piem-B
Bioglio,096005,Piem-B
Frugarolo,006075,Piem-G
Chieri,001078,Piem-L
Soglio,005107,Piem-L
Morsasco,006112,Piem-G
Inverso Pinasca,001122,Piem-D
Fiorano Canavese,001105,Piem-I
Orio Canavese,001172,Piem-L
Ghislarengo,002062,Piem-I
Chiaverano,001077,Piem-B
Chiaverano,001077,Piem-I
Villa del Bosco,096078,Piem-I
Gravellona Toce,103035,Piem-A
Monastero di Vasco,004126,Piem-F
Cunico,005051,Piem-L
Colazza,003051,Piem-A
Gorzegno,004097,Piem-G
Nonio,103048,Piem-A
Carpignano Sesia,003036,Piem-I
Chianocco,001076,Piem-C
Lesegno,004108,Piem-F
Salerano Canavese,001233,Piem-I
Pallanzeno,103052,Piem-A
Caprie,001055,Piem-C
Novalesa,001169,Piem-C
Bergolo,004021,Piem-G
Priola,004177,Piem-F
Vaprio d''Agogna,003153,Piem-I
San Maurizio d''Opaglio,003133,Piem-A
Montalenghe,001159,Piem-L
Fontanile,005054,Piem-G
Cessole,005037,Piem-G
Lemie,001131,Piem-C
Borriana,096006,Piem-I
Lenta,002068,Piem-I
Borgone Susa,001032,Piem-C
Lessolo,001132,Piem-I
Treiso,004230,Piem-G
Cameri,003032,Piem-I
Neive,004148,Piem-G
Castino,004057,Piem-G
Levone,001133,Piem-L
Levone,001133,Piem-C
Treville,006175,Piem-I
Molare,006095,Piem-G
Castelnuovo di Ceva,004054,Piem-G
Trecate,003149,Piem-I
Villadeati,006182,Piem-L
Mombello Monferrato,006097,Piem-I
Tavigliano,096066,Piem-B
Pancalieri,001178,Piem-L
Volpedo,006188,Piem-H
Moretta,004143,Piem-M
Cigliano,002042,Piem-I
Callabiana,096008,Piem-B
Granozzo con Monticello,003077,Piem-I
Masera,103042,Piem-A
Rosazza,096055,Piem-B
Chiusano d''Asti,005038,Piem-L
Piasco,004166,Piem-E
Castel Boglione,005024,Piem-G
San Sebastiano Curone,006155,Piem-H
Pavone Canavese,001181,Piem-I
Carbonara Scrivia,006030,Piem-H
Arguello,004007,Piem-G
Romagnano Sesia,003130,Piem-I
Castelnuovo Bormida,006052,Piem-G
Farigliano,004086,Piem-F
Borgolavezzaro,003023,Piem-I
Saliceto,004201,Piem-G
Roddi,004194,Piem-F
Fiano,001104,Piem-C
Fiano,001104,Piem-L
Corneliano d''Alba,004072,Piem-F
Cinzano,001085,Piem-L
Alto,004005,Piem-F
Venaus,001291,Piem-C
Pasturana,006127,Piem-G
Nole,001166,Piem-L
Merana,006093,Piem-G
Fara Novarese,003065,Piem-I
Villanova Biellese,096079,Piem-I
Cerro Tanaro,005036,Piem-G
Moriondo Torinese,001163,Piem-L
Pettenasco,003116,Piem-A
Fenestrelle,001103,Piem-D
Serole,005104,Piem-G
Boca,003019,Piem-I
Monale,005067,Piem-L
Costa Vescovato,006062,Piem-H
Celle di Macra,004060,Piem-E
Savigliano,004215,Piem-M
Ala di Stura,001003,Piem-C
Monastero Bormida,005068,Piem-G
Casaleggio Boiro,006038,Piem-G
Villamiroglio,006184,Piem-I
Rossana,004197,Piem-E
Montecrestese,103046,Piem-A
Prascorsano,001206,Piem-C
Montaldo di Mondovì,004134,Piem-F
Monesiglio,004131,Piem-G
Lusernetta,001140,Piem-D
Villa San Secondo,005119,Piem-L
Montafia,005073,Piem-L
Villar Perosa,001307,Piem-D
Castel Rocchero,005032,Piem-G
Bosconero,001033,Piem-L
Vesime,005113,Piem-G
San Secondo di Pinerolo,001254,Piem-M
San Secondo di Pinerolo,001254,Piem-D
Lisio,004111,Piem-F
Oldenico,002089,Piem-I
Pombia,003121,Piem-I
Rocchetta Belbo,004193,Piem-G
Igliano,004102,Piem-F
Osasco,001173,Piem-M
Dormelletto,003062,Piem-I
Giarole,006082,Piem-I
Cannero Riviera,103016,Piem-A
Silvano d''Orba,006162,Piem-G
Piedicavallo,096044,Piem-B
Serralunga d''Alba,004218,Piem-F
Sali Vercellese,002127,Piem-I
Alpignano,001008,Piem-L
Rodello,004196,Piem-F
Bubbio,005011,Piem-G
Sangano,001241,Piem-L
Grosso,001119,Piem-L
Vallo Torinese,001286,Piem-L
Vallo Torinese,001286,Piem-C
Pezzana,002093,Piem-I
Torino,001272,Piem-L
Barbaresco,004011,Piem-G
Alto Sermenza,002170,Piem-B
Alluvioni Piovera,006192,Piem-I
Alluvioni Piovera,006192,Piem-G
Cassano Spinola,006191,Piem-H
Pinasca,001190,Piem-D
Varallo,002156,Piem-B
Cellio con Breia,002171,Piem-B
Carisio,002032,Piem-I
Arola,103004,Piem-A
Lerma,006088,Piem-G
Sant''Albano Stura,004211,Piem-M
Monteu Roero,004140,Piem-L
Brosso,001036,Piem-B
Bognanco,103012,Piem-A
Terruggia,006171,Piem-I
Alice Bel Colle,006005,Piem-G
San Martino Canavese,001247,Piem-I
Leini,001130,Piem-L
Sale delle Langhe,004199,Piem-F
Valdilana,096088,Piem-B
Lu e Cuccaro Monferrato,006193,Piem-I
Castellania Coppi,006045,Piem-H
Valchiusa,001318,Piem-B
Valle Cannobina,103079,Piem-A
Val di Chy,001317,Piem-B
Calliano Monferrato,005014,Piem-L
Casorzo Monferrato,005020,Piem-I
Moransengo-Tonengo,005122,Piem-I
Bellino,004017,Piem-E
Arizzano,103003,Piem-A
Prarostino,001205,Piem-D
Elva,004083,Piem-E
Pratiglione,001207,Piem-C
Villastellone,001308,Piem-L
Ceresole Reale,001073,Piem-C
Sezzadio,006161,Piem-G
Balzola,006011,Piem-I
Francavilla Bisio,006070,Piem-G
Colleretto Castelnuovo,001091,Piem-C
Piatto,096043,Piem-B
Piatto,096043,Piem-I
Pragelato,001201,Piem-D
Viarigi,005115,Piem-G
Mombaruzzo,005065,Piem-G
Vigone,001299,Piem-L
Montemarzino,006108,Piem-H
Cissone,004070,Piem-F
Ovada,006121,Piem-G
Re,103060,Piem-A
San Mauro Torinese,001249,Piem-L
Melle,004122,Piem-E
San Francesco al Campo,001240,Piem-L
Balme,001019,Piem-C
Candia Canavese,001050,Piem-I
Bianzè,002011,Piem-I
Montaldo Scarampi,005074,Piem-G
Gignese,103034,Piem-A
Rocca d''Arazzo,005093,Piem-G
Buttigliera d''Asti,005012,Piem-L
Germagnano,001113,Piem-C
Valprato Soana,001288,Piem-C
Cantoira,001054,Piem-C
Castagnole Monferrato,005023,Piem-G
Rocca de Baldi,004189,Piem-F
Rocca Cigliè,004188,Piem-F
Ciriè,001086,Piem-L
Vestignè,001295,Piem-I
Vialfrè,001296,Piem-I
Lusigliè,001141,Piem-L
Loranzè,001137,Piem-I
Sanfrè,004208,Piem-M
Cigliè,004069,Piem-F
Torre Mondovì,004227,Piem-F
Villanova Mondovì,004245,Piem-F
Carrù,004043,Piem-F
\.

