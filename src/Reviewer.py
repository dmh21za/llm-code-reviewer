import os
import ast
import textwrap
from openai import OpenAI

class Reviewer:
    # Set file of reviewer than review it
    def __init__(self, groq_key : str, review_directory : str = None):
        print("Created a reviewer object successfully")

        if review_directory is None:
            review_directory = "./to_review/"

        # Append slash if necessary
        if not review_directory.endswith('/'):
            review_directory += '/'

        self.review_directory = review_directory
        self.groq_key = groq_key

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
            
    def _clean_code(self, code: str) -> str:
        """Remove prompt indentation and surrounding whitespace."""
        return textwrap.dedent(code).strip()


    def _check_syntax(self, code: str):
        """Return syntax error if one exists."""
        try:
            ast.parse(code)
            return None
        except SyntaxError as e:
            return f"SyntaxError: {e}"

    def _prompt_groq(self, prompt : str):
        output = ""
        client = OpenAI(
            api_key=self.groq_key,
            base_url="https://api.groq.com/openai/v1"
        )

        code = prompt

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    def _review_code(self, code : str):
        cleaned = self._clean_code(code)

        syntax_error = self._check_syntax(code)

        print("===== CODE =====")
        print(cleaned)

        if syntax_error:
            print("\n===== SYNTAX ERROR DETECTED =====")
            print(syntax_error)
            return

        prompt = f"""
You are a strict Python code reviewer.

Rules:
- Only report objective issues visible in the code.
- Do NOT suggest optional improvements or stylistic preferences.
- Ignore optional PEP8 suggestions such as type hints or docstring formats.
- If no issues exist in a section, write "None detected".
- Maximum 2 issues per section.

Format:

### Section name
Issue — exact line from code

Code to review:

```python
{cleaned}"""
        
        return self._prompt_groq(prompt)

    def review(self, file_path : str = None):
        if file_path == None:
            file_path = self.interactive_file_select()
        
        # Read file_path
        try:
            f = open(file_path, "r")
            return {
                'review': self._review_code(f.read())
            }
        except FileNotFoundError:
            print('Review failed, file could not be found')

        # print to console
        return None