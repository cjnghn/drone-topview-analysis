// composables/useIntersection.js
import { ref } from "vue";
import { useIntersectionApi } from "@/composables/api";

export function useIntersection() {
  const { getIntersectionsByTimeRange } = useIntersectionApi();
  const intersections = ref([]);

  const loadIntersections = async (videoId, currentTime) => {
    try {
      const data = await getIntersectionsByTimeRange(
        videoId,
        currentTime,
        currentTime + 10,
      );
      intersections.value = data;
    } catch (error) {
      console.error("교차점 로드 실패:", error);
      intersections.value = [];
    }
  };

  return {
    intersections,
    loadIntersections,
  };
}

