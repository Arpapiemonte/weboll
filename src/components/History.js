// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
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
    if (this.cursor >= 0 && this.snapshots[this.cursor].id === snapshot.id && this.snapshots[this.cursor].id_key === snapshot.id_key && this.snapshots[this.cursor].value_key === snapshot.value_key) {
      // collapse with last active change if they share the same id/id_key/value_key
      this.snapshots[this.cursor].new_value = snapshot.new_value
    } else {
      while (this.cursor < this.snapshots.length - 1) {
        this.snapshots.pop()
      }
      this.snapshots.push(roughlyToPlain(snapshot))
      this.cursor = this.snapshots.length - 1
    }
  }

  undo() {
    if (this.canUndo) {
      return this.snapshots[this.cursor--]
    }
    return null
  }

  redo() {
    if (this.canRedo) {
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
    let index = this.snapshots.findIndex(element => element.id === id && element.id_key === id_key && element.value_key === value_key) 
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
