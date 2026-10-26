/**
 * AuthGuard.tsx
 * ============================================================================
 * Production-Ready Login & Authentication Guard for CashSense
 * 
 * Features:
 * - Reactive state: useState(false) for isLoggedIn, useState("") for businessName
 * - Persistent session: localStorage caching for seamless reloads
 * - Dark-themed auth screen matching CashSense design tokens
 * - Header integration with business pill badge and Logout action
 * ============================================================================
 */

import React, { useState, useEffect } from "react";

export interface AuthUser {
  businessName: string;
  email: string;
}

interface AuthGuardProps {
  children: (user: AuthUser, onLogout: () => void) => React.ReactNode;
}

export const AuthGuard: React.FC<AuthGuardProps> = ({ children }) => {
  // 1. Reactive Auth Guard State
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [businessName, setBusinessName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [authError, setAuthError] = useState<string | null>(null);
  const [isSignUpMode, setIsSignUpMode] = useState<boolean>(false);

  // 2. LocalStorage Persistence on Initial Mount
  useEffect(() => {
    try {
      const savedAuth = localStorage.getItem("cashsense_auth");
      if (savedAuth) {
        const parsed = JSON.parse(savedAuth);
        if (parsed.isLoggedIn && parsed.businessName) {
          setIsLoggedIn(true);
          setBusinessName(parsed.businessName);
          setEmail(parsed.email || "");
        }
      }
    } catch (e) {
      console.warn("Unable to read localStorage:", e);
    }
  }, []);

  // 3. Login / Signup Handler
  const handleAuthSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setAuthError(null);

    const trimmedBiz = businessName.trim();
    if (!trimmedBiz) {
      setAuthError("Please enter your Business Name (e.g. GALAXY TEX).");
      return;
    }

    if (!email.trim()) {
      setAuthError("Please enter a valid email address.");
      return;
    }

    // Authenticate and persist
    setIsLoggedIn(true);
    try {
      localStorage.setItem(
        "cashsense_auth",
        JSON.stringify({
          isLoggedIn: true,
          businessName: trimmedBiz,
          email: email.trim(),
          loginTime: new Date().toISOString()
        })
      );
    } catch (err) {
      console.warn("Unable to save to localStorage:", err);
    }
  };

  // 4. Quick Demo Preset Handler
  const handleQuickDemo = (demoName: string, demoEmail: string) => {
    setBusinessName(demoName);
    setEmail(demoEmail);
    setIsLoggedIn(true);
    try {
      localStorage.setItem(
        "cashsense_auth",
        JSON.stringify({
          isLoggedIn: true,
          businessName: demoName,
          email: demoEmail,
          loginTime: new Date().toISOString()
        })
      );
    } catch (err) {
      console.warn("Unable to save to localStorage:", err);
    }
  };

  // 5. Logout Handler
  const handleLogout = () => {
    setIsLoggedIn(false);
    setBusinessName("");
    setEmail("");
    setPassword("");
    setAuthError(null);
    try {
      localStorage.removeItem("cashsense_auth");
    } catch (err) {
      console.warn("Unable to clear localStorage:", err);
    }
  };

  // 6. Conditional Render: Show ONLY Auth Screen if not logged in
  if (!isLoggedIn) {
    return (
      <div style={styles.authContainer}>
        <div style={styles.authCard}>
          {/* Logo & Header */}
          <div style={styles.logoHeader}>
            <div style={styles.logoTitle}>
              <span style={{ fontSize: "28px" }}>💰</span>
              <span>CashSense</span>
              <span style={styles.brandBadge}>SECURE AUTH</span>
            </div>
            <p style={styles.logoSubtitle}>
              {isSignUpMode
                ? "Create your business account to protect cash runway and maintain vendor trust."
                : "Sign in to manage your cash runway, invoices, and safe payment actions."}
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleAuthSubmit} style={styles.form}>
            {authError && <div style={styles.errorBanner}>{authError}</div>}

            <div style={styles.inputGroup}>
              <label style={styles.label}>Business / Firm Name</label>
              <input
                type="text"
                placeholder="e.g. GALAXY TEX or Sharma Kirana"
                value={businessName}
                onChange={(e) => setBusinessName(e.target.value)}
                style={styles.input}
                required
              />
            </div>

            <div style={styles.inputGroup}>
              <label style={styles.label}>Email Address</label>
              <input
                type="email"
                placeholder="owner@galaxytex.in"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={styles.input}
                required
              />
            </div>

            <div style={styles.inputGroup}>
              <label style={styles.label}>Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={styles.input}
                required
              />
            </div>

            <div style={styles.buttonRow}>
              <button
                type="submit"
                style={styles.primaryButton}
              >
                {isSignUpMode ? "✨ Create Business Account" : "🔑 Sign In"}
              </button>
              <button
                type="button"
                onClick={() => setIsSignUpMode(!isSignUpMode)}
                style={styles.secondaryButton}
              >
                {isSignUpMode ? "Already registered? Sign In" : "New Business? Create Account"}
              </button>
            </div>
          </form>

          {/* Quick Demo Credentials */}
          <div style={styles.demoSection}>
            <div style={styles.demoTitle}>⚡ One-Click Hackathon Presets:</div>
            <div style={styles.demoButtons}>
              <button
                type="button"
                onClick={() => handleQuickDemo("GALAXY TEX", "accounts@galaxytex.in")}
                style={styles.demoButton}
              >
                🏢 Login as GALAXY TEX
              </button>
              <button
                type="button"
                onClick={() => handleQuickDemo("Sharma Kirana Store", "sharma.kirana@gmail.com")}
                style={styles.demoButton}
              >
                🏪 Login as Sharma Kirana
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // 7. If Logged In: Render Dashboard with user and logout callback
  return (
    <div>
      {/* Top Header Navbar with User Pill & Logout Button */}
      <header style={styles.navbar}>
        <div style={styles.navLeft}>
          <span style={{ fontSize: "24px" }}>💰</span>
          <span style={styles.navBrand}>CashSense</span>
        </div>
        <div style={styles.navRight}>
          <div style={styles.userPill}>
            <span style={styles.activeDot}>🟢</span>
            <span style={styles.userText}>
              🏢 <b>Business:</b> {businessName}
            </span>
          </div>
          <button onClick={handleLogout} style={styles.logoutButton}>
            🚪 Logout
          </button>
        </div>
      </header>

      {/* Main Existing Dashboard */}
      <main>
        {children({ businessName, email }, handleLogout)}
      </main>
    </div>
  );
};

// Modern Dark Theme Styles matching CashSense design tokens
const styles: { [key: string]: React.CSSProperties } = {
  authContainer: {
    minHeight: "100vh",
    backgroundColor: "#0A0F1D",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
    fontFamily: "'Plus Jakarta Sans', sans-serif",
    color: "#F8FAFC"
  },
  authCard: {
    width: "100%",
    maxWidth: "480px",
    backgroundColor: "#111827",
    border: "1px solid #1F2937",
    borderRadius: "18px",
    padding: "36px 32px",
    boxShadow: "0 20px 40px rgba(0, 0, 0, 0.6)"
  },
  logoHeader: {
    marginBottom: "24px",
    textAlign: "center"
  },
  logoTitle: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "10px",
    fontSize: "28px",
    fontWeight: 800,
    color: "#FFFFFF",
    marginBottom: "8px"
  },
  brandBadge: {
    backgroundColor: "#00D26A",
    color: "#04381C",
    fontSize: "11px",
    fontWeight: 800,
    padding: "3px 10px",
    borderRadius: "20px",
    letterSpacing: "0.5px"
  },
  logoSubtitle: {
    fontSize: "14px",
    color: "#94A3B8",
    lineHeight: "1.4",
    margin: 0
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "16px"
  },
  errorBanner: {
    backgroundColor: "rgba(239, 68, 68, 0.15)",
    border: "1px solid #EF4444",
    color: "#FCA5A5",
    padding: "10px 14px",
    borderRadius: "8px",
    fontSize: "13px"
  },
  inputGroup: {
    display: "flex",
    flexDirection: "column",
    gap: "6px"
  },
  label: {
    fontSize: "13px",
    fontWeight: 700,
    color: "#CBD5E1",
    letterSpacing: "0.3px"
  },
  input: {
    backgroundColor: "#1A2234",
    border: "1px solid #2B384E",
    borderRadius: "10px",
    padding: "12px 14px",
    color: "#FFFFFF",
    fontSize: "14px",
    outline: "none"
  },
  buttonRow: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    marginTop: "8px"
  },
  primaryButton: {
    backgroundColor: "#00D26A",
    color: "#04381C",
    border: "none",
    borderRadius: "12px",
    padding: "14px",
    fontSize: "16px",
    fontWeight: 800,
    cursor: "pointer",
    boxShadow: "0 4px 15px rgba(0, 210, 106, 0.3)"
  },
  secondaryButton: {
    backgroundColor: "#1F2937",
    color: "#E2E8F0",
    border: "1px solid #374151",
    borderRadius: "12px",
    padding: "12px",
    fontSize: "14px",
    fontWeight: 700,
    cursor: "pointer"
  },
  demoSection: {
    marginTop: "24px",
    paddingTop: "18px",
    borderTop: "1px solid #1F2937",
    textAlign: "center"
  },
  demoTitle: {
    fontSize: "12px",
    color: "#94A3B8",
    fontWeight: 700,
    marginBottom: "10px"
  },
  demoButtons: {
    display: "flex",
    gap: "10px",
    justifyContent: "center"
  },
  demoButton: {
    backgroundColor: "#141C2E",
    border: "1px solid #28374E",
    color: "#60A5FA",
    borderRadius: "8px",
    padding: "8px 12px",
    fontSize: "12px",
    fontWeight: 700,
    cursor: "pointer"
  },
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#0F172A",
    borderBottom: "1px solid #1E293B",
    padding: "12px 24px"
  },
  navLeft: {
    display: "flex",
    alignItems: "center",
    gap: "8px"
  },
  navBrand: {
    fontSize: "20px",
    fontWeight: 800,
    color: "#FFFFFF"
  },
  navRight: {
    display: "flex",
    alignItems: "center",
    gap: "12px"
  },
  userPill: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    backgroundColor: "#161F30",
    border: "1px solid #2B3A55",
    padding: "6px 14px",
    borderRadius: "20px"
  },
  activeDot: {
    fontSize: "8px"
  },
  userText: {
    fontSize: "13px",
    color: "#E2E8F0"
  },
  logoutButton: {
    backgroundColor: "rgba(239, 68, 68, 0.15)",
    border: "1px solid #EF4444",
    color: "#F87171",
    padding: "6px 12px",
    borderRadius: "10px",
    fontSize: "12px",
    fontWeight: 700,
    cursor: "pointer"
  }
};
