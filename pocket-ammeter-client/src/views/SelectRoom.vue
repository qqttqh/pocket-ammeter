<template>
    <div class="container">
        <div class="main">
            <h1>选择宿舍</h1>
            <hr class="dashed">
            <div class="select-container">
                <!-- 栋数1 -->
                <select v-model="selectedBuilding1" id="selectedBuilding1">
                    <option value="">学</option>
                    <option v-for="(value, key) in roomInfoStore.data" :value="key">{{ key.substring(key.length - 1) }}
                    </option>
                </select>
                <!-- 栋数2 -->
                <select v-model="selectedBuilding2" id="selectedBuilding2">
                    <option value="">栋</option>
                    <option v-for="(value, key) in building2" :value="key">{{ key.substring(key.length - 1) }}</option>
                </select>
                <!-- 楼层 -->
                <select v-model="selectedFloor" id="selectedFloor">
                    <option value="">层</option>
                    <option v-for="(value, key) in floor" :value="key">{{ key.substring(key.length - 1) }}</option>
                </select>
                <!-- 房间号 -->
                <select v-model="selectedRoom" id="selectedRoom">
                    <option value="">房</option>
                    <option v-for="(value, key) in room" :value="value">{{ key.substring(key.length - 3) }}</option>
                </select>
            </div>
            <div class="button-container">
                <button @click="queryPower">查询</button>
            </div>
        </div>
    </div>
</template>

<script setup>

import { computed, onBeforeMount, ref, watch } from 'vue';
import { useRoomInfoStore } from '@/stores/roomInfo'
import { useRouter } from 'vue-router'

const router = useRouter()

// 宿舍信息仓库
const roomInfoStore = useRoomInfoStore()

// 属性
const selectedBuilding1 = ref('')
const selectedBuilding2 = ref('')
const selectedFloor = ref('')
const selectedRoom = ref('')

// 计算属性
const building2 = computed(() => {
    if (selectedBuilding1.value) {
        return roomInfoStore.data[selectedBuilding1.value]
    } else {
        return {}
    }
})

const floor = computed(() => {
    if (selectedBuilding2.value) {
        return building2.value[selectedBuilding2.value]
    } else {
        return {}
    }
})

const room = computed(() => {
    if (selectedFloor.value) {
        return floor.value[selectedFloor.value]
    } else {
        return {}
    }
})

// 监听
watch(selectedBuilding1, () => {
    selectedBuilding2.value = ''
    selectedFloor.value = ''
    selectedRoom.value = ''
})
watch(selectedBuilding2, () => {
    selectedFloor.value = ''
    selectedRoom.value = ''
})
watch(selectedFloor, () => {
    selectedRoom.value = ''
})

// 方法
const queryPower = () => {
    if (selectedRoom.value) {
        // 存储房间代码
        roomInfoStore.roomCode = selectedRoom.value
        // 存储房间名称
        const building1 = selectedBuilding1.value.substring(selectedBuilding1.value.length - 1)
        const building2 = selectedBuilding2.value.substring(selectedBuilding2.value.length - 1)
        const room = selectedRoom.value.substring(selectedRoom.value.length - 3)
        const name = `${building1}${building2}-${room}`

        roomInfoStore.roomName = name
        router.push('/')
    } else {
        alert('害 妹 选 完 房 号 呢 ！')
    }
}

</script>

<style scoped>
@import '../assets/SelectRoom.css';
</style>