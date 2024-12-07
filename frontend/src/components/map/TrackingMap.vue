// components/map/TrackingMap.vue
<template>
  <div>
    <div id="map" class="h-[400px] rounded"></div>
    <ClassLegend :colors="classColors" />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, watch, ref } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import ClassLegend from './ClassLegend.vue';
import { classColors } from '@/constants/colors';

const props = defineProps({
  video: Object,
  currentTracks: {
    type: Array,
    default: () => []
  },
  selectedTrack: Number,
  intersections: {
    type: Array,
    default: () => []
  }
});

const map = ref(null);
const trackMarkers = ref({});
const trackPaths = ref({});
const intersectionMarkers = ref([]);

const DEFAULT_CENTER = [37.5665, 126.9780];
const DEFAULT_ZOOM = 17;

const clearAllLayers = () => {
  // Clear track markers
  Object.values(trackMarkers.value).forEach(marker => {
    if (map.value) marker.remove();
  });
  trackMarkers.value = {};

  // Clear track paths
  Object.values(trackPaths.value).forEach(path => {
    if (map.value) path.remove();
  });
  trackPaths.value = {};

  // Clear intersection markers
  intersectionMarkers.value.forEach(marker => {
    if (map.value) marker.remove();
  });
  intersectionMarkers.value = [];
};

const initMap = () => {
  map.value = L.map('map', {
    minZoom: 15,
    maxZoom: 19
  }).setView(DEFAULT_CENTER, DEFAULT_ZOOM);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map.value);
};

const updateTrackMarkers = () => {
  // Clear existing markers
  Object.values(trackMarkers.value).forEach(marker => marker.remove());
  trackMarkers.value = {};

  if (!map.value) return;

  props.currentTracks.forEach(track => {
    if (!track.last_latitude || !track.last_longitude) return;

    const marker = L.circleMarker(
      [track.last_latitude, track.last_longitude],
      {
        radius: 8,
        color: props.selectedTrack === track.tracking_id ? '#ff0000' : classColors[track.class_id] || '#999',
        fillColor: props.selectedTrack === track.tracking_id ? '#ff0000' : classColors[track.class_id] || '#999',
        fillOpacity: 0.7,
        weight: 2
      }
    ).addTo(map.value);

    marker.bindPopup(`
      <div class="font-bold">Track ${track.tracking_id}</div>
      <div>Class ${track.class_id}</div>
      <div>Speed: ${track.last_speed.toFixed(1)} m/s</div>
    `);

    trackMarkers.value[track.tracking_id] = marker;
  });
};

const updateIntersectionMarkers = () => {
  // Clear existing intersection markers
  intersectionMarkers.value.forEach(marker => marker.remove());
  intersectionMarkers.value = [];

  if (!map.value || !props.video) return;

  props.intersections.forEach(intersection => {
    if (!intersection.latitude || !intersection.longitude) return;

    const marker = L.circleMarker(
      [intersection.latitude, intersection.longitude],
      {
        radius: 5,
        color: '#ff0000',
        fillColor: '#ff0000',
        fillOpacity: 0.5,
        weight: 1
      }
    ).addTo(map.value);

    marker.bindPopup(`
      <div class="font-bold">교차점</div>
      <div>Track ${intersection.track1} ↔ ${intersection.track2}</div>
      <div>Time: ${intersection.timestamp.toFixed(1)}s</div>
    `);

    intersectionMarkers.value.push(marker);
  });
};

const updateMapBounds = () => {
  if (!map.value || !props.video) return;

  const { start_latitude, start_longitude, end_latitude, end_longitude } = props.video;

  if (start_latitude != null &&
    start_longitude != null &&
    end_latitude != null &&
    end_longitude != null) {
    try {
      map.value.fitBounds([
        [start_latitude, start_longitude],
        [end_latitude, end_longitude]
      ], {
        padding: [50, 50],
        maxZoom: 17
      });
    } catch (error) {
      console.error('지도 범위 설정 실패:', error);
      map.value.setView(DEFAULT_CENTER, DEFAULT_ZOOM);
    }
  } else {
    map.value.setView(DEFAULT_CENTER, DEFAULT_ZOOM);
  }
};

// Watchers
watch(() => props.video, (newVideo) => {
  if (newVideo) {
    clearAllLayers();
    updateMapBounds();
  }
}, { deep: true });

watch(() => props.currentTracks, updateTrackMarkers, { deep: true });
watch(() => props.intersections, updateIntersectionMarkers, { deep: true });
watch(() => props.selectedTrack, (newTrackId) => {
  Object.entries(trackMarkers.value).forEach(([id, marker]) => {
    const track = props.currentTracks.find(t => t.tracking_id === parseInt(id));
    const isSelected = parseInt(id) === newTrackId;
    if (track) {
      marker.setStyle({
        color: isSelected ? '#ff0000' : classColors[track.class_id] || '#999',
        fillColor: isSelected ? '#ff0000' : classColors[track.class_id] || '#999'
      });
    }
  });
});

// Lifecycle hooks
onMounted(() => {
  initMap();
});

onUnmounted(() => {
  if (map.value) {
    clearAllLayers();
    map.value.remove();
    map.value = null;
  }
});
</script>

<style>
.leaflet-container {
  background-color: #f8f9fa;
}
</style>