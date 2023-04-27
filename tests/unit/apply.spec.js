import apply from '@/components/apply'
import diff from 'deep-diff'

// static data structure keep track of already used id_w99_xxx values
let ids = {}

// returns a dummy object in table w99_<secondaryTable> with key set to value and a unique id_w99_<secondaryTable>
// example:
// first invocation of factory("fruits", "test1, "kiwi") returns:
//   { id_w99_fruits: 0, test1: 'kiwi', id_w99: 0 }
// second invocation of factory("fruits", "test1, "kiwi") returns:
//   { id_w99_fruits: 1, test1: 'kiwi', id_w99: 0 }
function factory(secondaryTable, key, value) {
  let id = 0
  if (secondaryTable in ids) {
    id = (ids[secondaryTable] += 1)
  } else {
    ids[secondaryTable] = id
  }
  let pk = `id_w99_${secondaryTable}`
  let object = {}
  object[pk] = id
  object[key] = value
  object['id_w99'] = 0
  return object
}

// non-recursive deep object traversal, https://www.howtobuildsoftware.com/index.php/how-do/bmHA/javascript-data-structures-computer-science-is-it-possible-to-traverse-object-in-javascript-in-non-recursive-way
function traverse(obj, callback) {
  var stack = []
  stack.push(obj)
  while (stack.length) {
    for (var j in stack[0]) {
      if (typeof stack[0][j] === 'object' && !('id_w99' in stack[0][j])) {
        stack.push(stack[0][j])
      } else {
        callback(stack[0][j])
      }
    }
    stack.shift()
  }
}

// data structure with dummy data
let data = {
  w99_fruits: {
    a: {
      aa: [
        factory("fruits", "test1", "apple")
      ],
      ab: [
        factory("fruits", "test2", "cherry"),
        factory("fruits", "test3", "pear"),
      ],
      ae: [
        factory("fruits", "test2", "ananas"),
      ]
    },
    b: {
      bb: {
        bbb: [
          factory("fruits", "test1", "strawberry"),
        ],
        bbc: {
          bbcb: {
            bbcba: [
              factory("fruits", "test15", "kiwi"),
            ]
          }
        }
      }
    }
  },
  w99_animals: {
    a: {
      ab: [
        factory("animals", "test1111", "goat"),
        factory("animals", "test111", "dog")
      ],
      ac: [
        factory("animals", "test11", "sheep"),
        factory("animals", "test1", "horse"),
        factory("animals", "test", "duck"),
      ],
      ae: [
        factory("animals", "test0", "pangolin")
      ],
      ag: [
        factory("animals", "test1", "mammouth"),
        factory("animals", "test2", "elephant")
      ]
    },
    b: {
      bb: {
        bbb: [
          factory("animals", "test0", "bee")
        ],
        bbc: {
          bbca: [
            factory("animals", "test1", "butterfly"),
          ],
          bbcb: {
            bbcba: [
              factory("animals", "test2", "zebra")
            ]
          }
        }
      }
    }
  },
  w99_flowers: {
    a: {
      ac: [
        factory("flowers", "test1", "violet")
      ],
      ad: [
        factory("flowers", "test2", "violet"),
        factory("flowers", "test3", "rose"),
        factory("flowers", "test4", "lilly"),
        factory("flowers", "test5", "tulip")
      ],
      ae: [
        factory("flowers", "test6", "daisy")
      ]
    },
    b: {
      bb: {
        bbc: {
          bbcb: {
            bbcba: [
              factory("flowers", "test7", "hortensia")
            ]
          }
        }
      }
    }
  },
  w99_metals: {
    a: {
      aa: [
        factory("metals", "test8", "quicksilver")
      ],
      af: [
        factory("metals", "test9", "iron")
      ],
      ag: [
        factory("metals", "test10", "iron")
      ]
    },
    b: {
      ba: [
        factory("metals", "test11", "aluminum"),
      ],
      bb: {
        bba: [
          factory("metals", "test0", "copper"),
          factory("metals", "test1", "nickel"),
          factory("metals", "test2", "vanadium"),
        ],
        bbc: {
          bbca: [
            factory("metals", "test3", "silver"),
          ],
          bbcb: {
            bbcba: [
              factory("metals", "test4", "gold")
            ]
          }
        }
      }
    }
  }
}

describe("Apply function", () => {
  traverse(data, element => {
    test(`it should change only the element ${JSON.stringify(element)} and revert back`, () => {
      let pk = Object.keys(element)[0]
      let key = Object.keys(element)[1]
      const new_value = "X"
      let snapshot = {
        id_key: pk,
        id: element[pk],
        value_key: key,
        old_value: element[key],
        new_value: new_value
      }
      var data1 = JSON.parse(JSON.stringify(data)) // deep copy
      // do:
      apply(data1, snapshot, false)
      expect(data).not.toEqual(data1)
      var differences = diff(data, data1) // https://github.com/flitbit/diff#simple-examples
      expect(differences.length).toBe(1)
      expect(differences[0].kind).toBe('E')
      expect(differences[0].path.pop()).toBe(snapshot.value_key)
      expect(differences[0].lhs).toBe(snapshot.old_value)
      expect(differences[0].rhs).toBe(snapshot.new_value)
      // undo:
      apply(data1, snapshot, true)
      expect(data).toEqual(data1)
    })
  })
  var data2 = JSON.parse(JSON.stringify(data)) // deep copy
  // add main table data
  data2['water'] = 'acqua'
  data2['fire'] = 'fuoco'
  data2['earth'] = 'terra'
  data2['air'] = 'aria'
  Object.keys(data2).forEach(key => {
    if (key.substr(0, 4) != 'w99_') {
      test(`it should change only the main table key ${key} and revert back`, () => {
        let snapshot = {
          id_key: 'id_w99',
          id: 0,
          value_key: 'water',
          old_value: 'acqua',
          new_value: "X"
        }
        // do:
        var data3 = JSON.parse(JSON.stringify(data2)) // deep copy
        apply(data3, snapshot, false)
        expect(data2).not.toEqual(data3)
        var differences = diff(data2, data3) // https://github.com/flitbit/diff#simple-examples
        expect(differences.length).toBe(1)
        expect(differences[0].kind).toBe('E')
        expect(differences[0].path.pop()).toBe(snapshot.value_key)
        expect(differences[0].lhs).toBe(snapshot.old_value)
        expect(differences[0].rhs).toBe(snapshot.new_value)
        // undo:
        apply(data3, snapshot, true)
        expect(data2).toEqual(data3)
      })
    }
  })
})
