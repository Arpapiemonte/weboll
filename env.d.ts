// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt


/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BASE_DATA_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}