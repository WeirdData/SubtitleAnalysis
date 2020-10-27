const state = {
  currentSerial: null,
  numberOfWords: 40,
  temperature: 0.7,
  serialDetails: {
    got: {title: "Game of Thrones", img: "got.jpg", selected: false},
    bbt: {title: "Big Bang Theory", img: "bbt.jpg", selected: false},
    bb: {title: "Breaking Bad", img: "bb.jpg", selected: false},
    hp: {title: "Harry Potter Series", img: "hp.jpg", selected: false},
    cm: {title: "Criminal Minds", img: "cm.jpg", selected: false},

  },
  inputWords: ""
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
  },
  setNoOfWords(state, words) {
    state.numberOfWords = words;
  },
  setTemperature(state, temp) {
    state.temperature = temp;
  },
  setInputWords(state, words) {
    state.inputWords = words;
  }
}

const actions = {
  toggleSelection({commit}, id) {
    commit('toggleSelection', id)
  },
  setNoOfWords({commit}, words) {
    commit('setNoOfWords', words)
  },
  setTemperature({commit}, temp) {
    commit('setTemperature', temp)
  },
  setInputWords({commit}, words) {
    commit('setInputWords', words)
  }
}

const getters = {
  currentSerial: (state) => {
    return state.currentSerial
  },
  serialDetails: (state) => {
    return state.serialDetails
  },
  numberOfWords: (state) => {
    return state.numberOfWords
  },
  temperature: (state) => {
    return state.temperature
  },
  inputWords: (state) => {
    return state.inputWords
  }


}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
