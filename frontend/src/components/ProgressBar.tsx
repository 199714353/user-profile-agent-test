import React, { useEffect, useState } from 'react'
import { Card, Progress, Statistic, Row, Col, Tag, Space, Alert } from 'antd'
import {
  ClockCircleOutlined,
  CheckCircleOutlined,
  LoadingOutlined,
  SyncOutlined
} from '@ant-design/icons'
import type { BatchProgressResponse } from '../types/batch'

interface ProgressBarProps {
  taskId: number | null
  status?: 'idle' | 'uploading' | 'processing' | 'completed' | 'error'
  onComplete?: () => void
}

const ProgressBar: React.FC<ProgressBarProps> = ({
  taskId,
  status = 'idle',
  onComplete
}) => {
  const [progress, setProgress] = useState<BatchProgressResponse | null>(null)
  const [polling, setPolling] = useState(false)

  // 轮询进度
  useEffect(() => {
    if (taskId && status === 'processing') {
      setPolling(true)
      pollProgress()

      return () => {
        setPolling(false)
      }
    }
  }, [taskId, status])

  const pollProgress = async () => {
    if (!taskId) return

    try {
      const { getBatchProgress } = await import('../api/test')
      const result = await getBatchProgress(taskId)

      setProgress(result)

      // 如果已完成，通知父组件
      if (result.status === 'completed' && onComplete) {
        onComplete()
        return
      }

      // 如果未完成，继续轮询
      if (result.status === 'processing' && polling) {
        setTimeout(() => {
          pollProgress()
        }, 1000) // 每秒查询一次
      }
    } catch (error) {
      console.error('查询进度失败:', error)
    }
  }

  if (!progress || status === 'idle') {
    return null
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'processing':
        return 'processing'
      case 'completed':
        return 'success'
      case 'failed':
        return 'error'
      default:
        return 'default'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'processing':
        return '处理中...'
      case 'completed':
        return '已完成'
      case 'failed':
        return '处理失败'
      case 'pending':
        return '等待中'
      default:
        return status
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'processing':
        return <LoadingOutlined spin />
      case 'completed':
        return <CheckCircleOutlined />
      case 'failed':
        return <ClockCircleOutlined />
      default:
        return <SyncOutlined />
    }
  }

  return (
    <Card
      title="处理进度"
      extra={
        <Space>
          <Tag icon={getStatusIcon(progress.status)} color={getStatusColor(progress.status)}>
            {getStatusText(progress.status)}
          </Tag>
        </Space>
      }
    >
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        <Progress
          percent={progress.progress}
          status={progress.status === 'processing' ? 'active' : undefined}
          strokeColor={{
            '0%': '#108ee9',
            '100%': '#87d068',
          }}
        />

        <Row gutter={16}>
          <Col span={8}>
            <Statistic
              title="已处理"
              value={progress.processed_count}
              suffix={`/ ${progress.total_count}`}
            />
          </Col>
          <Col span={8}>
            <Statistic
              title="进度"
              value={progress.progress}
              suffix="%"
              precision={1}
            />
          </Col>
          <Col span={8}>
            <Statistic
              title="剩余"
              value={progress.total_count - progress.processed_count}
            />
          </Col>
        </Row>

        {progress.error_message && (
          <Alert
            message="处理错误"
            description={progress.error_message}
            type="error"
            showIcon
            style={{ marginTop: 16 }}
          />
        )}
      </Space>
    </Card>
  )
}

export default ProgressBar
