"use client";

import ReactMarkdown from "react-markdown";
import { PaperDetail as PaperDetailType } from "@/types/paper";
import { isQAFormat } from "@/lib/data";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ScoreBadge } from "./score-badge";
import { ExternalLink, FileText, ArrowLeft, Loader2, Github, Globe, FlaskConical } from "lucide-react";

const QA_COLORS = [
  "bg-blue-50 text-blue-700 ring-blue-200/60 dark:bg-blue-950/50 dark:text-blue-300 dark:ring-blue-800/40",
  "bg-emerald-50 text-emerald-700 ring-emerald-200/60 dark:bg-emerald-950/50 dark:text-emerald-300 dark:ring-emerald-800/40",
  "bg-violet-50 text-violet-700 ring-violet-200/60 dark:bg-violet-950/50 dark:text-violet-300 dark:ring-violet-800/40",
  "bg-amber-50 text-amber-700 ring-amber-200/60 dark:bg-amber-950/50 dark:text-amber-300 dark:ring-amber-800/40",
  "bg-rose-50 text-rose-700 ring-rose-200/60 dark:bg-rose-950/50 dark:text-rose-300 dark:ring-rose-800/40",
  "bg-cyan-50 text-cyan-700 ring-cyan-200/60 dark:bg-cyan-950/50 dark:text-cyan-300 dark:ring-cyan-800/40",
];

/**
 * 修复 CommonMark 解析器对中文全角标点 + ** 强调标记的兼容问题。
 * micromark 遵循 CommonMark 规范，全角标点（如 ）、】、》）被视为 Unicode 标点，
 * 导致紧跟其后的 ** 不被识别为强调结束符。
 * 解决方案：在全角标点与 ** 之间插入零宽空格（U+200B）。
 */
function fixCjkEmphasis(text: string): string {
  return text.replace(
    /([）」】》）」】》!！?？。，、；：])\*\*/g,
    "$1\u200B**"
  );
}

function Markdown({ children }: { children: string }) {
  return (
    <ReactMarkdown
      components={{
        p: ({ children }) => (
          <p className="text-sm text-foreground leading-relaxed mb-3 last:mb-0">
            {children}
          </p>
        ),
        strong: ({ children }) => (
          <strong className="font-semibold">{children}</strong>
        ),
        ul: ({ children }) => (
          <ul className="text-sm text-foreground space-y-1.5 list-disc pl-6 mb-3 last:mb-0">
            {children}
          </ul>
        ),
        ol: ({ children }) => (
          <ol className="text-sm text-foreground space-y-1.5 list-decimal pl-6 mb-3 last:mb-0">
            {children}
          </ol>
        ),
        li: ({ children }) => <li className="[&>p]:mb-1 [&>p:last-child]:mb-0">{children}</li>,
        a: ({ href, children }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary underline underline-offset-2"
          >
            {children}
          </a>
        ),
        code: ({ children }) => (
          <code className="bg-muted px-1 py-0.5 rounded text-xs font-mono">
            {children}
          </code>
        ),
      }}
    >
      {fixCjkEmphasis(children)}
    </ReactMarkdown>
  );
}

interface PaperDetailProps {
  paper: PaperDetailType | null;
  loading?: boolean;
  onBack?: () => void;
}

export function PaperDetail({ paper, loading, onBack }: PaperDetailProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground gap-2">
        <Loader2 className="h-4 w-4 animate-spin" />
        <p className="text-sm">加载论文详情...</p>
      </div>
    );
  }

  if (!paper) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <p className="text-sm">选择一篇论文查看详情</p>
      </div>
    );
  }

  return (
    <ScrollArea className="h-full">
      <div className="py-6 px-4 md:py-8 md:px-8 lg:px-10 max-w-5xl mx-auto">
        {/* Mobile back button */}
        {onBack && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onBack}
            className="mb-6 -ml-2 md:hidden text-muted-foreground"
          >
            <ArrowLeft className="h-4 w-4 mr-1" />
            返回列表
          </Button>
        )}

        {/* Title + score */}
        <div className="flex items-start justify-between gap-4">
          <h1 className="text-xl md:text-2xl font-bold leading-snug tracking-tight">
            {paper.title}
          </h1>
          <div className="shrink-0 md:mt-0.5">
            <ScoreBadge score={paper.relevance_score} />
          </div>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-1.5 mt-4">
          {paper.tags.map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs font-normal">
              {tag}
            </Badge>
          ))}
        </div>

        {/* Taxonomy */}
        {paper.taxonomy && (
          <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-muted-foreground">
            <span className="inline-flex items-center gap-1">
              <Globe className="h-3 w-3 shrink-0" />
              <span className="text-foreground/40">领域</span>
              {paper.taxonomy.domain}
            </span>
            <span className="inline-flex items-center gap-1">
              <FlaskConical className="h-3 w-3 shrink-0" />
              <span className="text-foreground/40">类型</span>
              {paper.taxonomy.research_type}
            </span>
          </div>
        )}

        {/* Meta */}
        <div className="mt-4 space-y-1 text-sm text-muted-foreground">
          <p>
            {paper.authors.slice(0, 5).join(", ")}
            {paper.author_count > 5 && ` 等 ${paper.author_count} 位作者`}
          </p>
          <p className="text-xs">
            {paper.categories.join(" / ")} · {paper.published}
          </p>
        </div>

        {/* Links */}
        <div className="flex items-center gap-2 mt-5">
          <a href={paper.arxiv_url} target="_blank" rel="noopener noreferrer">
            <Button variant="outline" size="sm" className="text-xs h-8 gap-1.5">
              <ExternalLink className="h-3.5 w-3.5" /> arxiv
            </Button>
          </a>
          <a href={paper.pdf_url} target="_blank" rel="noopener noreferrer">
            <Button variant="outline" size="sm" className="text-xs h-8 gap-1.5">
              <FileText className="h-3.5 w-3.5" /> PDF
            </Button>
          </a>
          {paper.github_url && (
            <a href={paper.github_url} target="_blank" rel="noopener noreferrer">
              <Button variant="outline" size="sm" className="text-xs h-8 gap-1.5">
                <Github className="h-3.5 w-3.5" /> Code
              </Button>
            </a>
          )}
        </div>

        {/* Divider */}
        <div className="my-8 border-t" />

        {/* Content */}
        {isQAFormat(paper) ? (
          <div className="space-y-8">
            {paper.qa_pairs!.map((pair, i) => (
              <div key={i}>
                <div className="flex items-start gap-3 mb-3">
                  <span
                    className={`inline-flex items-center justify-center text-[11px] font-semibold rounded-md px-2 py-0.5 ring-1 shrink-0 ${QA_COLORS[i % QA_COLORS.length]}`}
                  >
                    Q{i + 1}
                  </span>
                  <h3 className="text-sm font-semibold leading-snug">
                    {pair.question}
                  </h3>
                </div>
                <div className="pl-[calc(2rem+0.75rem)]">
                  <Markdown>{pair.answer}</Markdown>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-6">
            {paper.chinese_summary && (
              <div>
                <h3 className="text-sm font-semibold mb-2">中文摘要</h3>
                <Markdown>{paper.chinese_summary}</Markdown>
              </div>
            )}
            {paper.core_contributions && paper.core_contributions.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold mb-2">核心贡献</h3>
                <ul className="text-sm text-foreground space-y-1.5 list-disc list-inside">
                  {paper.core_contributions.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
            )}
            {paper.analysis && (
              <div>
                <h3 className="text-sm font-semibold mb-2">文章解读</h3>
                <Markdown>{paper.analysis}</Markdown>
              </div>
            )}
          </div>
        )}
      </div>
    </ScrollArea>
  );
}
