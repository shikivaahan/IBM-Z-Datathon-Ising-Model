import praw
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

# Fetch a specific submission by its URL
submission_url = "https://www.reddit.com/r/soccer/comments/1g75iu2/erik_ten_hag_we_have_won_trophies_remember_6/"
submission = reddit.submission(url=submission_url)

# Ensure the submission's comments are fully loaded
submission.comments.replace_more(limit=None)

# Iterate over all the comments
for comment in submission.comments.list():
    username = comment.author.name if comment.author else "[deleted]"
    comment_body = comment.body
    print(f"User: {username}\nComment: {comment_body}\n")
