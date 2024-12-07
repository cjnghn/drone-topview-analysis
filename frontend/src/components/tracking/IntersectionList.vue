// components/tracking/IntersectionList.vue
<template>
  <div v-if="intersections.length > 0" class="p-4 border-t">
    <h3 class="text-lg font-semibold mb-4">최근 교차점</h3>
    <div class="overflow-y-auto max-h-[200px]">
      <div class="space-y-2">
        <div
          v-for="intersection in intersections"
          :key="intersection.id"
          class="p-3 border rounded"
        >
          <div class="font-medium">
            Track {{ intersection.track1 }} ↔ {{ intersection.track2 }}
          </div>
          <div class="text-sm text-gray-600">
            <div>
              시간:
              {{ formatDuration(intersection.timestamp - videoStartTime) }}
            </div>
            <div>거리차: {{ intersection.time_difference.toFixed(2) }}s</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatDuration } from "@/utils/time";

defineProps({
  intersections: {
    type: Array,
    default: () => [],
  },
  videoStartTime: Number,
});
</script>
