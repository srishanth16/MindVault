"use client";

import { useAuth } from "@/components/AuthProvider";
import { useTheme } from "@/components/ThemeProvider";

export function Navbar() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header
      className="hidden md:flex justify-between items-center h-[40px] px-6 fixed top-0 right-0 z-40"
      style={{
        width: "calc(100% - 280px)",
        background: theme === "dark" ? "rgba(11, 19, 38, 0.6)" : "rgba(248, 249, 255, 0.6)",
        backdropFilter: "blur(12px)",
        WebkitBackdropFilter: "blur(12px)",
        borderBottom: "1px solid var(--glass-border)",
      }}
    >
      {/* Search */}
      <div className="flex-1 max-w-md">
        <div className="relative group cursor-text">
          <div className="absolute inset-y-0 left-0 pl-2 flex items-center pointer-events-none">
            <span className="material-symbols-outlined text-[18px]" style={{ color: "var(--outline)" }}>
              search
            </span>
          </div>
          <input
            type="text"
            placeholder="Search across your brain... (Cmd+K)"
            className="block w-full pl-8 pr-3 py-1.5 rounded-lg text-sm transition-all focus:outline-none focus:ring-2"
            style={{
              background: "var(--surface-container-high)",
              opacity: 0.5,
              border: "1px solid var(--glass-border)",
              color: "var(--on-surface)",
              fontSize: "13px",
            }}
          />
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-4">
        {/* Theme toggle */}
        <button
          onClick={toggleTheme}
          className="p-1.5 rounded-full transition-all hover:opacity-80"
          style={{ color: "var(--on-surface-variant)" }}
          title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
        >
          <span className="material-symbols-outlined text-[20px]">
            {theme === "dark" ? "light_mode" : "dark_mode"}
          </span>
        </button>

        {/* Notifications */}
        <button
          className="p-1.5 rounded-full transition-all hover:opacity-80 relative"
          style={{ color: "var(--on-surface-variant)" }}
        >
          <span className="material-symbols-outlined text-[20px]">notifications</span>
        </button>

        {/* New button */}
        <button
          className="flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-medium transition-all hover:opacity-80"
          style={{
            background: "var(--focus-ring)",
            color: "var(--primary)",
            border: "1px solid var(--primary)",
            opacity: 0.8,
          }}
        >
          <span className="material-symbols-outlined text-sm">add</span>
          New
        </button>

        {/* User avatar */}
        <div className="flex items-center gap-2">
          <div
            className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold cursor-pointer transition-all hover:opacity-80"
            style={{
              background: "var(--surface-variant)",
              color: "var(--on-surface)",
              border: "1px solid var(--glass-border)",
            }}
            onClick={logout}
            title="Logout"
          >
            {user?.name?.charAt(0)?.toUpperCase() || "U"}
          </div>
        </div>
      </div>
    </header>
  );
}
