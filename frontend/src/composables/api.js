// composables/api.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// API 응답에 대한 공통 에러 핸들링
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export function useVideoApi() {
  const getVideos = async () => {
    try {
      const response = await apiClient.get('videos/');
      return response.data;
    } catch (error) {
      console.error('비디오 목록 조회 실패:', error);
      throw error;
    }
  };

  const getTrackPositions = async (videoId, timestamp) => {
    try {
      const response = await apiClient.get(`videos/${videoId}/track_positions/`, {
        params: { timestamp }
      });
      return response.data;
    } catch (error) {
      console.error('트래킹 위치 조회 실패:', error);
      throw error;
    }
  };

  const getVideoStatistics = async (videoId) => {
    try {
      const response = await apiClient.get(`videos/${videoId}/statistics/`);
      return response.data;
    } catch (error) {
      console.error('비디오 통계 조회 실패:', error);
      throw error;
    }
  };

  return {
    getVideos,
    getTrackPositions,
    getVideoStatistics,
  };
}

export function useTrackingApi() {
  const getTrajectory = async (trackId) => {
    try {
      const response = await apiClient.get(`tracking/${trackId}/trajectory/`);
      return response.data;
    } catch (error) {
      console.error('궤적 조회 실패:', error);
      throw error;
    }
  };

  const getTrackingDetails = async (trackId) => {
    try {
      const response = await apiClient.get(`tracking/${trackId}/`);
      return response.data;
    } catch (error) {
      console.error('트래킹 상세 정보 조회 실패:', error);
      throw error;
    }
  };

  return {
    getTrajectory,
    getTrackingDetails,
  };
}

export function useIntersectionApi() {
  const getIntersectionsByTimeRange = async (videoId, startTime, endTime) => {
    try {
      const response = await apiClient.get('intersections/time_range/', {
        params: {
          video_id: videoId,
          start_time: startTime,
          end_time: endTime
        }
      });
      return response.data;
    } catch (error) {
      console.error('교차점 조회 실패:', error);
      throw error;
    }
  };

  const getIntersectionDetails = async (intersectionId) => {
    try {
      const response = await apiClient.get(`intersections/${intersectionId}/`);
      return response.data;
    } catch (error) {
      console.error('교차점 상세 정보 조회 실패:', error);
      throw error;
    }
  };

  return {
    getIntersectionsByTimeRange,
    getIntersectionDetails,
  };
}

export function useFrameApi() {
  const getFrameDetections = async (frameId) => {
    try {
      const response = await apiClient.get(`frames/${frameId}/detections/`);
      return response.data;
    } catch (error) {
      console.error('프레임 검출 정보 조회 실패:', error);
      throw error;
    }
  };

  return {
    getFrameDetections,
  };
}

// API 환경 설정을 위한 유틸리티 함수
export function configureApi(config) {
  if (config.baseURL) {
    apiClient.defaults.baseURL = config.baseURL;
  }

  if (config.headers) {
    apiClient.defaults.headers = {
      ...apiClient.defaults.headers,
      ...config.headers,
    };
  }

  if (config.timeout) {
    apiClient.defaults.timeout = config.timeout;
  }
}

// 선택적: 개발 환경에서 API 요청/응답 로깅
if (process.env.NODE_ENV === 'development') {
  apiClient.interceptors.request.use(request => {
    console.log('Starting Request:', request);
    return request;
  });

  apiClient.interceptors.response.use(response => {
    console.log('Response:', response);
    return response;
  });
}