'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Clock, CheckCircle, AlertCircle, XCircle, Shield } from 'lucide-react'
import { useScanStore } from '@/store/scanStore'

interface Scan {
  id: number
  target_url: string
  scan_type: string
  status: string
  progress: number
  created_at: string
}

interface ScanProgressProps {
  scan: Scan
}

export default function ScanProgress({ scan }: ScanProgressProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [stepStatus, setStepStatus] = useState<'pending' | 'running' | 'completed' | 'failed'>('pending')
  const { updateScanProgress, addVulnerability } = useScanStore()

  const scanSteps = [
    {
      name: 'Bağlantı Testi',
      description: 'Hedef URL\'ye bağlantı kuruluyor',
      icon: Shield,
      duration: 2000
    },
    {
      name: 'Port Taraması',
      description: 'Açık portlar ve servisler tespit ediliyor',
      icon: Shield,
      duration: 3000
    },
    {
      name: 'XSS Testi',
      description: 'Cross-Site Scripting açıkları kontrol ediliyor',
      icon: Shield,
      duration: 4000
    },
    {
      name: 'SQL Injection Testi',
      description: 'SQL Injection açıkları kontrol ediliyor',
      icon: Shield,
      duration: 3000
    },
    {
      name: 'Güvenlik Başlıkları',
      description: 'HTTP güvenlik başlıkları analiz ediliyor',
      icon: Shield,
      duration: 2000
    },
    {
      name: 'Sonuç Analizi',
      description: 'Tespit edilen açıklar analiz ediliyor',
      icon: Shield,
      duration: 2000
    }
  ]

  useEffect(() => {
    if (scan.status === 'running') {
      simulateScanProgress()
    }
  }, [scan.status])

  const simulateScanProgress = async () => {
    for (let i = 0; i < scanSteps.length; i++) {
      setCurrentStep(i)
      setStepStatus('running')
      
      // Simüle edilmiş güvenlik açıkları ekle
      if (i === 2) { // XSS testi
        setTimeout(() => {
          addVulnerability({
            id: Date.now(),
            title: 'Reflected XSS Tespit Edildi',
            description: 'URL parametresinde Cross-Site Scripting açığı tespit edildi',
            severity: 'high',
            location: scan.target_url,
            evidence: 'Parameter: search, Payload: <script>alert("XSS")</script>',
            scanner_name: 'XSS Scanner',
            timestamp: new Date().toISOString()
          })
        }, 2000)
      }
      
      if (i === 3) { // SQL Injection testi
        setTimeout(() => {
          addVulnerability({
            id: Date.now() + 1,
            title: 'SQL Injection Tespit Edildi',
            description: 'Form alanında SQL Injection açığı tespit edildi',
            severity: 'critical',
            location: scan.target_url,
            evidence: 'Field: username, Payload: \' OR 1=1--',
            scanner_name: 'SQLMap Scanner',
            timestamp: new Date().toISOString()
          })
        }, 2000)
      }
      
      if (i === 4) { // Security Headers testi
        setTimeout(() => {
          addVulnerability({
            id: Date.now() + 2,
            title: 'Güvenlik Başlıkları Eksik',
            description: 'Önemli güvenlik başlıkları eksik veya yanlış yapılandırılmış',
            severity: 'medium',
            location: scan.target_url,
            evidence: 'Missing: X-Frame-Options, X-Content-Type-Options',
            scanner_name: 'Security Headers Scanner',
            timestamp: new Date().toISOString()
          })
        }, 2000)
      }
      
      await new Promise(resolve => setTimeout(resolve, scanSteps[i].duration))
      setStepStatus('completed')
      
      // Progress'i güncelle
      const progress = ((i + 1) / scanSteps.length) * 100
      updateScanProgress(scan.id, progress)
    }
    
    // Tarama tamamlandı
    updateScanProgress(scan.id, 100, 'completed')
  }

  const getStepIcon = (stepIndex: number, status: string) => {
    if (stepIndex < currentStep) {
      return <CheckCircle className="h-5 w-5 text-success-600" />
    } else if (stepIndex === currentStep && status === 'running') {
      return <div className="animate-spin rounded-full h-5 w-5 border-2 border-primary-600 border-t-transparent"></div>
    } else if (stepIndex === currentStep && status === 'failed') {
      return <XCircle className="h-5 w-5 text-danger-600" />
    } else {
      return <Clock className="h-5 w-5 text-gray-400" />
    }
  }

  const getStepStatus = (stepIndex: number) => {
    if (stepIndex < currentStep) {
      return 'completed'
    } else if (stepIndex === currentStep) {
      return stepStatus
    } else {
      return 'pending'
    }
  }

  const getStepClasses = (stepIndex: number) => {
    const status = getStepStatus(stepIndex)
    
    switch (status) {
      case 'completed':
        return 'border-success-200 bg-success-50'
      case 'running':
        return 'border-primary-200 bg-primary-50'
      case 'failed':
        return 'border-danger-200 bg-danger-50'
      default:
        return 'border-gray-200 bg-white'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      className="card max-w-4xl mx-auto"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-semibold text-gray-900">
            Tarama İlerlemesi
          </h3>
          <p className="text-gray-600">
            {scan.target_url} - {scan.scan_type} taraması
          </p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-primary-600">
            {Math.round(scan.progress)}%
          </div>
          <div className="text-sm text-gray-500">
            {scan.status === 'completed' ? 'Tamamlandı' : 'Devam ediyor'}
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-6">
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className="bg-primary-600 h-2 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${scan.progress}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Scan Steps */}
      <div className="space-y-4">
        {scanSteps.map((step, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`flex items-center space-x-4 p-4 rounded-lg border-2 transition-all ${getStepClasses(index)}`}
          >
            <div className="flex-shrink-0">
              {getStepIcon(index, getStepStatus(index))}
            </div>
            
            <div className="flex-1">
              <div className="font-medium text-gray-900">
                {step.name}
              </div>
              <div className="text-sm text-gray-600">
                {step.description}
              </div>
            </div>
            
            <div className="flex-shrink-0">
              {getStepStatus(index) === 'completed' && (
                <CheckCircle className="h-5 w-5 text-success-600" />
              )}
              {getStepStatus(index) === 'failed' && (
                <AlertCircle className="h-5 w-5 text-danger-600" />
              )}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Status Messages */}
      {scan.status === 'running' && (
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-600 border-t-transparent"></div>
            <span className="text-blue-800">
              {scanSteps[currentStep]?.name} adımı çalışıyor...
            </span>
          </div>
        </div>
      )}

      {scan.status === 'completed' && (
        <div className="mt-6 p-4 bg-success-50 border border-success-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <CheckCircle className="h-5 w-5 text-success-600" />
            <span className="text-success-800 font-medium">
              Tarama başarıyla tamamlandı!
            </span>
          </div>
          <p className="text-success-700 mt-2">
            Tespit edilen güvenlik açıkları aşağıda listelenmiştir.
          </p>
        </div>
      )}

      {scan.status === 'failed' && (
        <div className="mt-6 p-4 bg-danger-50 border border-danger-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <XCircle className="h-5 w-5 text-danger-600" />
            <span className="text-danger-800 font-medium">
              Tarama sırasında hata oluştu
            </span>
          </div>
          <p className="text-danger-700 mt-2">
            Lütfen tekrar deneyin veya destek ekibi ile iletişime geçin.
          </p>
        </div>
      )}
    </motion.div>
  )
}
