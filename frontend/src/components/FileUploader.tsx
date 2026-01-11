import React, { useState } from 'react'
import { Upload, Button, Card, Space, Alert, Typography, message } from 'antd'
import { InboxOutlined, UploadOutlined } from '@ant-design/icons'
import type { UploadProps } from 'antd'

const { Text } = Typography
const { Dragger } = Upload

interface FileUploaderProps {
  onFileSelect: (file: File) => void
  loading?: boolean
}

const FileUploader: React.FC<FileUploaderProps> = ({
  onFileSelect,
  loading = false
}) => {
  const [fileList, setFileList] = useState<any[]>([])

  const props: UploadProps = {
    name: 'file',
    multiple: false,
    fileList: fileList,
    accept: '.csv',
    beforeUpload: (file) => {
      // 验证文件类型
      const isCSV = file.name.toLowerCase().endsWith('.csv')
      if (!isCSV) {
        message.error('只支持CSV文件格式！')
        return false
      }

      // 验证文件大小（10MB）
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        message.error('文件大小不能超过10MB！')
        return false
      }

      setFileList([file])
      onFileSelect(file)
      return false // 阻止自动上传
    },
    onRemove: () => {
      setFileList([])
    }
  }

  const handleClear = () => {
    setFileList([])
  }

  return (
    <Card title="上传CSV文件">
      <Space direction="vertical" style={{ width: '100%' }}>
        <Alert
          message="文件格式要求"
          description="CSV文件，需包含评论列（支持的列名：评论、comment、content、text、pinglun等），最多1000条评论"
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
        />

        <Dragger {...props} disabled={loading}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
          <p className="ant-upload-hint">
            支持单次上传，文件大小不超过10MB
          </p>
        </Dragger>

        {fileList.length > 0 && (
          <Space style={{ marginTop: 16 }}>
            <Text strong>已选择:</Text>
            <Text>{fileList[0].name}</Text>
            <Text type="secondary">({(fileList[0].size / 1024).toFixed(2)} KB)</Text>
            <Button
              size="small"
              danger
              onClick={handleClear}
              disabled={loading}
            >
              清除
            </Button>
          </Space>
        )}
      </Space>
    </Card>
  )
}

export default FileUploader
