import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, Spin, Alert, Select, Space } from 'antd'
import {
  CommentOutlined,
  TagsOutlined,
  ThunderboltOutlined,
  ClockCircleOutlined
} from '@ant-design/icons'
import TagChart from '../components/TagChart'
import CategoryChart from '../components/CategoryChart'
import { getStatisticsOverview } from '../api/statistics'
import type { StatisticsOverview } from '../types/statistics'

const { Option } = Select

const StatisticsPage: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [statistics, setStatistics] = useState<StatisticsOverview | null>(null)
  const [error, setError] = useState('')
  const [selectedTask, setSelectedTask] = useState<number | undefined>(undefined)

  useEffect(() => {
    loadStatistics()
  }, [selectedTask])

  const loadStatistics = async () => {
    try {
      setLoading(true)
      setError('')
      const data = await getStatisticsOverview(selectedTask)
      setStatistics(data)
    } catch (err: any) {
      console.error('加载统计数据失败:', err)
      setError(err.response?.data?.detail || '加载统计数据失败')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div style={{ padding: '24px', textAlign: 'center' }}>
        <Spin size="large" tip="加载统计数据..." />
      </div>
    )
  }

  if (error) {
    return (
      <div style={{ padding: '24px' }}>
        <Alert
          message="加载失败"
          description={error}
          type="error"
          showIcon
        />
      </div>
    )
  }

  if (!statistics) {
    return null
  }

  return (
    <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        {/* 统计概览卡片 */}
        <Row gutter={16}>
          <Col span={6}>
            <Card>
              <Statistic
                title="总评论数"
                value={statistics.total_comments}
                prefix={<CommentOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="总标签数"
                value={statistics.total_tags}
                prefix={<TagsOutlined />}
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="唯一标签"
                value={statistics.unique_tags}
                prefix={<ThunderboltOutlined />}
                valueStyle={{ color: '#722ed1' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="平均处理时间"
                value={statistics.avg_processing_time}
                suffix="秒"
                precision={2}
                prefix={<ClockCircleOutlined />}
                valueStyle={{ color: '#fa8c16' }}
              />
            </Card>
          </Col>
        </Row>

        {/* 图表展示 */}
        <Row gutter={16}>
          <Col span={24}>
            <TagChart data={statistics.top_tags} />
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={24}>
            <CategoryChart data={statistics.category_distribution} />
          </Col>
        </Row>

        {/* 数据洞察 */}
        {statistics.top_tags.length > 0 && (
          <Card title="数据洞察">
            <Space direction="vertical">
              <p>
                最热门标签是 <strong>{statistics.top_tags[0].tag}</strong>
                ，出现了 <strong>{statistics.top_tags[0].count}</strong> 次
                （占比 {statistics.top_tags[0].percentage}%）
              </p>
              <p>
                共有 <strong>{statistics.unique_tags}</strong> 个不同的标签，
                平均每条评论包含 <strong>{(statistics.total_tags / statistics.total_comments).toFixed(2)}</strong> 个标签
              </p>
              <p>
                正面情感标签占比 {statistics.category_distribution.find(c => c.category === '正面情感')?.percentage || 0}%，
                负面情感标签占比 {statistics.category_distribution.find(c => c.category === '负面情感')?.percentage || 0}%
              </p>
            </Space>
          </Card>
        )}
      </Space>
    </div>
  )
}

export default StatisticsPage
