import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { settingsService, WordPressSettings } from '../lib/services/settingsService';

export default function Settings() {
  const [settings, setSettings] = useState<WordPressSettings>({
    siteUrl: '',
    username: '',
    applicationPassword: '',
    postType: 'post',
    postStatus: 'draft',
  });

  const [isTesting, setIsTesting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const data = await settingsService.getSettings();
        setSettings(data);
      } catch (error) {
        console.error('Error fetching settings:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSettings();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setSettings((prev: WordPressSettings) => ({ ...prev, [name]: value }));
  };

  const handleTestConnection = async () => {
    setIsTesting(true);
    try {
      const success = await settingsService.testConnection(settings);
      if (success) {
        toast.success('WordPress connection successful!');
      } else {
        toast.error('Failed to connect to WordPress');
      }
    } catch (error) {
      toast.error('Failed to connect to WordPress');
      console.error(error);
    } finally {
      setIsTesting(false);
    }
  };

  const handleSave = async () => {
    try {
      await settingsService.updateSettings(settings);
      toast.success('Settings saved successfully!');
    } catch (error) {
      toast.error('Error saving settings');
      console.error(error);
    }
  };

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
        <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>
        <p className="mt-1 text-sm text-gray-500">
          Configure your WordPress integration settings
        </p>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="space-y-6">
            {/* WordPress Site URL */}
            <div>
              <label htmlFor="siteUrl" className="block text-sm font-medium text-gray-700">
                WordPress Site URL
              </label>
              <div className="mt-1">
                <input
                  type="url"
                  name="siteUrl"
                  id="siteUrl"
                  value={settings.siteUrl}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="https://your-wordpress-site.com"
                />
              </div>
            </div>

            {/* Username */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                Username
              </label>
              <div className="mt-1">
                <input
                  type="text"
                  name="username"
                  id="username"
                  value={settings.username}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="your-username"
                />
              </div>
            </div>

            {/* Application Password */}
            <div>
              <label htmlFor="applicationPassword" className="block text-sm font-medium text-gray-700">
                Application Password
              </label>
              <div className="mt-1">
                <input
                  type="password"
                  name="applicationPassword"
                  id="applicationPassword"
                  value={settings.applicationPassword}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="xxxx xxxx xxxx xxxx"
                />
              </div>
              <p className="mt-2 text-sm text-gray-500">
                Generate an application password in your WordPress profile settings
              </p>
            </div>

            {/* Post Type */}
            <div>
              <label htmlFor="postType" className="block text-sm font-medium text-gray-700">
                Post Type
              </label>
              <div className="mt-1">
                <select
                  name="postType"
                  id="postType"
                  value={settings.postType}
                  onChange={handleChange}
                  className="input-field"
                >
                  <option value="post">Post</option>
                  <option value="page">Page</option>
                  <option value="custom">Custom Post Type</option>
                </select>
              </div>
            </div>

            {/* Post Status */}
            <div>
              <label htmlFor="postStatus" className="block text-sm font-medium text-gray-700">
                Default Post Status
              </label>
              <div className="mt-1">
                <select
                  name="postStatus"
                  id="postStatus"
                  value={settings.postStatus}
                  onChange={handleChange}
                  className="input-field"
                >
                  <option value="draft">Draft</option>
                  <option value="publish">Published</option>
                  <option value="private">Private</option>
                </select>
              </div>
            </div>
          </div>

          <div className="mt-6 flex space-x-3">
            <button
              onClick={handleTestConnection}
              disabled={isTesting}
              className="btn-secondary"
            >
              {isTesting ? 'Testing...' : 'Test Connection'}
            </button>
            <button
              onClick={handleSave}
              className="btn-primary"
            >
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 