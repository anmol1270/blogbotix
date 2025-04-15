from typing import Dict, Optional
import openai
from app.core.config import settings
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure OpenAI
logger.debug(f"OpenAI API Key length: {len(settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else 0}")
openai.api_key = settings.OPENAI_API_KEY

DEFAULT_PROMPT = """Please analyze the following legal judgment and create a well-structured blog post. The blog post should:
1. Have a clear and engaging introduction that highlights the key legal issue and outcome
2. Be well-organized with proper headings and sections
3. Include relevant legal precedents and citations
4. Explain the legal reasoning and implications
5. Have a strong conclusion summarizing the key takeaways
6. Be optimized for readability while maintaining legal accuracy

Content to analyze:
{content}

Please format the response as a blog post with proper HTML formatting. Follow these formatting guidelines:

1. Images:
   - Center align all images using <div style="text-align: center;">
   - Add proper spacing before and after images
   - Include descriptive alt text for accessibility

2. Text Formatting:
   - Use proper heading hierarchy (h1, h2, h3)
   - Add appropriate spacing between sections
   - Use bullet points or numbered lists where appropriate
   - Highlight important quotes or citations in blockquotes
   - Use bold or italic text sparingly for emphasis
   - Keep paragraphs concise and well-spaced

3. Structure:
   - Start with a clear introduction
   - Break content into logical sections
   - Use subheadings to guide readers
   - End with a strong conclusion

Example formatting:
<div style="text-align: center;">
  <img src="image.jpg" alt="Description of the image" style="max-width: 100%; height: auto;">
</div>

<h2>Section Title</h2>
<p>Well-formatted paragraph with proper spacing...</p>

<blockquote>
  Important quote or citation...
</blockquote>

The title should be a concise representation of the key legal issue and outcome, following this format:
"[Case Name/Parties] v. [Case Name/Parties]: [Key Legal Issue] - [Outcome]"

For example:
"State of California v. Smith: Supreme Court Rules on Fourth Amendment Rights in Digital Age"
"Johnson v. Department of Education: Federal Court Upholds Title IX Protections for Transgender Students"

Please ensure the title accurately represents the judgment while being engaging and informative."""

class AIService:
    MODEL_NAME = "gpt-4o-mini"  # Using GPT-4O Mini model for all content generation
    
    @staticmethod
    async def process_content(content: str, custom_prompt: Optional[str] = None) -> Dict[str, str]:
        """
        Process content using GPT-4O Mini to generate a blog post.
        
        Args:
            content: The content to process
            custom_prompt: Optional custom prompt to use instead of the default
            
        Returns:
            Dict containing the processed content and metadata
        """
        try:
            # Use custom prompt if provided, otherwise use default
            prompt = custom_prompt if custom_prompt else DEFAULT_PROMPT
            prompt = prompt.format(content=content)
            
            logger.debug("Making OpenAI API call for content generation")
            # Call GPT-4O Mini
            response = openai.chat.completions.create(
                model=AIService.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a professional blog writer who creates engaging, well-structured content with proper HTML formatting. Focus on readability and visual appeal."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            logger.debug("Successfully generated content")
            # Extract the generated content
            generated_content = response.choices[0].message.content
            
            logger.debug("Making OpenAI API call for title generation")
            # Generate a title from the content
            title_response = openai.chat.completions.create(
                model=AIService.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a legal content writer who creates clear and informative titles for legal judgments. Follow this format: '[Case Name/Parties] v. [Case Name/Parties]: [Key Legal Issue] - [Outcome]'. Make the title concise but informative, highlighting the key legal issue and outcome."},
                    {"role": "user", "content": f"Create a compelling title for this legal judgment (max 100 characters):\n\n{generated_content}"}
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            logger.debug("Successfully generated title")
            title = title_response.choices[0].message.content.strip()
            
            logger.debug("Making OpenAI API call for keywords generation")
            # Generate keywords
            keywords_response = openai.chat.completions.create(
                model=AIService.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a professional content strategist who identifies relevant keywords."},
                    {"role": "user", "content": f"Extract 5-7 relevant keywords from this blog post:\n\n{generated_content}"}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            logger.debug("Successfully generated keywords")
            keywords = [k.strip() for k in keywords_response.choices[0].message.content.split(',')]
            
            # Generate a proper summary using GPT-4O Mini
            logger.debug("Making OpenAI API call for summary generation")
            summary_response = openai.chat.completions.create(
                model=AIService.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a professional content summarizer. Create a concise summary that captures the key points of the legal judgment."},
                    {"role": "user", "content": f"Create a brief summary (max 200 characters) of this blog post:\n\n{generated_content}"}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            logger.debug("Successfully generated summary")
            summary = summary_response.choices[0].message.content.strip()
            
            return {
                "title": title,
                "content": generated_content,
                "keywords": keywords,
                "summary": summary
            }
            
        except Exception as e:
            logger.error(f"Error processing content with GPT-4O Mini: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise Exception(f"Error processing content with GPT-4O Mini: {str(e)}")
