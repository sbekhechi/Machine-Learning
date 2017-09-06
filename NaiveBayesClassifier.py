# Andrew Altmaeir & Samir Bekhechi
# CSCI 300 Project 1 (2/25/2017)
# Naive Bayes Classification of Amazon Banana Slicer Reviews

from __future__ import division

def main():
    # read_bag_from_file()
    bag_of_words = read_bag_from_file()
    overall_positive = 0
    overall_negative = 0
    bag_of_words, overall_positive, overall_negative = assign_probabilities_from_reviews(bag_of_words, overall_positive, overall_negative)
    test_unlabeled_reviews(bag_of_words, overall_positive, overall_negative)

def read_bag_from_file():
    with open("bagofwords.txt") as f:
        bagwords = f.readlines()
        bagwords = [x.strip() for x in bagwords]
        dictwords = {}
        for i in bagwords:
            dictwords[i] = [0,0]
        return dictwords


def assign_probabilities_from_reviews(bag_of_words, overall_positive, overall_negative):
    # Read in the first 50% of reviews, assign probabilities to each of our words based on those reviews
    with open("reviews.txt") as read_file:
        training_reviews = read_file.readlines()                # Read the first 50% of reviews, line by line, into a list
    training_reviews = [x.strip() for x in training_reviews]    # Remove newline characters from all reviews
    training_reviews = list(filter(None, training_reviews))     # Remove empty strings from the review list

    for review in training_reviews:
        review_positive = False                                 # Boolean for whether a review is positive (True) or negative (False)
        review = review.lower()                                 # Make review lower-case, for ease of word handling
        if ('(5star)' in review) or ('(4star)' in review):
            review_positive = True                              # Check if review is positive
            overall_positive += 1
        else:
            overall_negative += 1

        bad_chars = [',', '.', '!', '?']                        # List of characters to be removed, to help with formatting
        for c in bad_chars:
            review = review.replace(c, "")
        review_text = review.split(" ")                         # Split words by spaces

        ignore_list = []                                        # List of words to be ignored, so they aren't counted multiple times
        for word in review_text:                                # Examine each individual word in the review
            if word in bag_of_words:                            # Check whether word is in our bag; if not, move on
                if word not in ignore_list:
                    if review_positive:                         # Check whether review is positive or not
                        bag_of_words[word][0] += 1              # If so, increment positive word counter
                        ignore_list.append(word)                # Add word to list of words to ignore
                    else:
                        bag_of_words[word][1] += 1              # If not, increment negative word counter
                        ignore_list.append(word)                # Add word to list of words to ignore
    return bag_of_words, overall_positive, overall_negative

def test_unlabeled_reviews(bag_of_words, overall_positive, overall_negative):
    new_positive = 0
    new_negative = 0
    with open("reviewsTest.txt") as read_file:
        testing_reviews = read_file.readlines()
    testing_reviews = [x.strip() for x in testing_reviews]
    testing_reviews = list(filter(None, testing_reviews))

    for review in testing_reviews:
        bad_chars = [',', '.', '!', '?']
        for c in bad_chars:
            review = review.replace(c, "")
        review_text = review.split(" ")

        included_list = []
        for word in review_text:
            if word in bag_of_words:
                if word not in included_list:
                    included_list.append(word)
        prob_pos = 1
        prob_neg = 1
        for p_word in included_list:
            prob_pos = prob_pos * (bag_of_words[p_word][0] / overall_positive)
            prob_neg = prob_neg * (bag_of_words[p_word][1] / overall_negative)
        prob_pos = prob_pos * (overall_positive / 57)
        prob_neg = prob_neg * (overall_negative / 57)

        if prob_pos > prob_neg:
            new_positive += 1
            print(review, "Positive review!")
        else:
            new_negative += 1
            print(review, "Negative review...")
    print("Total new positive reviews: " + str(new_positive))
    print("Total new negative reviews: " + str(new_negative))

main()