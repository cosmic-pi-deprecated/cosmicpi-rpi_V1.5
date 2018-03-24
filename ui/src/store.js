import Vue from 'vue';
import Vuex from 'vuex';
import moment from 'moment';


const SERIES_MAX_SIZE = 100;
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
            return state.series[state.series.length - 1][key];
        } 
        return 'NA';
    },
    getNumberOfEvents: (state) => () => {
        return state.series.length;
    },
    getPeriod: (state) => () => {
        if (state.series.length > 1) {
            return state.series[state.series.length - 1].UTCUnixTime - state.series[0].UTCUnixTime;
        } 
        return 0;
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
        let params = {
            format: 'json',
            limit: SERIES_MAX_SIZE,
            from: state.series.length > 0 ? state.series[state.series.length - 1].UTCUnixTime : 0,
        };
        Vue.http.get('series', { params }).then(response => {
            commit('setSeries', response.body);
        });
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
        data.sort((l, r) => l.UTCUnixTime + l.SubSeconds > r.UTCUnixTime + r.SubSeconds ? 1 : -1);
        for (let item of data) {
            let last = state.series[state.series.length - 1];
            let lastUTCUnixTime = last ? last.UTCUnixTime : 0;
            let lastSubSeconds = last ? last.SubSeconds : 0;
            if (item.UTCUnixTime + item.SubSeconds > lastUTCUnixTime + lastSubSeconds) {
                state.series.push(item);
            }
        }
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