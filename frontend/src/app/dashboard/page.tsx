"use client";

import { Card } from "@/components/ui/card";
import { Folder, FileText, Database } from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground text-slate-500">
          Overview of your knowledge brain.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card className="p-6 bg-white shadow-sm rounded-xl border border-slate-100 flex items-center gap-4">
          <div className="p-3 bg-violet-100 text-violet-600 rounded-full">
            <FileText className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Total Documents</p>
            <h3 className="text-2xl font-bold">12</h3>
          </div>
        </Card>
        <Card className="p-6 bg-white shadow-sm rounded-xl border border-slate-100 flex items-center gap-4">
          <div className="p-3 bg-pink-100 text-pink-600 rounded-full">
            <Folder className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Folders</p>
            <h3 className="text-2xl font-bold">4</h3>
          </div>
        </Card>
        <Card className="p-6 bg-white shadow-sm rounded-xl border border-slate-100 flex items-center gap-4">
          <div className="p-3 bg-emerald-100 text-emerald-600 rounded-full">
            <Database className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Storage Used</p>
            <h3 className="text-2xl font-bold">1.2 MB</h3>
          </div>
        </Card>
      </div>
    </div>
  );
}
