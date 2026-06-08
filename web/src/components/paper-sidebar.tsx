"use client";

import { PaperMeta } from "@/types/paper";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ScoreBadge } from "./score-badge";
import { cn } from "@/lib/utils";

interface PaperSidebarProps {
  papers: PaperMeta[];
  selectedId: string | null;
  onSelect: (arxivId: string) => void;
}

export function PaperSidebar({ papers, selectedId, onSelect }: PaperSidebarProps) {
  if (papers.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground text-sm">
        暂无论文数据
      </div>
    );
  }

  return (
    <ScrollArea className="h-full">
      <div className="py-2 px-3">
        {papers.map((paper, idx) => (
          <div key={paper.arxiv_id}>
            {idx > 0 && <div className="mx-3 border-b border-border/40" />}
            <button
              onClick={() => onSelect(paper.arxiv_id)}
              className={cn(
                "w-full text-left px-3 py-3.5 rounded-lg transition-colors",
                "hover:bg-accent/50",
                selectedId === paper.arxiv_id
                  ? "bg-accent text-accent-foreground"
                  : "text-foreground"
              )}
            >
              <div className="flex items-start justify-between gap-2.5">
                <h3 className="text-[13px] font-medium leading-snug line-clamp-2 flex-1">
                  {paper.title}
                </h3>
                <ScoreBadge score={paper.relevance_score} />
              </div>
              <div className="flex flex-wrap gap-1.5 mt-2">
                {paper.tags.slice(0, 2).map((tag) => (
                  <Badge key={tag} variant="secondary" className="text-[10px] px-1.5 py-0 font-normal">
                    {tag}
                  </Badge>
                ))}
              </div>
            </button>
          </div>
        ))}
      </div>
    </ScrollArea>
  );
}
