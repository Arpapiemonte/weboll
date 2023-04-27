CREATE FUNCTION public.w22_numero_bollettino() RETURNS character varying
    LANGUAGE plpgsql
    AS $$
BEGIN
  RETURN
  (SELECT COUNT(*) + 1 || '/' || date_part('year', current_date)
  FROM w22
  WHERE data_emissione >= date_trunc('year', current_date) AND status = 1);

END;
$$;
