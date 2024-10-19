from transformers import pipeline

def classify_comment(comment):
    # Use the model to predict sentiment
    result = pipe(comment)
    # Extract the label from the model output
    label = result[0]['label']
    # Assign 1 for positive, -1 for negative
    if label == 'POSITIVE':
        return 1
    else:
        return -1