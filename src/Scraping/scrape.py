import praw
import os
import pandas as pd
from dotenv import load_dotenv

def fetch_comments(post, reddit):
    
    """
    Fetches all comments from a given post.

    Parameters
    ----------
    post : praw.models.Submission
        The post to fetch comments from
    reddit : praw.Reddit
        The Reddit instance to use

    Returns
    -------
    list of dict
        A list of dictionaries containing the comment data, with the keys being "user", "replying_to", and "comment".
    """

    # Ensure the post's comments are fully loaded
    post.comments.replace_more(limit=None)

    comments_data = []
    post_author = post.author.name if post.author else "[deleted]"  # Get the post author's username

    # Iterate over all the comments
    for comment in post.comments.list():
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
            # If it's a parent comment, use the post's author as the one being replied to
            comments_data.append({
                'user': username,
                'replying_to': post_author,
                'comment': comment_body
            })

    return comments_data

def scrape(subreddit: str, limit: int = 10) -> pd.DataFrame:
    
    """
    Scrape comments from a given subreddit.

    Parameters
    ----------
    subreddit : str
        The subreddit to scrape from
    limit : int, optional
        The number of posts to scrape from (default is 10)

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the scraped comments with the columns 'user', 'replying_to', and 'comment'
    """

    # Load environment variables from .env file
    load_dotenv()

    # Create a Reddit instance
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),    
        user_agent=os.getenv("USER_AGENT")
    )

    # Fetch the top limit hot posts
    top_posts = reddit.subreddit(subreddit).hot(limit=limit)

    # DataFrame to store comments
    all_comments = pd.DataFrame(columns=['user', 'replying_to', 'comment'])

    # Iterate through each post
    for post in top_posts:
        print(f"Fetching comments for post: {post.title}\nURL: {post.url}\n")
        comments_data = fetch_comments(post, reddit)
        # Append the comments to the DataFrame
        all_comments = pd.concat([all_comments, pd.DataFrame(comments_data)], ignore_index=True)

    return all_comments