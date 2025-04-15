# AI Blog Assistant

A modern web application that helps content creators automate their blogging workflow using AI. The application allows users to upload documents, generate blog posts using AI, and publish them directly to WordPress.

## Features

- 🔐 Google OAuth2 authentication
- 📄 PDF and Word document upload with drag & drop
- 🤖 AI-powered content summarization and blog post generation
- 🎨 AI-generated featured images
- 🔑 Keyword extraction
- 📝 WordPress integration for direct publishing
- 🎯 Modern, responsive UI with Tailwind CSS

## Tech Stack

- React + TypeScript
- Tailwind CSS for styling
- React Router for navigation
- Redux Toolkit for state management
- React Dropzone for file uploads
- React Hot Toast for notifications
- Heroicons for icons

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:5173](http://localhost:5173) in your browser.

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── hooks/         # Custom React hooks
├── store/         # Redux store configuration
├── types/         # TypeScript type definitions
├── utils/         # Utility functions
└── App.tsx        # Main application component
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
VITE_GOOGLE_CLIENT_ID=your_google_client_id
VITE_API_URL=your_backend_api_url
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
