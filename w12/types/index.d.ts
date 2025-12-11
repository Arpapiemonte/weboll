// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
import { components } from '../../src/types/weboll'
type W12Data = components['schemas']['W12Data']

export type W12Processed = {
    id_w12: number
    /** Format: date */
    start_valid_time: string
    validity: number
    next_blt_time: string
    status: string
    /** Format: date-time */
    last_update: string
    username: string
    w12_data: W12_data
}


type W12_data = {
    45: Array<W12Data>
    46: Array<W12Data>
    60: Array<W12Data>
    61: Array<W12Data>
    62: Array<W12Data>
    63: Array<W12Data>
    81: Array<W12Data>
    82: Array<W12Data>
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