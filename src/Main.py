from dotenv import load_dotenv
from os import environ
from Reviewer import Reviewer


def main():
    load_dotenv()
    test_key = environ.get('TEST_KEY')
    groq_key = environ.get('GROQ_KEY')

    # Tell me all the files in project root
    reviewer = Reviewer(groq_key)
    review_obj = reviewer.review()
    if review_obj is not None:
        print(review_obj['review'])
    else:
        print('Something went wrong...')


if __name__ == '__main__':
    main()