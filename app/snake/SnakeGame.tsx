"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

type Vec2 = { x: number; y: number };

type Direction = "up" | "down" | "left" | "right";

type GameStatus = "ready" | "running" | "paused" | "gameover";

const DIR_VEC: Record<Direction, Vec2> = {
  up: { x: 0, y: -1 },
  down: { x: 0, y: 1 },
  left: { x: -1, y: 0 },
  right: { x: 1, y: 0 },
};

function add(a: Vec2, b: Vec2): Vec2 {
  return { x: a.x + b.x, y: a.y + b.y };
}

function eq(a: Vec2, b: Vec2): boolean {
  return a.x === b.x && a.y === b.y;
}

function wrap(p: Vec2, w: number, h: number): Vec2 {
  return {
    x: (p.x + w) % w,
    y: (p.y + h) % h,
  };
}

function isOpposite(a: Direction, b: Direction): boolean {
  return (
    (a === "up" && b === "down") ||
    (a === "down" && b === "up") ||
    (a === "left" && b === "right") ||
    (a === "right" && b === "left")
  );
}

function randInt(maxExclusive: number): number {
  return Math.floor(Math.random() * maxExclusive);
}

function placeFood(gridW: number, gridH: number, snake: Vec2[]): Vec2 {
  const occupied = new Set(snake.map((s) => `${s.x},${s.y}`));
  const free: Vec2[] = [];
  for (let y = 0; y < gridH; y++) {
    for (let x = 0; x < gridW; x++) {
      const key = `${x},${y}`;
      if (!occupied.has(key)) free.push({ x, y });
    }
  }
  if (free.length === 0) return { x: 0, y: 0 };
  return free[randInt(free.length)];
}

const DEFAULT_GRID_W = 24;
const DEFAULT_GRID_H = 18;
const DEFAULT_TICK_MS = 110;

export default function SnakeGame() {
  const [gridW] = useState(DEFAULT_GRID_W);
  const [gridH] = useState(DEFAULT_GRID_H);

  const initialSnake = useMemo<Vec2[]>(
    () => [
      { x: Math.floor(gridW / 2), y: Math.floor(gridH / 2) },
      { x: Math.floor(gridW / 2) - 1, y: Math.floor(gridH / 2) },
      { x: Math.floor(gridW / 2) - 2, y: Math.floor(gridH / 2) },
    ],
    [gridW, gridH],
  );

  const [snake, setSnake] = useState<Vec2[]>(initialSnake);
  const [dir, setDir] = useState<Direction>("right");
  const [nextDir, setNextDir] = useState<Direction>("right");
  const [food, setFood] = useState<Vec2>(() => placeFood(gridW, gridH, initialSnake));
  const [status, setStatus] = useState<GameStatus>("ready");
  const [score, setScore] = useState(0);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const statusRef = useRef<GameStatus>(status);
  const nextDirRef = useRef<Direction>(nextDir);
  const dirRef = useRef<Direction>(dir);
  const snakeRef = useRef<Vec2[]>(snake);
  const foodRef = useRef<Vec2>(food);

  useEffect(() => {
    statusRef.current = status;
  }, [status]);

  useEffect(() => {
    nextDirRef.current = nextDir;
  }, [nextDir]);

  useEffect(() => {
    dirRef.current = dir;
  }, [dir]);

  useEffect(() => {
    snakeRef.current = snake;
  }, [snake]);

  useEffect(() => {
    foodRef.current = food;
  }, [food]);

  const reset = useCallback(() => {
    const s = initialSnake;
    setSnake(s);
    setDir("right");
    setNextDir("right");
    setFood(placeFood(gridW, gridH, s));
    setScore(0);
    setStatus("ready");
  }, [gridH, gridW, initialSnake]);

  const togglePause = useCallback(() => {
    setStatus((prev) => {
      if (prev === "running") return "paused";
      if (prev === "paused") return "running";
      return prev;
    });
  }, []);

  const start = useCallback(() => {
    setStatus((prev) => (prev === "ready" ? "running" : prev));
  }, []);

  const requestDirection = useCallback((d: Direction) => {
    const current = dirRef.current;
    if (isOpposite(current, d)) return;
    setNextDir(d);
    start();
  }, [start]);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === " " || e.code === "Space") {
        e.preventDefault();
        togglePause();
        return;
      }
      if (e.key === "r" || e.key === "R") {
        reset();
        return;
      }

      switch (e.key) {
        case "ArrowUp":
        case "w":
        case "W":
          e.preventDefault();
          requestDirection("up");
          break;
        case "ArrowDown":
        case "s":
        case "S":
          e.preventDefault();
          requestDirection("down");
          break;
        case "ArrowLeft":
        case "a":
        case "A":
          e.preventDefault();
          requestDirection("left");
          break;
        case "ArrowRight":
        case "d":
        case "D":
          e.preventDefault();
          requestDirection("right");
          break;
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [requestDirection, reset, togglePause]);

  useEffect(() => {
    if (status !== "running") return;

    const id = window.setInterval(() => {
      if (statusRef.current !== "running") return;

      const nd = nextDirRef.current;
      const cd = dirRef.current;
      if (!isOpposite(cd, nd)) {
        dirRef.current = nd;
        setDir(nd);
      }

      const currentSnake = snakeRef.current;
      const head = currentSnake[0];
      const nextHead = wrap(add(head, DIR_VEC[dirRef.current]), gridW, gridH);

      const willHitSelf = currentSnake.some((seg) => eq(seg, nextHead));
      if (willHitSelf) {
        setStatus("gameover");
        return;
      }

      const willEat = eq(nextHead, foodRef.current);

      const nextSnake = [nextHead, ...currentSnake];
      if (!willEat) nextSnake.pop();

      snakeRef.current = nextSnake;
      setSnake(nextSnake);

      if (willEat) {
        setScore((s) => s + 1);
        const newFood = placeFood(gridW, gridH, nextSnake);
        foodRef.current = newFood;
        setFood(newFood);
      }
    }, DEFAULT_TICK_MS);

    return () => window.clearInterval(id);
  }, [gridH, gridW, status]);

  const cellSize = 24;
  const canvasW = gridW * cellSize;
  const canvasH = gridH * cellSize;

  const palette = useMemo(
    () => ({
      bg: "#0b1220",
      grid: "rgba(255,255,255,0.05)",
      snakeHead: "#34d399",
      snakeBody: "#10b981",
      food: "#fb7185",
      text: "rgba(255,255,255,0.85)",
    }),
    [],
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = Math.max(1, Math.floor(window.devicePixelRatio || 1));
    canvas.width = canvasW * dpr;
    canvas.height = canvasH * dpr;
    canvas.style.width = `${canvasW}px`;
    canvas.style.height = `${canvasH}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    ctx.fillStyle = palette.bg;
    ctx.fillRect(0, 0, canvasW, canvasH);

    ctx.strokeStyle = palette.grid;
    ctx.lineWidth = 1;
    for (let x = 0; x <= gridW; x++) {
      ctx.beginPath();
      ctx.moveTo(x * cellSize + 0.5, 0);
      ctx.lineTo(x * cellSize + 0.5, canvasH);
      ctx.stroke();
    }
    for (let y = 0; y <= gridH; y++) {
      ctx.beginPath();
      ctx.moveTo(0, y * cellSize + 0.5);
      ctx.lineTo(canvasW, y * cellSize + 0.5);
      ctx.stroke();
    }

    const drawCell = (p: Vec2, fill: string, inset = 2) => {
      ctx.fillStyle = fill;
      ctx.fillRect(
        p.x * cellSize + inset,
        p.y * cellSize + inset,
        cellSize - inset * 2,
        cellSize - inset * 2,
      );
    };

    drawCell(food, palette.food, 5);

    snake.forEach((seg, idx) => {
      drawCell(seg, idx === 0 ? palette.snakeHead : palette.snakeBody, idx === 0 ? 3 : 4);
    });

    if (status !== "running") {
      ctx.fillStyle = "rgba(0,0,0,0.45)";
      ctx.fillRect(0, 0, canvasW, canvasH);

      ctx.fillStyle = palette.text;
      ctx.font = "600 18px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      const lines: string[] = [];
      if (status === "ready") lines.push("Press an arrow key / WASD to start");
      if (status === "paused") lines.push("Paused (Space to resume)");
      if (status === "gameover") lines.push("Game Over (R to restart)");

      lines.forEach((line, i) => {
        ctx.fillText(line, canvasW / 2, canvasH / 2 + i * 24);
      });
    }
  }, [canvasH, canvasW, cellSize, food, gridH, gridW, palette, snake, status]);

  const statusLabel =
    status === "ready"
      ? "Ready"
      : status === "running"
        ? "Running"
        : status === "paused"
          ? "Paused"
          : "Game Over";

  return (
    <section className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-4">
          <div className="text-sm">
            <span className="font-medium">Score:</span> {score}
          </div>
          <div className="text-sm text-zinc-600 dark:text-zinc-400">
            <span className="font-medium text-zinc-900 dark:text-zinc-50">Status:</span> {statusLabel}
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            className="rounded-md bg-zinc-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-zinc-800 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
            onClick={() => setStatus((s) => (s === "running" ? "paused" : "running"))}
            disabled={status === "gameover"}
          >
            {status === "running" ? "Pause" : "Play"}
          </button>
          <button
            type="button"
            className="rounded-md border border-zinc-300 bg-white px-3 py-1.5 text-sm font-medium text-zinc-900 hover:bg-zinc-50 dark:border-zinc-700 dark:bg-black dark:text-zinc-50 dark:hover:bg-zinc-900"
            onClick={reset}
          >
            Restart
          </button>
        </div>
      </div>

      <div className="w-full overflow-auto rounded-xl border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-black">
        <div className="flex w-full justify-center">
          <canvas ref={canvasRef} className="rounded-lg" />
        </div>
      </div>

      <div className="text-xs text-zinc-600 dark:text-zinc-400">
        Wrap-around edges are enabled. Avoid running into yourself.
      </div>
    </section>
  );
}
