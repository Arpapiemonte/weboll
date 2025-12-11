#!/bin/bash
# Shift dates for the preload data
#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt

# list all dates with:
#   egrep '202(1|2|3)-' public/aria/qa_stations4weboll.json | sed 's/.*\(202.-..-..\).*/\1/g' | sort | uniq -c
#   egrep '/2023' public/slops/prog.conf | sed 's/.*\(..\/..\/2023\).*/\1/g' | sort | uniq -c

# yesterday => 2023-02-21

for n in {-7..8}; do
  DATE1=$(date --iso-8601 --date="2023-02-22 + $n days")
  DATE2=$(date --iso-8601 --date="$n day" | sed 's/-/X/g')
  DATE3=$(date --date="2023-02-22 + $n days" +%Y%m%d)
  DATE4=$(date --date="$n day" +%Y%m%d)
  echo "replace $DATE1 with $DATE2"
  sed -i "s/$DATE1/$DATE2/g" sql/*.copy sql/*.value public/aria/qa_stations4weboll.json public/piene_valutazione_bollettino/piene_valutazione_bollettino_1_2023.csv public/analisi/visibilita_analisi_meteo.json sql/060_w29.pg_dump.sql sql/106_w32.pg_dump.sql sql/129_w23verifica.pg_dump.sql sql/130_w38.pg_dump.sql
  sed -i "s/$DATE3/$DATE4/g" public/w35_json/*.json
done
sed -i "s/\([0-9]\+\)X\([0-9]\+\)X\([0-9]\+\)/\1-\2-\3/g" sql/*.copy sql/*.value public/aria/qa_stations4weboll.json public/piene_valutazione_bollettino/piene_valutazione_bollettino_1_2023.csv public/analisi/visibilita_analisi_meteo.json sql/060_w29.pg_dump.sql sql/106_w32.pg_dump.sql sql/129_w23verifica.pg_dump.sql sql/130_w38.pg_dump.sql
awk '!seen[$0]++' sql/forecast_zone.copy > sql/forecast_zone.copy_deduped
mv sql/forecast_zone.copy_deduped sql/forecast_zone.copy
DATE3=$(date --date="0 day" +"%d/%m/%Y")
sed -i "s/22\/02\/2023/${DATE3//\//\\\/}/g" public/slops/prog.conf
DATE1=$(date +%Y-%m-%d)
sed -i "s/2023-02-22/${DATE1}/g" public/defense/*.conf
DATE1=$(date +%Y%m%d)
cp -v public/uvi/cop_tot.json "public/uvi/${DATE1}_cop_tot.json"

