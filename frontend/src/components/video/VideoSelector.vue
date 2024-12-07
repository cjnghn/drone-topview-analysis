// components/video/VideoSelector.vue
<template>
  <div class="bg-white p-4 rounded shadow">
    <select :value="modelValue ? JSON.stringify(modelValue) : ''" @change="handleChange"
      class="w-full p-2 border rounded">
      <option value="">비디오를 선택하세요</option>
      <option v-for="video in videos" :key="video.id" :value="JSON.stringify(video)">
        {{ video.title }} ({{ formatDuration(video.end_time - video.start_time) }})
      </option>
    </select>
  </div>
</template>

<script setup>
import { formatDuration } from '@/utils/time';

const props = defineProps({
  modelValue: Object,
  videos: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue']);

const handleChange = (event) => {
  const value = event.target.value;
  try {
    emit('update:modelValue', value === '' ? null : JSON.parse(value));
  } catch (error) {
    console.error('비디오 데이터 파싱 오류:', error);
    emit('update:modelValue', null);
  }
};
</script>
