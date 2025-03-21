<template>
    <div class="container">
        <div class="left-bar">
            <div class="personal">
                <router-link to="/personal/personalInfo">个人信息</router-link>
            </div>
            <!-- <div class="predict-record">
                <router-link to="/personal/predictRecord">检查记录</router-link>
            </div> -->
            <div class="change-password">
                <router-link to="/personal/changePassword">修改密码</router-link>
            </div>
            <div class="return-home">
                <router-link to="/step/step1">返回首页</router-link>
            </div>
        </div>
        <div class="right-content">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';
export default {
    data() {
        return {

        }
    },
    mounted() {
        // 只有当路径正好是 /personal 时才重定向到 personalInfo
        if (this.$route.path === '/personal') {
            this.$router.push("/personal/personalInfo")
        }
    },
    setup() {
        // const route1 = useRoute()
        // const router1 = useRouter()
        // console.log(route1.path)
    }
}

</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
}

a {
    text-decoration: none;
    color: #ffffff;
}

.container {
    display: flex;
    margin: 30px 100px;
}

.container .left-bar {
    display: flex;
    flex-direction: column;
    flex: 1;
}

.container .right-content {
    flex: 5;
}

.container .personal,
.container .predict-record,
.container .return-home,
.container .change-password {
    color: #ffffff;
    background-color: #4A69BD;
    padding: 12px;
    margin: 16px;
    text-align: center;
}
</style>
