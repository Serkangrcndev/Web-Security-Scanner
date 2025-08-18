'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Search, Settings, Play, Shield } from 'lucide-react'
import { useScanStore } from '@/store/scanStore'
import toast from 'react-hot-toast'

interface ScanFormProps {
  onScanStart: () => void
}

export default function ScanForm({ onScanStart }: ScanFormProps) {
  const [url, setUrl] = useState('')
  const [scanType, setScanType] = useState('quick')
  const [isLoading, setIsLoading] = useState(false)
  const { startScan, setCurrentScan } = useScanStore()

  const scanTypes = [
    {
      id: 'quick',
      name: 'Hızlı Tarama',
      description: 'Temel güvenlik kontrolleri (5-10 dakika)',
      icon: Play,
      color: 'text-success-600'
    },
    {
      id: 'standard',
      name: 'Standart Tarama',
      description: 'Kapsamlı güvenlik analizi (15-30 dakika)',
      icon: Shield,
      color: 'text-primary-600'
    },
    {
      id: 'full',
      name: 'Tam Tarama',
      description: 'Tüm güvenlik testleri (30-60 dakika)',
      icon: Settings,
      color: 'text-warning-600'
    }
  ]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!url.trim()) {
      toast.error('Lütfen bir URL girin')
      return
    }

    // URL formatını kontrol et
    try {
      new URL(url)
    } catch {
      toast.error('Geçerli bir URL girin (örn: https://example.com)')
      return
    }

    setIsLoading(true)
    
    try {
      // Simüle edilmiş tarama başlatma
      const scan = {
        id: Date.now(),
        target_url: url,
        scan_type: scanType,
        status: 'running',
        progress: 0,
        created_at: new Date().toISOString()
      }

      setCurrentScan(scan)
      startScan(scan)
      onScanStart()
      
      toast.success('Tarama başlatıldı!')
      
      // Form'u temizle
      setUrl('')
      
    } catch (error) {
      toast.error('Tarama başlatılamadı')
      console.error('Scan error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card max-w-4xl mx-auto"
    >
      <div className="text-center mb-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          Güvenlik Taraması Başlat
        </h3>
        <p className="text-gray-600">
          Web sitenizin güvenlik açıklarını tespit etmek için URL'yi girin
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* URL Input */}
        <div>
          <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
            Hedef URL
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="url"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com"
              className="input pl-10"
              required
            />
          </div>
          <p className="mt-1 text-sm text-gray-500">
            HTTP veya HTTPS protokolü ile başlayan geçerli bir URL girin
          </p>
        </div>

        {/* Scan Type Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Tarama Türü
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {scanTypes.map((type) => {
              const Icon = type.icon
              return (
                <label
                  key={type.id}
                  className={`relative cursor-pointer rounded-lg border-2 p-4 transition-all hover:shadow-md ${
                    scanType === type.id
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="scanType"
                    value={type.id}
                    checked={scanType === type.id}
                    onChange={(e) => setScanType(e.target.value)}
                    className="sr-only"
                  />
                  <div className="flex items-start space-x-3">
                    <Icon className={`h-6 w-6 mt-1 ${type.color}`} />
                    <div className="flex-1">
                      <div className="font-medium text-gray-900">{type.name}</div>
                      <div className="text-sm text-gray-500 mt-1">
                        {type.description}
                      </div>
                    </div>
                    {scanType === type.id && (
                      <div className="absolute top-2 right-2">
                        <div className="w-4 h-4 bg-primary-500 rounded-full flex items-center justify-center">
                          <div className="w-2 h-2 bg-white rounded-full"></div>
                        </div>
                      </div>
                    )}
                  </div>
                </label>
              )
            })}
          </div>
        </div>

        {/* Scan Options */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Tarama Seçenekleri</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <input type="checkbox" id="xss" defaultChecked className="rounded" />
              <label htmlFor="xss" className="text-gray-700">XSS (Cross-Site Scripting)</label>
            </div>
            <div className="flex items-center space-x-2">
              <input type="checkbox" id="sql" defaultChecked className="rounded" />
              <label htmlFor="sql" className="text-gray-700">SQL Injection</label>
            </div>
            <div className="flex items-center space-x-2">
              <input type="checkbox" id="csrf" defaultChecked className="rounded" />
              <label htmlFor="csrf" className="text-gray-700">CSRF (Cross-Site Request Forgery)</label>
            </div>
            <div className="flex items-center space-x-2">
              <input type="checkbox" id="headers" defaultChecked className="rounded" />
              <label htmlFor="headers" className="text-gray-700">Security Headers</label>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="text-center">
          <button
            type="submit"
            disabled={isLoading || !url.trim()}
            className="btn btn-primary btn-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Tarama Başlatılıyor...
              </>
            ) : (
              <>
                <Play className="h-5 w-5 mr-2" />
                Taramayı Başlat
              </>
            )}
          </button>
        </div>

        {/* Info */}
        <div className="text-center text-sm text-gray-500">
          <p>
            Tarama sonuçları güvenli bir şekilde saklanır ve sadece size aittir.
          </p>
          <p className="mt-1">
            Premium kullanıcılar için daha hızlı tarama ve detaylı raporlar mevcuttur.
          </p>
        </div>
      </form>
    </motion.div>
  )
}
