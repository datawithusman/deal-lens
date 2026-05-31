"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, Plus, Trash2, Star, Search } from "lucide-react";
import { profilesApi, FundProfile } from "@/lib/api";
import { SECTORS, STAGES } from "@/lib/utils";

export default function ProfilesPage() {
  const router = useRouter();
  const [profiles, setProfiles] = useState<FundProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [saving, setSaving] = useState(false);

  const [form, setForm] = useState({
    name: "",
    description: "",
    fund_name: "",
    target_stages: [] as string[],
    target_sectors: [] as string[],
    excluded_sectors: [] as string[],
    valuation_min: "",
    valuation_max: "",
    focus_description: "",
    additional_notes: "",
    is_default: false,
  });

  useEffect(() => {
    const token = localStorage.getItem("deallens_token");
    if (!token) { router.push("/login"); return; }
    loadProfiles();
  }, [router]);

  const loadProfiles = async () => {
    try {
      const data = await profilesApi.list();
      setProfiles(data);
    } catch {} finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setForm({ name: "", description: "", fund_name: "", target_stages: [], target_sectors: [], excluded_sectors: [], valuation_min: "", valuation_max: "", focus_description: "", additional_notes: "", is_default: false });
    setEditingId(null);
    setShowForm(false);
  };

  const editProfile = (p: FundProfile) => {
    setForm({
      name: p.name,
      description: p.description || "",
      fund_name: p.fund_name,
      target_stages: p.target_stages,
      target_sectors: p.target_sectors,
      excluded_sectors: p.excluded_sectors,
      valuation_min: p.valuation_min?.toString() || "",
      valuation_max: p.valuation_max?.toString() || "",
      focus_description: p.focus_description || "",
      additional_notes: p.additional_notes || "",
      is_default: p.is_default,
    });
    setEditingId(p.id);
    setShowForm(true);
  };

  const toggleItem = (field: "target_stages" | "target_sectors" | "excluded_sectors", value: string) => {
    setForm((prev) => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter((v) => v !== value)
        : [...prev[field], value],
    }));
  };

  const handleSave = async () => {
    if (!form.name || !form.fund_name) return;
    setSaving(true);
    try {
      const payload = {
        ...form,
        valuation_min: form.valuation_min ? parseFloat(form.valuation_min) : null,
        valuation_max: form.valuation_max ? parseFloat(form.valuation_max) : null,
      };
      if (editingId) {
        await profilesApi.update(editingId, payload);
      } else {
        await profilesApi.create(payload as any);
      }
      resetForm();
      loadProfiles();
    } catch (err: any) {
      alert(err.message || "Failed to save profile");
    } finally {
      setSaving(false);
    }
  };

  const deleteProfile = async (id: number) => {
    if (!confirm("Delete this profile?")) return;
    try {
      await profilesApi.delete(id);
      loadProfiles();
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-muted-foreground">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="border-b border-border bg-background/95 backdrop-blur sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <button onClick={() => router.push("/dashboard")} className="flex items-center gap-2 text-muted-foreground hover:text-foreground">
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
            <span className="font-semibold">Fund Profiles</span>
            <div className="w-16" />
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-xl font-bold">Fund Profiles</h1>
            <p className="text-sm text-muted-foreground">Manage your investment criteria profiles</p>
          </div>
          {!showForm && (
            <button onClick={() => { resetForm(); setShowForm(true); }} className="bg-primary text-primary-foreground px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
              <Plus className="w-4 h-4" /> New Profile
            </button>
          )}
        </div>

        {/* Profile List */}
        {!showForm && (
          <div className="space-y-3">
            {profiles.map((p) => (
              <div key={p.id} className="border border-border rounded-xl p-5 hover:shadow-sm transition-shadow cursor-pointer" onClick={() => editProfile(p)}>
                <div className="flex justify-between items-start">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold">{p.name}</h3>
                      {p.is_default && (
                        <span className="text-xs bg-primary/10 text-primary px-2 py-0.5 rounded-full flex items-center gap-1">
                          <Star className="w-3 h-3" /> Default
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground mt-0.5">{p.fund_name}</p>
                    {p.description && <p className="text-sm text-muted-foreground mt-1">{p.description}</p>}
                  </div>
                  {!p.is_default && (
                    <button onClick={(e) => { e.stopPropagation(); deleteProfile(p.id); }} className="p-1.5 hover:bg-destructive/10 rounded text-muted-foreground hover:text-destructive">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
                <div className="flex flex-wrap gap-1.5 mt-3">
                  {p.target_sectors.map((s) => (
                    <span key={s} className="text-xs bg-primary/10 text-primary px-2 py-0.5 rounded">{s}</span>
                  ))}
                  {p.target_stages.map((s) => (
                    <span key={s} className="text-xs bg-secondary text-secondary-foreground px-2 py-0.5 rounded">{s}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Create/Edit Form */}
        {showForm && (
          <div className="border border-border rounded-xl p-6 space-y-4">
            <h2 className="font-semibold text-lg">{editingId ? "Edit Profile" : "Create Profile"}</h2>

            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium mb-1.5 block">Profile Name *</label>
                <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="e.g. K Street Capital Default" className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
              <div>
                <label className="text-sm font-medium mb-1.5 block">Fund Name *</label>
                <input value={form.fund_name} onChange={(e) => setForm({ ...form, fund_name: e.target.value })} placeholder="e.g. K Street Capital" className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
            </div>

            <div>
              <label className="text-sm font-medium mb-1.5 block">Description</label>
              <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} placeholder="What kind of companies does this fund invest in?" rows={2} className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring resize-none" />
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Target Sectors</label>
              <div className="flex flex-wrap gap-2">
                {SECTORS.map((s) => (
                  <button key={s} onClick={() => toggleItem("target_sectors", s)} className={`text-xs px-3 py-1.5 rounded-lg border transition-colors ${form.target_sectors.includes(s) ? "bg-primary text-primary-foreground border-primary" : "border-border hover:bg-accent"}`}>
                    {s}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Target Stages</label>
              <div className="flex flex-wrap gap-2">
                {STAGES.map((s) => (
                  <button key={s} onClick={() => toggleItem("target_stages", s)} className={`text-xs px-3 py-1.5 rounded-lg border transition-colors ${form.target_stages.includes(s) ? "bg-primary text-primary-foreground border-primary" : "border-border hover:bg-accent"}`}>
                    {s}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Excluded Sectors</label>
              <div className="flex flex-wrap gap-2">
                {SECTORS.map((s) => (
                  <button key={s} onClick={() => toggleItem("excluded_sectors", s)} className={`text-xs px-3 py-1.5 rounded-lg border transition-colors ${form.excluded_sectors.includes(s) ? "bg-destructive text-destructive-foreground border-destructive" : "border-border hover:bg-accent"}`}>
                    {s}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium mb-1.5 block">Min Valuation ($)</label>
                <input type="number" value={form.valuation_min} onChange={(e) => setForm({ ...form, valuation_min: e.target.value })} placeholder="1000000" className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
              <div>
                <label className="text-sm font-medium mb-1.5 block">Max Valuation ($)</label>
                <input type="number" value={form.valuation_max} onChange={(e) => setForm({ ...form, valuation_max: e.target.value })} placeholder="100000000" className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
            </div>

            <div>
              <label className="text-sm font-medium mb-1.5 block">Focus Description</label>
              <textarea value={form.focus_description} onChange={(e) => setForm({ ...form, focus_description: e.target.value })} placeholder="Describe the fund's investment focus in detail..." rows={3} className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring resize-none" />
            </div>

            <div>
              <label className="text-sm font-medium mb-1.5 block">Additional Notes</label>
              <textarea value={form.additional_notes} onChange={(e) => setForm({ ...form, additional_notes: e.target.value })} placeholder="Any additional criteria..." rows={2} className="w-full border border-input bg-background rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-ring resize-none" />
            </div>

            <div className="flex items-center gap-2">
              <input type="checkbox" checked={form.is_default} onChange={(e) => setForm({ ...form, is_default: e.target.checked })} className="rounded" />
              <label className="text-sm">Set as default profile</label>
            </div>

            <div className="flex gap-3 pt-2">
              <button onClick={handleSave} disabled={saving || !form.name || !form.fund_name} className="bg-primary text-primary-foreground px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-primary/90 disabled:opacity-50">
                {saving ? "Saving..." : editingId ? "Update Profile" : "Create Profile"}
              </button>
              <button onClick={resetForm} className="border border-border px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-accent">
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}