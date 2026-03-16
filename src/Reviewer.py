import os

class Reviewer:
    # Set file of reviewer than review it
    def __init__(self, review_directory : str = None):
        print("Created a reviewer object successfully")

        if review_directory is None:
            review_directory = "./to_review/"

        # Append slash if necessary
        if not review_directory.endswith('/'):
            review_directory += '/'

        self.review_directory = review_directory

    # Helper function for getting all file names in the review directory
    # Ignores sub directories and their contents
    def _get_all_files(self):
        files = os.listdir(self.review_directory)
        # Filtering only the files.
        files = [f for f in files if os.path.isfile(self.review_directory + f)]
        return files

    def interactive_file_select(self):
        page = 0
        page_size = 5
        # get all files in the directory
        files = self._get_all_files()
        selected = None
        while selected == None:
            for i in range(page_size):
                index = page * page_size + i
                if index >= len(files):
                    break
                print(f"[{i}]: {files[index]}")
            valid_answer = False
            while(not valid_answer):
                answer = input('Type number to select file or type n for next page, or p for previous page\n').strip().lower()
                if answer in ['p', 'n'] or (answer.isdigit() and int(answer) in range(page_size - 1) and int(answer) + page * page_size < len(files)):
                    valid_answer = True
                    if answer == 'p':
                        page = (page - 1) % (1 + len(files) // page_size)
                    elif answer == 'n':
                        page = (page + 1) % (1 + len(files) // page_size)
                    else:
                        selected = files[page * page_size + int(answer)]
        
        return f"./{self.review_directory}/{selected}"
            
    def _review_string(self, string):
        prompt = f"""
        Review attached python code. Give me four sections, each with bullet points on possible improvements.
        Don't give precise advice, just vague diagnoses e.g. Don't use magic numbers.
        The four sections should be: Syntax errors, Good practice, Optimisation, Possible logical issues
        Possible logical issues should be e.g. are you sure you're supposed to be printing X?
        Code is below:

        {string}
        """
        return 'Code is crap'

    def review(self, file_path : str = None):
        if file_path == None:
            file_path = self.interactive_file_select()
        
        # Read file_path
        try:
            f = open(file_path, "r")
            return {
                'review': self._review_string(f.read())
            }
        except FileNotFoundError:
            print('Review failed, file could not be found')

        # print to console
        return None