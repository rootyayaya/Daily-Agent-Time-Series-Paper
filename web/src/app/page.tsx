"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { IndexData, PaperMeta, PaperDetail as PaperDetailType } from "@/types/paper";
import { fetchIndex, fetchPapersForDate, fetchPaperDetail, getAvailableDates, formatDateStr } from "@/lib/data";
import { DatePicker } from "@/components/date-picker";
import { PaperSidebar } from "@/components/paper-sidebar";
import { PaperDetail } from "@/components/paper-detail";
import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight, Github } from "lucide-react";

export default function Home() {
  const [index, setIndex] = useState<IndexData | null>(null);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>();
  const [papers, setPapers] = useState<PaperMeta[]>([]);
  const [dateStr, setDateStr] = useState("");
  const [loading, setLoading] = useState(true);
  const [loadingPapers, setLoadingPapers] = useState(false);
  const [selectedPaperId, setSelectedPaperId] = useState<string | null>(null);
  const [selectedDetail, setSelectedDetail] = useState<PaperDetailType | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [mobileShowDetail, setMobileShowDetail] = useState(false);

  const loadDetail = useCallback(async (meta: PaperMeta) => {
    setLoadingDetail(true);
    try {
      const detail = await fetchPaperDetail(meta);
      setSelectedDetail(detail);
    } catch {
      setSelectedDetail({ ...meta, summary: "" });
    } finally {
      setLoadingDetail(false);
    }
  }, []);

  useEffect(() => {
    fetchIndex().then(async (idx) => {
      setIndex(idx);
      if (idx.available_dates && idx.available_dates.length > 0) {
        const latest = idx.available_dates[0];
        const date = new Date(latest + "T00:00:00");
        setSelectedDate(date);
        setDateStr(latest);
        const dayPapers = await fetchPapersForDate(latest);
        setPapers(dayPapers);
        if (dayPapers.length > 0) {
          setSelectedPaperId(dayPapers[0].arxiv_id);
          loadDetail(dayPapers[0]);
        }
      }
      setLoading(false);
    });
  }, [loadDetail]);

  const handleDateSelect = useCallback(
    async (date: Date | undefined) => {
      if (!date || !index) return;
      setSelectedDate(date);
      const str = formatDateStr(date);
      setDateStr(str);
      setLoadingPapers(true);
      setSelectedPaperId(null);
      setSelectedDetail(null);
      setMobileShowDetail(false);
      const dayPapers = await fetchPapersForDate(str);
      setPapers(dayPapers);
      if (dayPapers.length > 0) {
        setSelectedPaperId(dayPapers[0].arxiv_id);
        loadDetail(dayPapers[0]);
      }
      setLoadingPapers(false);
    },
    [index, loadDetail]
  );

  const navigateDate = useCallback(
    async (direction: -1 | 1) => {
      if (!index || !dateStr) return;
      const dates = index.available_dates;
      const idx = dates.indexOf(dateStr);
      const nextIdx = idx - direction;
      if (nextIdx >= 0 && nextIdx < dates.length) {
        const nextStr = dates[nextIdx];
        const nextDate = new Date(nextStr + "T00:00:00");
        setSelectedDate(nextDate);
        setDateStr(nextStr);
        setLoadingPapers(true);
        setSelectedPaperId(null);
        setSelectedDetail(null);
        setMobileShowDetail(false);
        const dayPapers = await fetchPapersForDate(nextStr);
        setPapers(dayPapers);
        if (dayPapers.length > 0) {
          setSelectedPaperId(dayPapers[0].arxiv_id);
          loadDetail(dayPapers[0]);
        }
        setLoadingPapers(false);
      }
    },
    [index, dateStr, loadDetail]
  );

  const handlePaperSelect = useCallback(
    (arxivId: string) => {
      setSelectedPaperId(arxivId);
      setMobileShowDetail(true);
      const meta = papers.find((p) => p.arxiv_id === arxivId);
      if (meta) {
        loadDetail(meta);
      }
    },
    [papers, loadDetail]
  );

  const handleMobileBack = useCallback(() => {
    setMobileShowDetail(false);
  }, []);

  const touchStartRef = useRef<{ x: number; y: number } | null>(null);

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    touchStartRef.current = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  }, []);

  const handleTouchEnd = useCallback(
    (e: React.TouchEvent) => {
      if (!touchStartRef.current || !mobileShowDetail) return;
      const deltaX = e.changedTouches[0].clientX - touchStartRef.current.x;
      const deltaY = Math.abs(e.changedTouches[0].clientY - touchStartRef.current.y);
      if (deltaX > 80 && deltaX > 2 * deltaY) {
        handleMobileBack();
      }
      touchStartRef.current = null;
    },
    [mobileShowDetail, handleMobileBack]
  );

  const availableDates = index ? getAvailableDates(index) : [];

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="shrink-0 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-50">
        {/* Mobile header: flex-wrap, no title */}
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
            {papers.length > 0 && (
              <span className="text-xs text-muted-foreground tabular-nums">
                {papers.length} 篇论文
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
        {/* Desktop header: 3-column grid */}
        <div className="hidden md:grid grid-cols-[1fr_auto_1fr] h-14 items-center px-8">
          <div className="flex items-center gap-2.5">
            <h1 className="text-base font-semibold tracking-tight">Agentic Time Series Papers</h1>
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
            {papers.length > 0 && (
              <span className="text-xs text-muted-foreground tabular-nums">
                {papers.length} 篇论文
              </span>
            )}
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Main content */}
      {loading ? (
        <div className="flex-1 flex items-center justify-center text-muted-foreground">
          <p className="text-sm">加载中...</p>
        </div>
      ) : loadingPapers ? (
        <div className="flex-1 flex items-center justify-center text-muted-foreground">
          <p className="text-sm">加载论文数据...</p>
        </div>
      ) : (
        <div className="flex-1 flex min-h-0">
          {/* Sidebar */}
          <aside
            className={`w-full md:w-[340px] md:shrink-0 md:border-r ${
              mobileShowDetail ? "hidden md:block" : "block"
            }`}
          >
            <PaperSidebar
              papers={papers}
              selectedId={selectedPaperId}
              onSelect={handlePaperSelect}
            />
          </aside>

          {/* Detail */}
          <main
            className={`flex-1 min-w-0 ${
              mobileShowDetail ? "block" : "hidden md:block"
            }`}
            onTouchStart={handleTouchStart}
            onTouchEnd={handleTouchEnd}
          >
            <PaperDetail
              paper={selectedDetail}
              loading={loadingDetail}
              onBack={handleMobileBack}
            />
          </main>
        </div>
      )}
    </div>
  );
}
