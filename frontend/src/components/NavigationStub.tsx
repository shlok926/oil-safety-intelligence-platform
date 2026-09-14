import React from 'react';
import { Activity, FileText, Layers, Shield, Clock } from 'lucide-react';

export type TabId = 'status' | 'incidents' | 'triad' | 'barriers' | 'audit';

interface NavigationStubProps {
  activeTab: TabId;
  onTabChange: (tab: TabId) => void;
}

export const NavigationStub: React.FC<NavigationStubProps> = ({
  activeTab,
  onTabChange,
}) => {
  return (
    <nav className="nav-tabs" aria-label="Module Navigation">
      <button
        className={`nav-tab ${activeTab === 'status' ? 'active' : ''}`}
        onClick={() => onTabChange('status')}
      >
        <Activity size={16} />
        System Foundation
      </button>

      <button
        className={`nav-tab ${activeTab === 'incidents' ? 'active' : ''}`}
        onClick={() => onTabChange('incidents')}
      >
        <FileText size={16} />
        Incident Ingestion
      </button>

      <button
        className={`nav-tab ${activeTab === 'triad' ? 'active' : ''}`}
        onClick={() => onTabChange('triad')}
      >
        <Layers size={16} />
        Precursor Triad
      </button>

      <button
        className={`nav-tab ${activeTab === 'barriers' ? 'active' : ''}`}
        onClick={() => onTabChange('barriers')}
      >
        <Shield size={16} />
        Safety Barriers
      </button>

      <button
        className={`nav-tab ${activeTab === 'audit' ? 'active' : ''}`}
        onClick={() => onTabChange('audit')}
      >
        <Clock size={16} />
        Audit Trail
      </button>
    </nav>
  );
};
