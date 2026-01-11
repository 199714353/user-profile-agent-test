import React, { useState } from 'react'
import { Card, Space, Alert, Button, Result, Typography } from 'antd'
import { ReloadOutlined } from '@ant-design/icons'
import FileUploader from '../components/FileUploader'
import ProgressBar from '../components/ProgressBar'
import { uploadBatchTest } from '../api/test'

const { Title, Text } = Typography

type TaskStatus = 'idle' | 'uploading' | 'processing' | 'completed' | 'error'

const BatchTestPage: React.FC = () => {
  const [taskId, setTaskId] = useState<number | null>(null)
  const [status, setStatus] = useState<TaskStatus>('idle')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [errorMessage, setErrorMesage] = useState('')

  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
    setStatus('idle')
    setTaskId(null)
    setErrorMesage('')
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      return
    }

    try {
      setStatus('uploading')
      setErrorMesage('')

      const response = await uploadBatchTest(selectedFile)

      setTaskId(response.task_id)
      setStatus('processing')
    } catch (error: any) {
      console.error('上传失败:', error)
      setStatus('error')
      setErrorMesage(error.response?.data?.detail || '上传失败，请重试')
    }
  }

  const handleReset = () => {
    setTaskId(null)
    setStatus('idle')
    setSelectedFile(null)
    setErrorMesate('')
  }

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <Title level={2}>批量评论测试</Title>

      <Space direction="vertical" style={{ width: '100%' }} size="large">
        {/* 错误提示 */}
        {status === 'error' && (
          <Alert
            message="处理失败"
            description={errorMessage}
            type="error"
            showIcon
            closable
            onClose={() => setStatus('idle')}
          />
        )}

        {/* 完成提示 */}
        {status === 'completed' && (
          <Result
            status="success"
            title="批量测试完成"
            subTitle={`任务ID: ${taskId}`}
            extra={[
              <Button type="primary" key="again" onClick={handleReset}>
                测试新文件
              </Button>
            ]}
          />
        )}

        {/* 文件上传组件 */}
        {status !== 'completed' && (
          <Card
            title="上传CSV文件"
            extra={
              selectedFile && status !== 'processing' && (
                <Button
                  type="primary"
                  loading={status === 'uploading'}
                  onClick={handleUpload}
                >
                  开始测试
                </Button>
              )
            }
          >
            <FileUploader
              onFileSelect={handleFileSelect}
              loading={status === 'uploading' || status === 'processing'}
            />
          </Card>
        )}

        {/* 进度条组件 */}
        {taskId && status === 'processing' && (
          <ProgressBar
            taskId={taskId}
            status={status}
            onComplete={() => setStatus('completed')}
          />
        )}

        {/* 操作说明 */}
        {status === 'idle' && (
          <Card title="操作说明">
            <Space direction="vertical">
              <Text>
                1. 点击上传区域或拖拽CSV文件到上传区域
              </Text>
              <Text>
                2. 确认文件后点击"开始测试"按钮
              </Text>
              <Text>
                3. 系统将自动处理评论，实时显示进度
              </Text>
              <Text>
                4. 处理完成后可在历史记录中查看详细结果
              </Text>
            </Space>
          </Card>
        )}
      </Space>
    </div>
  )
}

export default BatchTestPage
