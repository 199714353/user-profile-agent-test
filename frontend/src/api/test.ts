import apiClient from './client'
import type { BatchUploadResponse, BatchProgressResponse } from '../types/batch'

// 类型定义
export interface SingleTestRequest {
  comment: string
}

export interface TagResult {
  tags: string[]
  confidence: number
  processing_time: number
}

export interface SingleTestResponse {
  task_id: number
  status: string
  result: TagResult | null
}

export interface TaskDetail {
  task: {
    id: number
    task_type: string
    status: string
    total_count: number
    processed_count: number
    created_at: string
    completed_at: string | null
    error_message?: string
  }
  records: Array<{
    id: number
    task_id: number
    comment_text: string
    tags: string[]
    confidence: number | null
    processing_time: number | null
    created_at: string
  }>
}

/**
 * 单条评论测试API
 */
export const testSingleComment = async (comment: string): Promise<SingleTestResponse> => {
  const response = await apiClient.post<SingleTestResponse>('/test/single', {
    comment
  })
  return response
}

/**
 * 获取任务详情API
 */
export const getTaskDetail = async (taskId: number): Promise<TaskDetail> => {
  const response = await apiClient.get<TaskDetail>(`/test/task/${taskId}`)
  return response
}

/**
 * 批量测试上传API
 */
export const uploadBatchTest = async (file: File): Promise<BatchUploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post<BatchUploadResponse>(
    '/test/batch/upload',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
  )
  return response
}

/**
 * 批量测试进度查询API
 */
export const getBatchProgress = async (taskId: number): Promise<BatchProgressResponse> => {
  const response = await apiClient.get<BatchProgressResponse>(
    `/test/batch/progress/${taskId}`
  )
  return response
}
