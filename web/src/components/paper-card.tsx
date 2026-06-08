"use client";

import { useState } from "react";
import { PaperDetail } from "@/types/paper";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { ScoreBadge } from "./score-badge";
import { ChevronDown, ChevronUp, ExternalLink, FileText, Github } from "lucide-react";

export function PaperCard({ paper }: { paper: PaperDetail }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <Card className="transition-shadow hover:shadow-md">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-3">
          <CardTitle className="text-base leading-snug font-semibold">
            {paper.title}
          </CardTitle>
          <ScoreBadge score={paper.relevance_score} />
        </div>
        <div className="flex flex-wrap gap-1.5 mt-2">
          {paper.tags.slice(0, 5).map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>
        <p className="text-xs text-muted-foreground mt-1.5">
          {paper.authors.slice(0, 3).join(", ")}
          {paper.author_count > 3 && ` 等 ${paper.author_count} 位作者`}
          {" · "}
          {paper.categories.slice(0, 3).join(", ")}
        </p>
      </CardHeader>

      <CardContent className="pt-0">
        <p className="text-sm text-muted-foreground leading-relaxed">
          {paper.chinese_summary}
        </p>

        {expanded && (
          <>
            <Separator className="my-4" />
            <div className="space-y-3">
              <div>
                <h4 className="text-sm font-semibold mb-1.5">核心贡献</h4>
                <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
                  {(paper.core_contributions || []).map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="text-sm font-semibold mb-1.5">文章解读</h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {paper.analysis}
                </p>
              </div>
            </div>
          </>
        )}

        <div className="flex items-center gap-2 mt-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setExpanded(!expanded)}
            className="text-xs"
          >
            {expanded ? (
              <>
                <ChevronUp className="h-3.5 w-3.5 mr-1" /> 收起
              </>
            ) : (
              <>
                <ChevronDown className="h-3.5 w-3.5 mr-1" /> 展开详情
              </>
            )}
          </Button>
          <a href={paper.arxiv_url} target="_blank" rel="noopener noreferrer">
            <Button variant="outline" size="sm" className="text-xs">
              <ExternalLink className="h-3.5 w-3.5 mr-1" /> arxiv
            </Button>
          </a>
          <a href={paper.pdf_url} target="_blank" rel="noopener noreferrer">
            <Button variant="outline" size="sm" className="text-xs">
              <FileText className="h-3.5 w-3.5 mr-1" /> PDF
            </Button>
          </a>
          {paper.github_url && (
            <a href={paper.github_url} target="_blank" rel="noopener noreferrer">
              <Button variant="outline" size="sm" className="text-xs">
                <Github className="h-3.5 w-3.5 mr-1" /> Code
              </Button>
            </a>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
