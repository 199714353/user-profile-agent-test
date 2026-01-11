import React from 'react'
import Card from 'antd/es/card'
import ReactECharts from 'echarts-for-react'
import type { CategoryDistributionItem } from '../types/statistics'

interface CategoryChartProps {
  data: CategoryDistributionItem[]
  title?: string
}

const CategoryChart: React.FC<CategoryChartProps> = ({
  data,
  title = '标签分类分布'
}) => {
  const getOption = () => {
    return {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        top: 'middle',
        textStyle: {
          fontSize: 12
        }
      },
      series: [
        {
          name: '标签分类',
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['60%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 20,
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: data.map(item => ({
            value: item.count,
            name: item.category,
            itemStyle: {
              color: getCategoryColor(item.category)
            }
          }))
        }
      ]
    }
  }

  const getCategoryColor = (category: string): string => {
    const colorMap: Record<string, string> = {
      '正面情感': '#52c41a',
      '负面情感': '#ff4d4f',
      '产品性能': '#1890ff',
      '外观设计': '#722ed1',
      '空间尺寸': '#fa8c16',
      '价格性价比': '#eb2f96',
      '服务售后': '#13c2c2',
      '品牌口碑': '#fadb14',
      '其他': '#d9d9d9'
    }
    return colorMap[category] || '#8c8c8c'
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

export default CategoryChart
