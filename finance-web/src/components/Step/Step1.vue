<template>
    <div class="container">


        <!-- <div class="input-group">
            <span class="label">1</span>
            <input type="number" v-model="form.test1" class="input-field" placeholder="请输入新账户余额">
        </div>
        <div class="input-group">
            <span class="label">2</span>
            <input type="number" v-model="form.test2" class="input-field" placeholder="请输入新账户余额">
        </div>
        <div class="input-group">
            <span class="label">3</span>
            <input type="number" v-model="form.test3" class="input-field" placeholder="请输入新账户余额">
        </div>
        <div class="input-group">
            <span class="label">4</span>
            <input type="number" v-model="form.test4" class="input-field" placeholder="请输入新账户余额">
        </div> -->

        <!-- 数据更新按钮 -->
        <div class="table-header">
            <el-button type="primary" size="small" @click="refreshData">
                <el-icon><Refresh /></el-icon>
                更新数据
            </el-button>
        </div>

        <div class="table-container">
            <el-table :data="tableData" style="width: 100%" border fixed-header :max-height="500" v-loading="loading"
                element-loading-text="加载中..." highlight-current-row
                @current-change="handleCurrentRowChange" ref="dataTable">
                <!-- 添加单选列 -->
                <!-- <el-table-column type="radio" width="55" /> -->

                <!-- 原有的列保持不变 -->
                <el-table-column prop="transTime" label="交易时间" width="180" />
                <el-table-column prop="transType" label="交易类型" width="120" />
                <el-table-column prop="amount" label="交易金额" width="120" />
                <el-table-column prop="lastName" label="姓" width="100" />
                <el-table-column prop="firstName" label="名" width="100" />
                <el-table-column prop="gender" label="性别" width="80" />
                <el-table-column prop="longitude" label="经度" width="120"  :formatter="formatLongitude"/>
                <el-table-column prop="latitude" label="纬度" width="120"  :formatter="formatLongitude"/>
                <el-table-column prop="cityPopulation" label="所在城市人口" width="150" />
                <el-table-column prop="birthDate" label="出生年月" width="120" />
                <el-table-column prop="merchantLong" label="商家经度" width="120" />
                <el-table-column prop="merchantLat" label="商家纬度" width="120" />
            </el-table>
        </div>

        <div class="upload_file">
            <el-upload class="upload_block" accept=".csv,.xls,.xlsx" drag action="/api/upload" :on-success="fileRespone"
                :limit="2" :file-list="fileList">
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                    将文件拖至框内或<em>点击进行上传</em>
                </div>
                <template #tip>
                    <div class="el-upload__tip">
                        仅限csv、xls、xlsx文件
                    </div>
                </template>
            </el-upload>
        </div>


        <div class="analysis">
            <el-button type="primary" @click="analyze">点击开始分析</el-button>
        </div>
    </div>
</template>


<script>
import { InfoFilled, UploadFilled, Refresh } from '@element-plus/icons-vue'
import { Msg } from '../../utils/msg.js'
import axios from '../../req.js'
import { ElMessageBox } from 'element-plus'

export default {
    name: 'Step1',
    components: {
        InfoFilled,
        UploadFilled,
        Refresh
    },
    data() {
        return {
            file: {},
            fileList: [],
            loading: false, // 添加loading状态
            currentRow: null,
            tableData: [],
            useCache: true  // 控制是否使用缓存
        }
    },
    mounted() {
        this.fetchTableData()
        
        if (this.tableData && this.tableData.length > 0) {
            this.currentRow = this.tableData[0]
            this.$nextTick(() => {
                const table = this.$refs.dataTable
                if (table) {
                    table.setCurrentRow(this.tableData[0])
                }
            })
        }
    },
    methods: {
        fileRespone(res, file, fileList) {
            console.log(res, file, fileList)
            if (res.state == 'success') {
                Msg("上传成功", "success")
                this.file = {
                    filename: res.info.filename,
                    file_url: '/uploads/' + res.info.filename
                }
                localStorage.setItem("file", JSON.stringify(this.file))
                // 上传成功后跳转到Step2
                this.$router.push({
                    name: 'step2WithParam',  // 使用正确的路由名称
                    params: {
                        filename: res.info.filename
                    }
                })
            } else {
                Msg(res.msg, 'error?????')
            }
        },
        // 刷新数据方法
        refreshData() {
            this.useCache = false  // 强制不使用缓存
            this.fetchTableData()
        },
        
        // 修改获取表格数据的方法
        fetchTableData() {
            this.loading = true
            axios({
                method: 'get',
                url: '/api/getTableData',
                params: {
                    useCache: this.useCache  // 传递是否使用缓存的参数
                }
            })
                .then(res => {
                    if (res.data.state === 'success') {
                        this.tableData = res.data.data
                        this.useCache = true  // 重置缓存标志
                        //Msg("数据加载成功", "success")
                        
                        if (this.tableData && this.tableData.length > 0) {
                            this.currentRow = this.tableData[0]
                            this.$nextTick(() => {
                                const table = this.$refs.dataTable
                                if (table) {
                                    table.setCurrentRow(this.tableData[0])
                                }
                            })
                        }
                    } else {
                        Msg(res.data.msg || '获取数据失败', 'error')
                    }
                })
                .catch(err => {
                    console.error('获取数据失败:', err)
                    Msg("获取数据失败，请稍后重试", "error")
                })
                .finally(() => {
                    this.loading = false
                })
        },
        // 处理行选择变化
        handleCurrentRowChange(row) {
            this.currentRow = row
            if (row) {
                console.log('选中行的交易时间:', row.transTime)
            }
        },
        
        // 分析方法
        analyze() {
            if (!this.currentRow) {
                Msg("请先选择要分析的数据", "warning")
                return
            }

            // 添加数据检查和日志
            const sendData = {
                ...this.currentRow
            }
            console.log('发送的数据:', sendData)
            
            this.loading = true
            axios({
                method: 'post',
                url: '/api/analyze',
                headers: {
                    'Content-Type': 'application/json'
                },
                data: sendData,  // 直接发送对象，让axios处理序列化
                transformRequest: [(data) => JSON.stringify(data)]  // 确保正确的JSON序列化
            })
                .then(res => {
                    if (res.data.state === 'success') {
                        // 检查是否有预测结果
                        if (res.data.result.error) {
                            Msg(res.data.result.error, "error")
                            return
                        }

                        const prediction = res.data.result.predictions[0]
                        const fraudProbability = res.data.result.fraud_probability
                        
                        // 格式化概率为百分比
                        const probabilityPercent = (fraudProbability * 100).toFixed(2)

                        // 使用 Element Plus 的 ElMessageBox 显示结果
                        ElMessageBox.alert(
                            `<div style="text-align: center;">
                                <h2 style="color: ${prediction === 0 ? '#67c23a' : '#f56c6c'}">
                                    ${prediction === 0 ? '正常交易' : '疑似欺诈交易'}
                                </h2>
                                <div style="margin-top: 15px;">
                                    <p>交易时间：${this.currentRow.transTime}</p>
                                    <p>交易金额：${this.currentRow.amount}</p>
                                    <p>交易类型：${this.currentRow.transType}</p>
                                    <p>欺诈概率：${probabilityPercent}%</p>
                                </div>
                            </div>`,
                            '分析结果',
                            {
                                confirmButtonText: '确定',
                                dangerouslyUseHTMLString: true,
                                customClass: {
                                    container: 'custom-message-box'
                                }
                            }
                        )
                    } else {
                        Msg(res.data.msg || '分析失败', 'error')
                    }
                })
                .catch(err => {
                    console.error('分析请求错误:', err)
                    Msg("请求失败，请稍后重试", "error")
                })
                .finally(() => {
                    this.loading = false
                })
        },
        formatLongitude(row, column, cellValue) {
            return this.formatCoordinate(cellValue);
        },
        // 通用的坐标格式化函数
        formatCoordinate(value) {
            if (typeof value === "number") {
                return value.toFixed(3); // 保留三位小数
            }
            return value; // 如果不是数字，返回原值
        },
    }
}
</script>

<style scoped>
.container {
    margin: 66px 160px;
    display: flex;
    flex-direction: column;
    min-height: 620px;
    font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
        'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.table-header {
    margin-bottom: 10px;
    display: flex;
    align-items: center;
}

.table-container {
    /* 修改表格容器样式 */
    position: relative;
    height: 400px;
    /* 固定高度 */
    border: 1px solid #ebeef5;
    border-radius: 4px;
    overflow: hidden;
    /* 防止内容溢出 */
}

/* 自定义弹窗样式 */
:deep(.custom-message-box) {
    padding: 20px;
}

/* 添加选中行的样式 */
:deep(.el-table__row.current-row) {
    background-color: #f0f9eb;
}

:deep(.el-table) {
    height: 100%;
    /* 设置表格高度100% */
}

/* 设置表格体的滚动 */
:deep(.el-table__body-wrapper) {
    overflow-y: auto;
    max-height: calc(400px - 48px);
    /* 减去表头高度 */
    position: sticky;
    top: 0;
    z-index: 1;
}

:deep(.el-table__header) {
    th {
        background-color: #f5f7fa;
        color: #606266;
        font-weight: bold;
        text-align: center;
    }
}

/* 优化滚动条样式 */
:deep(.el-table__body-wrapper::-webkit-scrollbar) {
    width: 8px;
    height: 8px;
}

:deep(.el-table__body-wrapper::-webkit-scrollbar-thumb) {
    background-color: #dcdfe6;
    border-radius: 4px;
}

:deep(.el-table__body-wrapper::-webkit-scrollbar-track) {
    background-color: #f5f7fa;
}

.input-group {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
}

.input-field {
    flex: 1;
    height: 40px;
    line-height: 40px;
    padding: 0 15px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    color: #606266;
    font-size: 14px;
}

.container .introduce {
    flex: 5;
}

.container .introduce .head_title {
    font-size: 21px;
}

.container .upload_file {
    /* 上传区域样式 */
    margin-top: 20px;
    padding: 20px 0;
    display: flex;
    justify-content: center;
    align-content: center;
}

.container .analysis {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    align-content: center;
    flex: 1;
}
</style>
