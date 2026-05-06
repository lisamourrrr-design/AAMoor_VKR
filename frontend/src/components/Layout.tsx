import { useEffect, useState } from "react";
import { NavLink, Outlet } from "react-router-dom";

type Theme = "light" | "dark";

export function Layout() {
  const [theme, setTheme] = useState<Theme>(() => {
    const savedTheme = localStorage.getItem("theme");
    return savedTheme === "dark" ? "dark" : "light";
  });

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("theme", theme);
  }, [theme]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="brand">Проект ВКР</div>
          <p className="muted">Многокритериальный анализ</p>
        </div>
        <nav>
          <NavLink to="/">Редактор</NavLink>
          <NavLink to="/history">История</NavLink>
        </nav>
      </aside>
      <main className="content">
        <div className="top-tools">
          <button
            aria-label="Переключить тему"
            className={`theme-toggle ${theme}`}
            onClick={() => setTheme(theme === "light" ? "dark" : "light")}
            type="button"
          >
            <span className="theme-toggle-track">
              <span className="theme-toggle-thumb">{theme === "light" ? "☀" : "☾"}</span>
            </span>
          </button>
        </div>
        <Outlet />
      </main>
    </div>
  );
}
