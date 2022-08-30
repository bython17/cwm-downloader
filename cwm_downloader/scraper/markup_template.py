""" This modules provides a markup template for the text lectures."""

# Styles that are applied to all the text lectures
styles = '''
body {
    color: #aaa;
    font-family: 'ubuntu', sans-serif;
    margin: 0;
    padding: 0;
}

#root {
    background-color: #111112;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
}

p {
    line-height: 2;
}

a {
    color: #289;
    text-decoration: none;
    font-weight: 300;
}

svg {
    display: none;
}

div[role="main"] {
    max-width: 800px;
    min-width: 400px;
    margin-top: 20px;
    height: fit-content;
}

div.lecture-attachment.lecture-attachment-type-pdf_embed, div.lecture-attachment.lecture-attachment-type-file {
    margin-top: 40px;
    border-radius: 10px;
    padding: 10px;
    background-color: #222;
}

div.lecture-attachment div.attachment {
    padding: 5px;
}

div.lecture-attachment a {
    color: #289;
    text-decoration: none;
    font-weight: 900;
}

h2.section-title {
    color: #444;
    font-size: 32px;
    margin-bottom: 10px;
}
'''

# Here is the markup with some format strings
markup = '''<html>
  <head>
  <title> {0} </title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet">
  <style>
  {1}
  </style>
  </head>
  <body>
  <div id="root">
  {2}
  </div>
  </body>
  </html>
  '''


def create_markup(lecture_name: str, main_container: str):
    """
    Create a marukup given the container to be wraped and the name 
    of the lecture.

    :param lecture_name: The name of the lecture
    :param main_container: The container that contains all the useful information about
    the course
    """
    return markup.format(lecture_name, styles, main_container)
