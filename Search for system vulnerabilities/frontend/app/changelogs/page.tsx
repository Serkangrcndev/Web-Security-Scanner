'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
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
  Code,
  ArrowRight,
  Home,
  CheckCircle,
  Clock,
  TrendingUp,
  Users,
  Globe,
  Server,
  Key,
  LockKeyhole,
  Folder,
  Star,
  Sparkles,
  Zap,
  Target,
  Crosshair,
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
  BarChart3,
  PieChart as PieChartIcon,
  TrendingDown,
  Heart,
} from 'lucide-react';
import Link from 'next/link';

export default function ChangelogsPage() {
  const [isLoading, setIsLoading] = useState(false);

  const handleDashboardClick = () => {
    setIsLoading(true);
    // Simulate loading time
    setTimeout(() => {
      setIsLoading(false);
      window.location.href = '/dashboard';
    }, 2000);
  };

  const navigationLinks = [
    { name: 'Home', href: '/' },
    { name: 'Features', href: '/#features' },
    { name: 'Pricing', href: '/#pricing' },
    { name: 'FAQ', href: '/faq' },
    { name: 'Privacy', href: '/privacy' },
    { name: 'Changelogs', href: '/changelogs' },
  ];

  const updates = [
    {
      version: 'v2.1.0',
      date: 'December 15, 2024',
      title: 'Advanced AI Detection Engine',
      description:
        'Introducing our next-generation AI-powered vulnerability detection system with improved accuracy and reduced false positives.',
      features: [
        'Enhanced ML algorithms with 99.9% accuracy',
        'Real-time threat intelligence integration',
        'Improved scanning speed by 40%',
        'Advanced false positive reduction',
      ],
      type: 'major',
      highlights: ['AI Engine', 'Performance', 'Accuracy'],
    },
    {
      version: 'v2.0.5',
      date: 'November 28, 2024',
      title: 'Performance Optimizations',
      description:
        'Major performance improvements and bug fixes for better user experience and system stability.',
      features: [
        'Faster scan execution (30% improvement)',
        'Reduced memory usage by 25%',
        'UI responsiveness improvements',
        'Enhanced error handling and recovery',
      ],
      type: 'patch',
      highlights: ['Performance', 'Stability', 'UI'],
    },
    {
      version: 'v2.0.0',
      date: 'November 15, 2024',
      title: 'Complete Platform Overhaul',
      description:
        'Major redesign with new features, improved security, and better user interface for enhanced user experience.',
      features: [
        'New dashboard design with dark theme',
        'Enhanced reporting system with PDF export',
        'API v2.0 release with improved endpoints',
        'Advanced user management and permissions',
      ],
      type: 'major',
      highlights: ['Redesign', 'API', 'Dashboard'],
    },
    {
      version: 'v1.9.2',
      date: 'October 30, 2024',
      title: 'Security Enhancements',
      description:
        'Critical security updates and vulnerability patches to ensure the highest level of protection.',
      features: [
        'Updated SSL/TLS configurations',
        'Enhanced authentication mechanisms',
        'Improved input validation',
        'Security audit fixes',
      ],
      type: 'security',
      highlights: ['Security', 'Authentication', 'SSL'],
    },
    {
      version: 'v1.9.0',
      date: 'October 15, 2024',
      title: 'New Scanning Engines',
      description:
        'Added support for additional security scanning tools and improved existing engine capabilities.',
      features: [
        'New Nuclei integration for vulnerability scanning',
        'Enhanced Nmap capabilities',
        'Improved ZAP integration',
        'Better engine coordination and management',
      ],
      type: 'feature',
      highlights: ['Engines', 'Nuclei', 'Integration'],
    },
    {
      version: 'v1.8.5',
      date: 'September 28, 2024',
      title: 'Bug Fixes and Improvements',
      description:
        'Various bug fixes and minor improvements to enhance overall system stability and user experience.',
      features: [
        'Fixed scan progress tracking issues',
        'Improved error message clarity',
        'Enhanced mobile responsiveness',
        'Better handling of large scan results',
      ],
      type: 'patch',
      highlights: ['Bug Fixes', 'Mobile', 'Stability'],
    },
  ];

  const categories = ['All', 'Major', 'Feature', 'Patch', 'Security'];
  const [selectedCategory, setSelectedCategory] = useState('All');

  const filteredUpdates =
    selectedCategory === 'All'
      ? updates
      : updates.filter(
          (update) => update.type === selectedCategory.toLowerCase()
        );

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'major':
        return 'from-blue-500/20 to-cyan-500/20 text-blue-400';
      case 'feature':
        return 'from-green-500/20 to-emerald-500/20 text-green-400';
      case 'patch':
        return 'from-yellow-500/20 to-orange-500/20 text-yellow-400';
      case 'security':
        return 'from-red-500/20 to-pink-500/20 text-red-400';
      default:
        return 'from-gray-500/20 to-gray-600/20 text-gray-400';
    }
  };

  const getTypeGradient = (type: string) => {
    switch (type) {
      case 'major':
        return 'from-blue-500/5 to-cyan-500/5';
      case 'feature':
        return 'from-green-500/5 to-emerald-500/5';
      case 'patch':
        return 'from-yellow-500/5 to-orange-500/5';
      case 'security':
        return 'from-red-500/5 to-pink-500/5';
      default:
        return 'from-gray-500/5 to-gray-600/5';
    }
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
              <Link href="/">
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg blur-sm opacity-75"></div>
                  <div className="relative bg-gradient-to-r from-blue-500 to-cyan-500 p-2 rounded-lg">
                    <Code className="h-6 w-6 text-white" />
                  </div>
                </div>
              </Link>
              <Link href="/">
                <span className="text-xl font-bold text-white">
                  SecurityScanner
                </span>
              </Link>
            </motion.div>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center space-x-8">
              {navigationLinks.map((link, index) => (
                <motion.a
                  key={link.name}
                  href={link.href}
                  className={`text-gray-300 hover:text-white transition-colors duration-200 font-medium relative group ${
                    link.href === '/changelogs' ? 'text-cyan-400' : ''
                  }`}
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
            <motion.h1
              className="text-6xl md:text-7xl font-black tracking-tight mb-8"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1.2, ease: 'easeOut' }}
            >
              <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                LATEST
              </span>
              <br />
              <span className="text-white">UPDATES</span>
            </motion.h1>

            <motion.p
              className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto mb-12 leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.3 }}
            >
              Stay updated with our latest features, improvements, and security
              enhancements. Track the evolution of SecurityScanner and see
              what's new.
            </motion.p>

            {/* Category Filter */}
            <motion.div
              className="flex flex-wrap justify-center gap-3 mb-12"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.5 }}
            >
              {categories.map((category, index) => (
                <motion.button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 ${
                    selectedCategory === category
                      ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg shadow-blue-500/25'
                      : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50 hover:text-white'
                  }`}
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.6 + index * 0.1 }}
                >
                  {category}
                </motion.button>
              ))}
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Changelogs Section */}
      <section className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <div className="space-y-8">
            {filteredUpdates.map((update, index) => (
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
                    className={`absolute inset-0 bg-gradient-to-r ${getTypeGradient(
                      update.type
                    )} opacity-0 group-hover:opacity-100 transition-opacity duration-500`}
                  />
                  <CardContent className="relative p-8">
                    <div className="flex items-start justify-between mb-6">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-3">
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-bold ${getTypeColor(
                              update.type
                            )}`}
                          >
                            {update.type.toUpperCase()}
                          </span>
                          <span className="text-3xl font-black text-white">
                            {update.version}
                          </span>
                        </div>
                        <h3 className="text-2xl font-bold text-white group-hover:text-cyan-400 transition-colors duration-300 mb-3">
                          {update.title}
                        </h3>
                        <p className="text-gray-400 mb-6 text-lg">
                          {update.description}
                        </p>

                        {/* Highlights */}
                        <div className="flex flex-wrap gap-2 mb-6">
                          {update.highlights.map(
                            (highlight, highlightIndex) => (
                              <motion.span
                                key={highlight}
                                className="px-3 py-1 rounded-full text-xs font-medium bg-cyan-500/20 text-cyan-400"
                                initial={{ opacity: 0, scale: 0.8 }}
                                whileInView={{ opacity: 1, scale: 1 }}
                                transition={{
                                  duration: 0.3,
                                  delay: highlightIndex * 0.1,
                                }}
                              >
                                {highlight}
                              </motion.span>
                            )
                          )}
                        </div>

                        {/* Features */}
                        <div className="space-y-3">
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
                      </div>
                      <div className="text-right ml-6">
                        <span className="text-sm text-gray-500">
                          {update.date}
                        </span>
                      </div>
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
                  <span className="text-white">EXPERIENCE THE LATEST?</span>
                </motion.h2>
                <motion.p
                  className="text-2xl text-gray-300 mb-10 max-w-3xl mx-auto"
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.4 }}
                  viewport={{ once: true }}
                >
                  Try our latest features and improvements with a free trial of
                  SecurityScanner.
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
                            START FREE TRIAL
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
    </div>
  );
}
