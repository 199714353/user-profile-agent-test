// 通用类型
export interface ApiResponse<T> {
  data: T
  message?: string
  code?: number
}

// 测试相关类型
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

export interface TaskRecord {
  id: number
  task_id: number
  comment_text: string
  tags: string[]
  confidence: number | null
  processing_time: number | null
  created_at: string
}

export interface TaskInfo {
  id: number
  task_type: string
  status: string
  total_count: number
  processed_count: number
  created_at: string
  completed_at: string | null
  error_message?: string
}

export interface TaskDetail {
  task: TaskInfo
  records: TaskRecord[]
}
