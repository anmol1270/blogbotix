import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  DocumentTextIcon,
  ClockIcon,
  ChartBarIcon,
  SparklesIcon,
  CalendarIcon,
  ArrowRightIcon,
} from '@heroicons/react/24/outline';
import { blogService, BlogPost } from '../lib/services/blogService';
import toast from 'react-hot-toast';

export default function Dashboard() {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const data = await blogService.getBlogPosts();
        // Sort posts by creation date, most recent first
        const sortedPosts = data.sort((a, b) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        setPosts(sortedPosts);
      } catch (error) {
        console.error('Error fetching posts:', error);
        toast.error('Failed to load posts');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPosts();
  }, []);

  const stats = [
    { name: 'Total Posts', value: posts.length.toString(), icon: DocumentTextIcon },
    { name: 'Draft Posts', value: posts.filter(post => post.status === 'draft').length.toString(), icon: ClockIcon },
    { name: 'Published Posts', value: posts.filter(post => post.status === 'published').length.toString(), icon: ChartBarIcon },
    { name: 'AI Generated', value: posts.length.toString(), icon: SparklesIcon },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Welcome back! Here's an overview of your blog content.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="relative overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:px-6 sm:py-6"
          >
            <dt>
              <div className="absolute rounded-md bg-primary-500 p-3">
                <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">
                {stat.name}
              </p>
            </dt>
            <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
              <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
            </dd>
          </div>
        ))}
      </div>

      {/* Recent Posts */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">Recent Posts</h2>
          <Link
            to="/blog"
            className="inline-flex items-center text-sm text-primary-600 hover:text-primary-500"
          >
            View All Posts
            <ArrowRightIcon className="ml-1 h-4 w-4" />
          </Link>
        </div>
        <div className="border-t border-gray-200">
          <ul role="list" className="divide-y divide-gray-200">
            {posts.slice(0, 5).map((post) => (
              <li key={post.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center">
                      <Link
                        to={`/preview/${post.id}`}
                        className="text-sm font-medium text-primary-600 hover:text-primary-500 truncate"
                      >
                        {post.title}
                      </Link>
                    </div>
                    <div className="mt-1 flex items-center text-sm text-gray-500">
                      <CalendarIcon className="flex-shrink-0 mr-1.5 h-4 w-4" />
                      <span>
                        {new Date(post.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </span>
                    </div>
                    {post.summary && (
                      <p className="mt-1 text-sm text-gray-500 line-clamp-2">
                        {post.summary}
                      </p>
                    )}
                  </div>
                  <div className="ml-4 flex-shrink-0">
                    <p
                      className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                        post.status === 'published'
                          ? 'bg-green-100 text-green-800'
                          : post.status === 'draft'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {post.status}
                    </p>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
} 