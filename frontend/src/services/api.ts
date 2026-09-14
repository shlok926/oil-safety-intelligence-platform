/**
 * OIL Safety Intelligence Platform — API Client
 * Resilient HTTP client for liveness and readiness monitoring.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

export interface HealthResponse {
  status: 'healthy' | 'offline';
  service?: string;
  version?: string;
  environment?: string;
  error?: string;
}

export interface ReadinessResponse {
  status: 'ready' | 'degraded' | 'offline';
  database?: 'connected' | 'disconnected';
  service?: string;
  version?: string;
  detail?: string;
  error?: string;
}

export const api = {
  /**
   * Fetch backend liveness status (/api/v1/health)
   */
  async getHealth(): Promise<HealthResponse> {
    try {
      const response = await fetch(`${API_BASE}/api/v1/health`, {
        headers: { 'Accept': 'application/json' },
      });
      if (!response.ok) {
        return {
          status: 'offline',
          error: `HTTP ${response.status}: ${response.statusText}`,
        };
      }
      const data = await response.json();
      return data;
    } catch (err) {
      return {
        status: 'offline',
        error: err instanceof Error ? err.message : 'Network error or backend offline',
      };
    }
  },

  /**
   * Fetch database readiness status (/api/v1/health/ready)
   */
  async getReadiness(): Promise<ReadinessResponse> {
    try {
      const response = await fetch(`${API_BASE}/api/v1/health/ready`, {
        headers: { 'Accept': 'application/json' },
      });
      const data = await response.json();
      return data;
    } catch (err) {
      return {
        status: 'offline',
        database: 'disconnected',
        error: err instanceof Error ? err.message : 'Backend unreachable',
      };
    }
  },
};
