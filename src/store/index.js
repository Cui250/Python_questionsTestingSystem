import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        user: JSON.parse(window.localStorage.getItem('user')) || null, // 从 localStorage 初始化用户状态
    },
    getters: {
        getUser(state) {
            return state.user;
        },
    },
    mutations: {
        setUser(state, userData) {
            state.user = userData;
            window.localStorage.setItem('user', JSON.stringify(userData));
        },
        removeUser(state) {
            state.user = null;
            window.localStorage.removeItem('user');
        },
    },
    actions: {
        setUser({ commit }, userData) {
            commit('setUser', userData);
        },
        logout({ commit }) {
            commit('removeUser');
            // 这里可以添加其他登出后的逻辑
        },
    },
    modules: {},
});