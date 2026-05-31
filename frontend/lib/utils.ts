// DealLens Utility Functions
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function getScoreColor(verdict: string): string {
  switch (verdict) {
    case "Strong Fit":
      return "text-emerald-600 dark:text-emerald-400";
    case "Possible Fit":
      return "text-amber-600 dark:text-amber-400";
    case "Weak Fit":
      return "text-red-600 dark:text-red-400";
    default:
      return "text-muted-foreground";
  }
}

export function getScoreBg(verdict: string): string {
  switch (verdict) {
    case "Strong Fit":
      return "bg-emerald-50 border-emerald-200 dark:bg-emerald-950 dark:border-emerald-800";
    case "Possible Fit":
      return "bg-amber-50 border-amber-200 dark:bg-amber-950 dark:border-amber-800";
    case "Weak Fit":
      return "bg-red-50 border-red-200 dark:bg-red-950 dark:border-red-800";
    default:
      return "bg-muted border-border";
  }
}

export function getScoreBadge(verdict: string): string {
  switch (verdict) {
    case "Strong Fit":
      return "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200";
    case "Possible Fit":
      return "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200";
    case "Weak Fit":
      return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
    default:
      return "bg-muted text-muted-foreground";
  }
}

export function truncate(str: string, length: number): string {
  if (str.length <= length) return str;
  return str.slice(0, length) + "...";
}

export const SECTORS = [
  "FinTech",
  "HealthTech",
  "CyberSecurity",
  "ClimateTech",
  "AI/ML",
  "EdTech",
  "SaaS",
  "E-Commerce",
  "PropTech",
  "AgriTech",
  "Logistics",
  "Other",
];

export const STAGES = [
  "Pre-Seed",
  "Seed",
  "Series A",
  "Series B",
  "Series C+",
  "Growth",
];