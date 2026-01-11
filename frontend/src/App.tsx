import { ConfigProvider, Layout, Menu } from 'antd'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import zhCN from 'antd/locale/zh_CN'
import { CommentOutlined, UploadOutlined, BarChartOutlined } from '@ant-design/icons'
import SingleTestPage from './pages/SingleTestPage'
import BatchTestPage from './pages/BatchTestPage'
import StatisticsPage from './pages/StatisticsPage'

const { Header, Content } = Layout

function AppContent() {
  const location = useLocation()

  const menuItems = [
    {
      key: '/single',
      icon: <CommentOutlined />,
      label: <Link to="/single">单条测试</Link>
    },
    {
      key: '/batch',
      icon: <UploadOutlined />,
      label: <Link to="/batch">批量测试</Link>
    },
    {
      key: '/statistics',
      icon: <BarChartOutlined />,
      label: <Link to="/statistics">统计分析</Link>
    }
  ]

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#fff', padding: '0 24px', borderBottom: '1px solid #f0f0f0' }}>
        <div style={{ display: 'flex', alignItems: 'center', height: '64px' }}>
          <div style={{ fontSize: '20px', fontWeight: 'bold', marginRight: '48px' }}>
            用户画像Agent测试系统
          </div>
          <Menu
            mode="horizontal"
            selectedKeys={[location.pathname]}
            items={menuItems}
            style={{ flex: 1, border: 'none' }}
          />
        </div>
      </Header>
      <Content style={{ padding: '24px', background: '#f0f2f5' }}>
        <Routes>
          <Route path="/" element={<SingleTestPage />} />
          <Route path="/single" element={<SingleTestPage />} />
          <Route path="/batch" element={<BatchTestPage />} />
          <Route path="/statistics" element={<StatisticsPage />} />
        </Routes>
      </Content>
    </Layout>
  )
}

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <Router>
        <AppContent />
      </Router>
    </ConfigProvider>
  )
}

export default App
