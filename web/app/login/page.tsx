import LoginForm from '@/components/LoginForm'

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center p-8">
      <div className="max-w-md w-full space-y-6">
        <h1 className="text-3xl font-bold text-center">Login</h1>
        <LoginForm />
      </div>
    </main>
  )
}


