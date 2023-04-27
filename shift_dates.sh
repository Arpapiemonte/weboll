#!/bin/bash
# Shift dates for the preload data
#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt

# list all dates with:
#   egrep '202(1|2|3)-' public/aria/qa_stations4weboll.json | sed 's/.*\(202.-..-..\).*/\1/g' | sort | uniq -c
#   egrep '/2023' public/slops/prog.conf | sed 's/.*\(..\/..\/2023\).*/\1/g' | sort | uniq -c

for n in {-347..3}; do
  echo "pass $((n + 348)) of 352"
  DATE1=$(date --iso-8601 --date="2023-02-22 + $n days")
  DATE2=$(date --iso-8601 --date="$n day" | sed 's/-/X/g')
  sed -i "s/$DATE1/$DATE2/g" sql/*.copy sql/*.value public/aria/qa_stations4weboll.json public/piene_valutazione_bollettino/piene_valutazione_bollettino_1_2023.csv
done
echo "pass 352 of 352"
sed -i "s/\([0-9]\+\)X\([0-9]\+\)X\([0-9]\+\)/\1-\2-\3/g" sql/*.copy sql/*.value public/aria/qa_stations4weboll.json public/piene_valutazione_bollettino/piene_valutazione_bollettino_1_2023.csv
awk '!seen[$0]++' sql/forecast_zone.copy > sql/forecast_zone.copy_deduped
mv sql/forecast_zone.copy_deduped sql/forecast_zone.copy
DATE3=$(date --date="0 day" +"%d/%m/%Y")
sed -i "s/22\/02\/2023/${DATE3//\//\\\/}/g" public/slops/prog.conf
DATE1=$(date +%Y-%m-%d)
sed -i "s/2023-02-22/${DATE1}/g" public/defense/*.conf

