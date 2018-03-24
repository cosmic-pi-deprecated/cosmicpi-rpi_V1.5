import Vue from 'vue';
import Vuex from 'vuex';
import moment from 'moment';


const SERIES_MAX_SIZE = 30;
Vue.use(Vuex);


const state = {
    series: [],
    token: null,
    wifi: { 
        available: [], 
        current: '', 
    },
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
    },
    isLogged: (state) => () => {
        return (state.token !== null);
    },
    getToken: (state) => () => {
        return state.token;
    },
    getWifiList: (state) => () => {
        let wifis = state.wifi.available;
        let filtered = wifis.filter(function(item, pos) {
            return wifis.indexOf(item) == pos;
        })
        return filtered;
    },
    getCurrentWifi: (state) => () => {
        return state.wifi.current;
    },
}

const actions = {
    requestSeries({ commit }) {
        Vue.http.get('series?format=json').then(response => {
            commit('setSeries', response.body);
        });
    },
    addRandomValues({ commit }) {
        commit('setSeries', [ { 'UTCUnixTime': 123123, 'TemperatureC': 26.0 } ]);
    },
    requestWifi({ commit }) {
        let params = {
            token: state.token,
        };
        Vue.http.get('wifi', { params }).then(response => {
            commit('setWifi', response.body);
        });
    },
}

const mutations = {
    setSeries(state, data) {
        state.series.push(...data);
        state.series = state.series.slice(-SERIES_MAX_SIZE);
    },
    setAuth(state, token) {
        state.token = token;
    },
    setWifi(state, data) {
        state.wifi = data;
    },
}

export default new Vuex.Store({
    state,
    getters,
    actions,
    mutations
});