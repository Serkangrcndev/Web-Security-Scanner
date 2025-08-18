export default function TestPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-blue-900 mb-8">
          CSS Test Sayfası
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Tailwind CSS Test */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Tailwind CSS Test
            </h2>
            <div className="space-y-4">
              <div className="bg-blue-500 text-white p-4 rounded-lg">
                Mavi Kutu - Tailwind çalışıyor
              </div>
              <div className="bg-green-500 text-white p-4 rounded-lg">
                Yeşil Kutu - Tailwind çalışıyor
              </div>
              <div className="bg-red-500 text-white p-4 rounded-lg">
                Kırmızı Kutu - Tailwind çalışıyor
              </div>
            </div>
          </div>

          {/* Custom CSS Test */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Custom CSS Test
            </h2>
            <div className="space-y-4">
              <button className="btn-primary">
                Primary Button
              </button>
              <button className="btn-secondary">
                Secondary Button
              </button>
              <div className="card p-4">
                Card Component
              </div>
              <input 
                type="text" 
                placeholder="Input Field" 
                className="input-field"
              />
            </div>
          </div>

          {/* Utility Classes Test */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Utility Classes Test
            </h2>
            <div className="space-y-4">
              <h3 className="text-gradient text-2xl font-bold">
                Gradient Text
              </h3>
              <div className="glass p-4 rounded-lg">
                Glass Effect
              </div>
              <div className="bg-gray-100 p-4 rounded-lg">
                <span className="text-red-600">Red Text</span>
                <span className="text-blue-600 ml-2">Blue Text</span>
                <span className="text-green-600 ml-2">Green Text</span>
              </div>
            </div>
          </div>

          {/* Responsive Test */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Responsive Test
            </h2>
            <div className="space-y-4">
              <div className="bg-yellow-100 p-4 rounded-lg">
                <p className="text-sm md:text-base lg:text-lg">
                  Bu metin responsive olarak boyut değiştiriyor
                </p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                <div className="bg-purple-200 p-2 rounded text-center">1</div>
                <div className="bg-purple-300 p-2 rounded text-center">2</div>
                <div className="bg-purple-400 p-2 rounded text-center">3</div>
              </div>
            </div>
          </div>
        </div>

        {/* Status */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            CSS Durumu
          </h2>
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>Tailwind CSS: Aktif</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>Custom CSS: Aktif</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>Responsive Design: Aktif</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
