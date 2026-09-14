import React, { useEffect, useState } from 'react';
import { Server, Database, Monitor, RefreshCw, CheckCircle2 } from 'lucide-react';
import { api, HealthResponse, ReadinessResponse } from '../services/api';

export const SystemStatus: React.FC = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [lastChecked, setLastChecked] = useState<string>('');

  const checkStatus = async () => {
    setLoading(true);
    try {
      const [hRes, rRes] = await Promise.all([
        api.getHealth(),
        api.getReadiness(),
      ]);
      setHealth(hRes);
      setReadiness(rRes);
    } catch (err) {
      // Complete safety fallback so React never crashes
      setHealth({ status: 'offline', error: 'Unexpected error checking health' });
      setReadiness({ status: 'offline', database: 'disconnected', error: 'Unexpected error' });
    } finally {
      setLoading(false);
      setLastChecked(new Date().toLocaleTimeString());
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 30000); // 30s poll
    return () => clearInterval(interval);
  }, []);

  const getBackendStatusType = () => {
    if (!health) return 'degraded';
    return health.status === 'healthy' ? 'healthy' : 'offline';
  };

  const getDbStatusType = () => {
    if (!readiness) return 'degraded';
    if (readiness.database === 'connected' && readiness.status === 'ready') return 'healthy';
    if (readiness.database === 'disconnected' || readiness.status === 'degraded') return 'degraded';
    return 'offline';
  };

  return (
    <div className="panel-card">
      <div className="panel-header">
        <h2 className="panel-title">
          <Monitor size={20} color="var(--oil-yellow)" />
          H0 Foundation System Health & Connectivity
        </h2>
        <button
          className="refresh-button"
          onClick={checkStatus}
          disabled={loading}
          title="Refresh connection status"
        >
          <RefreshCw size={14} className={loading ? 'spin' : ''} />
          {loading ? 'Checking...' : 'Refresh'}
        </button>
      </div>

      <div className="status-grid">
        {/* Frontend Status */}
        <div className="status-card">
          <div className="status-card-header">
            <span className="status-card-title">Frontend Container</span>
            <span className="status-pill healthy">
              <span className="status-dot healthy"></span>
              Healthy
            </span>
          </div>
          <p className="status-detail">React 18 &bull; Vite &bull; Nginx SPA</p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            <CheckCircle2 size={14} color="var(--status-healthy)" />
            <span>Single-origin UI ready</span>
          </div>
        </div>

        {/* Backend Status */}
        <div className="status-card">
          <div className="status-card-header">
            <span className="status-card-title">FastAPI Backend</span>
            <span className={`status-pill ${getBackendStatusType()}`}>
              <span className={`status-dot ${getBackendStatusType()}`}></span>
              {health?.status === 'healthy' ? 'Healthy' : 'Offline'}
            </span>
          </div>
          <p className="status-detail">
            {health?.status === 'healthy'
              ? `${health.service} (${health.version})`
              : health?.error || 'Awaiting connection to :8000'}
          </p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            <Server size={14} color="var(--text-muted)" />
            <span>Endpoint: /api/v1/health</span>
          </div>
        </div>

        {/* Database Status */}
        <div className="status-card">
          <div className="status-card-header">
            <span className="status-card-title">PostgreSQL 16</span>
            <span className={`status-pill ${getDbStatusType()}`}>
              <span className={`status-dot ${getDbStatusType()}`}></span>
              {readiness?.database === 'connected' ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          <p className="status-detail">
            {readiness?.database === 'connected'
              ? 'SQLAlchemy 2.0 connection pool active'
              : readiness?.detail || readiness?.error || 'Database pending initialization'}
          </p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            <Database size={14} color="var(--text-muted)" />
            <span>Probe: /api/v1/health/ready</span>
          </div>
        </div>
      </div>

      <div style={{ marginTop: '1.25rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
        <span>Topology: 3-Container H0 Baseline (Nginx &rarr; FastAPI &rarr; PostgreSQL)</span>
        <span>Last checked: {lastChecked || 'Initial probe'}</span>
      </div>
    </div>
  );
};
