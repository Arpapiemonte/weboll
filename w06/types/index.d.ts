// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
import { components } from '../../src/types/weboll'
type W06Data = components['schemas']['W06Data']

export type W06Processed = {
    id_w06: number
    /** Format: date */
    start_valid_time: string
    validity: number
    next_blt_time: string
    status: string
    /** Format: date-time */
    last_update: string
    username: string
    w06_data: W06_data
}


type W06_data = {
    45: Array<W06Data>
    46: Array<W06Data>
    60: Array<W06Data>
    61: Array<W06Data>
    62: Array<W06Data>
    63: Array<W06Data>
    81: Array<W06Data>
    82: Array<W06Data>
}

type Icons = {
    [key: number]: Icon
}

type Icon = {
    description: string
    description_ita: string
    id_parametro: number | null
    id_sky_condition: number
    sky_condition: string
    ordinamento: number
}