export interface QAPair {
  question: string;
  answer: string;
}

export interface PaperTaxonomy {
  capability: string[];
  domain: string;
  research_type: string;
}

export interface PaperAttributes {
  base_model: string;
  key_technique: string;
  primary_benchmark: string;
}

// papers.json 中的轻量条目（列表展示用）
export interface PaperMeta {
  arxiv_id: string;
  title: string;
  authors: string[];
  author_count: number;
  categories: string[];
  arxiv_url: string;
  pdf_url: string;
  github_url?: string;
  published: string;
  tags: string[];
  relevance_score: number;
  md_path: string;
  version?: number;
  taxonomy?: PaperTaxonomy;
  attributes?: PaperAttributes;
}

// 从 .md 文件解析的完整详情
export interface PaperDetail extends PaperMeta {
  summary: string;
  qa_pairs?: QAPair[];
  chinese_summary?: string;
  core_contributions?: string[];
  analysis?: string;
}

export interface IndexData {
  available_dates: string[];
}
