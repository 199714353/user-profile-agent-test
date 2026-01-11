// 批量测试相关类型
export interface BatchUploadResponse {
  task_id: number
  status: string
  total_count: number
  message: string
}

export interface BatchProgressResponse {
  task_id: number
  status: string
  total_count: number
  processed_count: number
  progress: number
  error_message?: string
}

export interface UploadFile {
  file: File
  filename: string
  size: number
}
