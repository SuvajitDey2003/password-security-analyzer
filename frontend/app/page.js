"use client";

import { useEffect, useState } from "react";
import { analyzePassword } from "@/lib/api";

export default function Home() {
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // 🔒 Guard: do not analyze very short passwords
    if (!password || password.length < 6) {
      setResult(null);
      setError("");
      return;
    }

    const timer = setTimeout(async () => {
      try {
        setLoading(true);
        const data = await analyzePassword(password);
        setResult(data);
        setError("");
      } catch (err) {
        setError(err.message);
        setResult(null);
      } finally {
        setLoading(false);
      }
    }, 1200); // ⏱ Increased debounce (important)

    return () => clearTimeout(timer);
  }, [password]);

  const strengthColor = result
    ? {
        Weak: "red",
        Moderate: "orange",
        Strong: "green",
      }[result.strength]
    : "gray";

  const strengthPercent = result ? result.score : 0;

  return (
    <main className="container">
      <h1>Password Security Analyzer</h1>

      <input
        type={showPassword ? "text" : "password"}
        placeholder="Enter password (min 6 characters)"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <label className="checkbox">
        <input
          type="checkbox"
          checked={showPassword}
          onChange={() => setShowPassword(!showPassword)}
        />
        Show password
      </label>

      {loading && <p className="info">Analyzing…</p>}
      {error && <p className="error">{error}</p>}

      {result && (
        <>
          {/* 🔥 Strength Bar */}
          <div className="strength-bar">
            <div
              className="strength-fill"
              style={{
                width: `${strengthPercent}%`,
                backgroundColor: strengthColor,
              }}
            />
          </div>

          <p style={{ color: strengthColor }}>
            <b>Strength:</b> {result.strength}
          </p>

          <p><b>Score:</b> {result.score}</p>
          <p><b>Entropy:</b> {result.entropy}</p>

          {result.breach_count > 0 && (
            <p><b>Breach Count:</b> {result.breach_count}</p>
          )}

          {result.issues.length > 0 && (
            <ul>
              {result.issues.map((issue, i) => (
                <li key={i}>{issue}</li>
              ))}
            </ul>
          )}
        </>
      )}
    </main>
  );
}
