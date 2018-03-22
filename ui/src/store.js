import Vue from 'vue';
import Vuex from 'vuex';
import moment from 'moment';


const SERIES_MAX_SIZE = 30;
Vue.use(Vuex);


const state = {
    series: [],
}

const getters = {
    getSeries: (state) => (key, max=SERIES_MAX_SIZE) => {
        let values = state.series.map(x => x[key]);
        return values.slice(-max);
    },
    getTimeSeries: (state) => (format='LTS', max=SERIES_MAX_SIZE) => {
        let values = state.series.map(x => moment(x.UTCUnixTime * 1000).format(format));
        return values.slice(-max);
    },
    getLastValue: (state) => (key) => {
        if (state.series.length > 0) {
            let last = state.series.reduce((l, e) => e.UTCUnixTime > l.UTCUnixTime ? e : l);
            return last[key];
        } 
        return 'NA';
    }
}

const actions = {
    requestSeries({ commit }) {
        Vue.http.get('data?format=json').then(response => {
            commit('setSeries', response.body);
        });
    },
    addRandomValues({ commit }) {
        commit('setSeries', [ { 'UTCUnixTime': 123123, 'TemperatureC': 26.0 } ]);
    }
}

const mutations = {
    setSeries(state, data) {
        state.series.push(...data);
        state.series = state.series.slice(-SERIES_MAX_SIZE);
    }
}

export default new Vuex.Store({
    state,
    getters,
    actions,
    mutations
});