import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import "./style.css";

const API = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");

function App() {
  const [metrics, setMetrics] = useState<any>({});
  const [topEvents, setTopEvents] = useState<any[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    Promise.all([
      fetch(`${API}/analytics/metrics`, { signal: controller.signal }).then((response) => {
        if (!response.ok) throw new Error(`Metrics request failed (${response.status})`);
        return response.json();
      }),
      fetch(`${API}/analytics/top-events`, { signal: controller.signal }).then((response) => {
        if (!response.ok) throw new Error(`Top events request failed (${response.status})`);
        return response.json();
      }),
    ])
      .then(([nextMetrics, nextEvents]) => {
        setMetrics(nextMetrics);
        setTopEvents(nextEvents);
        setError("");
      })
      .catch((cause) => {
        if (cause.name !== "AbortError") setError("Could not load analytics. Check that the API is running.");
      });
    return () => controller.abort();
  }, []);

  return (
    <main>
      <header>
        <div><b>DATAPULSE</b><h1>Analytics overview</h1><p>Product-event intelligence dashboard.</p></div>
        <span>{error ? "● API unavailable" : "● Analytics dashboard"}</span>
      </header>
      {error && <p role="alert" className="error-message">{error}</p>}
      <section className="cards">
        {[
          ["Events", metrics.events ?? 0],
          ["Users", metrics.users ?? 0],
          ["Sessions", metrics.sessions ?? 0],
          ["Event value", new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(metrics.revenue ?? 0)],
        ].map(([label, value]) => (
          <article key={label}><small>{label}</small><strong>{value}</strong></article>
        ))}
      </section>
      <section className="panel">
        <h2>Top events</h2>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={topEvents}>
            <XAxis dataKey="event" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count" />
          </BarChart>
        </ResponsiveContainer>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
