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

                # ------------------------------------------------
                # READ IMAGE
                # ------------------------------------------------

                image_bytes = uploaded_file.getvalue()

                image_part = types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=uploaded_file.type
                )


                # ------------------------------------------------
                # AI PROMPT
                # ------------------------------------------------

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

Use exactly this JSON structure:

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
"""


                # ------------------------------------------------
                # SEND IMAGE TO GEMINI
                # ------------------------------------------------

                response = gemini_client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[
                        image_part,
                        visual_prompt
                    ]
                )


                # ------------------------------------------------
                # PARSE AI RESPONSE
                # ------------------------------------------------

                ai_text = response.text.strip()


                # Remove markdown code fences if Gemini adds them
                if ai_text.startswith("```json"):

                    ai_text = ai_text.replace(
                        "```json",
                        "",
                        1
                    )

                    ai_text = ai_text.replace(
                        "```",
                        ""
                    )

                    ai_text = ai_text.strip()


                ai_result = json.loads(ai_text)


                # ------------------------------------------------
                # SUCCESS MESSAGE
                # ------------------------------------------------

                st.success(
                    "✓ Visual AI analysis completed"
                )


                st.subheader(
                    "📋 AI Analysis Result"
                )


                # ------------------------------------------------
                # TOP RESULTS
                # ------------------------------------------------

                col1, col2, col3 = st.columns(3)


                with col1:

                    if ai_result["product_detected"]:

                        st.success(
                            "✓ Product Detected"
                        )

                    else:

                        st.error(
                            "✕ Product Not Detected"
                        )


                with col2:

                    if ai_result["product_fully_visible"]:

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


                # ------------------------------------------------
                # VISUAL DETAILS
                # ------------------------------------------------

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

                    if ai_result["text_detected"]:

                        st.warning("⚠ Yes")

                    else:

                        st.success("✓ No")


                    st.write(
                        "**Watermark Detected**"
                    )

                    if ai_result[
                        "watermark_detected"
                    ]:

                        st.warning("⚠ Yes")

                    else:

                        st.success("✓ No")


                    st.write(
                        "**Logo / Branding Detected**"
                    )

                    if ai_result[
                        "logo_or_branding_detected"
                    ]:

                        st.warning("⚠ Yes")

                    else:

                        st.success("✓ No")


                st.divider()


                # ------------------------------------------------
                # OVERALL OBSERVATION
                # ------------------------------------------------

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
