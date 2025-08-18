export default function SimplePage() {
  return (
    <div className="min-h-screen bg-blue-100 p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-blue-900 mb-6">
          Basit CSS Test
        </h1>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Tailwind CSS Test
          </h2>
          <div className="space-y-3">
            <div className="bg-blue-500 text-white p-3 rounded">
              Mavi Kutu
            </div>
            <div className="bg-green-500 text-white p-3 rounded">
              Yeşil Kutu
            </div>
            <div className="bg-red-500 text-white p-3 rounded">
              Kırmızı Kutu
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Custom CSS Test
          </h2>
          <div className="space-y-3">
            <button className="btn-primary">
              Primary Button
            </button>
            <button className="btn-secondary">
              Secondary Button
            </button>
            <div className="card p-3">
              Card Component
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
