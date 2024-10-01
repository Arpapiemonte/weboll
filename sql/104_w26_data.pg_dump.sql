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

CREATE TABLE public.w26_data (
    id_w26 bigint NOT NULL,
    id_w26_zone bigint NOT NULL,
    --localita character varying(100) NOT NULL,
    --corsoacqua character varying(100) NOT NULL,
    hmin character varying(8),
    hmax character varying(8),
    hmed character varying(8),
    qmin character varying(8),
    qmax character varying(8),
    qmed character varying(8),
    nota character varying(2000),
    idnota character varying(70)
    --numero integer NOT NULL
);


ALTER TABLE public.w26_data ADD COLUMN id_w26_data BIGSERIAL PRIMARY KEY;
ALTER TABLE public.w26_data OWNER TO weboll;

--COPY public.w26_data (id_w26, localita, corsoacqua, hmin, hmax, hmed, qmin, qmax, qmed, nota, idnota, numero) FROM stdin;

ALTER TABLE ONLY public.w26_data
    ADD CONSTRAINT w26_data_fkey001 FOREIGN KEY (id_w26) REFERENCES public.w26(id_w26) ON UPDATE CASCADE ON DELETE CASCADE;


REVOKE ALL ON TABLE public.w26_data FROM PUBLIC;
REVOKE ALL ON TABLE public.w26_data FROM weboll;
GRANT ALL ON TABLE public.w26_data TO weboll;
GRANT SELECT ON TABLE public.w26_data TO weboll;
GRANT SELECT ON TABLE public.w26_data TO weboll;
GRANT ALL ON TABLE public.w26_data TO weboll;
GRANT ALL ON TABLE public.w26_data TO weboll;


--
-- PostgreSQL database dump complete
--
\set command `echo "curl $DATA_LOCATION/w26_data.copy"`
COPY public.w26_data
  FROM PROGRAM :'command' CSV HEADER;

SELECT setval('public.w26_id_w26_seq', max(id_w26)) FROM public.w26;
SELECT setval('public.w26_data_id_w26_data_seq', max(id_w26_data)) FROM public.w26_data;
