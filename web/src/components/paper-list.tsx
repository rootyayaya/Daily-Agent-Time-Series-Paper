"use client";

import { PaperDetail } from "@/types/paper";
import { PaperCard } from "./paper-card";
import { ScrollArea } from "@/components/ui/scroll-area";

interface PaperListProps {
  papers: PaperDetail[];
  dateStr: string;
}

export function PaperList({ papers, dateStr }: PaperListProps) {
  if (papers.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
        <p className="text-lg">暂无论文数据</p>
        <p className="text-sm mt-1">选择一个有数据的日期查看论文</p>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">
          {dateStr} · 共 {papers.length} 篇
        </h2>
      </div>
      <ScrollArea className="h-[calc(100vh-12rem)]">
        <div className="space-y-4 pr-4">
          {papers.map((paper) => (
            <PaperCard key={paper.arxiv_id} paper={paper} />
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
