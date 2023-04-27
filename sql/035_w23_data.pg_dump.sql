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

CREATE TABLE public.w23_data (
    id_w23 bigint NOT NULL,
    id_w23_zone integer NOT NULL,
    idrogeologico_oggi character varying(10) NOT NULL,
    idrogeologico_domani character varying(10) NOT NULL,
    temporali_oggi character varying(10) NOT NULL,
    temporali_domani character varying(10) NOT NULL,
    idraulico_oggi character varying(10) NOT NULL,
    idraulico_domani character varying(10) NOT NULL,
    neve_oggi character varying(10) NOT NULL,
    neve_domani character varying(10) NOT NULL,
    valanghe_oggi character varying(10) NOT NULL,
    valanghe_domani character varying(10) NOT NULL,
    scenario_atteso text,
    idrogeologico_oggi_for character varying(10),
    idrogeologico_domani_for character varying(10),
    temporali_oggi_for character varying(10),
    temporali_domani_for character varying(10),
    idraulico_oggi_for character varying(10),
    idraulico_domani_for character varying(10),
    neve_oggi_for character varying(10),
    neve_domani_for character varying(10),
    valanghe_oggi_for character varying(10),
    valanghe_domani_for character varying(10),
    scenario_atteso_for text,
    pluvmax12hd0 character varying(5),
    pluvmax12hd1 character varying(5),
    pluvmax24hd1 character varying(5),
    pluvmax6h18g0 character varying(5),
    pluvmax6h00g1 character varying(5),
    pluvmax6h06g1 character varying(5),
    pluvmax6h12g1 character varying(5),
    pluvmax6h18g1 character varying(5),
    pluvmax6h00g2 character varying(5),
    pluvmax6h06g2 character varying(5),
    pluvmax6h12g2 character varying(5),
    pluvmax6h18g2 character varying(5),
    pluvmax6h00g3 character varying(5),
    pluvmed6h18g0 character varying(5),
    pluvmed6h00g1 character varying(5),
    pluvmed6h06g1 character varying(5),
    pluvmed6h12g1 character varying(5),
    pluvmed6h18g1 character varying(5),
    pluvmed6h00g2 character varying(5),
    pluvmed6h06g2 character varying(5),
    pluvmed6h12g2 character varying(5),
    pluvmed6h18g2 character varying(5),
    pluvmed6h00g3 character varying(5),
    pluvmed12h18g0_oss character varying(5),
    pluvmed12h00g1 character varying(5),
    pluvmed12h06g1 character varying(5),
    pluvmed12h12g1 character varying(5),
    pluvmed12h18g1 character varying(5),
    pluvmed12h00g2 character varying(5),
    pluvmed12h06g2 character varying(5),
    pluvmed12h12g2 character varying(5),
    pluvmed12h18g2 character varying(5),
    pluvmed12h00g3 character varying(5),
    pluvmed24h18g0_oss character varying(5),
    pluvmed24h00g1_oss character varying(5),
    pluvmed24h06g1_oss character varying(5),
    pluvmed24h12g1 character varying(5),
    pluvmed24h18g1 character varying(5),
    pluvmed24h00g2 character varying(5),
    pluvmed24h06g2 character varying(5),
    pluvmed24h12g2 character varying(5),
    pluvmed24h18g2 character varying(5),
    pluvmed24h00g3 character varying(5),
    pluvmed48h18g0_oss character varying(5),
    pluvmed48h00g1_oss character varying(5),
    pluvmed48h06g1_oss character varying(5),
    pluvmed48h12g1_oss character varying(5),
    pluvmed48h18g1_oss character varying(5),
    pluvmed48h00g2_oss character varying(5),
    pluvmed48h06g2_oss character varying(5),
    pluvmed48h12g2 character varying(5),
    pluvmed48h18g2 character varying(5),
    pluvmed48h00g3 character varying(5),
    neveqmin character varying(5),
    neveqmax character varying(5),
    neve400_oggi character varying(5),
    neve400_domani character varying(5),
    neve400_totale character varying(5),
    neve700_oggi character varying(5),
    neve700_domani character varying(5),
    neve700_totale character varying(5),
    neve1000_oggi character varying(5),
    neve1000_domani character varying(5),
    neve1000_totale character varying(5),
    temporale_oggi character varying(40),
    temporale_domani character varying(40),
    neveqd01 character varying(5),
    neveqd02 character varying(5),
    neveqd11 character varying(5),
    neveqd12 character varying(5),
    neveqd13 character varying(5),
    neveqd14 character varying(5)
);


ALTER TABLE public.w23_data OWNER TO weboll;

--

--

ALTER TABLE ONLY public.w23_data
    ADD CONSTRAINT w23_data_fkey001 FOREIGN KEY (id_w23) REFERENCES public.w23(id_w23) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: w23_data_fkey002; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w23_data
    ADD CONSTRAINT w23_data_fkey002 FOREIGN KEY (id_w23_zone) REFERENCES public.w23_zone(id_w23_zone) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: TABLE w23_data; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
/*
alter table public.w23_data add constraint w23_data_idrogeologico_oggi FOREIGN KEY (idrogeologico_oggi) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE CASCADE;
alter table public.w23_data add constraint w23_data_idrogeologico_domani FOREIGN KEY (idrogeologico_domani) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE CASCADE;
alter table public.w23_data add constraint w23_data_temporali_oggi FOREIGN KEY (temporali_oggi) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE CASCADE;
alter table public.w23_data add constraint w23_data_temporali_domani FOREIGN KEY (temporali_domani) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE CASCADE;
alter table public.w23_data add constraint w23_data_idraulico_oggi FOREIGN KEY (idraulico_oggi) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE CASCADE;
alter table public.w23_data add constraint w23_data_idraulico_domani FOREIGN KEY (idraulico_domani) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE CASCADE;
alter table public.w23_data add constraint w23_data_neve_oggi FOREIGN KEY (neve_oggi) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE CASCADE;
alter table public.w23_data add constraint w23_data_neve_domani FOREIGN KEY (neve_domani) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE CASCADE;
alter table public.w23_data add constraint w23_data_valanghe_oggi FOREIGN KEY (valanghe_oggi) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE CASCADE;
alter table public.w23_data add constraint w23_data_valanghe_domani FOREIGN KEY (valanghe_domani) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE CASCADE;
alter table public.w23_data add constraint w23_data_idrogeologico_oggi_for FOREIGN KEY (idrogeologico_oggi_for) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE SET NULL;
alter table public.w23_data add constraint w23_data_idrogeologico_domani_for FOREIGN KEY (idrogeologico_domani_for) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE SET NULL;
alter table public.w23_data add constraint w23_data_temporali_oggi_for FOREIGN KEY (temporali_oggi_for) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE SET NULL;
alter table public.w23_data add constraint w23_data_temporali_domani_for FOREIGN KEY (temporali_domani_for) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE SET NULL;
alter table public.w23_data add constraint w23_data_idraulico_oggi_for FOREIGN KEY (idraulico_oggi_for) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE SET NULL;
alter table public.w23_data add constraint w23_data_idraulico_domani_for FOREIGN KEY (idraulico_domani_for) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE SET NULL;
alter table public.w23_data add constraint w23_data_neve_oggi_for FOREIGN KEY (neve_oggi_for) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE SET NULL;
alter table public.w23_data add constraint w23_data_neve_domani_for FOREIGN KEY (neve_domani_for) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE SET NULL;
alter table public.w23_data add constraint w23_data_valanghe_oggi_for FOREIGN KEY (valanghe_oggi_for) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE SET NULL;
alter table public.w23_data add constraint w23_data_valanghe_domani_for FOREIGN KEY (valanghe_domani_for) REFERENCES public.w23_pericolo(id_w23_pericolo) ON UPDATE CASCADE ON DELETE SET NULL;
*/
