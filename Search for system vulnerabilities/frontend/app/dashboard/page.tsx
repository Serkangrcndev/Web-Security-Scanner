'use client';

import { useState, useEffect } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { 
  Shield, 
  Search, 
  BarChart3, 
  Download, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  Zap,
  TrendingUp,
  Activity,
  Target,
  Cpu,
  Eye,
  Lock,
  Database,
  Network,
  Bug,
  Code,
  Home,
  Radar,
  Fingerprint,
  Scan,
  AlertCircle,
  ShieldCheck,
  Users,
  Globe,
  Server,
  Key,
  LockKeyhole,
  Folder,
  Terminal,
  Code2,
  ShieldX,
  AlertOctagon,
  CheckCircle2,
  Clock2,
  Timer,
  Play,
  Pause,
  Square,
  RotateCcw,
  Settings,
  BarChart4,
  PieChart as PieChartIcon,
  TrendingDown,
  Pulse,
  Heart,
  Zap2,
  Target2,
  Crosshair,
  Binoculars,
  Telescope,
  Satellite,
  Wifi,
  WifiOff,
  Signal,
  SignalHigh,
  SignalMedium,
  SignalLow
} from 'lucide-react';
import { generateMockVulnerabilities, formatDate, getSeverityColor, formatSeverity } from '@/lib/utils';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, AreaChart, Area } from 'recharts';
import Link from 'next/link';

export default function DashboardPage() {
  const [url, setUrl] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [scanProgress, setScanProgress] = useState(0);
  const [vulnerabilities, setVulnerabilities] = useState(generateMockVulnerabilities());
  const [activeTab, setActiveTab] = useState('overview');
  const [detectedThreats, setDetectedThreats] = useState(0);
  const [securityScore, setSecurityScore] = useState(0);
  const [activeConnections, setActiveConnections] = useState(0);
  const [scanMode, setScanMode] = useState('stealth'); // stealth, aggressive, silent
  const [currentEngine, setCurrentEngine] = useState('Nmap');

  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], ['0%', '50%']);

  // Mock scan simulation
  useEffect(() => {
    if (isScanning) {
      const interval = setInterval(() => {
        setScanProgress(prev => {
          if (prev >= 100) {
            setIsScanning(false);
            return 100;
          }
          return prev + Math.random() * 15;
        });
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [isScanning]);

  // Mock threat detection
  useEffect(() => {
    if (isScanning) {
      const threatInterval = setInterval(() => {
        setDetectedThreats(prev => prev + Math.floor(Math.random() * 3));
      }, 2000);

      return () => clearInterval(threatInterval);
    }
  }, [isScanning]);

  // Mock security score
  useEffect(() => {
    if (isScanning) {
      const scoreInterval = setInterval(() => {
        setSecurityScore(prev => Math.min(100, prev + Math.random() * 5));
      }, 1500);

      return () => clearInterval(scoreInterval);
    }
  }, [isScanning]);

  // Mock active connections
  useEffect(() => {
    if (isScanning) {
      const connectionInterval = setInterval(() => {
        setActiveConnections(prev => Math.max(0, prev + Math.floor(Math.random() * 10) - 5));
      }, 1000);

      return () => clearInterval(connectionInterval);
    }
  }, [isScanning]);

  // Mock engine switching
  useEffect(() => {
    if (isScanning) {
      const engines = ['Nmap', 'Nuclei', 'ZAP', 'SQLMap', 'Nikto', 'Dirb'];
      const engineInterval = setInterval(() => {
        setCurrentEngine(engines[Math.floor(Math.random() * engines.length)]);
      }, 3000);

      return () => clearInterval(engineInterval);
    }
  }, [isScanning]);

  const handleScanStart = () => {
    if (!url) return;
    setIsScanning(true);
    setScanProgress(0);
    setDetectedThreats(0);
    setSecurityScore(0);
    setActiveConnections(0);
    console.log('Starting scan for:', url);
  };

  const handleScanStop = () => {
    setIsScanning(false);
    setScanProgress(0);
  };

  const handleScanPause = () => {
    setIsScanning(false);
  };

  const handleScanResume = () => {
    setIsScanning(true);
  };

  const chartData = [
    { name: 'Critical', value: 2, color: '#ef4444' },
    { name: 'High', value: 5, color: '#f97316' },
    { name: 'Medium', value: 8, color: '#22c55e' },
    { name: 'Low', value: 12, color: '#3b82f6' },
  ];

  const severityDistribution = [
    { severity: 'Critical', count: 2 },
    { severity: 'High', count: 5 },
    { severity: 'Medium', count: 8 },
    { severity: 'Low', count: 12 },
  ];

  const realTimeData = [
    { time: '00:00', threats: 0, score: 100 },
    { time: '00:05', threats: 2, score: 95 },
    { time: '00:10', threats: 5, score: 88 },
    { time: '00:15', threats: 8, score: 82 },
    { time: '00:20', threats: 12, score: 76 },
    { time: '00:25', threats: 15, score: 70 },
    { time: '00:30', threats: 18, score: 65 },
    { time: '00:35', threats: 22, score: 60 },
    { time: '00:40', threats: 25, score: 55 },
    { time: '00:45', threats: 27, score: 50 },
  ];

  const tabs = [
    { id: 'overview', label: 'OVERVIEW', icon: BarChart3 },
    { id: 'vulnerabilities', label: 'THREATS', icon: AlertTriangle },
    { id: 'reports', label: 'INTEL', icon: Download },
    { id: 'monitoring', label: 'MONITOR', icon: Activity },
  ];

  const quickActions = [
    { icon: Network, label: 'Network Scan', color: 'from-blue-500 to-cyan-500', description: 'Port scanning & service detection' },
    { icon: Database, label: 'Database Audit', color: 'from-purple-500 to-pink-500', description: 'SQL injection & DB vulnerabilities' },
    { icon: Bug, label: 'Vulnerability Check', color: 'from-green-500 to-emerald-500', description: 'CVE scanning & assessment' },
    { icon: Lock, label: 'Security Test', color: 'from-red-500 to-orange-500', description: 'Authentication & authorization' },
    { icon: Terminal, label: 'Command Injection', color: 'from-yellow-500 to-orange-500', description: 'OS command execution' },
    { icon: Code2, label: 'Code Analysis', color: 'from-indigo-500 to-purple-500', description: 'Source code review' },
  ];

  const scanningEngines = [
    { name: 'Nmap', status: 'active', icon: Network, color: 'from-blue-500 to-cyan-500', progress: 85 },
    { name: 'Nuclei', status: 'active', icon: Bug, color: 'from-green-500 to-emerald-500', progress: 72 },
    { name: 'ZAP', status: 'active', icon: Shield, color: 'from-purple-500 to-pink-500', progress: 63 },
    { name: 'SQLMap', status: 'active', icon: Database, color: 'from-red-500 to-orange-500', progress: 91 },
    { name: 'Nikto', status: 'active', icon: Search, color: 'from-yellow-500 to-orange-500', progress: 45 },
    { name: 'Dirb', status: 'active', icon: Folder, color: 'from-indigo-500 to-purple-500', progress: 78 },
  ];

  const navigationLinks = [
    { name: 'Home', href: '/' },
    { name: 'Features', href: '/#features' },
    { name: 'Pricing', href: '/#pricing' },
    { name: 'FAQ', href: '/#faq' },
    { name: 'Privacy', href: '/#privacy' },
    { name: 'Changelogs', href: '/#changelogs' },
  ];

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-gradient-to-br from-gray-900 via-black to-gray-900"></div>
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(59,130,246,0.05),transparent_50%)]"></div>
      
      {/* Animated Grid */}
      <div className="fixed inset-0 opacity-10">
        <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.1)_1px,transparent_1px)] bg-[size:50px_50px]"></div>
      </div>



      {/* Header */}
      <header className="relative z-10">
        <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            {/* Logo/Brand */}
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg blur-sm opacity-75"></div>
                <div className="relative bg-gradient-to-r from-blue-500 to-cyan-500 p-2 rounded-lg">
                  <Code className="h-6 w-6 text-white" />
                </div>
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold text-white">
                  SecurityScanner
                </span>
                <span className="text-xs text-gray-400 -mt-1">COMMAND CENTER</span>
              </div>
            </div>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center space-x-8">
              {navigationLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  className="text-gray-300 hover:text-white transition-colors duration-200 font-medium"
                >
                  {link.name}
                </a>
              ))}
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center space-x-4">
              <span className="inline-flex items-center rounded-full bg-gradient-to-r from-yellow-500 to-orange-500 px-3 py-1 text-xs font-medium text-black">
                <CheckCircle className="mr-1 h-3 w-3" />
                PREMIUM
              </span>
              <Link href="/">
                <Button variant="secondary" className="font-medium">
                  <Home className="mr-2 h-4 w-4" />
                  Home
                </Button>
              </Link>
            </div>
          </div>
        </nav>
      </header>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl md:text-6xl font-black mb-4">
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              SECURITY
            </span>
            <br />
            <span className="text-white">COMMAND CENTER</span>
          </h1>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Deploy advanced security scans and monitor real-time threat intelligence
          </p>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {quickActions.map((action, index) => (
              <motion.div
                key={action.label}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -5, scale: 1.05 }}
                className="group cursor-pointer"
              >
                <Card className="bg-gray-900/50 border-gray-800 hover:border-gray-700 transition-all duration-300 backdrop-blur-sm h-full">
                  <CardContent className="p-4 text-center">
                    <div className={`mx-auto w-12 h-12 bg-gradient-to-r ${action.color} rounded-xl p-3 mb-3 group-hover:scale-110 transition-transform duration-300`}>
                      <action.icon className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="text-white font-bold text-sm mb-1">{action.label}</h3>
                    <p className="text-xs text-gray-400">{action.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Scan Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-8"
        >
          <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-cyan-500/5"></div>
            <CardHeader className="relative">
              <CardTitle className="flex items-center space-x-3 text-white">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl p-3">
                  <Search className="h-6 w-6 text-white" />
                </div>
                <div>
                  <span className="text-2xl">DEPLOY SECURITY SCAN</span>
                  <p className="text-sm text-gray-400 font-normal mt-1">Enter target URL to initiate comprehensive security assessment</p>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent className="relative">
              <div className="space-y-4">
                <div className="flex space-x-4">
                  <Input
                    type="url"
                    placeholder="https://target-domain.com"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    className="flex-1 bg-gray-800 border-gray-700 text-white placeholder-gray-500 text-lg"
                  />
                  <select 
                    value={scanMode}
                    onChange={(e) => setScanMode(e.target.value)}
                    className="bg-gray-800 border-gray-700 text-white px-4 py-2 rounded-lg border"
                  >
                    <option value="stealth">Stealth Mode</option>
                    <option value="aggressive">Aggressive</option>
                    <option value="silent">Silent</option>
                  </select>
                </div>
                <div className="flex space-x-4">
                  {!isScanning ? (
                    <Button onClick={handleScanStart} disabled={!url} variant="premium" className="font-bold text-lg px-8 py-4">
                      <Zap className="mr-3 h-6 w-6" />
                      DEPLOY
                    </Button>
                  ) : (
                    <>
                      <Button variant="destructive" onClick={handleScanStop} className="font-bold text-lg px-6 py-4">
                        <Square className="mr-3 h-6 w-6" />
                        STOP
                      </Button>
                      <Button variant="outline" onClick={handleScanPause} className="font-bold text-lg px-6 py-4">
                        <Pause className="mr-3 h-6 w-6" />
                        PAUSE
                      </Button>
                      <Button variant="outline" onClick={handleScanResume} className="font-bold text-lg px-6 py-4">
                        <Play className="mr-3 h-6 w-6" />
                        RESUME
                      </Button>
                    </>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Scan Progress */}
        {isScanning && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-8"
          >
            <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-green-500/5 to-emerald-500/5"></div>
              <CardHeader className="relative">
                <CardTitle className="flex items-center space-x-3 text-white">
                  <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl p-3">
                    <Activity className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <span className="text-2xl">MISSION STATUS</span>
                    <p className="text-sm text-gray-400 font-normal mt-1">Real-time scanning progress and threat detection</p>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent className="relative">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Progress Bar */}
                  <div className="lg:col-span-2 space-y-6">
                    <div className="flex justify-between text-lg text-gray-300">
                      <span>Target: <span className="text-cyan-400 font-bold">{url}</span></span>
                      <span className="text-cyan-400 font-black text-2xl">{Math.round(scanProgress)}%</span>
                    </div>
                    <div className="w-full bg-gray-800 rounded-full h-4 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-cyan-500 h-4 rounded-full transition-all duration-300 relative"
                        style={{ width: `${scanProgress}%` }}
                      >
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
                      </div>
                    </div>
                    <div className="flex justify-between text-sm text-gray-500">
                      <span>ETA: {Math.max(0, Math.round((100 - scanProgress) / 10))} seconds</span>
                      <span>Status: {scanProgress < 100 ? 'SCANNING' : 'COMPLETE'}</span>
                    </div>
                    <div className="flex items-center space-x-4 text-sm text-gray-400">
                      <span>Mode: <span className="text-yellow-400 font-bold">{scanMode.toUpperCase()}</span></span>
                      <span>Engine: <span className="text-blue-400 font-bold">{currentEngine}</span></span>
                    </div>
                  </div>

                  {/* Live Stats */}
                  <div className="space-y-4">
                    <div className="bg-gray-800/50 p-4 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <AlertTriangle className="h-8 w-8 text-red-400" />
                        <div>
                          <p className="text-sm text-gray-400">Threats Detected</p>
                          <p className="text-2xl font-bold text-red-400">{detectedThreats}</p>
                        </div>
                      </div>
                    </div>
                    <div className="bg-gray-800/50 p-4 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <ShieldCheck className="h-8 w-8 text-green-400" />
                        <div>
                          <p className="text-sm text-gray-400">Security Score</p>
                          <p className="text-2xl font-bold text-green-400">{Math.round(securityScore)}%</p>
                        </div>
                      </div>
                    </div>
                    <div className="bg-gray-800/50 p-4 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Signal className="h-8 w-8 text-blue-400" />
                        <div>
                          <p className="text-sm text-gray-400">Active Connections</p>
                          <p className="text-2xl font-bold text-blue-400">{activeConnections}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Scanning Engines Progress */}
                <div className="mt-8">
                  <h3 className="text-xl font-bold text-white mb-4 text-center">SCANNING ENGINES STATUS</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                    {scanningEngines.map((engine, index) => (
                      <motion.div
                        key={engine.name}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.5, delay: index * 0.1 }}
                        className="text-center"
                      >
                        <div className={`mx-auto w-12 h-12 bg-gradient-to-r ${engine.color} rounded-xl p-3 mb-2`}>
                          <engine.icon className="h-6 w-6 text-white" />
                        </div>
                        <p className="text-sm text-white font-medium mb-2">{engine.name}</p>
                        <div className="w-full bg-gray-800 rounded-full h-2 mb-2">
                          <div
                            className="bg-gradient-to-r from-green-400 to-emerald-400 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${engine.progress}%` }}
                          />
                        </div>
                        <div className="flex items-center justify-center space-x-1">
                          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                          <span className="text-xs text-green-400">{engine.progress}%</span>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Tabs */}
        <div className="mb-8">
          <div className="border-b border-gray-800">
            <nav className="-mb-px flex space-x-8">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-2 border-b-2 font-bold text-sm flex items-center space-x-3 transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'border-cyan-500 text-cyan-400'
                      : 'border-transparent text-gray-500 hover:text-gray-300 hover:border-gray-600'
                  }`}
                >
                  <tab.icon className="h-6 w-6" />
                  <span>{tab.label}</span>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-8"
          >
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm hover:border-gray-700 transition-all duration-300 group hover:scale-105">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-4">
                    <div className="p-4 bg-red-500/20 rounded-2xl group-hover:bg-red-500/30 transition-colors">
                      <AlertTriangle className="h-10 w-10 text-red-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-400">THREAT COUNT</p>
                      <p className="text-4xl font-black text-white">27</p>
                      <p className="text-xs text-red-400 font-bold">+3 NEW</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm hover:border-gray-700 transition-all duration-300 group hover:scale-105">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-4">
                    <div className="p-4 bg-orange-500/20 rounded-2xl group-hover:bg-orange-500/30 transition-colors">
                      <TrendingUp className="h-10 w-10 text-orange-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-400">SECURITY SCORE</p>
                      <p className="text-4xl font-black text-white">94.2</p>
                      <p className="text-xs text-green-400 font-bold">+2.1%</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm hover:border-gray-700 transition-all duration-300 group hover:scale-105">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-4">
                    <div className="p-4 bg-blue-500/20 rounded-2xl group-hover:bg-blue-500/30 transition-colors">
                      <Clock className="h-10 w-10 text-blue-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-400">LAST SCAN</p>
                      <p className="text-4xl font-black text-white">2h</p>
                      <p className="text-xs text-blue-400 font-bold">AGO</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm hover:border-gray-700 transition-all duration-300 group hover:scale-105">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-4">
                    <div className="p-4 bg-green-500/20 rounded-2xl group-hover:bg-green-500/30 transition-colors">
                      <CheckCircle className="h-10 w-10 text-green-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-400">TARGETS</p>
                      <p className="text-4xl font-black text-white">12</p>
                      <p className="text-xs text-green-400 font-bold">SECURED</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-white text-xl">THREAT DISTRIBUTION</CardTitle>
                  <CardDescription className="text-gray-400">Vulnerability breakdown by severity level</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={chartData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {chartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#1F2937', 
                          border: '1px solid #374151',
                          borderRadius: '8px',
                          color: '#F9FAFB'
                        }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-white text-xl">REAL-TIME THREAT TREND</CardTitle>
                  <CardDescription className="text-gray-400">Live threat detection over time</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={realTimeData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                      <XAxis dataKey="time" stroke="#9CA3AF" />
                      <YAxis stroke="#9CA3AF" />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#1F2937', 
                          border: '1px solid #374151',
                          borderRadius: '8px',
                          color: '#F9FAFB'
                        }}
                      />
                      <Area type="monotone" dataKey="threats" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} />
                      <Area type="monotone" dataKey="score" stroke="#22c55e" fill="#22c55e" fillOpacity={0.3} />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </motion.div>
        )}

        {activeTab === 'vulnerabilities' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-white text-2xl">DETECTED THREATS</CardTitle>
                <CardDescription className="text-gray-400 text-lg">
                  {vulnerabilities.length} vulnerabilities identified in recent operations
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {vulnerabilities.map((vuln) => (
                    <motion.div
                      key={vuln.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      whileHover={{ x: 5 }}
                      className="border border-gray-800 rounded-2xl p-6 hover:bg-gray-800/50 transition-all duration-300 backdrop-blur-sm group"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-4 mb-3">
                            <h3 className="font-bold text-white text-lg group-hover:text-cyan-400 transition-colors">
                              {vuln.title}
                            </h3>
                            <span className={`px-4 py-2 rounded-full text-sm font-bold ${getSeverityColor(vuln.severity)}`}>
                              {formatSeverity(vuln.severity)}
                            </span>
                          </div>
                          <p className="text-gray-400 text-base mb-4 leading-relaxed">
                            {vuln.description}
                          </p>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                            <div className="bg-gray-800/50 p-3 rounded-lg">
                              <span className="text-gray-500">CVE:</span>
                              <span className="text-white ml-2 font-mono">{vuln.cve}</span>
                            </div>
                            <div className="bg-gray-800/50 p-3 rounded-lg">
                              <span className="text-gray-500">CVSS:</span>
                              <span className="text-white ml-2 font-bold">{vuln.cvss}</span>
                            </div>
                            <div className="bg-gray-800/50 p-3 rounded-lg">
                              <span className="text-gray-500">Type:</span>
                              <span className="text-white ml-2">{vuln.type}</span>
                            </div>
                            <div className="bg-gray-800/50 p-3 rounded-lg">
                              <span className="text-gray-500">Location:</span>
                              <span className="text-white ml-2 font-mono">{vuln.location}</span>
                            </div>
                          </div>
                        </div>
                        <div className="text-right text-sm text-gray-500 ml-4">
                          {formatDate(vuln.timestamp)}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {activeTab === 'reports' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-white text-2xl">INTELLIGENCE REPORTS</CardTitle>
                <CardDescription className="text-gray-400 text-lg">
                  Generate and download detailed security intelligence reports
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <motion.div whileHover={{ y: -10, scale: 1.05 }}>
                    <Button variant="outline" className="h-32 w-full flex-col space-y-3 bg-gray-800/50 border-gray-700 hover:border-blue-500 hover:bg-gray-800 text-lg">
                      <Download className="h-10 w-10" />
                      <span className="font-bold">PDF REPORT</span>
                      <span className="text-sm text-gray-400">Professional format</span>
                    </Button>
                  </motion.div>
                  <motion.div whileHover={{ y: -10, scale: 1.05 }}>
                    <Button variant="outline" className="h-32 w-full flex-col space-y-3 bg-gray-800/50 border-gray-700 hover:border-blue-500 hover:bg-gray-800 text-lg">
                      <Download className="h-10 w-10" />
                      <span className="text-sm text-gray-400">Data analysis</span>
                      <span className="font-bold">EXCEL REPORT</span>
                    </Button>
                  </motion.div>
                  <motion.div whileHover={{ y: -10, scale: 1.05 }}>
                    <Button variant="outline" className="h-32 w-full flex-col space-y-3 bg-gray-800/50 border-gray-700 hover:border-blue-500 hover:bg-gray-800 text-lg">
                      <Download className="h-10 w-10" />
                      <span className="text-sm text-gray-400">API integration</span>
                      <span className="font-bold">JSON REPORT</span>
                    </Button>
                  </motion.div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {activeTab === 'monitoring' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-8"
          >
            {/* Real-time Monitoring */}
            <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-white text-2xl flex items-center space-x-3">
                  <Activity className="h-8 w-8 text-cyan-400" />
                  <span>REAL-TIME MONITORING</span>
                </CardTitle>
                <CardDescription className="text-gray-400 text-lg">
                  Live system monitoring and threat detection
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="bg-gray-800/50 p-6 rounded-xl text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl p-4 mx-auto mb-4">
                      <SignalHigh className="h-8 w-8 text-white" />
                    </div>
                    <h3 className="text-white font-bold text-lg mb-2">Network Status</h3>
                    <p className="text-green-400 text-sm">STABLE</p>
                  </div>
                  <div className="bg-gray-800/50 p-6 rounded-xl text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl p-4 mx-auto mb-4">
                      <Server className="h-8 w-8 text-white" />
                    </div>
                    <h3 className="text-white font-bold text-lg mb-2">Server Load</h3>
                    <p className="text-blue-400 text-sm">45%</p>
                  </div>
                  <div className="bg-gray-800/50 p-6 rounded-xl text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl p-4 mx-auto mb-4">
                      <Users className="h-8 w-8 text-white" />
                    </div>
                    <h3 className="text-white font-bold text-lg mb-2">Active Users</h3>
                    <p className="text-purple-400 text-sm">1,247</p>
                  </div>
                  <div className="bg-gray-800/50 p-6 rounded-xl text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-2xl p-4 mx-auto mb-4">
                      <Globe className="h-8 w-8 text-white" />
                    </div>
                    <h3 className="text-white font-bold text-lg mb-2">Global Coverage</h3>
                    <p className="text-yellow-400 text-sm">89%</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* System Health */}
            <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-white text-2xl flex items-center space-x-3">
                  <Heart className="h-8 w-8 text-red-400" />
                  <span>SYSTEM HEALTH</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                      <span className="text-white">Database Connection</span>
                    </div>
                    <span className="text-green-400 font-bold">HEALTHY</span>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                      <span className="text-white">API Services</span>
                    </div>
                    <span className="text-green-400 font-bold">OPERATIONAL</span>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse"></div>
                      <span className="text-white">Memory Usage</span>
                    </div>
                    <span className="text-yellow-400 font-bold">78%</span>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                      <span className="text-white">Security Protocols</span>
                    </div>
                    <span className="text-green-400 font-bold">ACTIVE</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  );
}
