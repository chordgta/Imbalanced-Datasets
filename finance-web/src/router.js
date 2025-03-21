import { createRouter, createWebHashHistory } from 'vue-router'
import { setupRouterGuard } from './permission'
import { stepRoutes } from './step'
import { personalRoutes } from './personal'

import Login from './components/Login.vue'
import Home from './components/Home.vue'
import Register from './components/Register.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            component: Home,  
            redirect: '/step/step1', // 确保这里的重定向路径正确
            meta: {
                requiresAuth: true
            },
            children: [
                stepRoutes,
                personalRoutes
            ]
        },
        {
            path: '/login',
            name: 'Login',
            component: Login,
            meta: {
                title: '登录'
            }
        },
        {
            path: '/register',
            name: 'Register',
            component: Register,
            meta: {
                title: '注册'
            }
        }
    ]
})


// 设置全局路由守卫
setupRouterGuard(router)

export default router