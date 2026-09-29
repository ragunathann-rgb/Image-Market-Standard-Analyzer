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
# GEMINI AI CLIENT
# ============================================================

try:

    gemini_client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

except Exception:

    gemini_client = None


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
# MARKET STANDARD KEY
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
# SELECTED MARKET STANDARD
# ============================================================

st.subheader("📋 Selected Market Standard")


if analysis_type == "Product Image":

    product_rules = selected_standard["product_image"]

    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # COLUMN 1
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # COLUMN 2
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # COLUMN 3
    # --------------------------------------------------------

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
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
        "gif",
        "bmp",
        "tiff"
    ]
)


# ============================================================
# IMAGE ANALYSIS
# ============================================================

if uploaded_file:

    # ========================================================
    # OPEN IMAGE
    # ========================================================

    image = Image.open(uploaded_file)

    rgb_image = image.convert("RGB")


    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    width, height = image.size

    file_size_mb = uploaded_file.size / (1024 * 1024)

    image_format = image.format

    aspect_ratio = width / height


    # ========================================================
    # BRIGHTNESS
    # ========================================================

    grayscale = rgb_image.convert("L")

    brightness = ImageStat.Stat(
        grayscale
    ).mean[0]


    # ========================================================
    # CONTRAST
    # ========================================================

    contrast = ImageStat.Stat(
        grayscale
    ).stddev[0]


    # ========================================================
    # SHARPNESS
    # ========================================================

    edges = grayscale.filter(
        ImageFilter.FIND_EDGES
    )

    sharpness = ImageStat.Stat(
        edges
    ).mean[0]


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
    # IMAGE QUALITY METRICS
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


    # ========================================================
    # RESOLUTION CHECK
    # ========================================================

    if "minimum_width" in product_rules:

        min_width = product_rules["minimum_width"]

        min_height = product_rules["minimum_height"]

        resolution_pass = (
            width >= min_width
            and
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

        longest_side = max(
            width,
            height
        )

        shortest_side = min(
            width,
            height
        )

        min_longest = product_rules[
            "minimum_longest_side"
        ]

        min_shortest = product_rules[
            "minimum_shortest_side"
        ]


        resolution_pass = (
            longest_side >= min_longest
            and
            shortest_side >= min_shortest
        )


        if resolution_pass:

            st.success(
                f"✓ Resolution: {width} × {height} px — PASS"
            )

        else:

            st.error(
                f"✕ Resolution: {width} × {height} px — "
                f"Required longest side ≥ "
                f"{min_longest}px and shortest side ≥ "
                f"{min_shortest}px"
            )


    elif "current_minimum_width" in product_rules:

        current_min_width = product_rules[
            "current_minimum_width"
        ]

        current_min_height = product_rules[
            "current_minimum_height"
        ]


        resolution_pass = (
            width >= current_min_width
            and
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


    # ========================================================
    # FILE SIZE CHECK
    # ========================================================

    if "maximum_file_size_mb" in product_rules:

        max_file_size = product_rules[
            "maximum_file_size_mb"
        ]


        if file_size_mb <= max_file_size:

            st.success(
                f"✓ File size: {file_size_mb:.2f} MB — PASS"
            )

        else:

            st.error(
                f"✕ File size: {file_size_mb:.2f} MB — "
                f"Maximum: {max_file_size} MB"
            )


    # ========================================================
    # FORMAT CHECK
    # ========================================================

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


    # ========================================================
    # PRODUCT COVERAGE STANDARD
    # ========================================================

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


    elif "minimum_product_coverage" in product_rules:

        min_coverage = product_rules[
            "minimum_product_coverage"
        ]


        st.info(
            f"ℹ Amazon product coverage requirement: "
            f"minimum {min_coverage}%."
        )


    # ========================================================
    # VISUAL AI ANALYSIS
    # ========================================================

    st.divider()

    st.subheader("🤖 Visual AI Analysis")

    st.write(
        "Gemini will visually inspect the uploaded image "
        "against the selected market standard."
    )


    if gemini_client is None:

        st.error(
            "Gemini API key is not configured. "
            "Please check Streamlit Secrets."
        )

    else:

        analyze_button = st.button(
            "🔍 Analyze Image with AI"
        )


        if analyze_button:

            with st.spinner(
                "Gemini is analyzing the image..."
            ):

                try:

                    # ====================================================
                    # IMAGE DATA
                    # ====================================================

                    image_bytes = uploaded_file.getvalue()


                    image_part = types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=uploaded_file.type
                    )


                    # ====================================================
                    # VISUAL ANALYSIS PROMPT
                    # ====================================================

                    visual_prompt = f"""
You are an expert e-commerce product image quality analyst.

Analyze the uploaded image as a {analysis_type}
for the {market_standard} market.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations outside the JSON.

Evaluate:

1. Product detection
2. Product visibility
3. Product cropping
4. Estimated product coverage
5. Product positioning
6. Background
7. Text
8. Watermark
9. Logo or branding
10. Visual quality
11. Overall observation

Return exactly this JSON structure:

{{
    "product_detected": true,
    "product_fully_visible": true,
    "product_cropped": false,
    "estimated_product_coverage": 65,
    "product_position": "centered",
    "background": "light-colored background",
    "background_type": "non_white",
    "text_detected": false,
    "watermark_detected": false,
    "logo_or_branding_detected": false,
    "visual_quality": "good",
    "overall_observation": "The product is clearly visible."
}}

Rules:

- product_detected must be true or false.
- product_fully_visible must be true or false.
- product_cropped must be true or false.
- estimated_product_coverage must be a number from 0 to 100.
- product_position must be one of:
  centered, left, right, top, bottom, unclear.
- background_type must be one of:
  pure_white, white, light, dark, lifestyle, non_white, unclear.
- text_detected must be true or false.
- watermark_detected must be true or false.
- logo_or_branding_detected must be true or false.
- visual_quality must be one of:
  excellent, good, acceptable, poor.
- Do not invent information that cannot be visually determined.
- Estimate product coverage based on the visible main product area.
"""


                    # ====================================================
                    # SEND IMAGE TO GEMINI
                    # ====================================================

                    response = gemini_client.models.generate_content(

                        model="gemini-3.6-flash",

                        contents=[
                            image_part,
                            visual_prompt
                        ]
                    )


                    # ====================================================
                    # READ RESPONSE
                    # ====================================================

                    ai_text = response.text.strip()


                    # ====================================================
                    # REMOVE MARKDOWN CODE FENCES
                    # ====================================================

                    if ai_text.startswith("```json"):

                        ai_text = ai_text[
                            len("```json"):
                        ]

                        ai_text = ai_text.replace(
                            "```",
                            ""
                        )

                        ai_text = ai_text.strip()


                    elif ai_text.startswith("```"):

                        ai_text = ai_text[
                            len("```"):
                        ]

                        ai_text = ai_text.replace(
                            "```",
                            ""
                        )

                        ai_text = ai_text.strip()


                    # ====================================================
                    # CONVERT RESPONSE TO JSON
                    # ====================================================

                    ai_result = json.loads(
                        ai_text
                    )


                    # ====================================================
                    # SUCCESS
                    # ====================================================

                    st.success(
                        "✓ Visual AI analysis completed"
                    )


                    st.subheader(
                        "📋 AI Analysis Result"
                    )


                    # ====================================================
                    # TOP SUMMARY
                    # ====================================================

                    col1, col2, col3 = st.columns(3)


                    with col1:

                        if ai_result[
                            "product_detected"
                        ]:

                            st.success(
                                "✓ Product Detected"
                            )

                        else:

                            st.error(
                                "✕ Product Not Detected"
                            )


                    with col2:

                        if ai_result[
                            "product_fully_visible"
                        ]:

                            st.success(
                                "✓ Product Fully Visible"
                            )

                        else:

                            st.warning(
                                "⚠ Product Not Fully Visible"
                            )


                    with col3:

                        coverage = ai_result[
                            "estimated_product_coverage"
                        ]


                        st.metric(
                            "Product Coverage",
                            f"{coverage}%"
                        )


                    st.divider()


                    # ====================================================
                    # VISUAL DETAILS
                    # ====================================================

                    col1, col2 = st.columns(2)


                    with col1:

                        st.write(
                            "**Product Position**"
                        )

                        st.write(
                            ai_result[
                                "product_position"
                            ].title()
                        )


                        st.write(
                            "**Background**"
                        )

                        st.write(
                            ai_result[
                                "background"
                            ]
                        )


                        st.write(
                            "**Visual Quality**"
                        )

                        st.write(
                            ai_result[
                                "visual_quality"
                            ].title()
                        )


                    with col2:

                        st.write(
                            "**Text Detected**"
                        )


                        if ai_result[
                            "text_detected"
                        ]:

                            st.warning(
                                "⚠ Yes"
                            )

                        else:

                            st.success(
                                "✓ No"
                            )


                        st.write(
                            "**Watermark Detected**"
                        )


                        if ai_result[
                            "watermark_detected"
                        ]:

                            st.warning(
                                "⚠ Yes"
                            )

                        else:

                            st.success(
                                "✓ No"
                            )


                        st.write(
                            "**Logo / Branding Detected**"
                        )


                        if ai_result[
                            "logo_or_branding_detected"
                        ]:

                            st.warning(
                                "⚠ Yes"
                            )

                        else:

                            st.success(
                                "✓ No"
                            )


                    st.divider()


                    # ====================================================
                    # CROPPING
                    # ====================================================

                    st.write(
                        "**Product Cropped**"
                    )


                    if ai_result[
                        "product_cropped"
                    ]:

                        st.warning(
                            "⚠ Product appears to be cropped."
                        )

                    else:

                        st.success(
                            "✓ Product does not appear cropped."
                        )


                    # ====================================================
                    # OVERALL OBSERVATION
                    # ====================================================

                    st.write(
                        "**Overall Observation**"
                    )


                    st.write(
                        ai_result[
                            "overall_observation"
                        ]
                    )


                except Exception as e:

                    st.error(
                        f"AI analysis failed: {str(e)}"
                    )


    # ========================================================
    # ANALYSIS FOCUS
    # ========================================================

    st.divider()

    st.subheader("🔎 Analysis Focus")


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
- Product cropping
- Text
- Watermark
- Logo / branding
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
