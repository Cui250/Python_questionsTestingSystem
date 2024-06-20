import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    //数据，相当于data  调用方法 标签中使用{{$store.state.name}}   this.$store.state.全局数据名称
    state: {
        // user: null//初始化用户状态为null
        user:{
            id:'1',
            userName:'小明',
            email: '1111@111',
            password: '123456',
            role: 'student'
        }

    }
    ,
    //组件中使用$store.getters.xxx获取getters中的返回值  例如<span> 学生年龄总和：{{ $store.getters.getAllPersonAge }} </span>
    getters: {
        getUser(state) {
            return state.user;  // 获取用户数据的getter
        }
    },
    //里面定义方法，操作state方法
    mutations: {
        setUser(state, userData) {
            state.user = userData;  // 设置用户数据的mutation
        }
    },
    // 操作异步操作mutation
    actions: {
        setUser({ commit }, userData) {
            commit('setUser', userData);  // 触发设置用户数据的mutation的action
        }
    },
    modules: {},
})