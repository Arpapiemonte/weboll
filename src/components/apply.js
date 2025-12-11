// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt

// recursively traverse data until an object o is found with o[id_key] === id_value
// and return it
function find(data, id_key, id_value) {
  for (let k in data) {
    if (typeof data[k] === "object") {
      if (data[k]) {
        if (data[k][id_key] === id_value) {
          return data[k]
        } else {
          let found = find(data[k], id_key, id_value)
          if (Object.keys(found).length > 0)
            return found
        }
      }
    }
  }
  return {}
}

export default function apply(data, snapshot, reverse=false) {
  // console.log(`apply(${JSON.stringify(snapshot)}, ${reverse})`)
  let value = reverse ? snapshot.old_value : snapshot.new_value
  //  here we assume that the primary key column name for main bulletin tables will always be 6-characters long
  if (snapshot.id_key.length === 6) {
    // console.log(`- setting ${snapshot.value_key} = ${value}`)
    data[snapshot.value_key] = value
    return data
  } else {
    // here we assume that primary key column names for all tables are conventionally obtained
    // by prepending the 3-character long `id_` string to the table name
    let table = snapshot.id_key.substring(3)
    let found = find(data[table], snapshot.id_key, snapshot.id)
    if (Object.keys(found).length > 0) {
      // console.log(`- setting ${table}[${snapshot.id}].${snapshot.value_key} = ${value}`)
      found[snapshot.value_key] = value
    }
    return found
  }
}
