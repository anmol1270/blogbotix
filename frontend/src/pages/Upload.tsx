import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { DocumentArrowUpIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { fileService } from '../lib/services/fileService';
import { blogService } from '../lib/services/blogService';

export default function Upload() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [customPrompt, setCustomPrompt] = useState('');
  const navigate = useNavigate();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Check file type
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
      toast.error('Please upload a PDF or Word document');
      return;
    }

    setIsProcessing(true);
    try {
      // Upload and process file
      const result = await fileService.uploadFile(file, customPrompt || undefined);

      // Create blog post from processed content
      const blogPost = await blogService.createBlogPost({
        title: result.title,
        content: result.content,
        summary: result.summary,
        keywords: result.keywords,
        status: 'draft',
      });

      toast.success('File processed successfully!');
      navigate(`/preview/${blogPost.id}`);
    } catch (error) {
      toast.error('Error processing file');
      console.error(error);
    } finally {
      setIsProcessing(false);
    }
  }, [navigate, customPrompt]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Upload Content</h1>
        <p className="mt-1 text-sm text-gray-500">
          Upload your PDF or Word document to generate a blog post.
        </p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <div className="space-y-4">
          {/* Custom Prompt Input */}
          <div>
            <label htmlFor="customPrompt" className="block text-sm font-medium text-gray-700">
              Custom Processing Prompt (Optional)
            </label>
            <div className="mt-1">
              <textarea
                id="customPrompt"
                name="customPrompt"
                rows={4}
                value={customPrompt}
                onChange={(e) => setCustomPrompt(e.target.value)}
                className="input-field"
                placeholder="Enter a custom prompt for GPT-4 to process your content..."
              />
            </div>
            <p className="mt-2 text-sm text-gray-500">
              If left empty, a default prompt will be used to generate a well-structured blog post.
            </p>
          </div>

          {/* File Upload Area */}
          <div
            {...getRootProps()}
            className={`mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-lg ${
              isDragActive
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300 hover:border-primary-500'
            }`}
          >
            <div className="space-y-1 text-center">
              <input {...getInputProps()} />
              <DocumentArrowUpIcon
                className="mx-auto h-12 w-12 text-gray-400"
                aria-hidden="true"
              />
              <div className="flex text-sm text-gray-600">
                <label
                  htmlFor="file-upload"
                  className="relative cursor-pointer rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2"
                >
                  <span>Upload a file</span>
                </label>
                <p className="pl-1">or drag and drop</p>
              </div>
              <p className="text-xs text-gray-500">PDF or Word document up to 10MB</p>
            </div>
          </div>
        </div>
      </div>

      {isProcessing && (
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-gray-900">Processing your document</h3>
              <p className="text-sm text-gray-500">
                Please wait while we analyze your content and generate a blog post.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 