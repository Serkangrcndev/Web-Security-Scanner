'use client';

import { useState } from 'react';
import {
  motion,
  useScroll,
  useTransform,
  AnimatePresence,
} from 'framer-motion';
import { Button } from '@/components/ui/Button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/Card';
import {
  Shield,
  Zap,
  BarChart3,
  Lock,
  ArrowRight,
  CheckCircle,
  Target,
  Cpu,
  Eye,
  AlertTriangle,
  Home,
  Code,
  Download,
  Search,
  Activity,
  Bug,
  Network,
  Database,
  Fingerprint,
  Scan,
  AlertCircle,
  ShieldCheck,
  Clock,
  TrendingUp,
  Users,
  Server,
  Key,
  LockKeyhole,
  Folder,
  Star,
  Sparkles,
  Wifi,
  WifiOff,
  Signal,
  SignalHigh,
  SignalMedium,
  SignalLow,
  ArrowUpRight,
  ArrowDownRight,
  ArrowLeftRight,
  RotateCcw,
  Play,
  Pause,
  Square,
  Timer,
  Gauge,
  PieChart as PieChartIcon,
  TrendingDown,
  Heart,
} from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  const [hoveredFeature, setHoveredFeature] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], ['0%', '50%']);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);
  const scale = useTransform(scrollYProgress, [0, 1], [1, 0.8]);

  const startDemoScan = () => {
    // Dashboard'a yönlendir
    window.location.href = '/dashboard';
  };

  const handleDashboardClick = () => {
    setIsLoading(true);
    // Gerçek dashboard'a yönlendir
    setTimeout(() => {
      setIsLoading(false);
      window.location.href = '/dashboard';
    }, 1000);
  };

  const features = [
    {
      icon: Shield,
      title: 'Advanced Threat Detection',
      description:
        'AI-powered vulnerability scanning with real-time threat intelligence',
      gradient: 'from-blue-500 to-cyan-500',
      delay: 0.1,
      color: 'blue',
      stats: { value: '99.9%', label: 'Detection Rate' },
    },
    {
      icon: Cpu,
      title: 'Multi-Engine Scanning',
      description:
        'Nmap, Nuclei, ZAP, SQLMap and more integrated scanning engines',
      gradient: 'from-purple-500 to-pink-500',
      delay: 0.2,
      color: 'purple',
      stats: { value: '6+', label: 'Engines' },
    },
    {
      icon: Eye,
      title: 'Real-time Monitoring',
      description: 'Live scanning progress and instant vulnerability detection',
      gradient: 'from-green-500 to-emerald-500',
      delay: 0.3,
      color: 'green',
      stats: { value: '<50ms', label: 'Response' },
    },
    {
      icon: Target,
      title: 'Precision Targeting',
      description: 'Pinpoint security weaknesses with surgical precision',
      gradient: 'from-red-500 to-orange-500',
      delay: 0.4,
      color: 'red',
      stats: { value: '100%', label: 'Accuracy' },
    },
  ];

  const stats = [
    {
      label: 'Threats Detected',
      value: '2.8M+',
      change: '+15%',
      icon: AlertTriangle,
      color: 'text-red-400',
      trend: 'up',
    },
    {
      label: 'Sites Secured',
      value: '50K+',
      change: '+8%',
      icon: ShieldCheck,
      color: 'text-green-400',
      trend: 'up',
    },
    {
      label: 'Security Score',
      value: '99.2%',
      change: '+2.1%',
      icon: TrendingUp,
      color: 'text-blue-400',
      trend: 'up',
    },
    {
      label: 'Response Time',
      value: '<50ms',
      change: '-12%',
      icon: Clock,
      color: 'text-cyan-400',
      trend: 'down',
    },
  ];

  const gamingFeatures = [
    'Real-time threat visualization',
    'Advanced AI detection algorithms',
    'Multi-layer security scanning',
    'Instant vulnerability reporting',
    'Professional security dashboard',
    'API integration support',
  ];

  const scanningEngines = [
    {
      name: 'Nmap',
      status: 'active',
      icon: Network,
      color: 'from-blue-500 to-cyan-500',
      progress: 85,
      description: 'Network Discovery',
    },
    {
      name: 'Nuclei',
      status: 'active',
      icon: Bug,
      color: 'from-green-500 to-emerald-500',
      progress: 72,
      description: 'Vulnerability Scanner',
    },
    {
      name: 'ZAP',
      status: 'active',
      icon: Shield,
      color: 'from-purple-500 to-pink-500',
      progress: 63,
      description: 'Web App Security',
    },
    {
      name: 'SQLMap',
      status: 'active',
      icon: Database,
      color: 'from-red-500 to-orange-500',
      progress: 91,
      description: 'SQL Injection',
    },
    {
      name: 'Nikto',
      status: 'active',
      icon: Search,
      color: 'from-yellow-500 to-orange-500',
      progress: 45,
      description: 'Web Server Scanner',
    },
    {
      name: 'Dirb',
      status: 'active',
      icon: Folder,
      color: 'from-indigo-500 to-purple-500',
      progress: 78,
      description: 'Directory Brute Force',
    },
  ];

  const navigationLinks = [
    { name: 'Home', href: '/' },
    { name: 'Features', href: '#features' },
    { name: 'Pricing', href: '#pricing' },
    { name: 'FAQ', href: '/faq' },
    { name: 'Privacy', href: '/privacy' },
    { name: 'Changelogs', href: '/changelogs' },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.6,
        ease: 'easeOut',
      },
    },
  };

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-gradient-to-br from-gray-900 via-black to-gray-900"></div>
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(59,130,246,0.1),transparent_50%)]"></div>

      {/* Animated Grid */}
      <div className="fixed inset-0 opacity-20">
        <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.1)_1px,transparent_1px)] bg-[size:50px_50px]"></div>
      </div>

      {/* Animated Background Shapes */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-20 w-72 h-72 bg-gradient-to-r from-blue-500/10 to-cyan-500/10 rounded-full blur-3xl"
          animate={{
            x: [0, 100, 0],
            y: [0, -50, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
        <motion.div
          className="absolute bottom-20 right-20 w-96 h-96 bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-full blur-3xl"
          animate={{
            x: [0, -100, 0],
            y: [0, 50, 0],
            scale: [1, 0.8, 1],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      </div>

      {/* Header */}
      <motion.header
        className="relative z-10"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
      >
        <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            {/* Logo/Brand */}
            <motion.div
              className="flex items-center space-x-3"
              whileHover={{ scale: 1.05 }}
              transition={{ type: 'spring', stiffness: 400, damping: 10 }}
            >
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg blur-sm opacity-75"></div>
                <div className="relative bg-gradient-to-r from-blue-500 to-cyan-500 p-2 rounded-lg">
                  <Code className="h-6 w-6 text-white" />
                </div>
              </div>
              <span className="text-xl font-bold text-white">
                SecurityScanner
              </span>
            </motion.div>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center space-x-8">
              {navigationLinks.map((link, index) => (
                <motion.a
                  key={link.name}
                  href={link.href}
                  className="text-gray-300 hover:text-white transition-colors duration-200 font-medium relative group"
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  whileHover={{ y: -2 }}
                >
                  {link.name}
                  <motion.div
                    className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-500 to-cyan-500 group-hover:w-full transition-all duration-300"
                    initial={{ width: 0 }}
                    whileHover={{ width: '100%' }}
                  />
                </motion.a>
              ))}
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center space-x-4">
              <motion.span
                className="inline-flex items-center rounded-full bg-gradient-to-r from-yellow-500 to-orange-500 px-3 py-1 text-xs font-medium text-black"
                whileHover={{ scale: 1.05, rotate: 5 }}
                transition={{ type: 'spring', stiffness: 400, damping: 10 }}
              >
                <CheckCircle className="mr-1 h-3 w-3" />
                PREMIUM
              </motion.span>
              <motion.div
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                transition={{ type: 'spring', stiffness: 400, damping: 10 }}
              >
                <Button
                  variant="secondary"
                  className="font-medium"
                  onClick={handleDashboardClick}
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{
                          duration: 1,
                          repeat: Infinity,
                          ease: 'linear',
                        }}
                        className="mr-2"
                      >
                        <RotateCcw className="h-4 w-4" />
                      </motion.div>
                      LOADING...
                    </>
                  ) : (
                    <>
                      <Home className="mr-2 h-4 w-4" />
                      Dashboard
                    </>
                  )}
                </Button>
              </motion.div>
            </div>
          </div>
        </nav>
      </motion.header>

      {/* Hero Section */}
      <section className="relative px-4 py-32 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
            className="relative"
          >
            {/* Floating Icons Around Title */}
            <motion.div
              className="absolute -top-20 -left-20 w-16 h-16 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-2xl p-4 backdrop-blur-sm"
              animate={{
                y: [0, -10, 0],
                rotate: [0, 5, 0],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            >
              <Shield className="h-8 w-8 text-blue-400" />
            </motion.div>

            <motion.div
              className="absolute -top-10 -right-20 w-12 h-12 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-xl p-3 backdrop-blur-sm"
              animate={{
                y: [0, 10, 0],
                rotate: [0, -5, 0],
              }}
              transition={{
                duration: 5,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            >
              <Target className="h-6 w-6 text-purple-400" />
            </motion.div>

            {/* Main Title */}
            <motion.h1
              className="text-6xl md:text-8xl font-black tracking-tight mb-8 relative"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1.2, ease: 'easeOut' }}
            >
              <motion.span
                className="bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-600 bg-clip-text text-transparent"
                animate={{
                  backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
                }}
                transition={{
                  duration: 8,
                  repeat: Infinity,
                  ease: 'linear',
                }}
                style={{
                  backgroundSize: '200% 200%',
                }}
              >
                ULTIMATE
              </motion.span>
              <br />
              <motion.span
                className="text-white"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 1, delay: 0.3 }}
              >
                SECURITY
              </motion.span>
              <br />
              <motion.span
                className="bg-gradient-to-r from-red-400 via-pink-400 to-purple-600 bg-clip-text text-transparent"
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 1, delay: 0.6 }}
              >
                SCANNER
              </motion.span>
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto mb-12 leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.8 }}
            >
              Professional-grade vulnerability assessment platform. Detect,
              analyze, and eliminate security threats with{' '}
              <span className="text-cyan-400 font-semibold">
                military-grade precision
              </span>
              .
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-16"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 1 }}
            >
              <motion.div
                whileHover={{ scale: 1.05, y: -5 }}
                whileTap={{ scale: 0.95 }}
                transition={{ type: 'spring', stiffness: 400, damping: 10 }}
              >
                <Button
                  size="lg"
                  variant="premium"
                  className="text-lg px-8 py-4 font-bold relative overflow-hidden group"
                  onClick={handleDashboardClick}
                  disabled={isLoading}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  <div className="relative flex items-center">
                    {isLoading ? (
                      <>
                        <motion.div
                          animate={{ rotate: 360 }}
                          transition={{
                            duration: 1,
                            repeat: Infinity,
                            ease: 'linear',
                          }}
                          className="mr-3"
                        >
                          <RotateCcw className="h-6 w-6" />
                        </motion.div>
                        LOADING...
                      </>
                    ) : (
                      <>
                        <Zap className="mr-3 h-6 w-6" />
                        START SCANNING NOW
                      </>
                    )}
                  </div>
                </Button>
              </motion.div>
              <motion.div
                whileHover={{ scale: 1.05, y: -5 }}
                whileTap={{ scale: 0.95 }}
                transition={{ type: 'spring', stiffness: 400, damping: 10 }}
              >
                <Button
                  size="lg"
                  variant="outline"
                  className="text-lg px-8 py-4 font-bold border-2 border-gray-600 hover:border-blue-500 relative overflow-hidden group"
                  onClick={startDemoScan}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-cyan-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  <div className="relative flex items-center">
                    <Eye className="mr-3 h-6 w-6" />
                    WATCH DEMO
                  </div>
                </Button>
              </motion.div>
            </motion.div>

            {/* Gaming-style Feature List */}
            <motion.div
              className="grid grid-cols-2 md:grid-cols-3 gap-4 max-w-4xl mx-auto"
              variants={containerVariants}
              initial="hidden"
              animate="visible"
            >
              {gamingFeatures.map((feature, index) => (
                <motion.div
                  key={feature}
                  variants={itemVariants}
                  className="flex items-center space-x-2 text-gray-400 text-sm group"
                  whileHover={{ scale: 1.05, x: 5 }}
                  transition={{ type: 'spring', stiffness: 400, damping: 10 }}
                >
                  <motion.div
                    className="w-2 h-2 bg-cyan-500 rounded-full"
                    animate={{
                      scale: [1, 1.2, 1],
                      opacity: [1, 0.7, 1],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      delay: index * 0.2,
                    }}
                  />
                  <span className="group-hover:text-cyan-400 transition-colors duration-300">
                    {feature}
                  </span>
                </motion.div>
              ))}
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <motion.div
            className="text-center mb-20"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-5xl md:text-6xl font-black mb-6">
              <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                WEAPONIZED
              </span>
              <br />
              <span className="text-white">SECURITY TOOLS</span>
            </h2>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              Built for security professionals, penetration testers, and ethical
              hackers
            </p>
          </motion.div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 50, scale: 0.8 }}
                whileInView={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.6, delay: feature.delay }}
                viewport={{ once: true }}
                whileHover={{ y: -15, scale: 1.05 }}
                className="group cursor-pointer"
                onHoverStart={() => setHoveredFeature(index)}
                onHoverEnd={() => setHoveredFeature(null)}
              >
                <Card className="h-full bg-gray-900/50 border-gray-800 hover:border-gray-700 transition-all duration-500 backdrop-blur-sm relative overflow-hidden">
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: hoveredFeature === index ? 1 : 0 }}
                  />
                  <CardHeader className="text-center relative">
                    <motion.div
                      className={`mx-auto w-16 h-16 bg-gradient-to-r ${feature.gradient} rounded-2xl p-4 mb-4 group-hover:scale-110 transition-transform duration-300`}
                      whileHover={{ rotate: 5 }}
                      transition={{
                        type: 'spring',
                        stiffness: 400,
                        damping: 10,
                      }}
                    >
                      <feature.icon className="h-8 w-8 text-white" />
                    </motion.div>
                    <CardTitle className="text-xl text-white group-hover:text-cyan-400 transition-colors duration-300">
                      {feature.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-center relative">
                    <CardDescription className="text-gray-400 mb-4">
                      {feature.description}
                    </CardDescription>
                    <motion.div
                      className="bg-gray-800/50 p-3 rounded-lg"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{
                        opacity: hoveredFeature === index ? 1 : 0,
                        y: hoveredFeature === index ? 0 : 20,
                      }}
                      transition={{ duration: 0.3 }}
                    >
                      <p className="text-2xl font-bold text-cyan-400">
                        {feature.stats.value}
                      </p>
                      <p className="text-xs text-gray-400">
                        {feature.stats.label}
                      </p>
                    </motion.div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 50, scale: 0.8 }}
                whileInView={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center group"
                whileHover={{ scale: 1.1, y: -10 }}
              >
                <motion.div
                  className="mx-auto w-16 h-16 bg-gray-800/50 rounded-2xl p-4 mb-4 group-hover:scale-110 transition-transform duration-300"
                  whileHover={{ rotate: 5 }}
                  transition={{ type: 'spring', stiffness: 400, damping: 10 }}
                >
                  <stat.icon className={`h-8 w-8 ${stat.color}`} />
                </motion.div>
                <motion.div
                  className="text-4xl md:text-5xl font-black bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2"
                  key={stat.value}
                  initial={{ scale: 1.2, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.3 }}
                >
                  {stat.value}
                </motion.div>
                <div className="text-sm text-gray-400 mb-1">{stat.label}</div>
                <motion.div
                  className="text-xs text-green-400 font-bold flex items-center justify-center space-x-1"
                  whileHover={{ scale: 1.1 }}
                >
                  {stat.trend === 'up' ? (
                    <ArrowUpRight className="h-3 w-3" />
                  ) : stat.trend === 'down' ? (
                    <ArrowDownRight className="h-3 w-3" />
                  ) : (
                    <ArrowLeftRight className="h-3 w-3" />
                  )}
                  <span>{stat.change}</span>
                </motion.div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <motion.div
            className="text-center mb-20"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-5xl md:text-6xl font-black mb-6">
              <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                CHOOSE YOUR
              </span>
              <br />
              <span className="text-white">WEAPON PLAN</span>
            </h2>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              Select the perfect security arsenal for your needs
            </p>
          </motion.div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-3 px-4">
            {[
              {
                name: 'STARTER',
                price: '$29',
                period: '/month',
                description: 'Perfect for individual security researchers',
                features: [
                  'Basic vulnerability scanning',
                  '5 scan targets per month',
                  'Standard reports',
                  'Email support',
                  'Basic threat detection',
                ],
                gradient: 'from-gray-500 to-gray-600',
                popular: false,
              },
              {
                name: 'PROFESSIONAL',
                price: '$99',
                period: '/month',
                description: 'For security teams and professionals',
                features: [
                  'Advanced vulnerability scanning',
                  'Unlimited scan targets',
                  'Detailed reports & analytics',
                  'Priority support',
                  'AI-powered threat detection',
                  'Custom scan profiles',
                  'API access',
                ],
                gradient: 'from-blue-500 to-cyan-500',
                popular: true,
              },
              {
                name: 'ENTERPRISE',
                price: '$299',
                period: '/month',
                description: 'For large organizations and enterprises',
                features: [
                  'Enterprise-grade security',
                  'Unlimited everything',
                  'Custom integrations',
                  'Dedicated support team',
                  'Advanced AI algorithms',
                  'Compliance reporting',
                  'White-label solutions',
                  'On-premise deployment',
                ],
                gradient: 'from-purple-500 to-pink-500',
                popular: false,
              },
            ].map((plan, index) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 50, scale: 0.8 }}
                whileInView={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                whileHover={{ y: -15, scale: 1.05 }}
                className="group cursor-pointer"
              >
                <Card
                  className={`h-full bg-gray-900/50 border-gray-800 hover:border-gray-700 transition-all duration-500 backdrop-blur-sm relative overflow-hidden flex flex-col ${
                    plan.popular
                      ? 'ring-2 ring-blue-500/50 shadow-lg shadow-blue-500/25'
                      : ''
                  }`}
                >
                  {plan.popular && (
                    <motion.div
                      className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-4 py-1.5 rounded-full text-xs font-bold shadow-lg"
                      initial={{ scale: 0, y: -10 }}
                      whileInView={{ scale: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: 0.3 }}
                    >
                      MOST POPULAR
                    </motion.div>
                  )}
                  <motion.div
                    className={`absolute inset-0 bg-gradient-to-r ${plan.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-500`}
                  />
                  <CardHeader className="text-center relative pt-6">
                    <CardTitle className="text-2xl text-white group-hover:text-cyan-400 transition-colors duration-300 mb-2">
                      {plan.name}
                    </CardTitle>
                    <div className="mb-4">
                      <span className="text-4xl font-black text-white">
                        {plan.price}
                      </span>
                      <span className="text-gray-400">{plan.period}</span>
                    </div>
                    <CardDescription className="text-gray-400">
                      {plan.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="relative flex-1 flex flex-col justify-between">
                    <ul className="space-y-3 mb-8">
                      {plan.features.map((feature, featureIndex) => (
                        <motion.li
                          key={feature}
                          className="flex items-center space-x-3 text-gray-300"
                          initial={{ opacity: 0, x: -20 }}
                          whileInView={{ opacity: 1, x: 0 }}
                          transition={{
                            duration: 0.3,
                            delay: featureIndex * 0.1,
                          }}
                        >
                          <motion.div
                            className="w-2 h-2 bg-cyan-400 rounded-full"
                            animate={{
                              scale: [1, 1.2, 1],
                              opacity: [1, 0.7, 1],
                            }}
                            transition={{
                              duration: 2,
                              repeat: Infinity,
                              delay: featureIndex * 0.2,
                            }}
                          />
                          <span className="text-sm">{feature}</span>
                        </motion.li>
                      ))}
                    </ul>
                    <motion.div
                      whileHover={{ scale: 1.05, y: -2 }}
                      whileTap={{ scale: 0.95 }}
                      transition={{
                        type: 'spring',
                        stiffness: 400,
                        damping: 10,
                      }}
                    >
                      <Button
                        className={`w-full font-semibold transition-all duration-300 ${
                          plan.popular
                            ? 'bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 hover:shadow-lg hover:shadow-blue-500/25'
                            : 'bg-gray-700 hover:bg-gray-600 hover:shadow-lg hover:shadow-gray-500/25'
                        }`}
                        onClick={handleDashboardClick}
                        disabled={isLoading}
                      >
                        {isLoading ? (
                          <>
                            <motion.div
                              animate={{ rotate: 360 }}
                              transition={{
                                duration: 1,
                                repeat: Infinity,
                                ease: 'linear',
                              }}
                              className="mr-2"
                            >
                              <RotateCcw className="h-4 w-4" />
                            </motion.div>
                            LOADING...
                          </>
                        ) : (
                          <>
                            <Target className="mr-2 h-4 w-4" />
                            GET STARTED
                          </>
                        )}
                      </Button>
                    </motion.div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <motion.div
            className="text-center mb-20"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-5xl md:text-6xl font-black mb-6">
              <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                FREQUENTLY ASKED
              </span>
              <br />
              <span className="text-white">QUESTIONS</span>
            </h2>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              Everything you need to know about SecurityScanner
            </p>
          </motion.div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            {[
              {
                question: 'How accurate is the vulnerability detection?',
                answer:
                  'Our AI-powered system achieves 99.9% accuracy with false positive rates below 0.1%. We use multiple scanning engines and machine learning algorithms to ensure reliable results.',
              },
              {
                question: 'What types of targets can I scan?',
                answer:
                  'You can scan web applications, APIs, networks, cloud infrastructure, and mobile applications. We support both internal and external security assessments.',
              },
              {
                question: 'Is it legal to use SecurityScanner?',
                answer:
                  'Yes, SecurityScanner is designed for ethical hacking and authorized security testing. Always ensure you have proper authorization before scanning any target.',
              },
              {
                question: 'How fast are the scans?',
                answer:
                  'Scan speed depends on target complexity and scan depth. Basic scans complete in minutes, while comprehensive scans may take several hours for large targets.',
              },
              {
                question: 'Do you provide compliance reports?',
                answer:
                  'Yes, we generate detailed reports that help meet various compliance requirements including SOC2, ISO 27001, PCI DSS, and HIPAA standards.',
              },
              {
                question: 'Can I integrate with my existing tools?',
                answer:
                  'Absolutely! We provide comprehensive APIs and webhooks for integration with SIEM systems, ticketing platforms, and other security tools.',
              },
            ].map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -5, scale: 1.02 }}
                className="group cursor-pointer"
              >
                <Card className="h-full bg-gray-900/50 border-gray-800 hover:border-gray-700 transition-all duration-500 backdrop-blur-sm relative overflow-hidden">
                  <motion.div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                  <CardContent className="relative p-6">
                    <h3 className="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors duration-300 mb-3">
                      {faq.question}
                    </h3>
                    <p className="text-gray-400 text-sm leading-relaxed">
                      {faq.answer}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Privacy Section */}
      <section id="privacy" className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <motion.div
            className="text-center mb-20"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-5xl md:text-6xl font-black mb-6">
              <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                PRIVACY &
              </span>
              <br />
              <span className="text-white">SECURITY</span>
            </h2>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              Your data security is our top priority
            </p>
          </motion.div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            {[
              {
                icon: Lock,
                title: 'Data Encryption',
                description:
                  'All data is encrypted using AES-256 encryption both in transit and at rest. We never store sensitive information without proper encryption.',
                gradient: 'from-blue-500 to-cyan-500',
              },
              {
                icon: Shield,
                title: 'Privacy First',
                description:
                  'We follow strict privacy policies and never share your data with third parties. Your scan results and configurations remain completely private.',
                gradient: 'from-green-500 to-emerald-500',
              },
              {
                icon: Users,
                title: 'GDPR Compliant',
                description:
                  'Full compliance with GDPR, CCPA, and other privacy regulations. You have complete control over your data and can request deletion anytime.',
                gradient: 'from-purple-500 to-pink-500',
              },
            ].map((item, index) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 50, scale: 0.8 }}
                whileInView={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                whileHover={{ y: -15, scale: 1.05 }}
                className="group cursor-pointer"
              >
                <Card className="h-full bg-gray-900/50 border-gray-800 hover:border-gray-700 transition-all duration-500 backdrop-blur-sm relative overflow-hidden">
                  <motion.div
                    className={`absolute inset-0 bg-gradient-to-r ${item.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-500`}
                  />
                  <CardHeader className="text-center relative">
                    <motion.div
                      className={`mx-auto w-16 h-16 bg-gradient-to-r ${item.gradient} rounded-2xl p-4 mb-4 group-hover:scale-110 transition-transform duration-300`}
                      whileHover={{ rotate: 5 }}
                      transition={{
                        type: 'spring',
                        stiffness: 400,
                        damping: 10,
                      }}
                    >
                      <item.icon className="h-8 w-8 text-white" />
                    </motion.div>
                    <CardTitle className="text-xl text-white group-hover:text-cyan-400 transition-colors duration-300">
                      {item.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-center relative">
                    <CardDescription className="text-gray-400">
                      {item.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Changelogs Section */}
      <section id="changelogs" className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <motion.div
            className="text-center mb-20"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-5xl md:text-6xl font-black mb-6">
              <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                LATEST
              </span>
              <br />
              <span className="text-white">UPDATES</span>
            </h2>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              Stay updated with our latest features and improvements
            </p>
          </motion.div>

          <div className="space-y-8">
            {[
              {
                version: 'v2.1.0',
                date: 'December 15, 2024',
                title: 'Advanced AI Detection Engine',
                description:
                  'Introducing our next-generation AI-powered vulnerability detection system with improved accuracy and reduced false positives.',
                features: [
                  'Enhanced ML algorithms',
                  'Real-time threat intelligence',
                  'Improved scanning speed',
                ],
                type: 'major',
              },
              {
                version: 'v2.0.5',
                date: 'November 28, 2024',
                title: 'Performance Optimizations',
                description:
                  'Major performance improvements and bug fixes for better user experience.',
                features: [
                  'Faster scan execution',
                  'Reduced memory usage',
                  'UI responsiveness improvements',
                ],
                type: 'patch',
              },
              {
                version: 'v2.0.0',
                date: 'November 15, 2024',
                title: 'Complete Platform Overhaul',
                description:
                  'Major redesign with new features, improved security, and better user interface.',
                features: [
                  'New dashboard design',
                  'Enhanced reporting system',
                  'API v2.0 release',
                ],
                type: 'major',
              },
            ].map((update, index) => (
              <motion.div
                key={update.version}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                whileHover={{ y: -5, scale: 1.02 }}
                className="group cursor-pointer"
              >
                <Card className="bg-gray-900/50 border-gray-800 hover:border-gray-700 transition-all duration-500 backdrop-blur-sm relative overflow-hidden">
                  <motion.div
                    className={`absolute inset-0 bg-gradient-to-r ${
                      update.type === 'major'
                        ? 'from-blue-500/5 to-cyan-500/5'
                        : update.type === 'patch'
                          ? 'from-green-500/5 to-emerald-500/5'
                          : 'from-purple-500/5 to-pink-500/5'
                    } opacity-0 group-hover:opacity-100 transition-opacity duration-500`}
                  />
                  <CardContent className="relative p-8">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <div className="flex items-center space-x-3 mb-2">
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-bold ${
                              update.type === 'major'
                                ? 'bg-blue-500/20 text-blue-400'
                                : update.type === 'patch'
                                  ? 'bg-green-500/20 text-green-400'
                                  : 'bg-purple-500/20 text-purple-400'
                            }`}
                          >
                            {update.type.toUpperCase()}
                          </span>
                          <span className="text-2xl font-black text-white">
                            {update.version}
                          </span>
                        </div>
                        <h3 className="text-xl font-bold text-white group-hover:text-cyan-400 transition-colors duration-300 mb-2">
                          {update.title}
                        </h3>
                        <p className="text-gray-400 mb-4">
                          {update.description}
                        </p>
                      </div>
                      <span className="text-sm text-gray-500">
                        {update.date}
                      </span>
                    </div>
                    <div className="space-y-2">
                      {update.features.map((feature, featureIndex) => (
                        <motion.div
                          key={feature}
                          className="flex items-center space-x-3 text-gray-300"
                          initial={{ opacity: 0, x: -20 }}
                          whileInView={{ opacity: 1, x: 0 }}
                          transition={{
                            duration: 0.3,
                            delay: featureIndex * 0.1,
                          }}
                        >
                          <motion.div
                            className="w-2 h-2 bg-cyan-400 rounded-full"
                            animate={{
                              scale: [1, 1.2, 1],
                              opacity: [1, 0.7, 1],
                            }}
                            transition={{
                              duration: 2,
                              repeat: Infinity,
                              delay: featureIndex * 0.2,
                            }}
                          />
                          <span className="text-sm">{feature}</span>
                        </motion.div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            whileInView={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <Card className="relative overflow-hidden bg-gradient-to-r from-blue-900/50 to-purple-900/50 border-blue-500/30">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10"></div>
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5"
                animate={{
                  backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
                }}
                transition={{
                  duration: 10,
                  repeat: Infinity,
                  ease: 'linear',
                }}
                style={{
                  backgroundSize: '200% 200%',
                }}
              />
              <CardContent className="relative p-16 text-center">
                <motion.h2
                  className="text-5xl md:text-6xl font-black mb-6"
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.2 }}
                  viewport={{ once: true }}
                >
                  <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                    READY TO
                  </span>
                  <br />
                  <span className="text-white">DOMINATE SECURITY?</span>
                </motion.h2>
                <motion.p
                  className="text-2xl text-gray-300 mb-10 max-w-3xl mx-auto"
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.4 }}
                  viewport={{ once: true }}
                >
                  Join thousands of security professionals who trust
                  SecurityScanner
                </motion.p>
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.6 }}
                  viewport={{ once: true }}
                >
                  <motion.div
                    whileHover={{ scale: 1.05, y: -5 }}
                    whileTap={{ scale: 0.95 }}
                    transition={{ type: 'spring', stiffness: 400, damping: 10 }}
                  >
                    <Button
                      size="lg"
                      variant="premium"
                      className="text-xl px-10 py-5 font-bold relative overflow-hidden group"
                      onClick={handleDashboardClick}
                      disabled={isLoading}
                    >
                      <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                      <div className="relative flex items-center">
                        {isLoading ? (
                          <>
                            <motion.div
                              animate={{ rotate: 360 }}
                              transition={{
                                duration: 1,
                                repeat: Infinity,
                                ease: 'linear',
                              }}
                              className="mr-3"
                            >
                              <RotateCcw className="h-6 w-6" />
                            </motion.div>
                            LOADING...
                          </>
                        ) : (
                          <>
                            <Target className="mr-3 h-6 w-6" />
                            DEPLOY NOW
                            <ArrowRight className="ml-3 h-6 w-6" />
                          </>
                        )}
                      </div>
                    </Button>
                  </motion.div>
                </motion.div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <motion.footer
        className="relative border-t border-gray-800/50 py-12"
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              className="flex items-center justify-center space-x-3 mb-6"
              whileHover={{ scale: 1.05 }}
              transition={{ type: 'spring', stiffness: 400, damping: 10 }}
            >
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg blur-sm opacity-75"></div>
                <div className="relative bg-gradient-to-r from-blue-500 to-cyan-500 p-2 rounded-lg">
                  <Shield className="h-6 w-6 text-white" />
                </div>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                SecurityScanner
              </span>
            </motion.div>
            <p className="text-gray-500 mb-4">
              Professional security scanning and vulnerability assessment
              platform
            </p>
            <div className="flex items-center justify-center space-x-6 text-sm text-gray-500">
              <span>© 2024 SecurityScanner</span>
              <span>•</span>
              <span>All rights reserved</span>
              <span>•</span>
              <span>Built for professionals</span>
            </div>
          </div>
        </div>
      </motion.footer>

      {/* Loading Overlay */}
      <AnimatePresence>
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center"
          >
            <div className="text-center">
              {/* Loading Icon */}
              <motion.div
                className="mx-auto w-24 h-24 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full p-6 mb-8"
                animate={{
                  scale: [1, 1.1, 1],
                  rotate: [0, 360],
                }}
                transition={{
                  scale: { duration: 2, repeat: Infinity, ease: 'easeInOut' },
                  rotate: { duration: 3, repeat: Infinity, ease: 'linear' },
                }}
              >
                <Shield className="h-12 w-12 text-white" />
              </motion.div>

              {/* Loading Text */}
              <motion.h2
                className="text-3xl font-bold text-white mb-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                INITIALIZING SECURITY SCANNER
              </motion.h2>

              {/* Loading Description */}
              <motion.p
                className="text-xl text-gray-300 mb-8 max-w-md mx-auto"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                Deploying advanced security protocols and threat detection
                systems...
              </motion.p>

              {/* Progress Bar */}
              <div className="w-96 bg-gray-800 rounded-full h-3 mx-auto mb-6 overflow-hidden">
                <motion.div
                  className="bg-gradient-to-r from-blue-500 to-cyan-500 h-3 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: '100%' }}
                  transition={{ duration: 2, ease: 'easeInOut' }}
                />
              </div>

              {/* Loading Steps */}
              <div className="space-y-3">
                {[
                  'Initializing core systems...',
                  'Loading security engines...',
                  'Establishing secure connections...',
                  'Preparing dashboard interface...',
                ].map((step, index) => (
                  <motion.div
                    key={step}
                    className="flex items-center space-x-3 text-gray-300"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: index * 0.3 }}
                  >
                    <motion.div
                      className="w-2 h-2 bg-cyan-400 rounded-full"
                      animate={{
                        scale: [1, 1.5, 1],
                        opacity: [1, 0.7, 1],
                      }}
                      transition={{
                        duration: 1.5,
                        repeat: Infinity,
                        delay: index * 0.2,
                      }}
                    />
                    <span className="text-sm">{step}</span>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
