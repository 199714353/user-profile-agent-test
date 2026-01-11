import React from 'react'
import { Card, Tag, Space, Statistic, Row, Col } from 'antd'
import { ClockCircleOutlined, TagsOutlined } from '@ant-design/icons'

interface TagDisplayProps {
  tags: string[]
  processingTime?: number
  confidence?: number
  loading?: boolean
}

const TagDisplay: React.FC<TagDisplayProps> = ({
  tags,
  processingTime = 0,
  confidence = 0,
  loading = false
}) => {
  if (loading) {
    return (
      <Card title="标签结果" loading={loading}>
        <p>正在分析评论，请稍候...</p>
      </Card>
    )
  }

  if (!tags || tags.length === 0) {
    return (
      <Card title="标签结果">
        <p style={{ color: '#999' }}>暂无标签结果</p>
      </Card>
    )
  }

  // 根据标签内容设置颜色
  const getTagColor = (tag: string): string => {
    if (tag.includes('正面')) return 'green'
    if (tag.includes('负面')) return 'red'
    if (tag.includes('中立') || tag.includes('无法判断')) return 'default'
    return 'blue'
  }

  return (
    <Card title="标签结果" extra={<TagsOutlined />}>
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        <div>
          <h4>提取的标签：</h4>
          <Space wrap style={{ marginTop: 8 }}>
            {tags.map((tag, index) => (
              <Tag key={index} color={getTagColor(tag)} style={{ fontSize: 14 }}>
                {tag}
              </Tag>
            ))}
          </Space>
        </div>

        <Row gutter={16}>
          <Col span={12}>
            <Statistic
              title="处理时间"
              value={processingTime}
              suffix="ms"
              prefix={<ClockCircleOutlined />}
              precision={0}
            />
          </Col>
          <Col span={12}>
            <Statistic
              title="标签数量"
              value={tags.length}
              prefix={<TagsOutlined />}
            />
          </Col>
        </Row>
      </Space>
    </Card>
  )
}

export default TagDisplay
