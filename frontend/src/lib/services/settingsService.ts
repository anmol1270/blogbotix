import api from '../api';

export interface WordPressSettings {
  siteUrl: string;
  username: string;
  applicationPassword: string;
  postType: string;
  postStatus: string;
}

export const settingsService = {
  async getSettings(): Promise<WordPressSettings> {
    console.log('Token:', localStorage.getItem('token'));
    const response = await api.get('/settings/wordpress');
    return response.data;
  },

  async updateSettings(settings: WordPressSettings): Promise<WordPressSettings> {
    console.log('Token:', localStorage.getItem('token'));
    const response = await api.put('/settings/wordpress', settings);
    return response.data;
  },

  async testConnection(settings: WordPressSettings): Promise<boolean> {
    console.log('Token:', localStorage.getItem('token'));
    const response = await api.post('/settings/wordpress/test', settings);
    return response.data.success;
  },
}; 