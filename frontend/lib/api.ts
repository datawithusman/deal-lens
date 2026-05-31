const API_BASE = process.env.NEXT_PUBLIC_API_URL || "https://deal-lens.onrender.com/api";

// Types
export interface User {
  id: number;
  email: string;
  full_name: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface FitScore {
  total: number;
  sector_match: number;
  stage_match: number;
  team_quality: number;
  market_size: number;
  verdict: string;
}

export interface AnalysisData {
  id: number;
  company_name: string;
  one_liner: string | null;
  sector: string | null;
  stage: string | null;
  problem_solution: string | null;
  target_market: string | null;
  business_model: string | null;
  team_assessment: string | null;
  traction_signals: string | null;
  competitive_landscape: string | null;
  regulatory_notes: string | null;
  red_flags: string | null;
  fit_score: FitScore | null;
  llm_provider: string;
  status: string;
  processing_time_seconds: number | null;
  created_at: string;
}

export interface AnalysisListItem {
  id: number;
  company_name: string;
  sector: string | null;
  stage: string | null;
  total_score: number | null;
  verdict: string | null;
  status: string;
  created_at: string;
}

export interface FundProfile {
  id: number;
  name: string;
  description: string | null;
  fund_name: string;
  target_stages: string[];
  target_sectors: string[];
  excluded_sectors: string[];
  valuation_min: number | null;
  valuation_max: number | null;
  focus_description: string | null;
  additional_notes: string | null;
  is_default: boolean;
  created_at: string;
  updated_at: string;
}

export interface AnalysisStats {
  total_analyses: number;
  completed: number;
  failed: number;
  verdict_distribution: {
    strong_fit: number;
    possible_fit: number;
    weak_fit: number;
  };
  top_sectors: { sector: string; count: number }[];
}

// Helper
async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token =
    typeof window !== "undefined" ? localStorage.getItem("deallens_token") : null;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

// Auth API
export const authApi = {
  signup: (data: { email: string; full_name: string; password: string }) =>
    request<AuthResponse>("/auth/signup", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  login: (data: { email: string; password: string }) =>
    request<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  getMe: () => request<User>("/auth/me"),
};

// Analysis API
export const analysisApi = {
  analyze: (data: {
    company_name: string;
    website_url?: string;
    description?: string;
    fund_profile_id?: number;
    llm_provider?: string;
  }) =>
    request<AnalysisData>("/analyze", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  getAnalysis: (id: number) => request<AnalysisData>(`/analyze/${id}`),

  deleteAnalysis: (id: number) =>
    request<{ message: string }>(`/analyze/${id}`, { method: "DELETE" }),
};

// History API
export const historyApi = {
  getHistory: (params?: { skip?: number; limit?: number; status_filter?: string }) => {
    const searchParams = new URLSearchParams();
    if (params?.skip) searchParams.set("skip", String(params.skip));
    if (params?.limit) searchParams.set("limit", String(params.limit));
    if (params?.status_filter) searchParams.set("status_filter", params.status_filter);
    const qs = searchParams.toString();
    return request<AnalysisListItem[]>(`/history${qs ? `?${qs}` : ""}`);
  },

  getStats: () => request<AnalysisStats>("/history/stats"),
};

// Profiles API
export const profilesApi = {
  list: () => request<FundProfile[]>("/profiles"),

  get: (id: number) => request<FundProfile>(`/profiles/${id}`),

  create: (data: Partial<FundProfile> & { name: string; fund_name: string; target_stages: string[]; target_sectors: string[] }) =>
    request<FundProfile>("/profiles", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  update: (id: number, data: Partial<FundProfile>) =>
    request<FundProfile>(`/profiles/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    request<{ message: string }>(`/profiles/${id}`, { method: "DELETE" }),
};