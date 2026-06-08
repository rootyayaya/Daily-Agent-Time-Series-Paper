"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { DimensionKey } from "@/types/taxonomy";
import { IndexData, PaperMeta } from "@/types/paper";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import { DatePicker } from "@/components/date-picker";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import { Bar, BarChart, XAxis, YAxis } from "recharts";
import { ChevronLeft, ChevronRight, Github, Tags } from "lucide-react";
import Link from "next/link";
import {
  fetchIndex,
  getAvailableDates,
  formatDateStr,
} from "@/lib/data";

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || "";

// Pre-defined tag lists for each dimension (stable ordering + colors)
const CAPABILITY_TAGS = [
  "Time-Series Representation",
  "Semantic Captioning",
  "Report Generation",
  "Fault Diagnosis",
  "Anomaly Detection",
  "Forecasting",
  "Evidence Routing",
  "Tool Use & API Interaction",
  "RAG & Knowledge Retrieval",
  "Memory & Context Management",
  "Multi-Agent Reasoning",
  "Skill Learning & Optimization",
];

const DOMAIN_TAGS = [
  "Industrial Systems",
  "Predictive Maintenance",
  "Energy & Power",
  "Battery Management",
  "Manufacturing",
  "Transportation",
  "Healthcare Signals",
  "Finance & Trading",
  "Scientific Instruments",
  "General Time Series",
  "Agent Infrastructure",
];

const RESEARCH_TYPE_TAGS = [
  "New Method/Model",
  "New Algorithm",
  "Benchmark/Evaluation",
  "Empirical Study/Analysis",
  "System/Tooling/Library",
  "Survey/Position Paper",
];

const PALETTE = [
  "hsl(221 83% 53%)",
  "hsl(142 71% 45%)",
  "hsl(24 95% 53%)",
  "hsl(262 83% 58%)",
  "hsl(346 77% 50%)",
  "hsl(199 89% 48%)",
  "hsl(47 96% 53%)",
  "hsl(173 80% 40%)",
  "hsl(292 84% 61%)",
  "hsl(15 75% 48%)",
  "hsl(174 60% 51%)",
  "hsl(330 65% 55%)",
];

interface DayTaxonomy {
  date: string;
  entries: PaperMeta[];
}

function getTagCountsForDay(
  entries: PaperMeta[],
  dimension: DimensionKey
): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const entry of entries) {
    if (!entry.taxonomy) continue;
    if (dimension === "capability") {
      for (const cap of entry.taxonomy.capability) {
        counts[cap] = (counts[cap] || 0) + 1;
      }
    } else {
      const val = entry.taxonomy[dimension];
      counts[val] = (counts[val] || 0) + 1;
    }
  }
  return counts;
}

function buildChartData(
  days: DayTaxonomy[],
  dimension: DimensionKey,
  allTags: string[]
) {
  return days.map((day) => {
    const counts = getTagCountsForDay(day.entries, dimension);
    const row: Record<string, string | number> = {
      date: day.date.slice(5), // "03-05" format
    };
    for (const tag of allTags) {
      row[tag] = counts[tag] || 0;
    }
    return row;
  });
}

function buildChartConfig(
  allTags: string[]
): ChartConfig {
  const config: ChartConfig = {};
  for (let i = 0; i < allTags.length; i++) {
    config[allTags[i]] = {
      label: allTags[i],
      color: PALETTE[i % PALETTE.length],
    };
  }
  return config;
}

function DimensionStackedChart({
  days,
  dimension,
  label,
  allTags,
}: {
  days: DayTaxonomy[];
  dimension: DimensionKey;
  label: string;
  allTags: string[];
}) {
  const data = useMemo(
    () => buildChartData(days, dimension, allTags),
    [days, dimension, allTags]
  );

  const chartConfig = useMemo(() => buildChartConfig(allTags), [allTags]);

  // Only show tags that have at least 1 paper across all days
  const activeTags = useMemo(() => {
    return allTags.filter((tag) =>
      data.some((row) => (row[tag] as number) > 0)
    );
  }, [allTags, data]);

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-baseline gap-2 mb-1.5 px-1">
        <h2 className="text-sm font-semibold">{label}</h2>
        <span className="text-xs text-muted-foreground">
          {activeTags.length} 个标签
        </span>
      </div>
      <div className="flex-1 min-h-0 rounded-lg bg-muted/30 p-2">
        <ChartContainer config={chartConfig} className="h-full w-full">
          <BarChart
            accessibilityLayer
            data={data}
            margin={{ left: 0, right: 0, top: 4, bottom: 0 }}
          >
            <XAxis
              dataKey="date"
              tickLine={false}
              tickMargin={6}
              axisLine={false}
              tick={{ fontSize: 11 }}
            />
            <YAxis
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 10 }}
              width={28}
            />
            <ChartTooltip content={<ChartTooltipContent />} />
            {activeTags.map((tag, i) => (
              <Bar
                key={tag}
                dataKey={tag}
                stackId="a"
                fill={PALETTE[allTags.indexOf(tag) % PALETTE.length]}
                radius={
                  i === activeTags.length - 1
                    ? [3, 3, 0, 0]
                    : [0, 0, 0, 0]
                }
                isAnimationActive={false}
              />
            ))}
          </BarChart>
        </ChartContainer>
      </div>
    </div>
  );
}

export default function TaxonomyPage() {
  const [index, setIndex] = useState<IndexData | null>(null);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>();
  const [dateStr, setDateStr] = useState("");
  const [days, setDays] = useState<DayTaxonomy[]>([]);
  const [loading, setLoading] = useState(true);
  const [paperCount, setPaperCount] = useState(0);

  // Load taxonomy from papers.json for a range of dates (selected + up to 6 days before)
  const loadTaxonomyRange = useCallback(async (centerDate: string) => {
    const center = new Date(centerDate + "T00:00:00");
    const datesToTry: string[] = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date(center);
      d.setDate(d.getDate() - i);
      datesToTry.push(formatDateStr(d));
    }

    const fetches = datesToTry.map(async (ds) => {
      try {
        const [year, month, day] = ds.split("-");
        const res = await fetch(`${BASE_PATH}/data/${year}/${month}/${day}/papers.json`);
        if (res.ok) {
          const papers: PaperMeta[] = await res.json();
          // Only include papers that have taxonomy data
          const withTaxonomy = papers.filter((p) => p.taxonomy);
          if (withTaxonomy.length > 0) {
            return { date: ds, entries: withTaxonomy } as DayTaxonomy;
          }
        }
      } catch {}
      return null;
    });

    const results = (await Promise.all(fetches)).filter(
      (r): r is DayTaxonomy => r !== null
    );

    setDays(results);
    const selected = results.find((r) => r.date === centerDate);
    setPaperCount(selected ? selected.entries.length : 0);
  }, []);

  useEffect(() => {
    (async () => {
      const idx = await fetchIndex();
      setIndex(idx);
      const latestDate = idx.available_dates?.[0] || "2026-03-04";
      const defaultDate = latestDate;
      setDateStr(defaultDate);
      setSelectedDate(new Date(defaultDate + "T00:00:00"));
      await loadTaxonomyRange(defaultDate);
      setLoading(false);
    })();
  }, [loadTaxonomyRange]);

  const handleDateSelect = useCallback(
    async (date: Date | undefined) => {
      if (!date || !index) return;
      const ds = formatDateStr(date);
      setDateStr(ds);
      setSelectedDate(date);
      setLoading(true);
      await loadTaxonomyRange(ds);
      setLoading(false);
    },
    [index, loadTaxonomyRange]
  );

  const navigateDate = useCallback(
    async (direction: -1 | 1) => {
      if (!index || !dateStr) return;
      const dates = index.available_dates;
      const idx = dates.indexOf(dateStr);
      const nextIdx = idx - direction;
      if (nextIdx >= 0 && nextIdx < dates.length) {
        const ds = dates[nextIdx];
        setDateStr(ds);
        setSelectedDate(new Date(ds + "T00:00:00"));
        setLoading(true);
        await loadTaxonomyRange(ds);
        setLoading(false);
      }
    },
    [index, dateStr, loadTaxonomyRange]
  );

  const availableDates = index ? getAvailableDates(index) : [];

  return (
    <div className="h-screen flex flex-col bg-background overflow-hidden">
      {/* Header */}
      <header className="shrink-0 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-50">
        {/* Mobile header */}
        <div className="flex md:hidden h-12 items-center justify-between px-3">
          {dateStr && (
            <div className="flex items-center gap-0.5 rounded-lg border bg-muted/40 px-1 py-0.5">
              <Button
                variant="ghost"
                size="icon"
                className="h-7 w-7 rounded-md"
                onClick={() => navigateDate(-1)}
                disabled={
                  !index ||
                  index.available_dates.indexOf(dateStr) >=
                    index.available_dates.length - 1
                }
              >
                <ChevronLeft className="h-3.5 w-3.5" />
              </Button>
              <DatePicker
                selected={selectedDate}
                onSelect={handleDateSelect}
                availableDates={availableDates}
                dateStr={dateStr}
              />
              <Button
                variant="ghost"
                size="icon"
                className="h-7 w-7 rounded-md"
                onClick={() => navigateDate(1)}
                disabled={
                  !index || index.available_dates.indexOf(dateStr) <= 0
                }
              >
                <ChevronRight className="h-3.5 w-3.5" />
              </Button>
            </div>
          )}
          <div className="flex items-center gap-2">
            {paperCount > 0 && (
              <span className="text-xs text-muted-foreground tabular-nums">
                {paperCount} 篇
              </span>
            )}
            <a
              href="https://github.com/rootyayaya/Daily-Agent-Time-Series-Paper"
              target="_blank"
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              <Github className="h-4 w-4" />
            </a>
            <ThemeToggle />
          </div>
        </div>
        {/* Desktop header */}
        <div className="hidden md:grid grid-cols-[1fr_auto_1fr] h-14 items-center px-8">
          <div className="flex items-center gap-2.5">
            <h1 className="text-base font-semibold tracking-tight">
              Agentic Time Series Papers
            </h1>
            <span className="text-xs text-muted-foreground hidden lg:inline">
              每日 arXiv 时序智能体论文摘要
            </span>
            <a
              href="https://github.com/rootyayaya/Daily-Agent-Time-Series-Paper"
              target="_blank"
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              <Github className="h-4 w-4" />
            </a>
          </div>
          <div className="flex items-center justify-center">
            {dateStr && (
              <div className="flex items-center gap-0.5 rounded-lg border bg-muted/40 px-1 py-0.5">
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-7 w-7 rounded-md"
                  onClick={() => navigateDate(-1)}
                  disabled={
                    !index ||
                    index.available_dates.indexOf(dateStr) >=
                      index.available_dates.length - 1
                  }
                >
                  <ChevronLeft className="h-3.5 w-3.5" />
                </Button>
                <DatePicker
                  selected={selectedDate}
                  onSelect={handleDateSelect}
                  availableDates={availableDates}
                  dateStr={dateStr}
                />
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-7 w-7 rounded-md"
                  onClick={() => navigateDate(1)}
                  disabled={
                    !index || index.available_dates.indexOf(dateStr) <= 0
                  }
                >
                  <ChevronRight className="h-3.5 w-3.5" />
                </Button>
              </div>
            )}
          </div>
          <div className="flex items-center justify-end gap-2">
            {paperCount > 0 && (
              <span className="text-xs text-muted-foreground tabular-nums">
                {paperCount} 篇论文
              </span>
            )}
            <Link href="/">
              <Button variant="ghost" size="sm" className="text-xs gap-1">
                论文列表
              </Button>
            </Link>
            <Link href="/taxonomy">
              <Button variant="secondary" size="sm" className="text-xs gap-1">
                <Tags data-icon="inline-start" />
                标签聚合
              </Button>
            </Link>
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Content */}
      {loading ? (
        <div className="flex-1 flex items-center justify-center text-muted-foreground">
          <p className="text-sm">加载分类数据...</p>
        </div>
      ) : days.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-muted-foreground">
          <p className="text-sm">该日期范围暂无分类数据</p>
        </div>
      ) : (
        <main className="flex-1 min-h-0 grid grid-cols-1 md:grid-cols-3 gap-2 p-3 md:px-5 md:py-3">
          <DimensionStackedChart
            days={days}
            dimension="capability"
            label="核心能力"
            allTags={CAPABILITY_TAGS}
          />
          <DimensionStackedChart
            days={days}
            dimension="domain"
            label="应用领域"
            allTags={DOMAIN_TAGS}
          />
          <DimensionStackedChart
            days={days}
            dimension="research_type"
            label="研究类型"
            allTags={RESEARCH_TYPE_TAGS}
          />
        </main>
      )}
    </div>
  );
}
