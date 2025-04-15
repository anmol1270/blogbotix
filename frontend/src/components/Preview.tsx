import { useState } from 'react';
import { PhotoIcon, ArrowPathIcon } from '@heroicons/react/24/outline';
import { PhotoIcon as PhotoIconSolid } from '@heroicons/react/24/solid';
import toast from 'react-hot-toast';
import { imageService } from '../lib/services/imageService';

interface PreviewProps {
  title: string;
  content: string;
  summary: string;
  keywords: string[];
}

export default function Preview({ title, content, summary, keywords }: PreviewProps) {
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);

  const handleGenerateImage = async () => {
    setIsGeneratingImage(true);
    try {
      const imageUrl = await imageService.generateImage({ content, title });
      setGeneratedImage(imageUrl);
      toast.success('Image generated successfully!');
    } catch (error) {
      toast.error('Failed to generate image');
      console.error(error);
    } finally {
      setIsGeneratingImage(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Title Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{title}</h1>
        <div className="flex flex-wrap gap-2">
          {keywords.map((keyword, index) => (
            <span
              key={index}
              className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800"
            >
              {keyword}
            </span>
          ))}
        </div>
      </div>

      {/* Image Generation Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Featured Image</h2>
          <button
            onClick={handleGenerateImage}
            disabled={isGeneratingImage}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isGeneratingImage ? (
              <>
                <ArrowPathIcon className="animate-spin -ml-1 mr-2 h-5 w-5" />
                Generating...
              </>
            ) : (
              <>
                <PhotoIcon className="-ml-1 mr-2 h-5 w-5" />
                Generate Image
              </>
            )}
          </button>
        </div>
        <div className="aspect-w-16 aspect-h-9 bg-gray-100 rounded-lg overflow-hidden">
          {generatedImage ? (
            <img
              src={generatedImage}
              alt={title}
              className="object-cover w-full h-full"
            />
          ) : (
            <div className="flex items-center justify-center h-full">
              <PhotoIconSolid className="h-12 w-12 text-gray-400" />
            </div>
          )}
        </div>
      </div>

      {/* Summary Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Summary</h2>
        <div className="prose prose-primary max-w-none">
          <p className="text-gray-700 leading-relaxed">{summary}</p>
        </div>
      </div>

      {/* Content Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Content</h2>
        <div 
          className="prose prose-primary max-w-none"
          dangerouslySetInnerHTML={{ __html: content }}
        />
      </div>
    </div>
  );
} 