import { IndexData, PaperMeta, PaperDetail, QAPair } from "@/types/paper";

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || "";

let cachedIndex: IndexData | null = null;
const cachedDayPapers: Record<string, PaperMeta[]> = {};

export async function fetchIndex(): Promise<IndexData> {
  if (cachedIndex) return cachedIndex;

  try {
    const res = await fetch(`${BASE_PATH}/data/index.json`);
    if (!res.ok) {
      return { available_dates: [] };
    }
    const data: IndexData = await res.json();
    cachedIndex = data;
    return data;
  } catch {
    return { available_dates: [] };
  }
}

export async function fetchPapersForDate(dateStr: string): Promise<PaperMeta[]> {
  if (cachedDayPapers[dateStr]) return cachedDayPapers[dateStr];

  try {
    const [year, month, day] = dateStr.split("-");
    const res = await fetch(
      `${BASE_PATH}/data/${year}/${month}/${day}/papers.json`
    );
    if (!res.ok) return [];
    const all: PaperMeta[] = await res.json();
    const papers = all.filter((p) => p.relevance_score >= 8);
    cachedDayPapers[dateStr] = papers;
    return papers;
  } catch {
    return [];
  }
}

/**
 * 从 .md 文件解析论文详情（summary + Q&A 或旧格式内容）。
 * 接收已有的 PaperMeta，只从 .md body 提取内容字段。
 */
export async function fetchPaperDetail(meta: PaperMeta): Promise<PaperDetail> {
  const res = await fetch(`${BASE_PATH}/${meta.md_path}`);
  if (!res.ok) {
    return { ...meta, summary: "" };
  }

  const text = await res.text();
  const body = extractMarkdownBody(text);
  return { ...meta, ...parseMarkdownBody(body) };
}

/** 去掉 YAML frontmatter，返回 markdown body */
function extractMarkdownBody(md: string): string {
  const match = md.match(/^---\r?\n[\s\S]*?\r?\n---\r?\n?([\s\S]*)$/);
  return match ? match[1].trim() : md.trim();
}

/** 解析 markdown body，提取 summary + Q&A 或旧格式内容 */
function parseMarkdownBody(body: string): Omit<PaperDetail, keyof PaperMeta> {
  // 提取原始摘要（## 原始摘要 下的内容）
  const summaryMatch = body.match(
    /## 原始摘要\s*\r?\n\r?\n([\s\S]*?)(?=\r?\n## |$)/
  );
  const summary = summaryMatch ? summaryMatch[1].trim() : "";

  // 尝试提取 Q&A 格式
  const qaSection = body.match(/## Q&A 论文解读\s*\r?\n([\s\S]*?)$/);
  if (qaSection) {
    const qa_pairs = parseQAPairs(qaSection[1]);
    if (qa_pairs.length > 0) {
      return { summary, qa_pairs };
    }
  }

  // 旧格式：中文摘要 / 核心贡献 / 文章解读
  const chineseSummaryMatch = body.match(
    /## 中文摘要\s*\r?\n\r?\n([\s\S]*?)(?=\r?\n## |$)/
  );
  const contributionsMatch = body.match(
    /## 核心贡献\s*\r?\n\r?\n([\s\S]*?)(?=\r?\n## |$)/
  );
  const analysisMatch = body.match(
    /## 文章解读\s*\r?\n\r?\n([\s\S]*?)(?=\r?\n## |$)/
  );

  const chinese_summary = chineseSummaryMatch
    ? chineseSummaryMatch[1].trim()
    : undefined;
  const core_contributions = contributionsMatch
    ? contributionsMatch[1]
        .trim()
        .split(/\r?\n/)
        .map((l) => l.replace(/^-\s*/, "").trim())
        .filter(Boolean)
    : undefined;
  const analysis = analysisMatch ? analysisMatch[1].trim() : undefined;

  return { summary, chinese_summary, core_contributions, analysis };
}

/** 从 Q&A section 提取 QAPair[] */
function parseQAPairs(section: string): QAPair[] {
  const pairs: QAPair[] = [];
  const regex = /### Q\d+[:：]\s*(.*?)\r?\n\r?\n([\s\S]*?)(?=\r?\n### Q\d+|$)/g;
  let match;
  while ((match = regex.exec(section)) !== null) {
    pairs.push({
      question: match[1].trim(),
      answer: match[2].trim(),
    });
  }
  return pairs;
}

export function getAvailableDates(index: IndexData): Date[] {
  return (index.available_dates || []).map((d) => new Date(d + "T00:00:00"));
}

export function formatDateStr(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

export function isQAFormat(paper: PaperDetail): boolean {
  return Array.isArray(paper.qa_pairs) && paper.qa_pairs.length >= 6;
}

export function getPaperSummary(paper: PaperDetail): string {
  if (isQAFormat(paper)) {
    return paper.qa_pairs![5].answer;
  }
  return paper.chinese_summary || "";
}
