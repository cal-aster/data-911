import axios from 'axios';

export default {
  dashboard({ commit }) {
    return new Promise((resolve) => {
      let cities = [];
      axios
        .get('/city')
        .then((response) => {
          cities.push(...response.data);
        })
        .catch((error) => {
          console.log(error);
        });
      commit('dashboard', cities);
      resolve();
    });
  },
};
