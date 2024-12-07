// components/video/VideoPlayer.vue
<template>
  <div class="relative aspect-video">
    <video
      ref="videoRef"
      class="w-full h-full rounded"
      :src="video?.file"
      @timeupdate="handleTimeUpdate"
      @loadedmetadata="handleVideoLoaded"
    ></video>
    <div
      v-if="!video"
      class="absolute inset-0 flex items-center justify-center bg-gray-100 rounded"
    >
      <span class="text-gray-500">비디오를 선택해주세요</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  video: Object,
  currentTime: Number,
  isPlaying: Boolean,
});

const emit = defineEmits(["timeupdate"]);
const videoRef = ref(null);

const handleVideoLoaded = () => {
  if (videoRef.value && props.video) {
    videoRef.value.currentTime = props.currentTime;
  }
};

const handleTimeUpdate = (event) => {
  if (!props.isPlaying) return;
  emit("timeupdate", event.target.currentTime);
};

watch(
  () => props.isPlaying,
  (newValue) => {
    if (newValue) {
      videoRef.value?.play();
    } else {
      videoRef.value?.pause();
    }
  },
);

watch(
  () => props.currentTime,
  (newTime) => {
    if (
      videoRef.value &&
      Math.abs(videoRef.value.currentTime - newTime) > 0.1
    ) {
      videoRef.value.currentTime = newTime;
    }
  },
);
</script>

<style scoped>
video::-webkit-media-controls {
  display: none !important;
}
video {
  pointer-events: none;
}
</style>
