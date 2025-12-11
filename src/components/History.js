// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
// Original version: https://github.com/ioslh/undo-redo

function roughlyToPlain(obj) {
  return JSON.parse(JSON.stringify(obj))
}

class History {
  constructor() {
    this.snapshots = []
    this.cursor = -1
  }

  get canUndo() {
    return this.cursor >= 0
  }

  get canClear() {
    return this.snapshots.length
  }

  get canRedo() {
    return this.snapshots.length > this.cursor + 1
  }

  record(snapshot) {
    for (const [key, value] of Object.entries(snapshot)) {
      if (key == 'new_value'){
        if (value === ''){
          snapshot['new_value'] = null
        }
      }
    }
    // riscrivo tutta l'history tenendo solo l'ultima modifica x stessi id
    let new_snapshots = []
    let new_cursor = 0
    this.snapshots.forEach(element => {
      if (element.id === snapshot.id
        && element.id_key === snapshot.id_key
        && element.value_key === snapshot.value_key){
        // salto questo elemento perchè corrisponde a quello nuovo che voglio inserire
        // console.log("riscrittura history lo salto perchè corrisponde al nuovo", element)
      }else{
        // riporto la vecchia history e il vecchio cursor
        // console.log("riscrittura history lo inserisco", element)
        new_snapshots.push(roughlyToPlain(element))
        new_cursor = new_cursor + 1
      }
    })
    this.snapshots = new_snapshots
    this.cursor = new_cursor
    this.snapshots.push(roughlyToPlain(snapshot))
    this.cursor = this.snapshots.length - 1
    //console.log(this.snapshots, this.cursor)
  }

  undo() {
    if (this.canUndo) {
      let new_value = this.snapshots[this.cursor].new_value
      let old_value = this.snapshots[this.cursor].old_value
      this.snapshots[this.cursor].new_value = old_value
      this.snapshots[this.cursor].old_value = new_value
      return this.snapshots[this.cursor--]
    }
    return null
  }

  redo() {
    if (this.canRedo) {
      let cursor = this.cursor + 1
      let new_value = this.snapshots[cursor].new_value
      let old_value = this.snapshots[cursor].old_value
      this.snapshots[cursor].new_value = old_value
      this.snapshots[cursor].old_value = new_value
      return this.snapshots[++this.cursor]
    }
    return null
  }

  move(cursor) {
    if (this.snapshots.length > cursor) {
      this.cursor = cursor
      return this.snapshots[this.cursor]
    }
  }

  clear() {
    this.cursor = -1
    this.snapshots = []
  }
  
  splice() {
    let discarded = this.snapshots.splice(0, this.cursor + 1)
    this.cursor = -1
    return discarded
  }
  restore(snapshots) {
    // console.log('restoring', snapshots)
    this.snapshots = snapshots
    this.cursor = this.snapshots.length - 1
  }
  isDirty(id, id_key, value_key) {
    let index = this.snapshots.findIndex(
      element => element.id === id 
      && element.id_key === id_key 
      && element.value_key === value_key) 
    return index >= 0 && index <= this.cursor
  }
  shake() {
    // removes duplicate changes to the same id/id_key/value_key, retaining only the most recent one
    // 1. extract active changes (not undone)
    let actives = this.snapshots.splice(0, this.cursor + 1)
    // 2. execute a reducer function right-to-left ...
    let uniques = actives.reverse().reduce((filter, current) => {
      var found = filter.find(item => item.id === current.id && item.id_key === current.id_key && item.value_key === current.value_key)
      if (!found) {
        /// 2.1 that only includes the most recent change with each id ...
        return filter.concat([current])
      } else {
        // 2.2 updated to remember the old value that the least recent change overwrote
        found.old_value = current.old_value
        return filter
      }
    }, [])
    // 3. reassemble back the shaken active changes with the undone changes
    this.snapshots = uniques.reverse().concat(this.snapshots)
    // 4. move the cursor on top of the shaken active changes
    this.cursor = uniques.length - 1
  }

}

export default History
