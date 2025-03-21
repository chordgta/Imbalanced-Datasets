import Step from './components/Step/Step.vue'
import Step1 from './components/Step/Step1.vue'
import Step2 from './components/Step/Step2.vue'
import Step3 from './components/Step/Step3.vue'

// stepRoutes.js - 步骤相关路由
export const stepRoutes = {
    path: 'step',  // 更具描述性的路径名
    component: Step,
    meta: {
        title: '欺诈检测流程',
    },
    children: [
        {
            path: 'step1',  // 替代 step1
            name: 'step1',
            component: Step1,
            meta: {
                title: '数据上传',
                requiresAuth: true
            }
        },
        {
            path: 'step2',  // 无参数路由放在前面
            name: 'step2',
            component: Step2,
            meta: {
                title: '数据处理',
                step: 2
            }
        },
        {
            path: 'step2/:filename',  // 带参数路由放在后面
            name: 'step2WithParam',
            component: Step2,
            meta: {
                title: '数据处理',
                step: 2
            }
        },
        {
            path: 'step3',      // 替代 step3
            name: 'step3',
            component: Step3,
            meta: {
                title: '分析结果',
                step: 3
            }
        }
    ]
}