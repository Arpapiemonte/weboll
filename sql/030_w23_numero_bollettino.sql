CREATE OR REPLACE FUNCTION public.w23_numero_bollettino (
)
RETURNS varchar AS
$body$
BEGIN
RETURN
(SELECT COUNT(DISTINCT data_emissione) + 1 || '/' || date_part('year', current_date)
FROM w23
WHERE data_emissione >= date_trunc('year', current_date) AND data_emissione < current_date);



END;
$body$
LANGUAGE 'plpgsql'
VOLATILE
CALLED ON NULL INPUT
SECURITY INVOKER
COST 100;
