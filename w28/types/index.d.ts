// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
import { components } from '../../src/types/weboll'
type W07Data = components['schemas']['W07Data']

export type W07Processed = {
    id_w07: number
    /** Format: date */
    start_valid_time: string
    validity: number
    next_blt_time: string
    status: string
    /** Format: date-time */
    last_update: string
    username: string
    w07_data: W07_data
}


type W07_data = {
    45: Array<W07Data>
    46: Array<W07Data>
    60: Array<W07Data>
    61: Array<W07Data>
    62: Array<W07Data>
    63: Array<W07Data>
    81: Array<W07Data>
    82: Array<W07Data>
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