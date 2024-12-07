<template>
  <div class="container mx-auto p-4">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- 비디오 선택 및 컨트롤 패널 -->
      <div class="lg:col-span-3 bg-white p-4 rounded shadow">
        <VideoSelector v-model="selectedVideo" :videos="videos" @update:modelValue="handleVideoSelect" />
        <VideoControls :video="selectedVideo" :current-time="currentTime" :is-playing="isPlaying"
          @toggle-playback="handleTogglePlayback" @update:current-time="handleTimeUpdate" />
      </div>

      <!-- 지도와 비디오 컨테이너 -->
      <div class="lg:col-span-2 space-y-4">
        <!-- 비디오 플레이어 -->
        <div class="bg-white p-4 rounded shadow">
          <VideoPlayer ref="videoPlayerRef" :video="selectedVideo" :current-time="currentTime" :is-playing="isPlaying"
            @timeupdate="handleTimeUpdate" />
        </div>

        <!-- 지도 -->
        <div class="bg-white p-4 rounded shadow">
          <TrackingMap :video="selectedVideo" :current-tracks="currentTracks" :selected-track="selectedTrack"
            :intersections="intersections" />
        </div>
      </div>

      <!-- 정보 패널 -->
      <div class="h-[calc(400px+16rem)] flex flex-col bg-white rounded shadow">
        <TrackingList :tracks="currentTracks" :selected-track="selectedTrack" @select="handleTrackSelect" />
        <IntersectionList :intersections="intersections" :video-start-time="selectedVideo?.start_time" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';

import VideoSelector from './components/video/VideoSelector.vue';
import VideoControls from './components/video/VideoControls.vue';
import VideoPlayer from './components/video/VideoPlayer.vue';
import TrackingMap from './components/map/TrackingMap.vue';
import TrackingList from './components/tracking/TrackingList.vue';
import IntersectionList from './components/tracking/IntersectionList.vue';

import { useVideoApi } from '@/composables/api';
import { useTracking } from '@/composables/useTracking';
import { useIntersection } from '@/composables/useIntersection';

// State
const videos = ref([]);
const selectedVideo = ref(null);
const currentTime = ref(0);
const isPlaying = ref(false);
const currentTracks = ref([]);
const selectedTrack = ref(null);
const intersections = ref([]);
const videoPlayerRef = ref(null);

// Playback interval
let playbackInterval = null;

// API
const { getVideos, getTrackPositions } = useVideoApi();
const { getIntersectionsByTimeRange } = useIntersection();

// Event Handlers
const handleVideoSelect = async (video) => {
  selectedVideo.value = video;

  if (!video) {
    currentTime.value = 0;
    isPlaying.value = false;
    selectedTrack.value = null;
    currentTracks.value = [];
    intersections.value = [];
    return;
  }

  currentTime.value = video.start_time;
  isPlaying.value = false;
  selectedTrack.value = null;

  try {
    await Promise.all([
      updateTrackPositions(),
      loadIntersections()
    ]);
  } catch (error) {
    console.error('데이터 로드 실패:', error);
  }
};

const handleTimeUpdate = async (time) => {
  currentTime.value = time;

  if (selectedVideo.value?.id) {
    await Promise.all([
      updateTrackPositions(),
      loadIntersections()
    ]);
  }
};

const handleTrackSelect = async (trackId) => {
  selectedTrack.value = trackId;
};

const handleTogglePlayback = () => {
  isPlaying.value = !isPlaying.value;

  if (isPlaying.value && selectedVideo.value) {
    playbackInterval = setInterval(() => {
      if (currentTime.value >= selectedVideo.value.end_time) {
        isPlaying.value = false;
        clearInterval(playbackInterval);
        return;
      }
      currentTime.value = Math.min(
        currentTime.value + 0.1,
        selectedVideo.value.end_time
      );
    }, 100);
  } else {
    clearInterval(playbackInterval);
  }
};

// Data loading
const loadVideos = async () => {
  try {
    videos.value = await getVideos();
  } catch (error) {
    console.error('비디오 목록 로드 실패:', error);
    videos.value = [];
  }
};

const updateTrackPositions = async () => {
  if (!selectedVideo.value?.id) {
    currentTracks.value = [];
    return;
  }

  try {
    const tracks = await getTrackPositions(
      selectedVideo.value.id,
      currentTime.value
    );
    currentTracks.value = tracks;
  } catch (error) {
    console.error('트래킹 위치 업데이트 실패:', error);
    currentTracks.value = [];
  }
};

const loadIntersections = async () => {
  if (!selectedVideo.value?.id) {
    intersections.value = [];
    return;
  }

  try {
    const data = await getIntersectionsByTimeRange(
      selectedVideo.value.id,
      currentTime.value,
      currentTime.value + 10
    );
    intersections.value = data;
  } catch (error) {
    console.error('교차점 로드 실패:', error);
    intersections.value = [];
  }
};

// Lifecycle hooks
onMounted(() => {
  loadVideos();
});

onBeforeUnmount(() => {
  isPlaying.value = false;
  clearInterval(playbackInterval);
});

// Watchers
watch(currentTime, async (newTime) => {
  if (selectedVideo.value?.id) {
    await Promise.all([
      updateTrackPositions(),
      loadIntersections()
    ]);
  }
});
</script>