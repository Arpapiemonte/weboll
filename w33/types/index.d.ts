// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
import { components } from '../../src/types/weboll'
type W33Data = components['schemas']['W33Data']

export type W33Processed = {
    id_w33: number
    /** Format: date */
    data_emissione: string
    seq_num: number
    status: string
    /** Format: date-time */
    last_update: string
    username: string
    w33_data: W33_data
}

type W33_data = {
    45: Array<W33Data>
    46: Array<W33Data>
    60: Array<W33Data>
    61: Array<W33Data>
    62: Array<W33Data>
    63: Array<W33Data>
    81: Array<W33Data>
    82: Array<W33Data>
}

type TabsDate = {
    45: string
    46: string
    60: string
    61: string
    62: string
    63: string
    81: string
    82: string
}

type Icons = Array<Icon>

type Icon = {
    description: string
    description_ita: string
    id_parametro: number | null
    id_sky_condition: number
    sky_condition: string
    ordinamento: number
}

type GroupedIcons = {
    [key: string]: Array<Icon>
}

type VenueNames = {
    [key: number]: String
}
