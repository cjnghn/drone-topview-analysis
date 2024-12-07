// components/map/ClassLegend.vue
<template>
  <div class="mt-2 flex flex-wrap gap-2">
    <div
      v-for="(color, classId) in colors"
      :key="classId"
      class="flex items-center space-x-1"
    >
      <div
        class="w-4 h-4 rounded-full"
        :style="{ backgroundColor: color }"
      ></div>
      <span class="text-sm">Class {{ classId }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  colors: {
    type: Object,
    required: true,
  },
});
</script>
