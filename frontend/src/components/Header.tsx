import React from 'react';
import { ShieldCheck, Activity } from 'lucide-react';

interface HeaderProps {
  environment?: string;
  version?: string;
}

export const Header: React.FC<HeaderProps> = ({
  environment = 'development',
  version = '0.1.0',
}) => {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="header-brand">
          <span className="brand-badge" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
            <ShieldCheck size={14} />
            OIL INDIA
          </span>
          <div>
            <h1 className="brand-title">Safety Intelligence Platform</h1>
            <p className="brand-subtitle">SIH26165 &bull; H0 Foundation &bull; v{version}</p>
          </div>
        </div>

        <div className="header-controls">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            <Activity size={16} color="var(--oil-yellow)" />
            <span>ENV: <strong>{environment.toUpperCase()}</strong></span>
          </div>
        </div>
      </div>
    </header>
  );
};
