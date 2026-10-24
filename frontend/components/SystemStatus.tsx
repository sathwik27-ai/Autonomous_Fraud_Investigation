"use client";

import { API } from "@/lib/api";

type StatusDot = "good" | "warning" | "critical" | boolean | undefined;

function getDotColor(status: StatusDot): string {
  if (status === "good" || status === true) return "var(--status-good)";
  if (status === "warning") return "var(--status-warning)";
  if (status === "critical" || status === false) return "var(--status-critical)";
  return "var(--muted)";
}

export default function SystemStatus({
  online,
  latency,
  graphBackend,
  graphConnected,
  engine,
  environment,
  loading = false,
}: {
  online: boolean;
  latency: number | null;
  graphBackend: string | null;
  graphConnected?: boolean | null;
  engine: string | null;
  environment?: string | null;
  loading?: boolean;
}) {
  // Graph backend display logic
  let graphLabel = "unavailable";
  let graphStatus: StatusDot = "critical";

  if (loading && !graphBackend) {
    graphLabel = "connecting...";
    graphStatus = "warning";
  } else if (graphBackend) {
    if (graphConnected === false) {
      graphLabel = `${graphBackend} (unreachable)`;
      graphStatus = "critical";
    } else if (graphBackend === "neo4j") {
      graphLabel = graphConnected ? "neo4j (connected)" : "neo4j";
      graphStatus = "good";
    } else if (graphBackend === "memory") {
      graphLabel = "in-memory (fallback)";
      graphStatus = "warning";
    } else {
      graphLabel = graphBackend;
      graphStatus = "good";
    }
  } else if (online) {
    graphLabel = loading ? "connecting..." : "unavailable";
    graphStatus = loading ? "warning" : "critical";
  } else {
    graphLabel = "disconnected";
    graphStatus = "critical";
  }

  // Environment display logic
  let envLabel = "unavailable";
  let envStatus: StatusDot = "critical";
  if (loading && !environment) {
    envLabel = "connecting...";
    envStatus = "warning";
  } else if (environment) {
    envLabel = environment;
    envStatus = "good";
  } else if (online) {
    envLabel = "production";
    envStatus = "good";
  }

  // Decision engine display logic
  let engineLabel = "unavailable";
  let engineStatus: StatusDot = "critical";
  if (loading && !engine) {
    engineLabel = "connecting...";
    engineStatus = "warning";
  } else if (engine) {
    engineLabel = engine;
    engineStatus = "good";
  } else if (online) {
    engineLabel = "rules";
    engineStatus = "good";
  }

  const rows: { label: string; value: string; status?: StatusDot }[] = [
    { label: "API endpoint", value: API.replace(/^https?:\/\//, ""), status: online ? "good" : "critical" },
    { label: "Environment", value: envLabel, status: envStatus },
    {
      label: "Round-trip latency",
      value: latency == null ? "—" : `${latency} ms`,
      status: latency != null && latency < 500 ? "good" : latency != null ? "warning" : "critical",
    },
    {
      label: "Graph backend",
      value: graphLabel,
      status: graphStatus,
    },
    {
      label: "Decision engine",
      value: engineLabel,
      status: engineStatus,
    },
    { label: "Timezone", value: "Asia/Kolkata (IST · UTC+05:30)", status: "good" },
    { label: "Thresholds", value: "review ≥ 0.50 · block ≥ 0.80" },
  ];

  return (
    <div className="card p-5">
      <div className="kicker mb-0.5">Infrastructure</div>
      <div className="mb-3 text-sm font-semibold">System Status</div>
      <dl className="space-y-2">
        {rows.map((r) => (
          <div key={r.label} className="flex items-center justify-between gap-3 text-[11px]">
            <dt style={{ color: "var(--muted)" }}>{r.label}</dt>
            <dd className="mono flex items-center gap-1.5" style={{ color: "var(--ink-2)" }}>
              {r.status !== undefined && (
                <span
                  className="inline-block h-1.5 w-1.5 rounded-full"
                  style={{ background: getDotColor(r.status) }}
                />
              )}
              {r.value}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
