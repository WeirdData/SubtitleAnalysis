const state = {
  currentSerial: null,
  serialDetails: {
    got: {title: "Game of Thrones", img: "got.jpg", selected: false},
    bbt: {title: "Big Bang Theory", img: "bbt.jpg", selected: false},
    // bb: {title: "Breaking Bad", img: "bb.jpg", selected: false},
  }
}

const mutations = {
  toggleSelection(state, id) {
    for (let s in state.serialDetails) {
      if (state.serialDetails.hasOwnProperty(s)) {
        state.serialDetails[s].selected = s === id;
        if (s === id) {
          state.currentSerial = s;
        }
      }
    }
  }
}

const actions = {
  toggleSelection({commit}, id) {
    commit('toggleSelection', id)
  }
}

const getters = {
  currentSerial: (state) => {
    return state.currentSerial
  },
  serialDetails: (state) => {
    return state.serialDetails
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
