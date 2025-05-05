import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification

# Load tokenizer and model once
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertForSequenceClassification.from_pretrained(
    '/Users/anilthapa/Real-Time-Financial-Sentiment-Analysis/sentiment-analysis-model'
)

# Sentiment label mapping
label_map = {
    0: "Negative",
    1: "Neutral",
    2: "Positive"
}

def predict_sentiment(text):
    # Tokenize input
    inputs = tokenizer(text, return_tensors='tf', padding=True, truncation=True)

    # Run inference
    outputs = model(inputs)
    logits = outputs.logits

    # Get predicted class
    predicted_class_idx = tf.argmax(logits, axis=1).numpy()[0]
    predicted_label = label_map[predicted_class_idx]

    return predicted_label
