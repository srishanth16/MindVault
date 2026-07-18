"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useAuth } from "@/components/AuthProvider";

const mainRoutes = [
  { label: "Dashboard", icon: "dashboard", href: "/dashboard", fill: true },
  { label: "AI Chat", icon: "forum", href: "/chat" },
  { label: "Notes", icon: "description", href: "/notes" },
  { label: "Documents", icon: "folder_open", href: "/documents" },
  { label: "Memory", icon: "psychology", href: "/memory" },
  { label: "Knowledge Graph", icon: "hub", href: "/knowledge-graph" },
  { label: "Timeline", icon: "timeline", href: "/timeline" },
  { label: "Analytics", icon: "analytics", href: "/analytics" },
];

const footerRoutes = [
  { label: "Settings", icon: "settings", href: "/settings" },
];

const mobileRoutes = [
  { label: "Home", icon: "dashboard", href: "/dashboard" },
  { label: "Chat", icon: "forum", href: "/chat" },
  { label: "Docs", icon: "folder_open", href: "/documents" },
  { label: "Search", icon: "search", href: "/documents" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user } = useAuth();

  const isActive = (href: string) => pathname === href;

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col h-screen w-[280px] fixed left-0 top-0 py-6 z-30"
        style={{
          background: "var(--surface-container)",
          opacity: 0.95,
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          borderRight: "1px solid var(--glass-border)",
        }}
      >
        {/* Header */}
        <div className="px-6 mb-10">
          <div className="flex items-center gap-4">
            <div
              className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold"
              style={{ background: "var(--primary-container)", color: "var(--on-primary-container)" }}
            >
              {user?.name?.charAt(0)?.toUpperCase() || "M"}
            </div>
            <div>
              <h1 className="text-2xl font-bold" style={{ color: "var(--primary)" }}>
                MindVault
              </h1>
              <p
                className="text-xs uppercase tracking-wider font-medium"
                style={{ color: "var(--on-surface-variant)" }}
              >
                Second Brain
              </p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-2 space-y-1 overflow-y-auto">
          {mainRoutes.map((route) => (
            <Link
              key={route.href}
              href={route.href}
              className={cn(
                "flex items-center gap-4 px-4 py-2 rounded-xl transition-all duration-150",
                isActive(route.href)
                  ? "scale-[0.97] font-bold"
                  : "hover:opacity-80"
              )}
              style={
                isActive(route.href)
                  ? {
                      background: "var(--sidebar-active)",
                      color: "var(--on-secondary-container)",
                      borderLeft: "4px solid var(--tertiary)",
                      boxShadow: "0 0 15px rgba(87, 27, 193, 0.3)",
                    }
                  : {
                      color: "var(--on-surface-variant)",
                      borderLeft: "4px solid transparent",
                    }
              }
            >
              <span
                className="material-symbols-outlined text-[20px]"
                style={{
                  fontVariationSettings: isActive(route.href) ? "'FILL' 1" : "'FILL' 0",
                }}
              >
                {route.icon}
              </span>
              <span className="text-sm">{route.label}</span>
            </Link>
          ))}
        </nav>

        {/* Footer */}
        <div className="px-2 mt-auto pt-4" style={{ borderTop: "1px solid var(--glass-border)" }}>
          {footerRoutes.map((route) => (
            <Link
              key={route.href}
              href={route.href}
              className={cn(
                "flex items-center gap-4 px-4 py-2 rounded-xl transition-all duration-150",
                isActive(route.href) ? "font-bold" : ""
              )}
              style={
                isActive(route.href)
                  ? {
                      background: "var(--sidebar-active)",
                      color: "var(--on-secondary-container)",
                    }
                  : { color: "var(--on-surface-variant)" }
              }
            >
              <span
                className="material-symbols-outlined text-[20px]"
                style={{
                  fontVariationSettings: isActive(route.href) ? "'FILL' 1" : "'FILL' 0",
                }}
              >
                {route.icon}
              </span>
              <span className="text-sm">{route.label}</span>
            </Link>
          ))}
        </div>
      </aside>

      {/* Mobile Bottom Nav */}
      <nav
        className="md:hidden fixed bottom-0 w-full h-16 flex justify-around items-center z-50 px-2"
        style={{
          background: "var(--surface-container-low)",
          opacity: 0.95,
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          borderTop: "1px solid var(--glass-border)",
        }}
      >
        {mobileRoutes.map((route) => (
          <Link
            key={route.label}
            href={route.href}
            className="flex flex-col items-center gap-1 p-2 rounded-lg transition-all"
            style={
              isActive(route.href)
                ? { color: "var(--primary)", background: "var(--focus-ring)" }
                : { color: "var(--on-surface-variant)" }
            }
          >
            <span
              className="material-symbols-outlined text-[22px]"
              style={{
                fontVariationSettings: isActive(route.href) ? "'FILL' 1" : "'FILL' 0",
              }}
            >
              {route.icon}
            </span>
            <span className="text-[10px] font-medium">{route.label}</span>
          </Link>
        ))}
      </nav>
    </>
  );
}
