import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('omw-1.4')


def count_word_frequency(text):
    new_text = re.sub('[^a-zA-Z0-1]', ' ', text)
    new_text = new_text.lower()
    new_text = new_text.split()
    all_stopwords = stopwords.words('english')
    all_stopwords.extend(['ing', 'com', 'say'])
    lemmatizer = WordNetLemmatizer()
    new_text = [lemmatizer.lemmatize(word) for word in new_text if not word in set(all_stopwords)]

    word_frequences = {}
    for word in new_text:
        if word not in word_frequences.keys():
            word_frequences[word] = 1
        else:
            word_frequences[word] += 1
    return (word_frequences)
