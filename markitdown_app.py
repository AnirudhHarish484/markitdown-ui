import io
import tempfile
import zipfile
from pathlib import Path

import streamlit as st
from markitdown import MarkItDown

st.set_page_config(page_title="File to Markdown", page_icon="📄", layout="centered")

st.title("File to Markdown")
st.caption("Upload one or more files and download them as .md. Everything runs on your computer.")


@st.cache_resource
def get_converter():
    return MarkItDown()


files = st.file_uploader(
    "Choose files",
    accept_multiple_files=True,
    type=["pdf", "docx", "pptx", "xlsx", "xls", "csv", "json", "xml", "html", "htm",
          "txt", "epub", "zip", "jpg", "jpeg", "png", "wav", "mp3", "msg"],
)

if files:
    converter = get_converter()
    results = {}

    for f in files:
        suffix = Path(f.name).suffix
        with st.spinner(f"Converting {f.name}..."):
            try:
                # MarkItDown reads from disk, so save the upload to a temp file first
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(f.getbuffer())
                    tmp_path = tmp.name
                results[f.name] = converter.convert(tmp_path).markdown
                Path(tmp_path).unlink(missing_ok=True)
            except Exception as e:
                st.error(f"Could not convert {f.name}: {e}")

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
    st.info("Drag files here or click Choose files to start.")
