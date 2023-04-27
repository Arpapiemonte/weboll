ALTER TABLE ONLY public.forecast_zone ADD COLUMN id_forecast_zone serial;

ALTER TABLE ONLY public.forecast_zone DROP CONSTRAINT forecast_zone_pkey;

ALTER TABLE ONLY public.forecast_zone ADD CONSTRAINT forecast_zone_pkey PRIMARY KEY (id_forecast_zone);