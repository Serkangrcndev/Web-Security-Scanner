'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Shield, Code, ArrowRight, Home, CheckCircle, AlertTriangle, Clock, TrendingUp, Users, Globe, Server, Key, LockKeyhole, Folder, Star, Sparkles, Zap2, Target, Crosshair, Binoculars, Telescope, Satellite, Wifi, WifiOff, Signal, SignalHigh, SignalMedium, SignalLow, ArrowUpRight, ArrowDownRight, ArrowLeftRight, RotateCcw, Play, Pause, Square, Timer, Gauge, BarChart4, PieChart as PieChartIcon, TrendingDown, Pulse, Heart, Zap2 as ZapIcon, Target as TargetIcon, Crosshair as CrosshairIcon, Binoculars as BinocularsIcon, Telescope as TelescopeIcon, Satellite as SatelliteIcon, Wifi as WifiIcon, WifiOff as WifiOffIcon, Signal as SignalIcon, SignalHigh as SignalHighIcon, SignalMedium as SignalMediumIcon, SignalLow as SignalLowIcon } from 'lucide-react';
import Link from 'next/link';

export default function FAQPage() {
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

  const faqs = [
    {
      question: 'How accurate is the vulnerability detection?',
      answer: 'Our AI-powered system achieves 99.9% accuracy with false positive rates below 0.1%. We use multiple scanning engines and machine learning algorithms to ensure reliable results.',
      category: 'Accuracy'
    },
    {
      question: 'What types of targets can I scan?',
      answer: 'You can scan web applications, APIs, networks, cloud infrastructure, and mobile applications. We support both internal and external security assessments.',
      category: 'Targets'
    },
    {
      question: 'Is it legal to use SecurityScanner?',
      answer: 'Yes, SecurityScanner is designed for ethical hacking and authorized security testing. Always ensure you have proper authorization before scanning any target.',
      category: 'Legal'
    },
    {
      question: 'How fast are the scans?',
      answer: 'Scan speed depends on target complexity and scan depth. Basic scans complete in minutes, while comprehensive scans may take several hours for large targets.',
      category: 'Performance'
    },
    {
      question: 'Do you provide compliance reports?',
      answer: 'Yes, we generate detailed reports that help meet various compliance requirements including SOC2, ISO 27001, PCI DSS, and HIPAA standards.',
      category: 'Compliance'
    },
    {
      question: 'Can I integrate with my existing tools?',
      answer: 'Absolutely! We provide comprehensive APIs and webhooks for integration with SIEM systems, ticketing platforms, and other security tools.',
      category: 'Integration'
    },
    {
      question: 'What scanning engines do you use?',
      answer: 'We integrate multiple industry-standard tools including Nmap, Nuclei, ZAP, SQLMap, Nikto, and Dirb for comprehensive security assessment.',
      category: 'Engines'
    },
    {
      question: 'How do you handle false positives?',
      answer: 'Our AI system learns from previous scans and user feedback to continuously improve accuracy. We also provide manual verification tools for suspicious findings.',
      category: 'Accuracy'
    },
    {
      question: 'Can I schedule automated scans?',
      answer: 'Yes, you can set up recurring scans with custom schedules, automated reporting, and instant alerts when vulnerabilities are detected.',
      category: 'Automation'
    },
    {
      question: 'What support options are available?',
      answer: 'We offer email support for all plans, priority support for Professional users, and dedicated support teams for Enterprise customers.',
      category: 'Support'
    }
  ];

  const categories = ['All', 'Accuracy', 'Targets', 'Legal', 'Performance', 'Compliance', 'Integration', 'Engines', 'Automation', 'Support'];
  const [selectedCategory, setSelectedCategory] = useState('All');

  const filteredFaqs = selectedCategory === 'All' ? faqs : faqs.filter(faq => faq.category === selectedCategory);

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
            ease: "easeInOut"
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
            ease: "easeInOut"
          }}
        />
      </div>

      {/* Header */}
      <motion.header 
        className="relative z-10"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      >
        <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            {/* Logo/Brand */}
            <motion.div 
              className="flex items-center space-x-3"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 400, damping: 10 }}
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
                    link.href === '/faq' ? 'text-cyan-400' : ''
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
                    whileHover={{ width: "100%" }}
                  />
                </motion.a>
              ))}
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center space-x-4">
              <motion.span 
                className="inline-flex items-center rounded-full bg-gradient-to-r from-yellow-500 to-orange-500 px-3 py-1 text-xs font-medium text-black"
                whileHover={{ scale: 1.05, rotate: 5 }}
                transition={{ type: "spring", stiffness: 400, damping: 10 }}
              >
                <CheckCircle className="mr-1 h-3 w-3" />
                PREMIUM
              </motion.span>
              <motion.div
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                transition={{ type: "spring", stiffness: 400, damping: 10 }}
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
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
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
              transition={{ duration: 1.2, ease: "easeOut" }}
            >
              <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                FREQUENTLY ASKED
              </span>
              <br />
              <span className="text-white">QUESTIONS</span>
            </motion.h1>
            
            <motion.p 
              className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto mb-12 leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, delay: 0.3 }}
            >
              Everything you need to know about SecurityScanner. Find answers to common questions about our platform, features, and security scanning capabilities.
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

      {/* FAQ Section */}
      <section className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {filteredFaqs.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                whileHover={{ y: -5, scale: 1.02 }}
                className="group cursor-pointer"
              >
                <Card className="h-full bg-gray-900/50 border-gray-800 hover:border-gray-700 transition-all duration-500 backdrop-blur-sm relative overflow-hidden">
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
                  />
                  <CardContent className="relative p-8">
                    <div className="flex items-start justify-between mb-4">
                      <span className="px-3 py-1 rounded-full text-xs font-bold bg-blue-500/20 text-blue-400">
                        {faq.category}
                      </span>
                    </div>
                    <h3 className="text-xl font-bold text-white group-hover:text-cyan-400 transition-colors duration-300 mb-4">
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
                  backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
                }}
                transition={{
                  duration: 10,
                  repeat: Infinity,
                  ease: "linear"
                }}
                style={{
                  backgroundSize: "200% 200%"
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
                    STILL HAVE
                  </span>
                  <br />
                  <span className="text-white">QUESTIONS?</span>
                </motion.h2>
                <motion.p 
                  className="text-2xl text-gray-300 mb-10 max-w-3xl mx-auto"
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.4 }}
                  viewport={{ once: true }}
                >
                  Can't find what you're looking for? Contact our support team for personalized assistance.
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
                    transition={{ type: "spring", stiffness: 400, damping: 10 }}
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
                              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                              className="mr-3"
                            >
                              <RotateCcw className="h-6 w-6" />
                            </motion.div>
                            LOADING...
                          </>
                        ) : (
                          <>
                            <Target className="mr-3 h-6 w-6" />
                            CONTACT SUPPORT
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
              transition={{ type: "spring", stiffness: 400, damping: 10 }}
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
              Professional security scanning and vulnerability assessment platform
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
