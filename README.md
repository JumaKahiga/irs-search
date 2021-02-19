# irs-search
Utilities for searching IRS tax forms

### Running Locally
- Clone the repository to your machine using the following command `git clone https://github.com/JumaKahiga/irs-search.git`

- Navigate into the project folder using `cd irs-search`

- Create a virtual environment using the following command `python3 -m venv env` . (If you have not yet installed Python, please see instructions [here](https://www.python.org/downloads/))

- Activate the environment using the following command if on MacOS or Linux `source env/bin/activate`. If on any other platform, please check activation instructions [here](https://www.python.org/downloads/)

- Install the required packages by running the following command `pip install -r requirements.txt`

- There are two scripts available with this program and here is how you can run them after the above steps:

#### Get information results
- Run this command: `python -m main run-json-script`
- This will give you the following prompt:
```
Please enter comma separated form names:
```
- The years should be provided as shown in this example `Form W-2, Form 1095-C`
- A successful run will output the informational results on your screen
- If the run was not successful, you will get an error message describing the issue

#### Download pdfs
- Run this command: `python -m main run-pdf-script`
- This will give you the following prompts:
```
Please enter a form name: 
Please specify start year: 
Please specify end year: 
```
- Press enter after the providing a value for the last result.
- If the script runs successfully, you can find the downloaded pdfs in `irs-search/form-pdf/pdf-downloads`.
- If the run was not successful, you will get an error message describing the issue

