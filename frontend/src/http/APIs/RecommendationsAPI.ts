import { apiAuth } from '../api';


export async function getRecommendations(limit: number, offset: number) {
  return await apiAuth.get(`/recommendations`, {
    params: {
      limit, offset
    }
  });
}