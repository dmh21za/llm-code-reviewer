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
    print(reviewer.interactive_file_select())

if __name__ == '__main__':
    main()