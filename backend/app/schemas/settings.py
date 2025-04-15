from pydantic import BaseModel, HttpUrl
from typing import Optional

class WordPressSettingsBase(BaseModel):
    siteUrl: Optional[HttpUrl] = None
    username: str
    applicationPassword: str
    postType: str = "post"
    postStatus: str = "draft"

class WordPressSettings(WordPressSettingsBase):
    pass

class WordPressSettingsUpdate(WordPressSettingsBase):
    pass 