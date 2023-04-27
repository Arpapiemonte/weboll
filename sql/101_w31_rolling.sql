-- CREATE VIEW W31_rolling instead of a table

DROP VIEW IF EXISTS w31_rolling;

CREATE VIEW w31_rolling AS
    SELECT
        row_number() OVER () as id,
        w31_input.temp,
        w31_input.umid,
        w31_input.velv,
        w31_input.prec,
        w31_input.id_w31_microaree,
        (data - current_date) * 17 + 49 AS id_time_layouts
    FROM    
        w31_input;
    -- commented WHERE since we may need to redo a bulletin from the past
    -- WHERE (data - current_date) * 17 + 49 >= 49;
