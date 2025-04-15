import openai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ImageGenerator:
    @staticmethod
    async def generate_image_prompt(content: str, title: str) -> str:
        """
        Generate an image prompt using GPT-4O Mini
        
        Args:
            content: The blog post content
            title: The blog post title
            
        Returns:
            A detailed prompt for DALL-E
        """
        try:
            logger.debug("Generating image prompt with GPT-4O Mini")
            
            # Create a prompt for GPT-4O Mini to analyze the content and generate an image prompt
            system_prompt = """You are an expert at creating detailed image prompts for legal blog posts. 
            Analyze the content and create a prompt that will generate a professional, relevant image.
            The prompt should:
            1. Be specific and detailed
            2. Focus on legal/professional themes which are related to the indian judicial system.
            3. Avoid any controversial or inappropriate content
            4. Make sure the image is not too dark or too light and make sure the image does not contain any people or text.
            5. Be suitable for a professional blog
            6. Be in English
            7. Be between 100-200 characters
            
            Format the response as just the prompt text, nothing else."""
            
            # Call GPT-4O Mini to generate the image prompt
            client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-4O Mini model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Title: {title}\n\nContent: {content}"}
                ],
                temperature=0.5,
                max_tokens=200
            )
            
            prompt = response.choices[0].message.content.strip()
            logger.debug(f"Generated image prompt: {prompt}")
            
            return prompt
            
        except Exception as e:
            logger.error(f"Error generating image prompt: {str(e)}")
            raise Exception(f"Failed to generate image prompt: {str(e)}")

    @staticmethod
    async def generate_image(content: str, title: str) -> str:
        """
        Generate an image using DALL-E 3 with a GPT-4O Mini generated prompt
        
        Args:
            content: The blog post content
            title: The blog post title
            
        Returns:
            The URL of the generated image
        """
        try:
            # First, generate a prompt using GPT-4O Mini
            prompt = await ImageGenerator.generate_image_prompt(content, title)
            
            logger.debug(f"Generating image with DALL-E 3 using prompt: {prompt}+Make sure the spelling of any word in the image is correct")
            
            # Call DALL-E 3
            client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="hd",
                n=1,
                style="natural"
            )
            
            # Get the image URL
            image_url = response.data[0].url
            logger.debug(f"Generated image URL: {image_url}")
            
            return image_url
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise Exception(f"Failed to generate image: {str(e)}") 