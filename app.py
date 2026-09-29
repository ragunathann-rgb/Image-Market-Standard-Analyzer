import streamlit as st
from PIL import Image, ImageStat, ImageFilter
import io

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Image Market Standard Analyzer",
    page_icon="🖼️",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🖼️ Image Market Standard Analyzer")

st.write(
    "Analyze image quality, dimensions, composition, "
    "and market-standard compliance."
)

st.divider()

# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload an image for analysis",
    type=["jpg", "jpeg", "png", "webp"]
)

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if uploaded_file:

    # Open image
    image = Image.open(uploaded_file)

    # Convert to RGB for analysis
    rgb_image = image.convert("RGB")

    # ----------------------------------------------
    # BASIC INFORMATION
    # ----------------------------------------------

    width, height = image.size

    file_size_mb = uploaded_file.size / (1024 * 1024)

    image_format = image.format

    # Aspect ratio
    aspect_ratio = width / height

    # ----------------------------------------------
    # BRIGHTNESS
    # ----------------------------------------------

    grayscale = rgb_image.convert("L")

    brightness = ImageStat.Stat(grayscale).mean[0]

    # ----------------------------------------------
    # CONTRAST
    # ----------------------------------------------

    contrast = ImageStat.Stat(grayscale).stddev[0]

    # ----------------------------------------------
    # SHARPNESS
    # ----------------------------------------------

    edges = grayscale.filter(ImageFilter.FIND_EDGES)

    sharpness = ImageStat.Stat(edges).mean[0]

    # --------------------------------------------------
    # DISPLAY IMAGE
    # --------------------------------------------------

    st.subheader("Uploaded Image")

    st.image(
        image,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------
    # IMAGE INFORMATION
    # --------------------------------------------------

    st.subheader("📊 Image Analysis")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Width",
            f"{width:,} px"
        )

    with col2:
        st.metric(
            "Height",
            f"{height:,} px"
        )

    with col3:
        st.metric(
            "File Size",
            f"{file_size_mb:.2f} MB"
        )

    with col4:
        st.metric(
            "Format",
            image_format
        )

    # --------------------------------------------------
    # QUALITY METRICS
    # --------------------------------------------------

    st.subheader("🔍 Quality Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Aspect Ratio",
            f"{aspect_ratio:.2f}:1"
        )

    with col2:
        st.metric(
            "Brightness",
            f"{brightness:.1f}"
        )

    with col3:
        st.metric(
            "Contrast",
            f"{contrast:.1f}"
        )

    st.metric(
        "Sharpness",
        f"{sharpness:.1f}"
    )

    st.divider()

    # --------------------------------------------------
    # INITIAL OBSERVATIONS
    # --------------------------------------------------

    st.subheader("📝 Initial Observations")

    if width >= 1000 and height >= 1000:
        st.success(
            "✓ Image resolution meets the initial 1000 × 1000 px reference."
        )
    else:
        st.warning(
            "⚠ Image resolution is below the initial 1000 × 1000 px reference."
        )

    if brightness < 50:
        st.warning(
            "⚠ Image appears relatively dark."
        )
    elif brightness > 200:
        st.warning(
            "⚠ Image appears very bright."
        )
    else:
        st.success(
            "✓ Brightness is within a moderate range."
        )

    if contrast < 25:
        st.warning(
            "⚠ Image has relatively low contrast."
        )
    else:
        st.success(
            "✓ Image has reasonable contrast."
        )

    if sharpness < 10:
        st.warning(
            "⚠ Image may require a sharpness review."
        )
    else:
        st.success(
            "✓ Image contains visible edge detail."
        )

else:

    st.info(
        "👆 Upload an image above to start the analysis."
    )
