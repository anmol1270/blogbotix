import api from '../api';

export interface ImageGenerationResponse {
  imageUrl: string;
}

export interface ImageGenerationRequest {
  content: string;
  title: string;
}

export const imageService = {
  async generateImage(request: ImageGenerationRequest): Promise<string> {
    const response = await api.post<ImageGenerationResponse>('/images/generate/', request);
    return response.data.imageUrl;
  },
}; 