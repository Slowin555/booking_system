import { z } from 'zod'

export const BookingSchema = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  serviceId: z.string().uuid(),
  startTime: z.date(),
  endTime: z.date(),
  status: z.enum(['pending', 'confirmed', 'cancelled', 'completed']),
  notes: z.string().optional(),
  createdAt: z.date(),
  updatedAt: z.date(),
})

export const CreateBookingSchema = z.object({
  serviceId: z.string().uuid(),
  startTime: z.date(),
  endTime: z.date(),
  notes: z.string().optional(),
})

export const UpdateBookingSchema = z.object({
  startTime: z.date().optional(),
  endTime: z.date().optional(),
  status: z.enum(['pending', 'confirmed', 'cancelled', 'completed']).optional(),
  notes: z.string().optional(),
})

export const ServiceSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  duration: z.number().positive(), // in minutes
  price: z.number().positive(),
  isActive: z.boolean(),
  createdAt: z.date(),
  updatedAt: z.date(),
})

export const CreateServiceSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  duration: z.number().positive(),
  price: z.number().positive(),
})

export const UpdateServiceSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  description: z.string().optional(),
  duration: z.number().positive().optional(),
  price: z.number().positive().optional(),
  isActive: z.boolean().optional(),
})

export type Booking = z.infer<typeof BookingSchema>
export type CreateBooking = z.infer<typeof CreateBookingSchema>
export type UpdateBooking = z.infer<typeof UpdateBookingSchema>
export type Service = z.infer<typeof ServiceSchema>
export type CreateService = z.infer<typeof CreateServiceSchema>
export type UpdateService = z.infer<typeof UpdateServiceSchema>
