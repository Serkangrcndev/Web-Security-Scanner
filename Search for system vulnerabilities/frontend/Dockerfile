# GuardMesh Frontend - Basit Dockerfile
FROM node:18-alpine

# Çalışma dizini oluştur
WORKDIR /app

# Package dosyalarını kopyala
COPY package*.json ./

# Bağımlılıkları yükle
RUN npm install

# Tüm dosyaları kopyala
COPY . .

# Build yap
RUN npm run build

# Port aç
EXPOSE 3000

# Uygulamayı başlat
CMD ["npm", "start"]
