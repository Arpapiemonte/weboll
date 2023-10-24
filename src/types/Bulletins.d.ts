// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
// tipo lista bollettini

type Bulletin =  {
  bollettino: string,
  id: string,
  name: string,
  readyForProduction: boolean,
  menu: string,
}

declare global {
  interface Window {
    bulletins_list: Bulletin[];
  }
}

export {}
