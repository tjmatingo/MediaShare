from fastapi import FastAPI, HTTPException


app = FastAPI()

text_posts = {
    1:{"title": "first Post", "content": "This is my first post ever using UV instead of pip"},
}

# creating endpoint
@app.get("/posts")
def get_all_posts():
    return text_posts


@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return text_posts.get(id)