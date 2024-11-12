<template>
  <RouterView></RouterView>
</template>

<script setup>
import { provide } from 'vue';
import { RouterView } from 'vue-router';

//引入echarts
import * as echarts from "echarts";

//通过provide提供echarts
provide("echarts", echarts);
</script>

<style scoped></style>