import streamlit as st

st.set_page_config(
    page_title="Image Market Standard Analyzer",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ Image Market Standard Analyzer")

st.write(
    "Analyze output images against defined market standards."
)

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:
    st.subheader("Uploaded Image")

    st.image(
        uploaded_file,
        use_container_width=True
    )

    st.success("Image uploaded successfully!")
