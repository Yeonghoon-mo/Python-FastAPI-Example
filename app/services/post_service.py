from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository import post_repository
from app.schemas.post import PostCreate, PostUpdate

def create_new_post(db: Session, post: PostCreate, user_id: str):
    return post_repository.create_post(db=db, post=post, user_id=user_id)

def get_posts_list(db: Session, skip: int = 0, limit: int = 100):
    return post_repository.get_posts(db=db, skip=skip, limit=limit)

def get_post_detail(db: Session, post_id: int):
    db_post = post_repository.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

def update_existing_post(db: Session, post_id: int, post_update: PostUpdate, user_id: str):
    db_post = get_post_detail(db, post_id)
    
    # 본인 확인 (Authorization)
    if db_post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
        
    return post_repository.update_post(db=db, db_post=db_post, post_update=post_update)

def delete_existing_post(db: Session, post_id: int, user_id: str):
    db_post = get_post_detail(db, post_id)
    
    # 본인 확인 (Authorization)
    if db_post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
        
    post_repository.delete_post(db=db, db_post=db_post)
    return {"message": "Post deleted successfully"}
