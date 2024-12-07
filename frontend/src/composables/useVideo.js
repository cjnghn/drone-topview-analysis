// composables/useVideo.js
import { ref } from "vue";
import { useVideoApi } from "@/composables/api";

export function useVideo() {
  const { getVideos } = useVideoApi();
  const videos = ref([]);
  const selectedVideo = ref(null);
  const currentTime = ref(0);
  const isPlaying = ref(false);
  let playbackInterval = null;

  const loadVideos = async () => {
    try {
      videos.value = await getVideos();
    } catch (error) {
      console.error("비디오 로드 실패:", error);
    }
  };

  const togglePlayback = () => {
    isPlaying.value = !isPlaying.value;

    if (isPlaying.value && selectedVideo.value) {
      playbackInterval = setInterval(() => {
        currentTime.value = Math.min(
          currentTime.value + 0.1,
          selectedVideo.value.end_time,
        );

        if (currentTime.value >= selectedVideo.value.end_time) {
          isPlaying.value = false;
          clearInterval(playbackInterval);
        }
      }, 100);
    } else {
      clearInterval(playbackInterval);
    }
  };

  const cleanup = () => {
    clearInterval(playbackInterval);
  };

  return {
    videos,
    selectedVideo,
    currentTime,
    isPlaying,
    loadVideos,
    togglePlayback,
    cleanup,
  };
}
