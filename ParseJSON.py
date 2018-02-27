import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

UNHELPFUL_LIMIT = 5
LOWEST_REVIEW_SCORE = 3

review_list = []
positive_review_text_list = []
negative_review_text_list = []

review_list_dict = dict()


with open('review_video.json') as f:
    for line in f:
       review_list.append(json.loads(line))

for json_obj in review_list:
    asin = json_obj.get('asin')
    if asin not in review_list_dict:
        review_list_dict[asin] = dict()

    if 'negative_text' not in review_list_dict.get(asin):
        review_list_dict.get(asin)['negative_text'] = []

    if 'positive_text' not in review_list_dict.get(asin):
        review_list_dict.get(asin)['positive_text'] = []

    overall_score = json_obj.get('overall')
    if overall_score > 2:
        review_list_dict.get(asin).get('positive_text').append(json_obj.get('reviewText'))
    else:
        review_list_dict.get(asin).get('negative_text').append(json_obj.get('reviewText'))

print(len(review_list_dict.get('B000H00VBQ').get('positive_text')))


# I choose asin as the dictionary key. asin key represents the product number in the amazon
# dict { 'asin': {'positive_text': [], 'negative_text': []}}

# Clean reviews

def cleanReview(text):


    # punctuation
    review = re.sub('[^a-zA-Z]', ' ', text)

    # lowercase
    review = review.lower()

    review = review.split()
    # stop words
    review = [word for word in review if not word in set(stopwords.words('english'))]

    # stemming
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = " ".join(review)
    #print(review)

    cleaned_text = review

    return cleaned_text


cleaned_reviews = []
flag = 0

for json_obj in review_list[:500]:

    cleaned_text = cleanReview(json_obj.get("reviewText"))
    #asin = json_obj.get('asin')
    overall = json_obj.get("overall")
    pos_or_neg = 0
    # if review overall is greater than 3 review = POSITIVE
    if overall > LOWEST_REVIEW_SCORE:
        pos_or_neg = 1

    # if review wasn't helpful to more than 5 people = THROW AWAy
    if json_obj.get("helpful")[1] > UNHELPFUL_LIMIT:
        flag = 1

    rated_review_t = (cleaned_text, pos_or_neg)

    # check if review should be thrown away
    if flag == 0:
        cleaned_reviews.append(rated_review_t)

    flag = 0

print("size of sample = " + str(len(cleaned_reviews)))

