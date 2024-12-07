// components/tracking/TrackingList.vue
<template>
  <div class="p-4 flex flex-col flex-grow overflow-hidden">
    <h3 class="text-lg font-semibold mb-4">현재 추적 객체</h3>
    <div class="overflow-y-auto flex-grow">
      <div v-if="tracks.length === 0" class="text-gray-500">
        추적 중인 객체가 없습니다
      </div>
      <div class="space-y-2">
        <div v-for="track in tracks" :key="track.tracking_id"
          class="p-3 border rounded cursor-pointer transition-colors" :class="{
            'bg-blue-50 border-blue-200': selectedTrack === track.tracking_id,
            'hover:bg-gray-50': selectedTrack !== track.tracking_id,
          }" @click="$emit('select', track.tracking_id)">
          <div class="font-medium">
            ID: {{ track.tracking_id }}
            <span class="ml-2 px-2 py-0.5 rounded text-sm text-white" :style="{
              backgroundColor: classColors[track.class_id] || '#999',
            }">
              Class {{ track.class_id }}
            </span>
          </div>
          <div class="text-sm text-gray-600">
            <div>속도: {{ track.last_speed.toFixed(1) }} m/s</div>
            <div>
              좌표: [{{ track.last_latitude.toFixed(5) }},
              {{ track.last_longitude.toFixed(5) }}]
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { classColors } from "@/constants/colors";

defineProps({
  tracks: {
    type: Array,
    default: () => [],
  },
  selectedTrack: Number,
});

defineEmits(["select"]);
</script>
