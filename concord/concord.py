# concord.py

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.datasets import fetch_20newsgroups

from bert.bert import initialize_model


def preprocess_documents(documents):
    """
    Preprocess the documents by:
    - Lowercasing
    - Removing punctuation
    - Removing stop words
    - Lemmatizing
    """
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    processed_docs = []

    for doc in documents:
        # Lowercase
        doc = doc.lower()
        # Tokenize
        tokens = nltk.word_tokenize(doc)
        # Remove punctuation and non-alphabetic tokens
        tokens = [word for word in tokens if word.isalpha()]
        # Remove stop words and short words
        tokens = [
            word for word in tokens if word not in stop_words and len(word) > 2
        ]
        # Lemmatize
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        # Rejoin tokens to form the cleaned document
        processed_doc = ' '.join(tokens)
        processed_docs.append(processed_doc)

    return processed_docs


def main():
    # Load the dataset and limit to 100 documents
    print("Loading data...")
    newsgroups = fetch_20newsgroups(subset='all',
                                    remove=('headers', 'footers', 'quotes'))
    documents = newsgroups['data'][:100]  # Limit to first 100 documents
    print(f"Loaded {len(documents)} documents.")

    # Preprocess the documents
    print("Preprocessing documents...")
    documents = preprocess_documents(documents)

    # Initialize the BERTopic model with custom parameters
    print("Initializing BERTopic model...")
    topic_model = initialize_model()

    # Fit the model on the documents
    print("Fitting the BERTopic model...")
    topics, probs = topic_model.fit_transform(documents)

    # Get topic information
    topic_info = topic_model.get_topic_info()

    # Print the main topics
    print("\nMain Topics:")
    for index, row in topic_info.iterrows():
        topic_id = row['Topic']
        if topic_id == -1:
            continue  # Skip outliers
        topic_freq = row['Count']
        topic_words = topic_model.get_topic(topic_id)
        words = ', '.join([word for word, _ in topic_words])
        print(f"Topic {topic_id} (Frequency: {topic_freq}): {words}")

    print("\nTopic modeling completed.")


if __name__ == "__main__":
    main()
