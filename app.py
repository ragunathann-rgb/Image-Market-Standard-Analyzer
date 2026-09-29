import streamlit as st
from PIL import Image, ImageStat, ImageFilter


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Image Market Standard Analyzer",
    page_icon="🖼️",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🖼️ Image Market Standard Analyzer")

st.write(
    "Analyze output images against selected market and visual standards."
)

st.divider()


# ============================================================
# ANALYSIS SETTINGS
# ============================================================

st.subheader("⚙️ Analysis Settings")

col1, col2 = st.columns(2)


with col1:

    analysis_type = st.selectbox(
        "What type of image are you analyzing?",
        [
            "Product Image",
            "Product Page Screenshot",
            "Website Screenshot",
            "Marketing Banner",
            "Social Media Creative",
            "AI Generated Image",
            "Custom"
        ]
    )


with col2:

    market_standard = st.selectbox(
        "Which market standard should be used?",
        [
            "General E-commerce",
            "Amazon",
            "Google Shopping",
            "Shopify",
            "Custom"
        ]
    )


# ============================================================
# SHOW SELECTED SETTINGS
# ============================================================

st.info(
    f"Analysis Type: **{analysis_type}**  |  "
    f"Market Standard: **{market_standard}**"
)


st.divider()


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.subheader("📤 Upload Image")

uploaded_file = st.file_uploader(
    "Upload an image for analysis",
    type=["jpg", "jpeg", "png", "webp"]
)


# ============================================================
# IMAGE ANALYSIS
# ============================================================

if uploaded_file:

    # --------------------------------------------------------
    # OPEN IMAGE
    # --------------------------------------------------------

    image = Image.open(uploaded_file)

    rgb_image = image.convert("RGB")


    # --------------------------------------------------------
    # BASIC IMAGE INFORMATION
    # --------------------------------------------------------

    width, height = image.size

    file_size_mb = uploaded_file.size / (1024 * 1024)

    image_format = image.format

    aspect_ratio = width / height


    # --------------------------------------------------------
    # BRIGHTNESS
    # --------------------------------------------------------

    grayscale = rgb_image.convert("L")

    brightness = ImageStat.Stat(grayscale).mean[0]


    # --------------------------------------------------------
    # CONTRAST
    # --------------------------------------------------------

    contrast = ImageStat.Stat(grayscale).stddev[0]


    # --------------------------------------------------------
    # SHARPNESS
    # --------------------------------------------------------

    edges = grayscale.filter(ImageFilter.FIND_EDGES)

    sharpness = ImageStat.Stat(edges).mean[0]


    # ========================================================
    # DISPLAY IMAGE
    # ========================================================

    st.subheader("🖼️ Uploaded Image")

    st.image(
        image,
        use_container_width=True
    )


    st.divider()


    # ========================================================
    # BASIC IMAGE INFORMATION
    # ========================================================

    st.subheader("📊 Technical Information")

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


    # ========================================================
    # QUALITY METRICS
    # ========================================================

    st.subheader("🔍 Image Quality Metrics")

    col1, col2, col3, col4 = st.columns(4)

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

    with col4:

        st.metric(
            "Sharpness",
            f"{sharpness:.1f}"
        )


    st.divider()


    # ========================================================
    # ANALYSIS BASED ON IMAGE TYPE
    # ========================================================

    st.subheader("🔎 Analysis Focus")


    if analysis_type == "Product Image":

        st.write(
            """
            **Product Image Analysis**

            The application will evaluate:
            - Image dimensions
            - Product visibility
            - Product positioning
            - Background
            - Product coverage
            - Image quality
            - Cropping
            """
        )


    elif analysis_type == "Product Page Screenshot":

        st.write(
            """
            **Product Page Analysis**

            The application will evaluate:
            - Product presentation
            - Product title
            - Price visibility
            - Reviews
            - Navigation
            - Call-to-action visibility
            - Visual hierarchy
            - Layout
            """
        )


    elif analysis_type == "Website Screenshot":

        st.write(
            """
            **Website Screenshot Analysis**

            The application will evaluate:
            - Navigation
            - Layout
            - Visual hierarchy
            - Typography
            - Spacing
            - Branding
            - Content visibility
            """
        )


    elif analysis_type == "Marketing Banner":

        st.write(
            """
            **Marketing Banner Analysis**

            The application will evaluate:
            - Visual hierarchy
            - Headline visibility
            - CTA visibility
            - Product positioning
            - Branding
            - Image quality
            - Composition
            """
        )


    elif analysis_type == "Social Media Creative":

        st.write(
            """
            **Social Media Creative Analysis**

            The application will evaluate:
            - Composition
            - Text readability
            - Branding
            - Visual hierarchy
            - Platform suitability
            - Image quality
            """
        )


    elif analysis_type == "AI Generated Image":

        st.write(
            """
            **AI Generated Image Analysis**

            The application will evaluate:
            - Image quality
            - Visual consistency
            - Composition
            - Artifacts
            - Text rendering
            - Product presentation
            """
        )


    else:

        st.write(
            """
            **Custom Analysis**

            A custom set of standards will be applied.
            """
        )


    # ========================================================
    # INITIAL TECHNICAL CHECKS
    # ========================================================

    st.subheader("📝 Initial Technical Checks")


    # --------------------------------------------------------
    # Resolution check
    # --------------------------------------------------------

    if analysis_type == "Product Image":

        if width >= 1000 and height >= 1000:

            st.success(
                "✓ Image meets the initial product-image resolution reference."
            )

        else:

            st.warning(
                "⚠ Image is below the initial product-image resolution reference."
            )


    else:

        st.info(
            "ℹ Resolution will be evaluated according to the selected "
            "image type and market standard."
        )


    # --------------------------------------------------------
    # Brightness check
    # --------------------------------------------------------

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
            "✓ Brightness is within the initial reference range."
        )


    # --------------------------------------------------------
    # Contrast check
    # --------------------------------------------------------

    if contrast < 25:

        st.warning(
            "⚠ Image has relatively low contrast."
        )

    else:

        st.success(
            "✓ Image has reasonable contrast."
        )


    # --------------------------------------------------------
    # Sharpness check
    # --------------------------------------------------------

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
        "👆 Select your analysis settings and upload an image to begin."
    )
