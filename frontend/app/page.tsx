"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  Search,
  Zap,
  BarChart3,
  Shield,
  ArrowRight,
  Sparkles,
  Target,
  Clock,
} from "lucide-react";

export default function LandingPage() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("deallens_token");
    if (token) {
      router.push("/dashboard");
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <Search className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold">DealLens</span>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => router.push("/login")}
                className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                Login
              </button>
              <button
                onClick={() => router.push("/login?mode=signup")}
                className="bg-primary text-primary-foreground px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-3 py-1 rounded-full text-sm font-medium mb-6">
            <Sparkles className="w-4 h-4" />
            AI-Powered VC Research Tool
          </div>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6">
            Analyze startups in{" "}
            <span className="text-primary">under 3 minutes</span>
          </h1>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
            DealLens generates structured VC-style investment snapshots. Stop
            spending 2-3 hours on manual research for every inbound deal.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <button
              onClick={() => router.push("/login?mode=signup")}
              className="bg-primary text-primary-foreground px-6 py-3 rounded-lg font-medium hover:bg-primary/90 transition-colors flex items-center justify-center gap-2"
            >
              Start Analyzing <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => router.push("/login")}
              className="border border-border px-6 py-3 rounded-lg font-medium hover:bg-accent transition-colors"
            >
              I have an account
            </button>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 border-t border-border">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-3">How it works</h2>
          <p className="text-muted-foreground">
            Three simple steps to structured deal analysis
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Search className="w-6 h-6" />}
            title="1. Enter Company"
            description="Paste a startup name, website URL, or short description. That's all the input we need."
          />
          <FeatureCard
            icon={<Zap className="w-6 h-6" />}
            title="2. AI Analysis"
            description="GLM-5.1 or GPT-4 analyzes the company against your fund's investment criteria in real-time."
          />
          <FeatureCard
            icon={<BarChart3 className="w-6 h-6" />}
            title="3. Get Snapshot"
            description="Receive a structured VC-style report with fit score, competitive landscape, and red flags."
          />
        </div>
      </section>

      {/* What You Get */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 border-t border-border">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-3">Every analysis includes</h2>
          <p className="text-muted-foreground">
            10 structured sections that mirror what a VC analyst needs
          </p>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            "Company one-liner",
            "Sector & stage classification",
            "Problem & solution summary",
            "Target market & TAM",
            "Business model breakdown",
            "Team assessment",
            "Traction signals",
            "Competitive landscape",
            "Regulatory notes",
            "Red flags",
            "Custom fit score (0-100)",
            "Fund-specific verdict",
          ].map((item, i) => (
            <div
              key={i}
              className="flex items-center gap-3 p-3 rounded-lg border border-border bg-card"
            >
              <div className="w-2 h-2 rounded-full bg-primary flex-shrink-0" />
              <span className="text-sm">{item}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Stats */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 border-t border-border">
        <div className="grid md:grid-cols-3 gap-8 text-center">
          <div>
            <Clock className="w-8 h-8 text-primary mx-auto mb-3" />
            <div className="text-3xl font-bold">3 min</div>
            <div className="text-muted-foreground text-sm">
              Average analysis time
            </div>
          </div>
          <div>
            <Target className="w-8 h-8 text-primary mx-auto mb-3" />
            <div className="text-3xl font-bold">0-100</div>
            <div className="text-muted-foreground text-sm">
              Fund-specific fit score
            </div>
          </div>
          <div>
            <Shield className="w-8 h-8 text-primary mx-auto mb-3" />
            <div className="text-3xl font-bold">10+</div>
            <div className="text-muted-foreground text-sm">
              Structured sections per report
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 border-t border-border">
        <div className="bg-primary/5 border border-primary/20 rounded-2xl p-8 sm:p-12 text-center">
          <h2 className="text-2xl sm:text-3xl font-bold mb-3">
            Ready to speed up your deal flow?
          </h2>
          <p className="text-muted-foreground mb-6 max-w-lg mx-auto">
            Join analysts who use DealLens to evaluate startups faster and more
            consistently.
          </p>
          <button
            onClick={() => router.push("/login?mode=signup")}
            className="bg-primary text-primary-foreground px-6 py-3 rounded-lg font-medium hover:bg-primary/90 transition-colors inline-flex items-center gap-2"
          >
            Get Started Free <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-primary rounded flex items-center justify-center">
              <Search className="w-3 h-3 text-primary-foreground" />
            </div>
            <span className="text-sm font-medium">DealLens</span>
          </div>
          <p className="text-xs text-muted-foreground">
            Built by Muhammad Usman — datawithusman.com
          </p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="p-6 rounded-xl border border-border bg-card hover:shadow-md transition-shadow">
      <div className="w-12 h-12 bg-primary/10 text-primary rounded-lg flex items-center justify-center mb-4">
        {icon}
      </div>
      <h3 className="font-semibold mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}