import React, { useState } from 'react'
import { TextArea, Button, Space, Card } from 'antd'
import { ClearOutlined } from '@ant-design/icons'

interface CommentInputProps {
  value: string
  onChange: (value: string) => void
  onTest: () => void
  loading?: boolean
  placeholder?: string
}

const CommentInput: React.FC<CommentInputProps> = ({
  value,
  onChange,
  onTest,
  loading = false,
  placeholder = '请输入汽车用户评论...'
}) => {
  const [inputValue, setInputValue] = useState(value)

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value)
    onChange(e.target.value)
  }

  const handleClear = () => {
    setInputValue('')
    onChange('')
  }

  const handleTest = () => {
    if (inputValue.trim()) {
      onTest()
    }
  }

  return (
    <Card title="输入评论" style={{ marginBottom: 16 }}>
      <Space direction="vertical" style={{ width: '100%' }}>
        <TextArea
          value={inputValue}
          onChange={handleChange}
          placeholder={placeholder}
          rows={4}
          maxLength={5000}
          showCount
          allowClear
        />
        <Space>
          <Button
            type="primary"
            onClick={handleTest}
            loading={loading}
            disabled={!inputValue.trim()}
            size="large"
          >
            开始测试
          </Button>
          <Button
            icon={<ClearOutlined />}
            onClick={handleClear}
            disabled={loading || !inputValue}
          >
            清空
          </Button>
        </Space>
      </Space>
    </Card>
  )
}

export default CommentInput
