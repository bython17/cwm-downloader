## Code With Mosh Downloader

This is a python CLI program made for downloading enrolled courses and lectures from https://codewithmosh.com including all exercises and pdfs needed. This program allows you to download full courses, sections and lectures with ease. This program requires a valid credentials(headers and cookies) of an enrolled user to work.

**Note:** **This project is only valid for people who have a valid account Or if the courses are free and are not locked. The project has no malicious intents what so ever.**

### Motivation for the project

For along time I watched Mosh's youtube channel where he only shows a tiny part of the full course. This made me eager to buy his courses and I ended up subscribing to the monthly subscription plan. But then I wanted to download alot of courses from the site so using my tiny python skills I made [cwm-downloader-old](https://github.com/bython17/cwm-downloader-old) but that didn't seem clean and was kinda bulky. So I rewrote it again and here it is.

**Note** Currently my subscription has ended and I can't test the app properly anymore. So I would appreciate contributions alot. Read more about contribution's at the bottom.

### Requirements

- Python 3

### Installation

#### Install poetry

This project uses poetry for dependency management, building and generating a cli command. So to install [poetry](https://python-poetry.org/). run

```bash
python -m pip install poetry
```

Or go to the [docs](https://python-poetry.org/docs/) and install poetry using another way.

#### clone the repo

Clone the repo and move in to it

```bash
git clone https://github.com/bython17/cwm-downloader && cd cwm-downloader
```

#### Install dependencies and setup the CLI using poetry

```bash
poetry install
```

Now all dependencies should be installed in a venv and you can issue the command without using python like ` cwm-downloader --help` after typing ```poetry shell```

#### Edit the credentials.json file

The app relies on a json file that contains the headers and cookies of a valid account that is enrolled in some sort of course or lecture. To get the valid cookies and headers follow these simple steps.

- Get the cookies and headers as a cURL
  - Go to your browser.
  - Sign in with your valid account.
  - Navigate to any lecture that you are enrolled in.
  - Open the devtools of the browser.
  - Go to the "Networks" tab
  - Click on the filter "Doc"
  - Right click on the first request
  - Select the sub option "copy all as cURL" from the option copy
- Go to https://www.scrapingbee.com/curl-converter/json/ and paste the cURL you copied on the space provided and copy the final json output to your clipboard.
- Assuming you run `poetry install` , let's edit the credentials.json file to do that run the following command inside the root dir of the project

  ```bash
  poetry run cwm-downloader --edit-credentials
  ```

  **_Note_** We did the the `poetry run` because we need to use the venv's python and bin not the globals. If you want you can also spawn a child shell using `poetry shell` and then run `cwm-downloader` .

- When the editor opens with the credentials.json file, delete all the contents inside and paste the contents you copied from https://www.scrapingbee.com/curl-converter/json/.

Now you are ready to run and use the program! 😎

### Usage

The app is a CLI, so you can use the `--help` option to learn more about the commands. But here are the basics

**Tip** to use the ` cwm-downloader` command like the below: First run `poetry shell` which creates a child shell or skip around to the bottom to make the command global. If you don't mind typing a longer command then you can use ` poetry run cwm-downloader` to run the command from the project root.

**Download all the courses**
To do that just execute the command with the download sub command and give it the url. For example let's download part one of the brand new C++ course.

```
cwm-downloader download https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187035
```

This should download all the sections and lectures of the course. and btw you can use any lecture URL that is found on that course.

**Download only one lecture**
To download a single lecture you can do this

```
cwm-downloader download https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187035 --section 2 --lecture 1 --only
```

This will tell the downloader you want to download that specifiec lecture only and nothin after that. notice here we specified a section because we need sections to get the correct lecture. if no section is given it is going to default to the first one.

**Download a course from a specific point on wards**
To do that just specifiy the point you want to start and don't specifiy the ` --only` flag.

There are a few more commands to play around with just check em out using

```
cwm-downloader --help
```

And you can also see the help message for the download subcommand

```
cwm-downloader download --help
```

### Making the command global

If you are tired of going to the project directory every time and download the courses (you should be unless you are a psycho) then you can make it global by installing it using pip.

Navigate to the projects root directory for the last time and run

```
poetry build
```

Poetry will now generate a dist directory which contains a wheel file that is installable by pip so run

```
pip install dist/cwm_downloader-0.1.0-py3-none-any.whl
```
Or you can install the ```tar.gz``` file that is in the same directory. 

**Note** Make sure that you run this outside a child shell or while not in a venv just to be safe.

and **Horay 😃** Now you can access the command from any where in your computer !

### Contributions

I have tried to document my code very well to make it easy to understand. I am not a pro python engineer by any means just a high school kid who fell in love with code. So I would greatly appreciate any comments and code reviews from the community and If you have a great feature in mind don't forget to hit that pull request 😁. Thanks
