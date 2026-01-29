import SnakeGame from "./snake/SnakeGame";

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-50 p-6 font-sans text-zinc-900 dark:bg-black dark:text-zinc-50">
      <main className="mx-auto flex w-full max-w-4xl flex-col gap-6">
        <header className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold tracking-tight">Snake</h1>
          <p className="text-sm text-zinc-600 dark:text-zinc-400">
            Use arrow keys or WASD. Space pauses. R restarts.
          </p>
        </header>

        <SnakeGame />
      </main>
    </div>
  );
}
