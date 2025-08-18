import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface Vulnerability {
  id: number;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  cve: string;
  cvss: number;
  type: string;
  location: string;
  timestamp: string;
}

export interface Scan {
  id: string;
  url: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  vulnerabilities: Vulnerability[];
  startedAt: string;
  completedAt?: string;
  error?: string;
}

interface ScanState {
  // State
  currentScan: Scan | null;
  scans: Scan[];
  vulnerabilities: Vulnerability[];
  isLoading: boolean;
  error: string | null;

  // Actions
  startScan: (url: string) => void;
  updateScanProgress: (scanId: string, progress: number) => void;
  completeScan: (scanId: string, vulnerabilities: Vulnerability[]) => void;
  stopScan: (scanId: string) => void;
  clearError: () => void;
  resetState: () => void;
}

const initialState = {
  currentScan: null,
  scans: [],
  vulnerabilities: [],
  isLoading: false,
  error: null,
};

export const useScanStore = create<ScanState>()(
  devtools(
    (set, get) => ({
      ...initialState,

      startScan: (url: string) => {
        const newScan: Scan = {
          id: `scan_${Date.now()}`,
          url,
          status: 'running',
          progress: 0,
          vulnerabilities: [],
          startedAt: new Date().toISOString(),
        };

        set((state) => ({
          currentScan: newScan,
          scans: [newScan, ...state.scans],
          isLoading: true,
          error: null,
        }));
      },

      updateScanProgress: (scanId: string, progress: number) => {
        set((state) => ({
          scans: state.scans.map((scan) =>
            scan.id === scanId ? { ...scan, progress } : scan
          ),
          currentScan: state.currentScan?.id === scanId
            ? { ...state.currentScan, progress }
            : state.currentScan,
        }));
      },

      completeScan: (scanId: string, vulnerabilities: Vulnerability[]) => {
        set((state) => ({
          scans: state.scans.map((scan) =>
            scan.id === scanId
              ? {
                  ...scan,
                  status: 'completed',
                  progress: 100,
                  vulnerabilities,
                  completedAt: new Date().toISOString(),
                }
              : scan
          ),
          currentScan: state.currentScan?.id === scanId
            ? {
                ...state.currentScan,
                status: 'completed',
                progress: 100,
                vulnerabilities,
                completedAt: new Date().toISOString(),
              }
            : state.currentScan,
          vulnerabilities: [...vulnerabilities, ...state.vulnerabilities],
          isLoading: false,
        }));
      },

      stopScan: (scanId: string) => {
        set((state) => ({
          scans: state.scans.map((scan) =>
            scan.id === scanId
              ? { ...scan, status: 'cancelled', progress: 0 }
              : scan
          ),
          currentScan: state.currentScan?.id === scanId
            ? { ...state.currentScan, status: 'cancelled', progress: 0 }
            : state.currentScan,
          isLoading: false,
        }));
      },

      clearError: () => {
        set({ error: null });
      },

      resetState: () => {
        set(initialState);
      },
    }),
    {
      name: 'scan-store',
    }
  )
);
