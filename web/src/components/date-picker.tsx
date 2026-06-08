"use client";

import { useState } from "react";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { CalendarIcon } from "lucide-react";

interface DatePickerProps {
  selected: Date | undefined;
  onSelect: (date: Date | undefined) => void;
  availableDates: Date[];
  dateStr: string;
}

export function DatePicker({ selected, onSelect, availableDates, dateStr }: DatePickerProps) {
  const [open, setOpen] = useState(false);

  const availableSet = new Set(
    availableDates.map(
      (d) =>
        `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`
    )
  );

  const isDisabled = (date: Date) => {
    const str = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
    return !availableSet.has(str);
  };

  const handleSelect = (date: Date | undefined) => {
    onSelect(date);
    setOpen(false);
  };

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="ghost" size="sm" className="text-sm font-mono h-7 px-2.5 gap-1.5 rounded-md">
          <CalendarIcon className="h-3.5 w-3.5" />
          {dateStr || "选择日期"}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="center">
        <Calendar
          mode="single"
          selected={selected}
          onSelect={handleSelect}
          disabled={isDisabled}
          modifiers={{
            available: availableDates,
          }}
          modifiersClassNames={{
            available: "font-bold text-primary",
          }}
        />
      </PopoverContent>
    </Popover>
  );
}
