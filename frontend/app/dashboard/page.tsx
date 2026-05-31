"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  Search, Plus, History, BarChart3, Settings, Moon, Sun, LogOut, Trash2, ExternalLink
} from "lucide-react";
import { authApi, historyApi, analysisApi, AnalysisListItem, AnalysisStats } from "@/lib/api";
import { formatDate, getScoreBadge, truncate } from "@/lib/utils";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [analyses, setAnalyses] = useState<AnalysisListItem[]>([]);
  const [stats, setStats] = useState<AnalysisStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("deallens_token");
    if (!token) { router.push("/login"); return; }

    const userData = localStorage.getItem("deallens_user");
    if (userData) setUser(JSON.parse(userData));

    setDarkMode(document.documentElement.classList.contains("dark"));
    loadData();
  }, [router]);

  const loadData = async () => {
    try {
      const [historyData, statsData] = await Promise.all([
        historyApi.getHistory({ limit: 10 }),
        historyApi.getStats(),
      ]);
      setAnalyses(historyData);
      setStats(statsData);
    } catch {
      localStorage.removeItem("deallens_token");
      router.push("/login");
    } finally {
      setLoading(false);
    }
  };

  const toggleDark = () => {
    const newDark = !darkMode;
    setDarkMode(newDark);
    document.documentElement.classList.toggle("dark", newDark);
    localStorage.setItem("deallens_theme", newDark ? "dark" : "light");
  };

  const logout = () => {
    localStorage.removeItem("deallens_token");
    localStorage.removeItem("deallens_user");
    router.push("/");
  };

  const deleteAnalysis = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm("Delete this analysis?")) return;
    await analysisApi.deleteAnalysis(id);
    loadData();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-pulse text-muted-foreground">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="border-b border-border bg-background/95 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2 cursor-pointer" onClick={() => router.push("/dashboard")}>
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <Search className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold">DealLens</span>
            </div>
            <div className="flex items-center gap-2">
              <button onClick={() => router.push("/profiles")} className="p-2 hover:bg-accent rounded-lg transition-colors" title="Fund Profiles">
                <Settings className="w-5 h-5" />
              </button>
              <button onClick={toggleDark} className="p-2 hover:bg-accent rounded-lg transition-colors">
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              <button onClick={logout} className="p-2 hover:bg-accent rounded-lg transition-colors text-muted-foreground" title="Logout">
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <p className="text-muted-foreground text-sm">
              Welcome back{user?.full_name ? `, ${user.full_name}` : ""}
            </p>
          </div>
          <button
            onClick={() => router.push("/analyze")}
            className="bg-primary text-primary-foreground px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors flex items-center gap-2"
          >
            <Plus className="w-4 h-4" /> New Analysis
          </button>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <StatCard label="Total Analyses" value={stats.total_analyses} icon={<History className="w-5 h-5" />} />
            <StatCard label="Strong Fits" value={stats.verdict_distribution.strong_fit} icon={<BarChart3 className="w-5 h-5" />} color="text-emerald-600" />
            <StatCard label="Possible Fits" value={stats.verdict_distribution.possible_fit} icon={<BarChart3 className="w-5 h-5" />} color="text-amber-600" />
            <StatCard label="Weak Fits" value={stats.verdict_distribution.weak_fit} icon={<BarChart3 className="w-5 h-5" />} color="text-red-600" />
          </div>
        )}

        {/* Recent Analyses */}
        <div>
          <h2 className="text-lg font-semibold mb-4">Recent Analyses</h2>
          {analyses.length === 0 ? (
            <div className="text-center py-16 border border-dashed border-border rounded-xl">
              <Search className="w-12 h-12 text-muted-foreground/50 mx-auto mb-4" />
              <h3 className="font-medium mb-1">No analyses yet</h3>
              <p className="text-sm text-muted-foreground mb-4">Start by analyzing your first startup</p>
              <button
                onClick={() => router.push("/analyze")}
                className="bg-primary text-primary-foreground px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary/90"
              >
                <Plus className="w-4 h-4 inline mr-1" /> New Analysis
              </button>
            </div>
          ) : (
            <div className="space-y-2">
              {analyses.map((a) => (
                <div
                  key={a.id}
                  onClick={() => router.push(`/analyze?id=${a.id}`)}
                  className="flex items-center justify-between p-4 border border-border rounded-lg hover:bg-accent/50 cursor-pointer transition-colors"
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-medium truncate">{a.company_name}</span>
                      {a.verdict && (
                        <span className={`text-xs px-2 py-0.5 rounded-full ${getScoreBadge(a.verdict)}`}>
                          {a.verdict}
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-muted-foreground mt-0.5">
                      {a.sector && `${a.sector} · `}{a.stage && `${a.stage} · `}{formatDate(a.created_at)}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {a.total_score !== null && (
                      <span className="text-lg font-bold">{a.total_score}/100</span>
                    )}
                    <button
                      onClick={(e) => deleteAnalysis(a.id, e)}
                      className="p-1.5 hover:bg-destructive/10 rounded text-muted-foreground hover:text-destructive transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                    <ExternalLink className="w-4 h-4 text-muted-foreground" />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function StatCard({ label, value, icon, color }: { label: string; value: number; icon: React.ReactNode; color?: string }) {
  return (
    <div className="border border-border rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-muted-foreground">{label}</span>
        <span className={color || "text-primary"}>{icon}</span>
      </div>
      <div className={`text-2xl font-bold ${color || ""}`}>{value}</div>
    </div>
  );
}