"use client"

import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { api } from '@/lib/api'
import { useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

type FormValues = z.infer<typeof schema>

export default function LoginForm() {
  const qc = useQueryClient()
  const [error, setError] = useState<string | null>(null)
  const { register, handleSubmit, formState: { isSubmitting } } = useForm<FormValues>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: FormValues) => {
    setError(null)
    try {
      await api.post('/auth/login', data)
      await qc.invalidateQueries({ queryKey: ['me'] })
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label className="block text-sm font-medium">Email</label>
        <input className="mt-1 w-full border rounded px-3 py-2" type="email" {...register('email')} />
      </div>
      <div>
        <label className="block text-sm font-medium">Password</label>
        <input className="mt-1 w-full border rounded px-3 py-2" type="password" {...register('password')} />
      </div>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <button disabled={isSubmitting} className="rounded bg-black text-white px-4 py-2 disabled:opacity-50">Login</button>
    </form>
  )
}


