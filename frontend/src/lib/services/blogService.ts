import api from '../api';

export interface BlogPost {
  id: number;
  title: string;
  content: string;
  summary: string;
  keywords: string[];
  image_url?: string;
  status: 'draft' | 'published' | 'private';
  created_at: string;
  updated_at: string;
}

export interface BlogPostCreate {
  title: string;
  content: string;
  summary: string;
  keywords: string[];
  image_url?: string;
  status?: 'draft' | 'published' | 'private';
}

export interface BlogPostUpdate {
  title?: string;
  content?: string;
  summary?: string;
  keywords?: string[];
  image_url?: string;
  status?: 'draft' | 'published' | 'private';
}

export const blogService = {
  async getBlogPosts(): Promise<BlogPost[]> {
    const response = await api.get('/blog/');
    return response.data;
  },

  async getBlogPost(id: number): Promise<BlogPost> {
    const response = await api.get(`/blog/${id}`);
    return response.data;
  },

  async createBlogPost(post: BlogPostCreate): Promise<BlogPost> {
    const response = await api.post('/blog/', post);
    return response.data;
  },

  async updateBlogPost(id: number, post: BlogPostUpdate): Promise<BlogPost> {
    const response = await api.put(`/blog/${id}`, post);
    return response.data;
  },

  async deleteBlogPost(id: number): Promise<void> {
    await api.delete(`/blog/${id}`);
  },

  async publishBlogPost(id: number): Promise<BlogPost> {
    const response = await api.post(`/blog/${id}/publish`);
    return response.data;
  },
}; 