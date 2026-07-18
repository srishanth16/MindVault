"use client";

import { Card } from "@/components/ui/card";
import { Upload, File, FileText, MoreVertical } from "lucide-react";

export default function DocumentsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-bold tracking-tight">Documents</h1>
          <p className="text-slate-500">
            Manage your uploaded files and knowledge sources.
          </p>
        </div>
        <button className="bg-slate-900 text-white px-4 py-2 flex items-center gap-2 rounded-lg hover:bg-slate-800 transition">
          <Upload className="w-4 h-4" />
          Upload Document
        </button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i} className="p-4 bg-white shadow-sm rounded-xl border border-slate-100 flex flex-col hover:border-slate-300 transition cursor-pointer">
            <div className="flex justify-between items-start mb-4">
              <div className="p-2 bg-violet-100 text-violet-600 rounded-lg">
                <FileText className="w-6 h-6" />
              </div>
              <button className="text-slate-400 hover:text-slate-600">
                <MoreVertical className="w-5 h-5" />
              </button>
            </div>
            <h3 className="font-semibold text-slate-800 truncate">Machine Learning PDF {i}</h3>
            <p className="text-xs text-slate-500 mt-1">Uploaded 2 days ago • 2.4 MB</p>
          </Card>
        ))}
      </div>
    </div>
  );
}
