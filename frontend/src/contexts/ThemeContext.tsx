"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";

type Theme = "dark" | "light";

type ThemeContextType = {
  theme: Theme;
  toggleTheme: () => void;
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  // Initialize with a default value but we'll update it after mount
  const [theme, setTheme] = useState<Theme>("light");
  const [mounted, setMounted] = useState(false);

  // Initial theme setup - runs after component mounts on client
  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    setMounted(true);
    
    try {
      const storedTheme = window.localStorage.getItem("theme") as Theme | null;
      const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)")?.matches;
      
      // Set theme based on stored preference or system preference
      const initialTheme = storedTheme || (prefersDark ? "dark" : "light");
      setTheme(initialTheme);
      applyTheme(initialTheme);
    } catch (error) {
      console.error("Error setting up theme:", error);
    }
  }, []);

  // Apply theme changes
  const applyTheme = (newTheme: Theme) => {
    if (typeof document === 'undefined') return;
    
    try {
      const root = document.documentElement;
      
      // Remove both classes and then add the correct one
      root.classList.remove("dark", "light");
      root.classList.add(newTheme);
      
      // Store in localStorage - wrap in try/catch for incognito mode
      try {
        window.localStorage.setItem("theme", newTheme);
      } catch (e) {
        console.warn("Failed to save theme preference:", e);
      }
    } catch (error) {
      console.error("Error applying theme:", error);
    }
  };

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    applyTheme(newTheme);
  };

  // Provide a default value during SSR to prevent hydration mismatch warnings
  const contextValue: ThemeContextType = {
    theme: mounted ? theme : "light",
    toggleTheme
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
} 