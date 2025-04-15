import httpx
from urllib.parse import urljoin
import logging
from typing import Optional
from app.models.user import User
from httpx import TimeoutException, HTTPError

logger = logging.getLogger(__name__)

class WordPressService:
    @staticmethod
    async def publish_post(
        title: str,
        content: str,
        user: User,
        image_url: Optional[str] = None,
        status: str = "publish"
    ) -> int:
        """
        Publish a post to WordPress
        
        Args:
            title: The post title
            content: The post content
            user: The user whose WordPress settings to use
            image_url: Optional featured image URL
            status: Post status (draft, publish, etc.)
            
        Returns:
            The WordPress post ID
        """
        try:
            if not user.wordpress_url or not user.wordpress_username or not user.wordpress_password:
                raise Exception("WordPress settings not configured for user")
                
            # Construct the WordPress REST API URL
            wp_url = user.wordpress_url.rstrip('/')
            api_url = urljoin(wp_url, '/wp-json/wp/v2/posts')
            
            # Create basic auth header
            auth = (user.wordpress_username, user.wordpress_password)
            
            # Prepare the post data
            post_data = {
                "title": title,
                "content": content,
                "status": status
            }
            
            # Configure timeout
            timeout = httpx.Timeout(30.0, connect=10.0)
            
            # If we have an image URL, upload it first and set it as featured image
            if image_url:
                try:
                    # Download the image
                    async with httpx.AsyncClient(timeout=timeout) as client:
                        logger.info(f"Downloading image from: {image_url}")
                        image_response = await client.get(image_url)
                        if image_response.status_code != 200:
                            raise Exception(f"Failed to download image: {image_response.status_code}")
                        
                        # Upload the image to WordPress
                        media_url = urljoin(wp_url, '/wp-json/wp/v2/media')
                        files = {'file': ('image.jpg', image_response.content, 'image/jpeg')}
                        logger.info(f"Uploading image to WordPress: {media_url}")
                        media_response = await client.post(
                            media_url,
                            files=files,
                            auth=auth,
                            timeout=timeout
                        )
                        
                        if media_response.status_code == 201:
                            post_data["featured_media"] = media_response.json()["id"]
                            logger.info("Successfully uploaded featured image")
                        else:
                            logger.warning(f"Failed to upload featured image: {media_response.status_code} - {media_response.text}")
                except TimeoutException:
                    logger.error("Timeout while handling image upload")
                    raise Exception("Timeout while uploading image to WordPress")
                except HTTPError as e:
                    logger.error(f"HTTP error while handling image: {str(e)}")
                    raise Exception(f"Failed to handle image: {str(e)}")
            
            # Create the post
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    logger.info(f"Publishing post to WordPress: {api_url}")
                    response = await client.post(
                        api_url,
                        json=post_data,
                        auth=auth,
                        timeout=timeout
                    )
                    
                    if response.status_code == 201:
                        post_id = response.json()["id"]
                        logger.info(f"Successfully published post to WordPress with ID: {post_id}")
                        return post_id
                    else:
                        error_msg = f"Failed to publish post: {response.status_code} - {response.text}"
                        logger.error(error_msg)
                        raise Exception(error_msg)
            except TimeoutException:
                logger.error("Timeout while publishing post")
                raise Exception("Timeout while publishing post to WordPress")
            except HTTPError as e:
                logger.error(f"HTTP error while publishing post: {str(e)}")
                raise Exception(f"Failed to publish post: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error publishing to WordPress: {str(e)}")
            raise Exception(f"Failed to publish to WordPress: {str(e)}") 