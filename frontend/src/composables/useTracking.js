// composables/useTracking.js
import { ref, computed } from "vue";
import { useTrackingApi } from "@/composables/api";

export function useTracking() {
  const { getTrajectory } = useTrackingApi();
  const currentTracks = ref([]);
  const selectedTrack = ref(null);
  const trajectoryData = ref(null);

  const hasSelectedTrack = computed(() => selectedTrack.value !== null);

  const selectTrack = async (trackId) => {
    selectedTrack.value = trackId === selectedTrack.value ? null : trackId;

    if (selectedTrack.value) {
      try {
        trajectoryData.value = await getTrajectory(trackId);
      } catch (error) {
        console.error("궤적 로드 실패:", error);
        trajectoryData.value = null;
      }
    } else {
      trajectoryData.value = null;
    }
  };

  return {
    currentTracks,
    selectedTrack,
    trajectoryData,
    hasSelectedTrack,
    selectTrack,
  };
}
