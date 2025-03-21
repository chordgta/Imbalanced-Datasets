// 定义全局路由守卫配置
import { Msg } from './utils/msg'
// 定义白名单路由（不需要登录即可访问的路由）
const whiteList = ['/login', '/register']

// 全局路由守卫
export function setupRouterGuard(router) {
    router.beforeEach((to, from, next) => {
        // 获取用户信息，这里假设存储在localStorage中
        const user = JSON.parse(localStorage.getItem('user'))
        
        // 白名单直接放行
        if (whiteList.includes(to.path)) {
            next()
            return
        }

        // 检查是否登录
        if (!user) {
            // 未登录，跳转到登录页
            Msg('请先登录', 'warning')
            next({
                path: '/login',
                query: {
                    redirect: to.fullPath // 保存原本要访问的路径
                }
            })
            return
        }

        // 这里可以添加其他权限检查逻辑
        // 例如：角色检查、特定权限检查等
        // 更新页面标题
        // if (to.meta.title) {
        //     document.title = `${to.meta.title} - 欺诈检测系统`
        // }
        // 通过权限检查，允许访问
        next()
    })
}

