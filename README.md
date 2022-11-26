# Code With Mosh Downloader

This is a python CLI program made for downloading  enrolled courses and lectures from https://codewithmosh.com with high quality including all exercises and pdfs needed. This program allows you to download full courses, sections and lectures with ease. This program requires a valid credentials (headers and cookies) of an enrolled user to work.

**Note:** **This project is only valid for people who have a valid account Or if the courses are free and are not locked. The project has no malicious intents what so ever.**

## Motivation for the project

For a long time I watched Mosh's YouTube channel where he only shows a tiny part of the full course. This made me eager to buy his courses and I ended up subscribing to the monthly subscription plan. But then I wanted to download a lot of courses from the site so using my python skills I made [cwm-downloader-old](https://github.com/bython17/cwm-downloader-old) but that didn't seem clean and was kinda bulky. So, I rewrote it again and here it is.

**Note** Currently my subscription has ended and I can't test the app with all the courses available anymore. So, I would appreciate contributions a lot. Read more about contributions at the bottom.
<br>
<br>

## Requirements

- python 3
-  pip

<br>

## Installation

### Using pre-built `.whl` files
#### -> Download the python wheel file
Head over to the [releases](https://github.com/bython17/cwm-downloader/releases/latest) page and download the python wheel or the `.whl` file.
#### -> Install the program using pip
First navigate to the directory  where you downloaded the wheel file and execute the following command.
```bash
pip install [whl-file]
```
_Replace the `[whl-file]` with the python wheel file you downloaded_

Even though it isn't recommended, you can use the sdist(`.tar.gz`) file to install the project.

And there you go, the program is installed. Go to the [Edit credentials section](#edit-the-credentialsjson-file) to authenticate yourself and download the courses you paid for. <br>
If for any reason the pre-built binary doesn't work or has an error when installing with pip, check out the [Manual installation](#manual-build-installation), may be that could help.

### Manual build installation
#### -> Install poetry

This project uses poetry for dependency management, building and generating a cli command. So to install [poetry](https://python-poetry.org/). run

```bash
python -m pip install poetry
```

Or go to the [docs](https://python-poetry.org/docs/) and install poetry using another way.

<br>

#### -> Clone the repo

Clone the repo and move in to it

```bash
git clone https://github.com/bython17/cwm-downloader && cd cwm-downloader
```

<br>

#### -> Install dependencies and setup the CLI using poetry

**NOTICE**: If you are a windows user, you need to enable the [Windows Long Path](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=powershel) in order to install the dependencies. To enable [Windows Long Path](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=powershel) you can execute the following PowerShell script(Windows 10, Version 1607, and Later)

```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```
Learn more at [Microsoft](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=powershel)

<br>

To install all the dependencies run
```bash
python -m poetry install
```
or
```bash
poetry install
``` 
*If you installed poetry globally.*


Now all dependencies should be installed in a venv and you can issue the command without using python like ` cwm-downloader --help` after typing ```poetry shell```

<br>

#### -> Building and installing the project using `pip` and `poetry build`
To build and install the project follow the steps below, but before doing anything, you need to have python in path. If you don't have python in path, then  [Check this out](https://medium.com/edureka/add-python-to-path-f97fcab2a58d).


Navigate to the projects root directory for the last time and run

```
poetry build
```

Poetry will now generate a dist directory which contains a wheel file that is installable by pip so run

```
pip install dist/[.whl file]
```
_Replace the `[.whl file]` with the `.whl` file that poetry has created for you in the dist directory from the project's root. Or you can install the ```.tar.gz``` file that is in the same directory._

**Note** Make sure that you run this outside a child shell or while not in a venv just to be safe.

and **Horay 😃** Now you can access the command from any where in your computer !


## Edit the credentials.json file

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
- Run the program with the `--edit-credentials` option

  ```bash
  cwm-downloader --edit-credentials
  ```


- When the editor opens with the credentials.json file, delete all the contents inside and paste the contents you copied from https://www.scrapingbee.com/curl-converter/json/.

Now you are ready to run and use the program! 😎

<br>

## Usage

The app is a CLI, so you can use the `--help` option to learn more about the commands. But here are the basics
<br>
<br>
<br>
**Download all lectures**
<br>
<br>
To do that just execute the command with the download sub command and give it the url. For example let's download part one of the brand new C++ course.

```
cwm-downloader download https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187035
```

This should download all the sections and lectures of the course. and btw you can use any lecture URL that is found on that course.
<br>
<br>
<br>
**Download only one lecture**
<br>
<br>
To download a single lecture you can do this

```
cwm-downloader download https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187035 --section 2 --lecture 1 --only
```

This will tell the downloader you want to download that specifiec lecture only and nothin after that. notice here we specified a section because we need sections to get the correct lecture. if no section is given it is going to default to the first one.
<br>
<br>
<br>
**Download a course from a specific point on wards**
<br>
<br>
To do that just specifiy the point you want to start and don't specifiy the ` --only` flag.

```
cwm-downloader download https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187035 --section 2 --lecture 1
```
<br>
<br>

There are a few more commands to play around with just check em out using
```
cwm-downloader --help
```

And you can also see the help message for the download subcommand

```
cwm-downloader download --help
```

## Contributions

I have tried to document my code very well to make it easy to understand. I am not a pro python engineer by any means just a high school kid who loves to code. So I would greatly appreciate any comments and code reviews from the community and If you have a great feature in mind don't forget to hit that pull request 😁. Thanks
