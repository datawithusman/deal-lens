"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Search, ArrowLeft, Loader2, AlertTriangle, Zap } from "lucide-react";
import { analysisApi, profilesApi, AnalysisData, FundProfile } from "@/lib/api";
import { formatDate, getScoreColor, getScoreBg, getScoreBadge } from "@/lib/utils";

export default function AnalyzePage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-primary" /></div>}>
      <AnalyzeContent />
    </Suspense>
  );
}

function AnalyzeContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const existingId = searchParams.get("id");

  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [profiles, setProfiles] = useState<FundProfile[]>([]);
  const [loading, setLoading] = useState(!!existingId);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState("");

  // Form state
  const [companyName, setCompanyName] = useState("");
  const [websiteUrl, setWebsiteUrl] = useState("");
  const [description, setDescription] = useState("");
  const [selectedProfile, setSelectedProfile] = useState<number | undefined>();
  const [llmProvider, setLlmProvider] = useState("glm");

  useEffect(() => {
    const token = localStorage.getItem("deallens_token");
    if (!token) { router.push("/login"); return; }
    loadProfiles();
    if (existingId) loadExisting(parseInt(existingId));
  }, [router, existingId]);

  const loadProfiles = async () => {
    try {
      const data = await profilesApi.list();
      setProfiles(data);
      const def = data.find((p) => p.is_default);
      if (def) setSelectedProfile(def.id);
    } catch {}
  };

  const loadExisting = async (id: number) => {
    try {
      const data = await analysisApi.getAnalysis(id);
      setAnalysis(data);
    } catch {
      setError("Analysis not found");
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!companyName.trim()) { setError("Company name is required"); return; }
    setError("");
    setAnalyzing(true);
    setAnalysis(null);

    try {
      const data = await analysisApi.analyze({
        company_name: companyName.trim(),
        website_url: websiteUrl.trim() || undefined,
        description: description.trim() || undefined,
        fund_profile_id: selectedProfile,
        llm_provider: llmProvider,
      });
      setAnalysis(data);
    } catch (err: any) {
      setError(err.message || "Analysis failed");
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="border-b border-border bg-background/95 backdrop-blur sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <button onClick={() => router.push("/dashboard")} className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <Search className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold">DealLens</span>
            </div>
            <div className="w-16" />
          </div>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Input Form (show when no analysis or analyzing) */}
        {(!analysis || analyzing) && (
          <div className="border border-border rounded-xl p-6 mb-8">
            <h1 className="text-xl font-bold mb-1">Analyze a Startup</h1>
            <p className="text-sm text-muted-foreground mb-6">
              Enter company details and we'll generate a full VC-style snapshot
            </p>

            {error && (
              <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-lg border border-destructive/20 mb-4">
                {error}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-1.5 block">Company Name *</label>
                <input value={companyName} onChange={(e) => setCompanyName(e.target.value)} placeholder="e.g. Stripe, Notion, or any startup" className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
              <div>
                <label className="text-sm font-medium mb-1.5 block">Website URL (optional)</label>
                <input value={websiteUrl} onChange={(e) => setWebsiteUrl(e.target.value)} placeholder="https://example.com" className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
              <div>
                <label className="text-sm font-medium mb-1.5 block">Description (optional)</label>
                <textarea value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Brief description of what the company does..." rows={3} className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring resize-none" />
              </div>
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium mb-1.5 block">Fund Profile</label>
                  <select value={selectedProfile || ""} onChange={(e) => setSelectedProfile(e.target.value ? parseInt(e.target.value) : undefined)} className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring">
                    <option value="">Default criteria</option>
                    {profiles.map((p) => (<option key={p.id} value={p.id}>{p.name}</option>))}
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium mb-1.5 block">AI Provider</label>
                  <select value={llmProvider} onChange={(e) => setLlmProvider(e.target.value)} className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring">
                    <option value="glm">GLM-5.1 (Recommended)</option>
                    <option value="openai">OpenAI GPT-4</option>
                  </select>
                </div>
              </div>
              <button onClick={handleAnalyze} disabled={analyzing || !companyName.trim()} className="w-full bg-primary text-primary-foreground py-3 rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors disabled:opacity-50 flex items-center justify-center gap-2">
                {analyzing ? (<><Loader2 className="w-4 h-4 animate-spin" /> Analyzing... (2-3 min)</>) : (<><Zap className="w-4 h-4" /> Analyze Startup</>)}
              </button>
            </div>
          </div>
        )}

        {/* Analyzing State */}
        {analyzing && (
          <div className="text-center py-16 animate-pulse-slow">
            <Loader2 className="w-16 h-16 animate-spin text-primary mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">Analyzing {companyName}...</h2>
            <p className="text-sm text-muted-foreground">Scraping website, processing data, and generating VC snapshot</p>
            <p className="text-xs text-muted-foreground mt-2">This usually takes 2-3 minutes</p>
          </div>
        )}

        {/* Results */}
        {analysis && !analyzing && (
          <div className="space-y-6 animate-slide-up">
            {/* Header */}
            <div className={`border rounded-xl p-6 ${getScoreBg(analysis.fit_score?.verdict || "")}`}>
              <div className="flex flex-col sm:flex-row justify-between items-start gap-4">
                <div>
                  <h1 className="text-2xl font-bold">{analysis.company_name}</h1>
                  {analysis.one_liner && <p className="text-muted-foreground mt-1">{analysis.one_liner}</p>}
                  <div className="flex flex-wrap gap-2 mt-3">
                    {analysis.sector && <span className="text-xs bg-background/80 px-2 py-1 rounded">{analysis.sector}</span>}
                    {analysis.stage && <span className="text-xs bg-background/80 px-2 py-1 rounded">{analysis.stage}</span>}
                    <span className="text-xs bg-background/80 px-2 py-1 rounded">via {analysis.llm_provider}</span>
                    <span className="text-xs bg-background/80 px-2 py-1 rounded">{formatDate(analysis.created_at)}</span>
                  </div>
                </div>
                {analysis.fit_score && (
                  <div className="text-center">
                    <div className={`text-4xl font-bold ${getScoreColor(analysis.fit_score.verdict)}`}>
                      {analysis.fit_score.total}/100
                    </div>
                    <span className={`text-xs px-3 py-1 rounded-full font-medium mt-2 inline-block ${getScoreBadge(analysis.fit_score.verdict)}`}>
                      {analysis.fit_score.verdict}
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Score Breakdown */}
            {analysis.fit_score && (
              <div className="border border-border rounded-xl p-6">
                <h2 className="font-semibold mb-4">Fit Score Breakdown</h2>
                <div className="grid sm:grid-cols-2 gap-4">
                  {[
                    { label: "Sector Match", value: analysis.fit_score.sector_match },
                    { label: "Stage Match", value: analysis.fit_score.stage_match },
                    { label: "Team Quality", value: analysis.fit_score.team_quality },
                    { label: "Market Size", value: analysis.fit_score.market_size },
                  ].map((s) => (
                    <div key={s.label} className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">{s.label}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-24 h-2 bg-muted rounded-full overflow-hidden">
                          <div className="h-full bg-primary rounded-full" style={{ width: `${s.value}%` }} />
                        </div>
                        <span className="text-sm font-medium w-8 text-right">{s.value}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Detail Sections */}
            <div className="grid gap-4">
              {[
                { title: "Problem & Solution", content: analysis.problem_solution },
                { title: "Target Market", content: analysis.target_market },
                { title: "Business Model", content: analysis.business_model },
                { title: "Team Assessment", content: analysis.team_assessment },
                { title: "Traction Signals", content: analysis.traction_signals },
                { title: "Competitive Landscape", content: analysis.competitive_landscape },
                { title: "Regulatory Notes", content: analysis.regulatory_notes },
              ].filter(s => s.content).map((s) => (
                <div key={s.title} className="border border-border rounded-xl p-5">
                  <h3 className="font-semibold text-sm mb-2">{s.title}</h3>
                  <p className="text-sm text-muted-foreground whitespace-pre-line">{s.content}</p>
                </div>
              ))}
            </div>

            {/* Red Flags */}
            {analysis.red_flags && (
              <div className="border border-destructive/30 bg-destructive/5 rounded-xl p-5">
                <h3 className="font-semibold text-sm mb-2 flex items-center gap-2 text-destructive">
                  <AlertTriangle className="w-4 h-4" /> Red Flags
                </h3>
                <p className="text-sm text-muted-foreground whitespace-pre-line">{analysis.red_flags}</p>
              </div>
            )}

            {/* New Analysis Button */}
            <div className="text-center pt-4 pb-8">
              <button onClick={() => { setAnalysis(null); setCompanyName(""); setWebsiteUrl(""); setDescription(""); }} className="bg-primary text-primary-foreground px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-primary/90">
                Analyze Another Startup
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}