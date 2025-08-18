# Premium Web Security Scanner

Professional-grade web security scanning and vulnerability assessment platform with modern React frontend and FastAPI backend.

## 🚀 Features

### Core Functionality
- **Advanced Security Scanning**: Comprehensive vulnerability assessment using industry-leading tools
- **Real-time Monitoring**: Live scanning progress and instant vulnerability detection
- **Multiple Scanner Support**: Nmap, Nikto, Nuclei, SQLMap, XSS Scanner, ZAP, and Shodan integration
- **Detailed Analytics**: In-depth reports with CVSS scoring and remediation guidance

### Premium Features
- **Enhanced Reporting**: PDF, Excel, and JSON report generation
- **Advanced Analytics**: Interactive charts and vulnerability distribution analysis
- **Priority Scanning**: Faster scan processing for premium users
- **Enterprise Security**: Bank-level security for sensitive data

## 🏗️ Architecture

### Frontend (React + Next.js)
- **Modern UI**: Built with React 18, Next.js 14, and TypeScript
- **Beautiful Design**: TailwindCSS with Framer Motion animations
- **Responsive Layout**: Mobile-first design with dark/light mode support
- **Interactive Charts**: Recharts integration for data visualization
- **State Management**: Zustand for efficient state management

### Backend (FastAPI)
- **RESTful API**: Clean, documented API endpoints
- **Async Processing**: Celery integration for background task processing
- **Database**: SQLAlchemy with PostgreSQL support
- **Authentication**: JWT-based authentication system
- **Scanner Integration**: Multiple security scanner engines

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18 + Next.js 14
- **Styling**: TailwindCSS + Framer Motion
- **Charts**: Recharts
- **State**: Zustand
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Forms**: React Hook Form
- **Notifications**: React Hot Toast

### Backend
- **Framework**: FastAPI
- **Database**: SQLAlchemy + PostgreSQL
- **Task Queue**: Celery + Redis
- **Authentication**: JWT
- **Documentation**: OpenAPI/Swagger

### Security Scanners
- **Network**: Nmap
- **Web**: Nikto, Nuclei, ZAP
- **Database**: SQLMap
- **XSS**: Custom XSS Scanner
- **OSINT**: Shodan

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Docker and Docker Compose
- PostgreSQL
- Redis

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Docker Deployment
```bash
docker-compose up -d
```

## 📱 Screenshots

### Dashboard
- Modern, responsive dashboard with real-time scanning
- Interactive charts showing vulnerability distribution
- Tab-based navigation for different sections

### Scanning Interface
- Clean URL input with validation
- Real-time progress tracking
- Comprehensive vulnerability listing

### Reports
- Multiple export formats (PDF, Excel, JSON)
- Detailed vulnerability analysis
- Professional reporting templates

## 🔧 Configuration

### Environment Variables
```bash
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
```

### Scanner Configuration
Each scanner can be configured independently through the backend configuration files.

## 📊 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout

### Scanning
- `POST /scan/start` - Start new scan
- `GET /scan/status/{id}` - Get scan status
- `GET /scan/result/{id}` - Get scan results
- `POST /scan/stop/{id}` - Stop running scan

### Reports
- `GET /reports/pdf/{id}` - Generate PDF report
- `GET /reports/excel/{id}` - Generate Excel report
- `GET /reports/json/{id}` - Generate JSON report

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Basic scanning functionality
- ✅ Modern React frontend
- ✅ Multiple scanner integration
- ✅ Real-time progress tracking

### Phase 2 (Next)
- 🔄 Advanced reporting system
- 🔄 User management dashboard
- 🔄 API rate limiting
- 🔄 Webhook integrations

### Phase 3 (Future)
- 📋 Enterprise features
- 📋 Team collaboration
- 📋 Advanced analytics
- 📋 Mobile application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Contact the development team

## 🔒 Security

This is a security tool - please use responsibly and only on systems you own or have permission to test.
