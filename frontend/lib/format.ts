/**
 * Currency and Timezone formatting utilities.
 * Enforces Asia/Kolkata (IST) for all user-facing clocks and timestamps.
 * Enforces standard finite USD formatting with thousands separators.
 */

const USD_FORMATTER = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

/**
 * Format any number or string amount as a clean USD value with commas.
 * Handles NaN, Infinity, negative, zero, and extreme values safely.
 */
export function formatUSD(amount: number | string | null | undefined): string {
  if (amount == null) return "$0.00";
  const num = typeof amount === "number" ? amount : parseFloat(String(amount));
  if (isNaN(num) || !isFinite(num) || num <= 0) return "$0.00";

  // If a legacy extreme value exists in historical data (e.g., 1e+207 or 6.7e+38),
  // cap the display safely with a clear indicator rather than scientific notation.
  if (num > 10_000_000) {
    return "$10,000,000.00+";
  }

  return USD_FORMATTER.format(num);
}

/**
 * Live clock formatter displaying Indian Standard Time (IST, Asia/Kolkata).
 * Daylight-independent (UTC+05:30 year-round).
 */
export function formatISTClock(date: Date = new Date()): string {
  try {
    const timeStr = new Intl.DateTimeFormat("en-IN", {
      timeZone: "Asia/Kolkata",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    }).format(date);

    const dateStr = new Intl.DateTimeFormat("en-IN", {
      timeZone: "Asia/Kolkata",
      day: "2-digit",
      month: "short",
      year: "numeric",
    }).format(date);

    return `${dateStr} · ${timeStr} IST`;
  } catch {
    return date.toISOString().slice(11, 19) + " UTC";
  }
}

/**
 * Format a timestamp into an unambiguous Indian date and time string:
 * e.g. "24 Oct 2026, 15:30:00 IST"
 */
export function formatISTDateTime(isoOrDate: string | number | Date | null | undefined): string {
  if (!isoOrDate) return "—";
  try {
    const d = typeof isoOrDate === "object" ? isoOrDate : new Date(isoOrDate);
    if (isNaN(d.getTime())) return String(isoOrDate);

    return (
      new Intl.DateTimeFormat("en-IN", {
        timeZone: "Asia/Kolkata",
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
      }).format(d) + " IST"
    );
  } catch {
    return String(isoOrDate);
  }
}

/**
 * Format a timestamp into a short time-only IST string: e.g. "15:30:00 IST"
 */
export function formatISTTime(isoOrDate: string | number | Date | null | undefined): string {
  if (!isoOrDate) return "—";
  try {
    const d = typeof isoOrDate === "object" ? isoOrDate : new Date(isoOrDate);
    if (isNaN(d.getTime())) return "—";

    return (
      new Intl.DateTimeFormat("en-IN", {
        timeZone: "Asia/Kolkata",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
      }).format(d) + " IST"
    );
  } catch {
    return "—";
  }
}

/**
 * Format current Asia/Kolkata time for <input type="datetime-local"> (YYYY-MM-DDTHH:mm).
 */
export function getIndiaInputDateTime(date: Date = new Date()): string {
  try {
    const formatter = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Kolkata",
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
    const parts = formatter.formatToParts(date);
    const getVal = (type: string) => parts.find((p) => p.type === type)?.value || "00";
    return `${getVal("year")}-${getVal("month")}-${getVal("day")}T${getVal("hour")}:${getVal("minute")}`;
  } catch {
    return date.toISOString().slice(0, 16);
  }
}

/**
 * Parse a datetime-local input string (which was entered as IST) into a valid UTC ISO-8601 string.
 * Appends +05:30 directly so that no local browser offset subtraction or double-conversion occurs.
 */
export function parseISTInputToISO(datetimeLocalVal: string): string | undefined {
  if (!datetimeLocalVal) return undefined;
  try {
    // If input is YYYY-MM-DDTHH:mm, append :00+05:30
    const normalized = datetimeLocalVal.length === 16 ? `${datetimeLocalVal}:00+05:30` : `${datetimeLocalVal}+05:30`;
    const d = new Date(normalized);
    if (isNaN(d.getTime())) return undefined;
    return d.toISOString();
  } catch {
    return undefined;
  }
}
