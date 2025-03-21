import Personal from './components/Personal/Personal.vue'
import PersonInfo from './components/Personal/PersonInfo.vue'
import PredictRecord from './components/Personal/PredictRecord.vue'
import ChangePassword from './components/Personal/ChangePassword.vue'


// personalRoutes.js - 个人中心路由
export const personalRoutes = {
    path: 'personal',
    component: Personal,
    meta: {
        title: '个人中心',
        requiresAuth: true
    },
    children: [
        {
            path: 'personalInfo',  // 替代 personalInfo
            name: 'UserProfile',
            component: PersonInfo,
            meta: {
                title: '个人信息'
                
            }
        },
        {
            path: 'predictRecord',  // 替代 predictRecord
            name: 'PredictionHistory',
            component: PredictRecord,
            meta: {
                title: '预测记录'
            }
        },
        {
            path: 'changePassword', // 替代 changePassword
            name: 'SecuritySettings',
            component: ChangePassword,
            meta: {
                title: '安全设置'
            }
        }
    ]
}