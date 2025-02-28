<template>
    <div class="header">
        <div class="left">
            <router-link to="/step/step1">
                <img src="/money.png" class="logo">
                <span class="title">不平衡数据欺诈检测系统</span>
            </router-link>
        </div>

        <div class="right">
            <span class="us" @click="toPersonal">{{ username }}</span>
            <el-avatar @click="toPersonal" style="width:42px;height:42px;cursor: pointer;" v-if="avatar_url != ''"
                :src="avatar_url"></el-avatar>
            <el-avatar @click="toPersonal" style="width:42px;height:42px;cursor: pointer;" v-else>头像</el-avatar>
            <span class="quit" @click="quit">退出</span>
        </div>
    </div>
    <div class="container">
        <router-view></router-view>
    </div>
</template>



<script>
import { SetUp } from '@element-plus/icons-vue';
import router from '../router';
// import { useRoute, useRouter } from 'vue-router';


export default {
    name: 'Home',
    data() {
        return {
            username: "yule",
            avatar_url: ""
        }
    },
    mounted() {
        this.checkUserLogin();

    },
    methods: {
        checkUserLogin() {
            let user = JSON.parse(localStorage.getItem("user"))
            if (this.$route.fullPath == '/personal/personalInfo') {
                this.updateUserInfo(user);
                return
            }
            if (user) {
                this.updateUserInfo(user)
                this.$router.push('/step/step1')
            } else {
                this.$router.push('/login')
            }
        },
        updateUserInfo(user) {
            this.username = user.username
            if (user.avatar_url != '') {
                this.avatar_url = './api/uploads/' + user.avatar_url
            }
        },
        quit() {
            localStorage.clear()
            this.$router.push('/login')
        },
        toPersonal() {
            this.$router.push('/personal')
        }
    },
    // setup() {
       
    //     const route1 = useRoute()
    //     const router1 = useRouter()
    //     console.log(route1.path)
    // }

}
</script>

<style scoped>
a {
    text-decoration: none;
    color: #ffffff;
}

.header {
    height: 66px;
    background-color: #4A69BD;
    border: 1px solid #4A69BD;
    box-shadow: 2px 2px 3px;
    display: flex;
    justify-content: space-between;
}

.header .left {
    display: flex;
}

.header .left .logo {
    width: 50px;
    height: 50px;
    margin-left: 12px;
}

.header .left .title {
    position: relative;
    /* 相对定位 */
    top: -10px;
    /* 上移 5px，根据需要调整 */
    color: #ffffff;
    font-size: 26px;
    /* margin-top: 10px; */
    margin-left: 12px;
    align-items: center;
    /* 垂直居中 */

}

.header .right {
    display: flex;
    color: #ffffff;
    align-items: center;
    width: 220px;
    justify-content: space-around;
    margin-right: 38px;
}

.header .right .quit {
    cursor: pointer;
}

.header .right .us {
    cursor: pointer;
    margin-right: 1px;
}
</style>
