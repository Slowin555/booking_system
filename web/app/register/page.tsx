import RegisterForm from '@/components/RegisterForm'

export default function RegisterPage() {
  return (
    <main className="flex min-h-screen items-center justify-center p-8">
      <div className="max-w-md w-full space-y-6">
        <h1 className="text-3xl font-bold text-center">Register</h1>
        <RegisterForm />
      </div>
    </main>
  )
}


