import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { PhotoIcon, DocumentArrowUpIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import { blogService, BlogPost } from '../lib/services/blogService';
import { imageService } from '../lib/services/imageService';

export default function BlogPreview() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState<BlogPost | null>(null);
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
  const [isPublishing, setIsPublishing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPost = async () => {
      if (!id) {
        setError('No blog post selected');
        setIsLoading(false);
        return;
      }

      try {
        const data = await blogService.getBlogPost(parseInt(id));
        setPost(data);
      } catch (error) {
        console.error(error);
        setError('Blog post not found');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPost();
  }, [id]);

  const handleGenerateImage = async () => {
    if (!post) return;
    
    setIsGeneratingImage(true);
    try {
      const imageUrl = await imageService.generateImage({
        content: post.content,
        title: post.title
      });
      
      // Update the post with the new image URL
      const updatedPost = await blogService.updateBlogPost(post.id, {
        ...post,
        image_url: imageUrl
      });
      
      setPost(updatedPost);
      toast.success('Image generated successfully!');
    } catch (error) {
      toast.error('Failed to generate image');
      console.error(error);
    } finally {
      setIsGeneratingImage(false);
    }
  };

  const handlePublish = async () => {
    if (!post) return;

    setIsPublishing(true);
    try {
      const publishedPost = await blogService.publishBlogPost(post.id);
      setPost(publishedPost);
      toast.success('Post published successfully!');
      navigate('/');
    } catch (error) {
      toast.error('Error publishing post');
      console.error(error);
    } finally {
      setIsPublishing(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!id) {
    return (
      <div className="flex flex-col items-center justify-center h-64 space-y-4">
        <DocumentArrowUpIcon className="w-12 h-12 text-gray-400" />
        <h2 className="text-xl font-semibold text-gray-900">No Blog Post Selected</h2>
        <p className="text-gray-500">Upload a document to generate a blog post</p>
        <Link to="/upload" className="btn-primary">
          Upload Document
        </Link>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-64 space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Error</h2>
        <p className="text-gray-500">{error}</p>
        <Link to="/" className="btn-primary">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="flex flex-col items-center justify-center h-64 space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Blog Post Not Found</h2>
        <p className="text-gray-500">The requested blog post could not be found</p>
        <Link to="/" className="btn-primary">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold text-gray-900">{post.title}</h1>
        <div className="flex space-x-4">
          <button
            onClick={handleGenerateImage}
            disabled={isGeneratingImage}
            className="btn-secondary flex items-center"
          >
            <PhotoIcon className="w-5 h-5 mr-2" />
            {isGeneratingImage ? 'Generating...' : 'Generate Image'}
          </button>
          <button 
            onClick={handlePublish} 
            disabled={isPublishing}
            className="btn-primary"
          >
            {isPublishing ? 'Publishing...' : 'Publish'}
          </button>
        </div>
      </div>

      {/* Featured Image Section */}
      {post.image_url && (
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <img
            src={post.image_url}
            alt={post.title}
            className="w-full h-auto"
          />
        </div>
      )}

      <div className="prose max-w-none">
        <div dangerouslySetInnerHTML={{ __html: post.content }} />
      </div>
    </div>
  );
} 