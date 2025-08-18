import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: Date | string): string {
  const d = new Date(date);
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function formatSeverity(severity: string): string {
  return severity.charAt(0).toUpperCase() + severity.slice(1).toLowerCase();
}

export function getSeverityColor(severity: string): string {
  switch (severity.toLowerCase()) {
    case 'critical':
      return 'text-red-600 bg-red-100';
    case 'high':
      return 'text-orange-600 bg-orange-100';
    case 'medium':
      return 'text-yellow-600 bg-yellow-100';
    case 'low':
      return 'text-green-600 bg-green-100';
    case 'info':
      return 'text-blue-600 bg-blue-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
}

export function generateMockVulnerabilities() {
  return [
    {
      id: 1,
      title: 'SQL Injection Vulnerability',
      description: 'Potential SQL injection point detected in login form',
      severity: 'high',
      cve: 'CVE-2024-1234',
      cvss: 8.5,
      type: 'Injection',
      location: '/login',
      timestamp: new Date().toISOString(),
    },
    {
      id: 2,
      title: 'XSS Cross-Site Scripting',
      description: 'Reflected XSS vulnerability in search parameter',
      severity: 'medium',
      cve: 'CVE-2024-5678',
      cvss: 6.1,
      type: 'XSS',
      location: '/search?q=',
      timestamp: new Date().toISOString(),
    },
    {
      id: 3,
      title: 'Outdated SSL/TLS Version',
      description: 'Server supports outdated TLS 1.0 protocol',
      severity: 'low',
      cve: 'CVE-2024-9012',
      cvss: 3.1,
      type: 'Cryptography',
      location: 'TLS Configuration',
      timestamp: new Date().toISOString(),
    },
  ];
}
