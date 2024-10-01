// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
import { components } from '../../src/types/weboll'
type W35Data = components['schemas']['W35Data']

export type W35Processed = {
    id_w35: number
    /** Format: date */
    start_valid_time: string
    validity: number
    next_blt_time: string
    status: string
    /** Format: date-time */
    last_update: string
    username: string
    w35_data: object
}


// type W12_data = {
//     45: Array<W12Data>
//     46: Array<W12Data>
//     60: Array<W12Data>
//     61: Array<W12Data>
//     62: Array<W12Data>
//     63: Array<W12Data>
//     81: Array<W12Data>
//     82: Array<W12Data>
// }

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

type TabsDate = {
    48: string
    64: string
    65: string
    81: string
    82: string
    98: string
    99: string
}