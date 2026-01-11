// 统计分析相关类型
export interface TagDistributionItem {
  tag: string
  count: number
  percentage: number
}

export interface CategoryDistributionItem {
  category: string
  count: number
  percentage: number
}

export interface StatisticsOverview {
  total_comments: number
  total_tags: number
  unique_tags: number
  avg_confidence: number
  avg_processing_time: number
  top_tags: TagDistributionItem[]
  category_distribution: CategoryDistributionItem[]
}
