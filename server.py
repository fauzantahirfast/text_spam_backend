from flask import Flask, request, jsonify
import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
nltk.download("punkt", quiet=True)  # Ensure "punkt" tokenizer is downloaded
ps = PorterStemmer()
def preprocess_text(text):
    text = text.lower()
    text = word_tokenize(text)
    y = []
    for words in text:
        if words.isalnum():
            y.append(words)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(ps.stem(i))

    return " ".join(y)


def spam_classifier(incoming_data):
    tfidf = pickle.load(open('vectorizer (1).pkl', 'rb'))
    model = pickle.load(open('model (1).pkl', 'rb'))

    transformed_sms = preprocess_text(incoming_data)
    vector_input = tfidf.transform([transformed_sms])
    result = model.predict(vector_input)[0]

    if result == 1:
        return "Spam"
    else:
        return "Not Spam"


@app.route('/api/data', methods=["POST", "GET"])
def recieve_data():
    data = request.get_json()  # Get JSON data from the request body
    print("Received data:", data)
    result = spam_classifier(data)
    return jsonify({
        "message": "Data classified successfully!",
        "originalData": data,
        "Classified data": result
    })

if __name__ == "main":
    app.run(debug=True)