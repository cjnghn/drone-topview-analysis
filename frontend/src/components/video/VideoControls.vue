// components/video/VideoControls.vue
<template>
  <div v-if="video" class="mt-4 space-y-2">
    <div class="flex items-center space-x-4">
      <button
        @click="$emit('toggle-playback')"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        {{ isPlaying ? "일시정지" : "재생" }}
      </button>
      <span class="font-mono">
        {{ formatDuration(currentTime - video.start_time) }} /
        {{ formatDuration(video.end_time - video.start_time) }}
      </span>
    </div>

    <div class="flex items-center space-x-4">
      <input
        type="range"
        :value="currentTime"
        @input="$emit('update:currentTime', +$event.target.value)"
        :min="video.start_time"
        :max="video.end_time"
        step="0.1"
        class="flex-grow"
      />
    </div>
  </div>
</template>

<script setup>
import { formatDuration } from "@/utils/time";

defineProps({
  video: Object,
  currentTime: Number,
  isPlaying: Boolean,
});
defineEmits(["toggle-playback", "update:currentTime"]);
</script>
