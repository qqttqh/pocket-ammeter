<template>
    <div class="container">
        <div class="main">
            <h1 class="title">电表 ({{ roomInfoStore.roomName }})&nbsp;&nbsp;&nbsp;&nbsp;<FeedBack></FeedBack>
            </h1>
            <hr class="dashed">
            <!-- 余额部分 -->
            <div class="balance-container">
                <div class="balance-item">
                    <div>账户余额</div>
                    <div>¥ {{ totalBalance }}</div>
                </div>
                <div class="balance-item">
                    <div>人均(<input v-model="numOfPeople" type="text" value="6">人)</div>
                    <div>¥ {{ avgBalance }}</div>
                </div>
            </div>
            <!-- 折线图部分 -->
            <LineChart></LineChart>

            <!-- 电表部分 -->
            <div class="power-container">
                <div class="dormitory-number">宿舍编号：{{ roomInfoStore.roomCode }}</div>
                <div class="power-data-container">
                    <div v-for="(item, index) in power" class="data-item" :key="index">{{ item
                        }}</div>
                    <div class="data-item" v-show="roomInfoStore.power">度</div>
                </div>
                <div class="update-time">更新时间：{{ roomInfoStore.date }}</div>
            </div>
            <!-- 按钮部分 -->
            <div class="button-container">
                <button @click="cahngeDormitory">切换宿舍</button>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { computed, onBeforeMount, ref } from 'vue';
    import { useRoomInfoStore } from '@/stores/roomInfo'
    import { useRouter } from 'vue-router'
    import LineChart from '@/components/LineChart.vue';
    import FeedBack from '@/components/FeedBack.vue';
    import sentry from "@/utils/sentry.js";

    const router = useRouter()
    const roomInfoStore = useRoomInfoStore()
    // 属性
    // const myPowerInfo = reactive({ roomcode: '', power: '', date: '', dates: [], electricities: [] })
    const numOfPeople = ref(6)


    // 计算属性
    // 总余额
    const totalBalance = computed(() => {
        if (roomInfoStore.power) {
            return (roomInfoStore.power * 0.626).toFixed(2)
        } else {
            return '0.00'
        }
    })

    // 平均余额
    const avgBalance = computed(() => {
        if (totalBalance) {
            return (totalBalance.value / numOfPeople.value).toFixed(2)
        } else {
            return '0.00'
        }
    })

    // 电量
    const power = computed(() => {
        if (roomInfoStore.power) {
            return roomInfoStore.power
        } else {
            return '将在5分钟内爬取'
        }
    })

    // 检查自己的房号是否存在 不存在则跳转去选房号
    onBeforeMount(async () => {
        if (!roomInfoStore.roomCode) {
            router.push('/select')
        } else {
            try {
                const response = await fetch(`https://io.power.xyquan.top/query.php?roomcode=${roomInfoStore.roomCode}`);
                if (!response.ok) {
                    throw new Error('网络响应不好');
                }
                const data = await response.json();
                roomInfoStore.power = data.power
                roomInfoStore.date = data.date
                roomInfoStore.dates.data = data.dates
                roomInfoStore.electricities.data = data.electricities

            } catch (error) {
                console.error('获取或解析数据时出现问题：', error);
            }
            // 调用哨兵
            sentry()
        }
    })

    // 方法
    const cahngeDormitory = () => {
        router.push('/select')
    }

</script>

<style scoped>
    @import url(../assets/PowerInfo.css);

    .title {
        display: flex;
        align-items: center;
    }
</style>
