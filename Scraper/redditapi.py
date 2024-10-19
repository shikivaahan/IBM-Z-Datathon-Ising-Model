import praw
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

def fetch_comments(submission):
    # Ensure the submission's comments are fully loaded
    submission.comments.replace_more(limit=None)
    
    comments_data = []
    # Iterate over all the comments
    for comment in submission.comments.list():
        username = comment.author.name if comment.author else "[deleted]"
        comment_body = comment.body
        
        # Check if the comment is a reply
        if comment.parent_id.startswith("t1_"):  # t1_ indicates a comment
            parent_comment = reddit.comment(id=comment.parent_id[3:])  # Remove the 't1_' prefix
            parent_username = parent_comment.author.name if parent_comment.author else "[deleted]"
            comments_data.append({
                'user': username,
                'replying_to': parent_username,
                'comment': comment_body
            })
        else:
            # If it's a parent comment
            comments_data.append({
                'user': username,
                'replying_to': "N/A (Parent Comment)",
                'comment': comment_body
            })
    
    return comments_data

def fetch_subreddit_comments(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)

    # Fetch the top 10 hot posts
    top_posts = subreddit.hot(limit=10)

    # DataFrame to store comments
    all_comments = pd.DataFrame(columns=['user', 'replying_to', 'comment'])

    # Iterate through each post
    for post in top_posts:
        print(f"Fetching comments for post: {post.title}\nURL: {post.url}\n")
        comments_data = fetch_comments(post)
        # Append the comments to the DataFrame
        all_comments = pd.concat([all_comments, pd.DataFrame(comments_data)], ignore_index=True)

    return all_comments

def main():
    subreddit_name = input("Enter the subreddit name: ")
    comments_df = fetch_subreddit_comments(subreddit_name)

    # You can choose to print or return the DataFrame here
    print(comments_df)
    return comments_df

if __name__ == "__main__":
    main()
