<template>
    <div ref="info" style="width: 100%; height: 200px; margin-top: 20px;"></div>
</template>

<script setup>
import { useRoomInfoStore } from "@/stores/roomInfo";
import { onMounted, ref, inject, onUnmounted, watch } from "vue";

const roomInfoStore = useRoomInfoStore()

//通过inject使用echarts
const echarts = inject("echarts");

//通过ref获取html元素
const info = ref(null);
let userEc = null;

const resizeChart = () => {
    if (userEc) {
        userEc.resize();
    }
};

onMounted(() => {
    // 渲染echarts的父元素
    var infoEl = info.value;

    //  light dark
    userEc = echarts.init(infoEl);

    // 指定图表的配置项和数据
    var option = {
        xAxis: {
            type: 'category',
            data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            axisLabel: {
                formatter: '{value} 日'
            },
            axisLine: {
                lineStyle: {
                    color: '#fff' // 设置轴线颜色
                }
            },
            axisTick: {
                alignWithLabel: true // 刻度与标签对齐
            },
            boundaryGap: true // 去除边界空白
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} 度'
            },
            axisLine: {
                lineStyle: {
                    color: '#aaa'
                }
            },
            splitLine: {
                show: false // 去除网格线
            }
        },
        grid: {
            top: '10%', // 设置顶部内边距
            bottom: '10%', // 设置底部内边距
            left: '0%', // 设置左侧内边距
            right: '0%', // 设置右侧内边距
            containLabel: true,
            backgroundColor: '#f0f0f0', // 自定义背景颜色
            borderWidth: 1, // 设置边框宽度
            borderColor: '#ccc', // 设置边框颜色
            borderRadius: [100, 100, 100, 100] // 设置左上、右上、右下、左下的圆角半径
        },
        dataZoom: [{
            type: 'inside', // 滑动条型 dataZoom 组件
            show: true, // 显示滑动条
            start: 40, // 滑动条开始位置（0-100）
            end: 100, // 滑动条结束位置（0-100）
            bottom: '2%' // 位置调整到底部
        }],
        series: [{
            name: '度',
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].map(value => parseFloat(value.toFixed(2))),
            type: 'line',
            color: '#3f99ff',
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            label: {
                show: true,
                position: 'top',
                color: 'white',
                formatter: '{c} 度',
            }
        }, {
            name: '元',
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].map(value => parseFloat((value * 0.626).toFixed(2))),
            type: 'line',
            color: '#f8b500',
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            label: {
                show: true,
                position: 'top',
                color: 'white',
                formatter: '{c} 元',
            }
        }]
    };

    // 使用刚指定的配置项和数据显示图表。
    userEc.setOption(option);
    userEc.resize(); // 初始渲染时调整图表大小
    window.addEventListener('resize', resizeChart); // 监听窗口大小变化事件

    // 通过 watch 监听数据是否准备好，当数据准备好时执行回调
    watch([roomInfoStore.electricities, roomInfoStore.dates], ([electricities, dates]) => {
        if (electricities && dates) {
            userEc.setOption({
                xAxis: {
                    data: dates.data
                },
                series: [{
                    data: electricities.data.map(value => parseFloat(value.toFixed(2)))
                }, {
                    data: electricities.data.map(value => parseFloat((value * 0.626).toFixed(2)))
                }]
            });
        } else {
            console.log('else内容');
        }
    });
});

onUnmounted(() => {
    window.removeEventListener('resize', resizeChart); // 组件销毁时移除事件监听器
    if (userEc) {
        userEc.dispose(); // 销毁 ECharts 实例
    }
});
</script>


<style scoped>
div {
    border-radius: 20px;
}
</style>
