from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str
    email: str


class UserLogin(BaseModel):
    username: str
    password: str


class Interest(BaseModel):
    category: str


class FavoriteArticle(BaseModel):
    title: str
    url: str
    image: str | None = None
    source: str | None = None
    category: str | None = None


class CommentCreate(BaseModel):
    article_url: str
    comment_text: str