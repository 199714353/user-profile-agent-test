import React, { useState } from 'react'
import { Layout, message, Card, Alert } from 'antd'
import CommentInput from '../components/CommentInput'
import TagDisplay from '../components/TagDisplay'
import { testSingleComment } from '../api/test'
import type { TagResult } from '../types/test'

const { Content, Header } = Layout

const SingleTestPage: React.FC = () => {
  const [comment, setComment] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<TagResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [taskId, setTaskId] = useState<number | null>(null)

  const handleTest = async () => {
    if (!comment.trim()) {
      message.warning('请输入评论内容')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await testSingleComment(comment)

      console.log('测试结果:', response)

      setTaskId(response.task_id)

      if (response.result) {
        setResult(response.result)
        message.success('标签提取成功！')
      } else if (response.status === 'failed') {
        setError('标签提取失败，请稍后重试')
        message.error('标签提取失败')
      }
    } catch (err: any) {
      console.error('测试失败:', err)

      const errorMessage = err.response?.data?.detail || err.message || '未知错误'
      setError(errorMessage)
      message.error(`测试失败: ${errorMessage}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#001529', padding: '0 50px' }}>
        <h1 style={{ color: '#fff', lineHeight: '64px', margin: 0 }}>
          用户画像Agent测试系统 - 单条评论测试
        </h1>
      </Header>

      <Content style={{ padding: '50px', background: '#f0f2f5' }}>
        <div style={{ maxWidth: 1000, margin: '0 auto' }}>
          <Card style={{ marginBottom: 16 }}>
            <Alert
              message="功能说明"
              description="输入汽车用户评论，系统将自动分析并提取标签（如：动力性能、油耗、外观、内饰等维度，以及正面/负面/中立等情感倾向）"
              type="info"
              showIcon
              style={{ marginBottom: 16 }}
            />

            <CommentInput
              value={comment}
              onChange={setComment}
              onTest={handleTest}
              loading={loading}
            />

            {error && (
              <Alert
                message="测试失败"
                description={error}
                type="error"
                showIcon
                closable
                style={{ marginBottom: 16 }}
                onClose={() => setError(null)}
              />
            )}

            {result && (
              <TagDisplay
                tags={result.tags}
                processingTime={result.processing_time}
                confidence={result.confidence}
              />
            )}

            {taskId && (
              <Alert
                message="任务已创建"
                description={`任务ID: ${taskId}`}
                type="success"
                showIcon
                style={{ marginTop: 16 }}
              />
            )}
          </Card>
        </div>
      </Content>
    </Layout>
  )
}

export default SingleTestPage
