import React, { useState } from 'react';
import { Header } from './components/Header';
import { SystemStatus } from './components/SystemStatus';
import { NavigationStub, TabId } from './components/NavigationStub';
import { Box, GitBranch, Cpu, Lock, CheckCircle } from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabId>('status');

  return (
    <div className="app-container">
      <Header environment="development" version="0.1.0" />

      <main className="main-content">
        <NavigationStub activeTab={activeTab} onTabChange={setActiveTab} />

        {activeTab === 'status' && (
          <>
            <SystemStatus />

            <div className="panel-card">
              <div className="panel-header">
                <h3 className="panel-title">
                  <Box size={20} color="var(--oil-yellow)" />
                  H0 3-Container Architectural Foundation
                </h3>
                <span className="status-pill healthy">
                  <CheckCircle size={12} />
                  Canonical H0
                </span>
              </div>

              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem' }}>
                Phase 1 establishes the verified container baseline, data contracts, and testable scaffolding.
                All SIF detection, triad classification, and barrier analytics are scheduled for subsequent execution phases.
              </p>

              <div className="arch-grid">
                <div className="arch-node">
                  <div className="arch-node-title">1. Frontend SPA</div>
                  <p className="arch-node-desc">
                    React 18, TypeScript, Vite, Vanilla CSS design tokens. Single-origin routing served via Nginx reverse proxy.
                  </p>
                </div>

                <div className="arch-node">
                  <div className="arch-node-title">2. FastAPI Backend</div>
                  <p className="arch-node-desc">
                    Python 3.11, Pydantic v2 Settings, SQLAlchemy 2.0 connection pool, Alembic migrations, liveness/readiness probes.
                  </p>
                </div>

                <div className="arch-node">
                  <div className="arch-node-title">3. PostgreSQL 16</div>
                  <p className="arch-node-desc">
                    Relational store for incident narratives, audit trails, precursor triad taxonomy, and barrier status records.
                  </p>
                </div>
              </div>

              <div style={{ marginTop: '1.5rem', display: 'flex', gap: '2rem', flexWrap: 'wrap', paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  <Cpu size={16} color="var(--oil-yellow)" />
                  <span>ML Cache Contract: <code>/app/models/cache</code></span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  <Lock size={16} color="var(--status-healthy)" />
                  <span>Security: SHA-256 Chaining &amp; Structured PII Scrubbing</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  <GitBranch size={16} color="var(--oil-yellow)" />
                  <span>Governance: Frozen Documentation Baseline</span>
                </div>
              </div>
            </div>
          </>
        )}

        {activeTab !== 'status' && (
          <div className="panel-card" style={{ textAlign: 'center', padding: '3.5rem 1.5rem' }}>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
              Module Scheduled for Subsequent Implementation Phase
            </h3>
            <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto 1.5rem', fontSize: '0.9rem' }}>
              In adherence to the frozen architectural roadmap, Phase 1 focuses exclusively on the lean
              3-container foundation, health probes, and offline model contracts. Business intelligence and
              SIF pipelines will be activated in Phase 2 &amp; Phase 3.
            </p>
            <button className="refresh-button" onClick={() => setActiveTab('status')}>
              Return to Foundation Health
            </button>
          </div>
        )}
      </main>

      <footer className="footer">
        OIL India Limited (OIL) &bull; Problem Statement SIH26165 &bull; AI/NLP Safety Intelligence Platform
      </footer>
    </div>
  );
};
