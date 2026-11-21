import io
import tempfile
import zipfile
from pathlib import Path

import streamlit as st
from markitdown import MarkItDown

MAX_MB = 20
MAX_FILES = 10

st.set_page_config(page_title="File to Markdown", page_icon="📄", layout="centered")

st.title("File to Markdown")
st.caption("Upload files and download them as .md, ready for LLMs and notes.")
st.info(
    "Your files are processed on the server only to make the Markdown. "
    "They are not saved. Avoid uploading sensitive documents to a hosted copy; "
    "run the app on your own computer if privacy matters."
)


@st.cache_resource
def get_converter():
    return MarkItDown()


files = st.file_uploader(
    f"Choose files (up to {MAX_FILES} files, {MAX_MB} MB each)",
    accept_multiple_files=True,
    type=["pdf", "docx", "pptx", "xlsx", "csv", "json", "xml", "html", "htm", "epub", "txt"],
)

if files:
    if len(files) > MAX_FILES:
        st.warning(f"Only the first {MAX_FILES} files will be converted.")
        files = files[:MAX_FILES]

    converter = get_converter()
    results = {}

    for f in files:
        if f.size > MAX_MB * 1024 * 1024:
            st.error(f"{f.name} is larger than {MAX_MB} MB and was skipped.")
            continue
        tmp_path = None
        with st.spinner(f"Converting {f.name}..."):
            try:
                # MarkItDown reads from disk, so save the upload to a temp file first
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(f.name).suffix) as tmp:
                    tmp.write(f.getbuffer())
                    tmp_path = tmp.name
                results[f.name] = converter.convert(tmp_path).markdown
            except Exception as e:
                st.error(f"Could not convert {f.name}: {e}")
            finally:
                if tmp_path:
                    Path(tmp_path).unlink(missing_ok=True)

    for name, text in results.items():
        md_name = Path(name).stem + ".md"
        with st.expander(f"{name}  →  {md_name}", expanded=len(results) == 1):
            st.download_button(
                "Download .md",
                data=text.encode("utf-8"),
                file_name=md_name,
                mime="text/markdown",
                key=f"dl_{name}",
            )
            st.text_area("Preview", text, height=300, key=f"prev_{name}")

    if len(results) > 1:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for name, text in results.items():
                z.writestr(Path(name).stem + ".md", text)
        st.download_button(
            "Download all as ZIP",
            data=buf.getvalue(),
            file_name="markdown_files.zip",
            mime="application/zip",
        )
else:
    st.write("Drag files here or click Browse files to start.")
