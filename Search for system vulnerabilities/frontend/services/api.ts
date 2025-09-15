import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Scan API endpoints
export const scanAPI = {
  // Start a new scan
  startScan: async (url: string, options?: any) => {
    const response = await api.post('/scan/start', { url, ...options });
    return response.data;
  },

  // Get scan status
  getScanStatus: async (scanId: string) => {
    const response = await api.get(`/scan/status/${scanId}`);
    return response.data;
  },

  // Get scan results
  getScanResults: async (scanId: string) => {
    const response = await api.get(`/scan/results/${scanId}`);
    return response.data;
  },

  // Get all scans
  getAllScans: async () => {
    const response = await api.get('/scan/list');
    return response.data;
  },

  // Stop a scan
  stopScan: async (scanId: string) => {
    const response = await api.post(`/scan/stop/${scanId}`);
    return response.data;
  },

  // Get available scanners
  getScanners: async () => {
    const response = await api.get('/scanners');
    return response.data;
  },
};

// Vulnerability API endpoints
export const vulnerabilityAPI = {
  // Get all vulnerabilities
  getAllVulnerabilities: async () => {
    const response = await api.get('/vulnerabilities');
    return response.data;
  },

  // Get vulnerability by ID
  getVulnerabilityById: async (id: string) => {
    const response = await api.get(`/vulnerabilities/${id}`);
    return response.data;
  },

  // Update vulnerability status
  updateVulnerabilityStatus: async (id: string, status: string) => {
    const response = await api.put(`/vulnerabilities/${id}`, { status });
    return response.data;
  },
};

// Report API endpoints
export const reportAPI = {
  // Generate PDF report
  generatePDFReport: async (scanId: string) => {
    const response = await api.get(`/reports/pdf/${scanId}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Generate Excel report
  generateExcelReport: async (scanId: string) => {
    const response = await api.get(`/reports/excel/${scanId}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Generate JSON report
  generateJSONReport: async (scanId: string) => {
    const response = await api.get(`/reports/json/${scanId}`);
    return response.data;
  },
};

// Auth API endpoints
export const authAPI = {
  // Login
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },

  // Register
  register: async (userData: any) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  // Logout
  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

export default api;
