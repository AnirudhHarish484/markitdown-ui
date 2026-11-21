# File to Markdown

A simple web app for converting files to Markdown. Drag in a file, get a `.md` back.

Built on [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft and [Streamlit](https://streamlit.io).

## Try it online

**https://YOUR-APP-NAME.streamlit.app**

The hosted copy processes files on a shared server. Nothing is saved, but avoid uploading sensitive documents. For private files, run it on your own computer (below).

## Supported files

PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx), CSV, JSON, XML, HTML, EPUB and plain text.

Limits: up to 10 files at a time, 20 MB each.

## Run it on your computer

Your files never leave your machine this way. You need [Python 3.10 or newer](https://www.python.org/downloads/). On Windows, tick **Add Python to PATH** during install.

1. Click the green **Code** button, then **Download ZIP**.
2. **Extract the ZIP** to a normal folder such as your Desktop. Don't run it from inside the ZIP.
3. Start the app:
   - **Windows:** double-click `run.bat`
   - **Mac/Linux:** run `./run.sh` in a terminal
4. Your browser opens at http://localhost:8501. Upload files and download the results.

The first launch installs everything it needs and takes a few minutes. Later launches start right away.

On Windows you may see a blue "Windows protected your PC" warning. Click **More info**, then **Run anyway**.

### Manual install

```
pip install -r requirements.txt
streamlit run markitdown_app.py
```

## Features

- Convert one file or several at once
- Preview the Markdown before downloading
- Download each file, or all of them as a ZIP

## Credits and license

Conversion is done by Microsoft's MarkItDown (MIT). This project is also MIT licensed. See `LICENSE`.
