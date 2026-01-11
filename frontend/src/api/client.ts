import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 60000, // 60秒超时
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 可以在这里添加token等
    console.log('API请求:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    console.log('API响应:', response.status, response.config.url)
    return response.data
  },
  (error) => {
    console.error('响应错误:', error.response?.data || error.message)

    // 统一错误处理
    if (error.response?.status === 401) {
      console.error('未授权，请重新登录')
    } else if (error.response?.status === 500) {
      console.error('服务器内部错误')
    } else if (error.response?.status === 422) {
      console.error('请求参数验证失败')
    }

    return Promise.reject(error)
  }
)

export default apiClient
