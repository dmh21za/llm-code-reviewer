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
        
        return selected
            