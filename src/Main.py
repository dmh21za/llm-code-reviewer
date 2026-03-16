from dotenv import load_dotenv
from os import environ
from Reviewer import Reviewer


load_dotenv()
test_key = environ.get('TEST_KEY')

def main():
    print('Hello world')
    print('TEST KEY: ', test_key)
    # Tell me all the files in project root
    reviewer = Reviewer()
    review_obj = reviewer.review()
    if review_obj is not None:
        print(review_obj['review'])
    else:
        print('Something went wrong...')

if __name__ == '__main__':
    main()