<template>
    <div class="feedback-container" v-if="isFeedbackVisible">
        <div class="feedback-header">
            <div class="back-button" @click="toggleFeedback">
                <svg t="1715706118770" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                    p-id="5126" width="200" height="200">
                    <path
                        d="M744.3372563 1017.13692445c11.1289837 0 22.2701037-4.2477037 30.76551111-12.74311112 16.99081482-16.99081482 16.99081482-44.54020741 0-61.51888592L345.02883555 512.80099555 775.10276741 82.7392c16.99081482-16.97867852 16.99081482-44.54020741 0-61.51888592-16.99081482-16.99081482-44.52807111-16.99081482-61.51888593 0L252.74443852 482.04762075a43.51469037 43.51469037 0 0 0 0 61.53102222l460.83944296 460.81517036c8.48327111 8.49540741 19.62439111 12.74311111 30.75337482 12.74311112z"
                        fill="#fff" p-id="5127"></path>
                </svg>
            </div>
            <h5>给我一些建议或帮助</h5>
        </div>
        <div class="feedback-body">
            <textarea v-model="feedbackText" placeholder="请输入您的反馈..."></textarea>
        </div>
        <div class="feedback-footer">
            <button @click="sendFeedback">发送</button>
        </div>
    </div>
    <button class="feedback-icon" v-else @click="toggleFeedback">
        <svg t="1715707402407" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
            p-id="6137" width="200" height="200">
            <path
                d="M143.992471 650.511059v181.458823l180.374588-104.448c24.877176 4.065882 81.408 8.463059 107.64047 8.463059 229.737412 0 384-170.977882 384-372.013176S623.284706 0 432.007529 0C201.938824 0 15.992471 162.966588 15.992471 364.001882c0 116.464941 44.423529 215.341176 128 286.509177z m464.022588-330.511059a47.977412 47.977412 0 1 1 0 95.924706 47.977412 47.977412 0 0 1 0-95.924706z m-192.030118 0a48.007529 48.007529 0 1 1 0 95.984941 48.007529 48.007529 0 0 1 0-95.984941z m-192 0a48.007529 48.007529 0 1 1 0.030118 96.045176 48.007529 48.007529 0 0 1-0.030118-96.045176z m176.00753 479.984941h-95.984942c76.197647 74.511059 164.773647 119.988706 288.015059 119.988706 26.202353 0 51.772235-2.349176 76.649412-6.415059L847.992471 1024v-181.519059c97.28-66.620235 160.015059-170.014118 160.015058-286.479059 0-103.815529-49.904941-197.240471-129.596235-263.559529l1.596235 27.557647c0.271059 26.142118 0 23.762824 0 47.977412 0 255.216941-201.065412 432.007529-480.015058 432.007529z"
                fill="#28d875" p-id="6138"></path>
        </svg>
    </button>
</template>
  
<script setup>
import { ref } from 'vue';
import { useRoomInfoStore } from '@/stores/roomInfo'

const roomInfoStore = useRoomInfoStore()

const isFeedbackVisible = ref(false);
const feedbackText = ref('');

const toggleFeedback = () => {
    isFeedbackVisible.value = !isFeedbackVisible.value;
};

function sendBark(title, content) {
    const api = 'https://api.day.app';
    const key = 'Qndcjv9tmLsoB3cYuSPaPi';
    const icon = 'https://s3.bmp.ovh/imgs/2024/05/15/727a7943bad750c8.png';
    const group = '口袋电表反馈';

    fetch(`${api}/${key}/${title}/${content}?icon=${icon}&group=${group}`)
        .then(response => {
            response.json();
        })
        .then(data => {
            console.log('Bark推送相应：', data);
            alert("收到");
        })
        .catch(error => {
            console.error('Bark推送失败：', error);
            alert("出了点问题，再试试？")
        })

}

const sendFeedback = () => {
    if (feedbackText.value.trim()) {
        // 在这里处理发送反馈的逻辑
        sendBark(`口袋电表反馈-${roomInfoStore.roomName}`, feedbackText.value)
        feedbackText.value = '';
        isFeedbackVisible.value = false;
    } else {
        alert('请输入反馈内容');
    }
};
</script>
  
<style scoped>
.feedback-container {
    background-color: #000;
    color: #fff;
    padding: 20px;
    border-radius: 10px;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 300px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    z-index: 1000;
}

.feedback-header {
    /* display: flex; */
    justify-content: space-between;
    align-items: center;
}

.back-button {
    cursor: pointer;
    color: #fff;
}

.back-button svg {
    width: 20px;
    height: 20px;
}

.feedback-body {
    margin-top: 20px;
}

textarea {
    width: 90%;
    height: 100px;
    padding: 10px;
    border: 1px solid #555;
    border-radius: 5px;
    background-color: #333;
    color: #fff;
    font-size: 16px;
}

.feedback-footer {
    margin-top: 20px;
    text-align: right;
}

button {
    background-color: white;
    color: #000;
    border: none;
    width: 100px;
    padding: 10px 20px;
    border-radius: 20px;
    font-size: .5em;
    font-weight: 600;
    cursor: pointer;
}

.feedback-icon {
    display: inline-block;
    width: 2em;
    height: 2em;
    padding: 0;
    border-radius: 50%;
    background-color: transparent;
}

.feedback-icon svg {
    width: 2em;
    height: 2em;
}
</style>
  