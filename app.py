import streamlit as st
from PIL import Image, ImageStat, ImageFilter
import json

from google import genai
from google.genai import types


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Image Market Standard Analyzer",
    page_icon="🖼️",
    layout="wide"
)


# ============================================================
# LOAD MARKET STANDARDS
# ============================================================
with open("standards.json", "r") as file:
    standards = json.load(file)

# ============================================================
# GEMINI AI
# ============================================================

gemini_client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
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
# CONVERT MARKET NAME TO JSON KEY
# ============================================================

standard_key_map = {
    "General E-commerce": "general_ecommerce",
    "Amazon": "amazon",
    "Google Shopping": "google_shopping",
    "Shopify": "shopify",
    "Custom": "custom"
}

standard_key = standard_key_map[market_standard]

selected_standard = standards[standard_key]


# ============================================================
# SHOW SELECTED SETTINGS
# ============================================================

st.info(
    f"Analysis Type: **{analysis_type}**  |  "
    f"Market Standard: **{market_standard}**"
)

st.divider()


# ============================================================
# DISPLAY MARKET STANDARD
# ============================================================

st.subheader("📋 Selected Market Standard")

if analysis_type == "Product Image":

    product_rules = selected_standard["product_image"]

    col1, col2, col3 = st.columns(3)

    with col1:

        if "minimum_width" in product_rules:

            st.metric(
                "Minimum Width",
                f"{product_rules['minimum_width']} px"
            )

        elif "minimum_longest_side" in product_rules:

            st.metric(
                "Minimum Longest Side",
                f"{product_rules['minimum_longest_side']} px"
            )

        elif "current_minimum_width" in product_rules:

            st.metric(
                "Current Minimum Width",
                f"{product_rules['current_minimum_width']} px"
            )

        else:

            st.metric(
                "Maximum Width",
                f"{product_rules.get('maximum_width', 'N/A')} px"
            )


    with col2:

        if "minimum_height" in product_rules:

            st.metric(
                "Minimum Height",
                f"{product_rules['minimum_height']} px"
            )

        elif "minimum_shortest_side" in product_rules:

            st.metric(
                "Minimum Shortest Side",
                f"{product_rules['minimum_shortest_side']} px"
            )

        elif "current_minimum_height" in product_rules:

            st.metric(
                "Current Minimum Height",
                f"{product_rules['current_minimum_height']} px"
            )

        else:

            st.metric(
                "Maximum Height",
                f"{product_rules.get('maximum_height', 'N/A')} px"
            )


    with col3:

        if "maximum_file_size_mb" in product_rules:

            st.metric(
                "Maximum File Size",
                f"{product_rules['maximum_file_size_mb']} MB"
            )

        else:

            st.metric(
                "Standard",
                market_standard
            )


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.subheader("📤 Upload Image")

uploaded_file = st.file_uploader(
    "Upload an image for analysis",
    type=["jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff"]
)


# ============================================================
# ANALYSIS
# ============================================================

if uploaded_file:

    # --------------------------------------------------------
    # OPEN IMAGE
    # --------------------------------------------------------

    image = Image.open(uploaded_file)

    rgb_image = image.convert("RGB")


    # --------------------------------------------------------
    # BASIC INFORMATION
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
    # IMAGE PREVIEW
    # ========================================================

    st.subheader("🖼️ Uploaded Image")

    st.image(
        image,
        use_container_width=True
    )

    st.divider()


    # ========================================================
    # TECHNICAL INFORMATION
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
    # MARKET STANDARD CHECKS
    # ========================================================

    st.subheader("✅ Market Standard Checks")


    product_rules = selected_standard["product_image"]


    # --------------------------------------------------------
    # RESOLUTION CHECK
    # --------------------------------------------------------

    if "minimum_width" in product_rules:

        min_width = product_rules["minimum_width"]
        min_height = product_rules["minimum_height"]

        resolution_pass = (
            width >= min_width and
            height >= min_height
        )

        if resolution_pass:

            st.success(
                f"✓ Resolution: {width} × {height} px — PASS"
            )

        else:

            st.error(
                f"✕ Resolution: {width} × {height} px — "
                f"Required: {min_width} × {min_height} px"
            )


    elif "minimum_longest_side" in product_rules:

        longest_side = max(width, height)
        shortest_side = min(width, height)

        min_longest = product_rules["minimum_longest_side"]
        min_shortest = product_rules["minimum_shortest_side"]

        resolution_pass = (
            longest_side >= min_longest and
            shortest_side >= min_shortest
        )

        if resolution_pass:

            st.success(
                f"✓ Resolution: {width} × {height} px — PASS"
            )

        else:

            st.error(
                f"✕ Resolution: {width} × {height} px — "
                f"Required longest side ≥ {min_longest}px "
                f"and shortest side ≥ {min_shortest}px"
            )


    elif "current_minimum_width" in product_rules:

        current_min_width = product_rules["current_minimum_width"]
        current_min_height = product_rules["current_minimum_height"]

        resolution_pass = (
            width >= current_min_width and
            height >= current_min_height
        )

        if resolution_pass:

            st.success(
                f"✓ Resolution: {width} × {height} px — PASS"
            )

        else:

            st.warning(
                f"⚠ Resolution: {width} × {height} px — "
                f"Below current minimum reference."
            )


    # --------------------------------------------------------
    # FILE SIZE CHECK
    # --------------------------------------------------------

    if "maximum_file_size_mb" in product_rules:

        max_file_size = product_rules["maximum_file_size_mb"]

        if file_size_mb <= max_file_size:

            st.success(
                f"✓ File size: {file_size_mb:.2f} MB — PASS"
            )

        else:

            st.error(
                f"✕ File size: {file_size_mb:.2f} MB — "
                f"Maximum: {max_file_size} MB"
            )


    # --------------------------------------------------------
    # FORMAT CHECK
    # --------------------------------------------------------

    allowed_formats = product_rules.get(
        "allowed_formats",
        []
    )

    if image_format in allowed_formats:

        st.success(
            f"✓ Format: {image_format} — PASS"
        )

    else:

        st.error(
            f"✕ Format: {image_format} — "
            f"Allowed: {', '.join(allowed_formats)}"
        )


    # --------------------------------------------------------
    # PRODUCT COVERAGE STANDARD
    # --------------------------------------------------------

    if "recommended_product_coverage_min" in product_rules:

        min_coverage = product_rules[
            "recommended_product_coverage_min"
        ]

        max_coverage = product_rules[
            "recommended_product_coverage_max"
        ]

        st.info(
            f"ℹ Product coverage standard: "
            f"{min_coverage}% – {max_coverage}%."
        )

        st.warning(
            "⚠ Automatic product-coverage measurement will be "
            "added in the visual AI analysis stage."
        )


    elif "minimum_product_coverage" in product_rules:

        min_coverage = product_rules[
            "minimum_product_coverage"
        ]

        st.info(
            f"ℹ Amazon product coverage requirement: "
            f"minimum {min_coverage}%."
        )

        st.warning(
            "⚠ Automatic product-coverage measurement will be "
            "added in the visual AI analysis stage."
        )


    # ========================================================
    # ANALYSIS FOCUS
    # ========================================================

     # ========================================================
    # VISUAL AI ANALYSIS
    # ========================================================

    st.divider()

    st.subheader("🤖 Visual AI Analysis")

    st.write(
        "Gemini will visually inspect the uploaded image "
        "against the selected market standard."
    )

    if st.button("🔍 Analyze Image with AI"):

        with st.spinner("Gemini is analyzing the image..."):

            try:

                # Read uploaded image bytes
                image_bytes = uploaded_file.getvalue()

                # Create image input for Gemini
                image_part = types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=uploaded_file.type
                )

                # Visual analysis instructions
                visual_prompt = f"""
You are an e-commerce image quality analyst.

Analyze the uploaded image as a {analysis_type}
for the {market_standard} market.

Focus ONLY on what can be visually determined from
the image.

Evaluate:

1. Is a product clearly visible?
2. Is the product fully visible or cropped?
3. Does the product appear centered?
4. Estimate the percentage of the image occupied by
   the main product.
5. Describe the background.
6. Is there visible text?
7. Is there a visible watermark?
8. Is there a visible logo or branding?
9. Does the image look visually clean?
10. Are there obvious quality problems such as blur,
    distortion, or poor composition?

Return the findings in a simple structured format.

Use these exact headings:

Product Detected:
Product Fully Visible:
Estimated Product Coverage:
Product Position:
Background:
Text Detected:
Watermark Detected:
Logo/Branding Detected:
Visual Quality:
Overall Observation:

Do not invent information that cannot be determined
from the image.
"""

                # Send image to Gemini
                response = gemini_client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[
                        image_part,
                        visual_prompt
                    ]
                )

                # Display result
                st.success("✓ Visual AI analysis completed")

                st.subheader("📋 AI Analysis Result")

                st.markdown(response.text)

            except Exception as e:

                st.error(
                    f"AI analysis failed: {str(e)}"
                )


    if analysis_type == "Product Image":

        st.write(
            """
            **Product Image Analysis**

            The application is evaluating:

            - Image dimensions
            - File size
            - File format
            - Product coverage
            - Product visibility
            - Background
            - Product positioning
            - Image quality
            """
        )


    elif analysis_type == "Product Page Screenshot":

        st.write(
            """
            **Product Page Analysis**

            The visual AI stage will evaluate:

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

            The visual AI stage will evaluate:

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

            The visual AI stage will evaluate:

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

            The visual AI stage will evaluate:

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

            The visual AI stage will evaluate:

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

else:

    st.info(
        "👆 Select your analysis settings and upload an image to begin."
    )
