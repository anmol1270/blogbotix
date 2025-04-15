import api from '../api';

export interface FileUploadResponse {
  title: string;
  content: string;
  summary: string;
  keywords: string[];
}

export const fileService = {
  async uploadFile(file: File, customPrompt?: string): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    if (customPrompt) {
      formData.append('custom_prompt', customPrompt);
    }

    const response = await api.post('/files/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
}; 