export interface TaxonomyEntry {
  arxiv_id: string;
  title: string;
  relevance_score: number;
  taxonomy: {
    capability: string[];
    domain: string;
    research_type: string;
  };
  attributes: {
    base_model: string;
    key_technique: string;
    primary_benchmark: string;
  };
  content_source: string;
}

export type TaxonomyData = Record<string, TaxonomyEntry>;

export type DimensionKey = "capability" | "domain" | "research_type";
