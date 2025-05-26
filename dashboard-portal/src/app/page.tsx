import Link  from "next/link";
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <main className="flex flex-col min-h-screen justify-center h-full text-center gap-6 max-w-5xl mx-auto">
      <h1 className="text-5xl font-bold">
        Investor Portal
      </h1>
      <p>
        <Button className="bg-blue-500" asChild>
          <Link href="/dashboard">
            Welcome
          </Link>
        </Button>
      </p>
    </main>

  );
}
