import React from 'react'
import Card from 'antd/es/card'
import ReactECharts from 'echarts-for-react'
import type { TagDistributionItem } from '../types/statistics'

interface TagChartProps {
  data: TagDistributionItem[]
  title?: string
}

const TagChart: React.FC<TagChartProps> = ({
  data,
  title = '标签分布Top 10'
}) => {
  const getOption = () => {
    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: data.map(item => item.tag),
        axisLabel: {
          interval: 0,
          rotate: 45,
          fontSize: 10
        }
      },
      yAxis: {
        type: 'value',
        name: '出现次数'
      },
      series: [
        {
          name: '出现次数',
          type: 'bar',
          data: data.map(item => ({
            value: item.count,
            itemStyle: {
              color: getItemColor(item.tag)
            }
          })),
          label: {
            show: true,
            position: 'top',
            formatter: (params: any) => {
              const idx = params.dataIndex
              return `${data[idx].count}次`
            }
          }
        }
      ]
    }
  }

  const getItemColor = (tag: string): string => {
    if (tag.includes('正面') || tag.includes('积极')) {
      return '#52c41a'
    }
    if (tag.includes('负面') || tag.includes('消极')) {
      return '#ff4d4f'
    }
    if (tag.includes('动力') || tag.includes('性能') || tag.includes('操控')) {
      return '#1890ff'
    }
    if (tag.includes('外观') || tag.includes('内饰') || tag.includes('设计')) {
      return '#722ed1'
    }
    if (tag.includes('空间') || tag.includes('尺寸')) {
      return '#fa8c16'
    }
    if (tag.includes('价格') || tag.includes('性价比')) {
      return '#eb2f96'
    }
    return '#13c2c2'
  }

  return (
    <Card title={title}>
      <ReactECharts
        option={getOption()}
        style={{ height: '400px' }}
        notMerge={true}
        lazyUpdate={true}
      />
    </Card>
  )
}

export default TagChart
