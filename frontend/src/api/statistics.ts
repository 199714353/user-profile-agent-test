import apiClient from './client'
import type { StatisticsOverview } from '../types/statistics'

/**
 * 获取统计概览API
 */
export const getStatisticsOverview = async (taskId?: number): Promise<StatisticsOverview> => {
  const params = taskId ? `?task_id=${taskId}` : ''
  const response = await apiClient.get<StatisticsOverview>(
    `/statistics/overview${params}`
  )
  return response
}
