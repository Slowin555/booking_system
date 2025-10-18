import axios from 'axios'

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  withCredentials: true,
})

// Simple 401 interceptor that tries to refresh once
let isRefreshing = false
let pending: Array<() => void> = []

api.interceptors.response.use(
  r => r,
  async (error) => {
    const { response, config } = error || {}
    if (response?.status === 401 && !config.__isRetry) {
      if (isRefreshing) {
        await new Promise<void>(resolve => pending.push(resolve))
      } else {
        isRefreshing = true
        try {
          await api.post('/auth/refresh')
          pending.forEach(fn => fn())
          pending = []
        } catch {
          pending = []
          throw error
        } finally {
          isRefreshing = false
        }
      }
      config.__isRetry = true
      return api(config)
    }
    return Promise.reject(error)
  },
)


