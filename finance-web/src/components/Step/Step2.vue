<template>
    <div class="container">
        <div class="head">
            <el-icon color="#909399" style="margin-right:12px;"><data-analysis /></el-icon>
            <span>数据分析结果</span>
            <el-divider style="background-color: #7f8c8d;"></el-divider>
        </div>

        <!-- 欺诈数据统计卡片 -->
        <div class="statistics-card">
            <el-card>
                <template #header>
                    <div class="card-header">
                        <span>欺诈数据统计</span>
                    </div>
                </template>
                <div class="statistics-content">
                    <div class="stat-item">
                        <span class="label">总数据条数：</span>
                        <span class="value">{{ totalCount }}</span>
                    </div>
                    <div class="stat-item">
                        <span class="label">欺诈数据条数：</span>
                        <span class="value fraud">{{ fraudCount }}</span>
                    </div>
                    <div class="stat-item">
                        <span class="label">欺诈数据占比：</span>
                        <span class="value">{{ fraudPercentage }}%</span>
                    </div>
                </div>
            </el-card>
        </div>

        <!-- 数据显示控制 -->
        <div class="data-control">
            <div class="control-group">
                <el-button type="primary" @click="toggleFraudData" :loading="loading">
                    {{ showFraudData ? '隐藏欺诈数据' : '显示欺诈数据' }}
                </el-button>
            </div>

            <div class="control-group">
                <el-input
                    v-model="rangeStart"
                    placeholder="起始行"
                    type="number"
                    style="width: 120px;"
                />
                <span class="range-separator">至</span>
                <el-input
                    v-model="rangeEnd"
                    placeholder="结束行"
                    type="number"
                    style="width: 120px;"
                />
                <el-button type="primary" @click="toggleRangeData" :loading="loading">
                    {{ showRangeData ? '隐藏范围数据' : '显示范围数据' }}
                </el-button>
            </div>
        </div>

        <!-- 欺诈数据表格 -->
        <div class="fraud-table" v-if="showFraudData && fraudData.length > 0">
            <div class="table-title">欺诈数据</div>
            <el-table :data="fraudData" border style="width: 100%" v-loading="loading">
                <el-table-column prop="transTime" label="交易时间" width="180" />
                <el-table-column prop="transType" label="交易类型" width="120" />
                <el-table-column prop="amount" label="交易金额" width="120" />
                <el-table-column prop="lastName" label="姓" width="100" />
                <el-table-column prop="firstName" label="名" width="100" />
                <el-table-column prop="gender" label="性别" width="80" />
                <el-table-column prop="longitude" label="经度" width="120" />
                <el-table-column prop="latitude" label="纬度" width="120" />
                <el-table-column prop="cityPopulation" label="所在城市人口" width="150" />
                <el-table-column prop="birthDate" label="出生年月" width="120" />
                <el-table-column prop="merchantLong" label="商家经度" width="120" />
                <el-table-column prop="merchantLat" label="商家纬度" width="120" />
                <el-table-column prop="fraudProbability" label="欺诈概率" width="120">
                    <template #default="scope">
                        <span :style="{ color: scope.row.fraudProbability > 0.5 ? '#F56C6C' : '#67C23A' }">
                            {{ (scope.row.fraudProbability * 100).toFixed(2) }}%
                        </span>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <!-- 范围数据表格 -->
        <div class="range-table" v-if="showRangeData && rangeData.length > 0">
            <div class="table-title">范围数据（第 {{ rangeStart }} 行至第 {{ rangeEnd }} 行）</div>
            <el-table :data="rangeData" border style="width: 100%" v-loading="loading">
                <el-table-column prop="transTime" label="交易时间" width="180" />
                <el-table-column prop="transType" label="交易类型" width="120" />
                <el-table-column prop="amount" label="交易金额" width="120" />
                <el-table-column prop="lastName" label="姓" width="100" />
                <el-table-column prop="firstName" label="名" width="100" />
                <el-table-column prop="gender" label="性别" width="80" />
                <el-table-column prop="longitude" label="经度" width="120" />
                <el-table-column prop="latitude" label="纬度" width="120" />
                <el-table-column prop="cityPopulation" label="所在城市人口" width="150" />
                <el-table-column prop="birthDate" label="出生年月" width="120" />
                <el-table-column prop="merchantLong" label="商家经度" width="120" />
                <el-table-column prop="merchantLat" label="商家纬度" width="120" />
                <el-table-column prop="fraudProbability" label="欺诈概率" width="120">
                    <template #default="scope">
                        <span :style="{ color: scope.row.fraudProbability > 0.5 ? '#F56C6C' : '#67C23A' }">
                            {{ (scope.row.fraudProbability * 100).toFixed(2) }}%
                        </span>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <div v-if="!showFraudData && !showRangeData" class="no-data-tip">
            请选择要显示的数据类型
        </div>
        <div v-else-if="showFraudData && fraudData.length === 0" class="no-data-tip">
            未发现欺诈数据
        </div>
        <div v-else-if="showRangeData && rangeData.length === 0" class="no-data-tip">
            所选范围内没有数据
        </div>
    </div>
</template>

<script>
import { DataAnalysis } from '@element-plus/icons-vue'
import axios from '../../req.js'
import { Msg } from '../../utils/msg.js'

export default {
    name: 'Step2',
    components: {
        DataAnalysis
    },
    data() {
        return {
            loading: false,
            showFraudData: false,
            showRangeData: false,
            rangeStart: 1,
            rangeEnd: 10,
            totalCount: 0,
            fraudCount: 0,
            fraudData: [],
            allData: [],  // 存储所有数据
            filename: ''
        }
    },
    computed: {
        fraudPercentage() {
            if (this.totalCount === 0) return 0
            return ((this.fraudCount / this.totalCount) * 100).toFixed(2)
        },
        rangeData() {
            const start = Math.max(0, parseInt(this.rangeStart) - 1 || 0)
            const end = Math.min(this.allData.length, parseInt(this.rangeEnd) || this.allData.length)
            return this.allData.slice(start, end)
        }
    },
    mounted() {
        // 从路由参数获取文件名
        this.filename = this.$route.params.filename
        if (!this.filename) {
            Msg("请先上传数据文件", "warning")
            this.$router.push({
                name: 'step1'
            })
            return
        }
        this.fetchFraudData()
    },
    methods: {
        async fetchFraudData() {
            this.loading = true
            try {
                const response = await axios({
                    method: 'get',
                    url: '/api/getFraudData',
                    params: {
                        filename: this.filename
                    }
                })
                
                if (response.data.state === 'success') {
                    this.totalCount = response.data.totalCount
                    this.fraudCount = response.data.fraudCount
                    this.fraudData = response.data.fraudData
                    this.allData = response.data.allData  // 后端需要返回所有数据
                } else {
                    Msg(response.data.msg || '获取数据失败', 'error')
                }
            } catch (error) {
                console.error('获取欺诈数据失败:', error)
                Msg("获取数据失败，请稍后重试", "error")
            } finally {
                this.loading = false
            }
        },
        toggleFraudData() {
            this.showFraudData = !this.showFraudData
            if (this.showFraudData) {
                this.showRangeData = false
            }
        },
        toggleRangeData() {
            if (!this.rangeStart || !this.rangeEnd) {
                Msg("请输入有效的范围", "warning")
                return
            }
            if (parseInt(this.rangeStart) > parseInt(this.rangeEnd)) {
                Msg("起始行不能大于结束行", "warning")
                return
            }
            if (parseInt(this.rangeStart) < 1) {
                Msg("起始行不能小于1", "warning")
                return
            }
            if (parseInt(this.rangeEnd) > this.allData.length) {
                Msg(`结束行不能大于总行数 ${this.allData.length}`, "warning")
                return
            }
            
            this.showRangeData = !this.showRangeData
            if (this.showRangeData) {
                this.showFraudData = false
            }
        }
    }
}
</script>

<style scoped>
.container {
    margin: 16px 60px;
    display: flex;
    flex-direction: column;
    min-height: 660px;
    font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
        'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.head {
    font-size: 21px;
    width: 100%;
    text-align: center;
    margin-top: 30px;
}

.statistics-card {
    margin: 20px 0;
}

.statistics-content {
    display: flex;
    justify-content: space-around;
    padding: 20px 0;
}

.stat-item {
    text-align: center;
}

.stat-item .label {
    font-size: 14px;
    color: #606266;
}

.stat-item .value {
    font-size: 24px;
    font-weight: bold;
    color: #409EFF;
    margin-left: 10px;
}

.stat-item .value.fraud {
    color: #F56C6C;
}

.data-control {
    margin: 20px 0;
    display: flex;
    gap: 20px;
    justify-content: center;
    align-items: center;
}

.control-group {
    display: flex;
    gap: 10px;
    align-items: center;
}

.range-separator {
    color: #606266;
    margin: 0 5px;
}

.table-title {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #409EFF;
}

.fraud-table, .range-table {
    margin-top: 20px;
}

.no-data-tip {
    text-align: center;
    color: #909399;
    margin-top: 40px;
    font-size: 16px;
}
</style>
