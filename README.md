# File to Markdown

A simple web app for converting files to Markdown. Drag in a file, get a `.md` back.
Everything runs on your own computer, so your files are never uploaded anywhere.

Built on [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft and [Streamlit](https://streamlit.io).

## Supported files

PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx/.xls), CSV, JSON, XML, HTML, EPUB, ZIP, images, audio and more.

## Quick start

You need [Python 3.10 or newer](https://www.python.org/downloads/). On Windows, tick **Add Python to PATH** during install.

1. Click the green **Code** button, then **Download ZIP**, and unzip it.
2. Start the app:
   - **Windows:** double-click `run.bat`
   - **Mac/Linux:** run `./run.sh` in a terminal
3. Your browser opens at http://localhost:8501. Upload files and download the results.

The first launch installs everything it needs and takes a few minutes. Later launches start right away.

## Manual install

```
pip install -r requirements.txt
streamlit run markitdown_app.py
```

## Features

- Convert one file or many at once
- Preview the Markdown before downloading
- Download each file, or all of them as a ZIP

## License

MIT. See `LICENSE`.
