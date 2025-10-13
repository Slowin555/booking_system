// Export all schemas
export * from './userSchema'
export * from './bookingSchema'

// Common response schemas
import { z } from 'zod'

export const ApiResponseSchema = z.object({
  success: z.boolean(),
  message: z.string().optional(),
  data: z.any().optional(),
  error: z.string().optional(),
})

export const PaginationSchema = z.object({
  page: z.number().positive(),
  limit: z.number().positive().max(100),
  total: z.number().nonnegative(),
  totalPages: z.number().nonnegative(),
})

export const PaginatedResponseSchema = z.object({
  data: z.array(z.any()),
  pagination: PaginationSchema,
})

export type ApiResponse = z.infer<typeof ApiResponseSchema>
export type Pagination = z.infer<typeof PaginationSchema>
export type PaginatedResponse = z.infer<typeof PaginatedResponseSchema>
