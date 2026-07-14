import streamlit as st
import tempfile
import os
import pandas as pd
from PIL import Image

from bioclip import TreeOfLifeClassifier, Rank


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="BioSight AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM THEME
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top right, #123d32 0%, transparent 30%),
        linear-gradient(135deg, #061a15 0%, #09271f 50%, #071914 100%);
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.hero {
    padding: 40px;
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        rgba(28, 92, 67, 0.80),
        rgba(11, 42, 34, 0.90)
    );
    border: 1px solid rgba(130, 220, 170, 0.30);
    margin-bottom: 30px;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
}

.hero-subtitle {
    font-size: 18px;
    color: #d1eadc;
    max-width: 900px;
    margin-top: 15px;
    line-height: 1.6;
}

.info-card {
    padding: 22px;
    border-radius: 18px;
    min-height: 180px;
    background: rgba(17, 54, 43, 0.75);
    border: 1px solid rgba(120, 200, 155, 0.25);
}

.prediction-card {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        rgba(22, 75, 55, 0.95),
        rgba(11, 42, 34, 0.95)
    );
    border: 1px solid rgba(125, 220, 165, 0.35);
    margin-bottom: 20px;
}


.footer {
    text-align: center;
    color: #8eb6a3;
    padding-top: 50px;
    padding-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD BIOCLIP
# =========================================================

@st.cache_resource
def load_classifier():
    return TreeOfLifeClassifier()


with st.spinner("Loading BioCLIP and the Tree of Life..."):
    classifier = load_classifier()


# =========================================================
# SAVE UPLOADED IMAGE TEMPORARILY
# =========================================================

def save_uploaded_image(uploaded_file):

    suffix = os.path.splitext(
        uploaded_file.name
    )[1]

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    temp_file.write(
        uploaded_file.getbuffer()
    )

    temp_file.close()

    return temp_file.name


# =========================================================
# RUN PREDICTION
# IMPORTANT:
# Your installed pybioclip version requires Rank.SPECIES
# as a POSITIONAL argument.
# =========================================================

def run_prediction(image_path):

    predictions = classifier.predict(
        image_path,
        Rank.SPECIES
    )

    return list(predictions)


# =========================================================
# CONVERT PREDICTION OBJECT TO DICTIONARY
# =========================================================

def prediction_to_dict(result):

    if isinstance(result, dict):
        return result

    if hasattr(result, "_asdict"):
        return result._asdict()

    try:
        return vars(result)

    except Exception:
        return {}


# =========================================================
# SAFELY GET VALUES
# =========================================================

def get_value(data, keys, default="Unknown"):

    for key in keys:

        value = data.get(key)

        if value is not None and value != "":
            return value

    return default


# =========================================================
# NORMALIZE BIOCLIP RESULT
# =========================================================

def normalize_prediction(result):

    data = prediction_to_dict(result)

    score = get_value(
        data,
        [
            "score",
            "probability",
            "confidence"
        ],
        0
    )

    try:
        score = float(score)

    except Exception:
        score = 0.0


    # Some models return 0-1.
    # Some outputs may already be percentages.
    if score <= 1:
        score_percent = score * 100

    else:
        score_percent = score


    return {

        "common_name": get_value(
            data,
            [
                "common_name",
                "common",
                "vernacular_name"
            ],
            "Common name unavailable"
        ),

        "species": get_value(
            data,
            [
                "species",
                "species_name",
                "scientific_name"
            ]
        ),

        "genus": get_value(
            data,
            ["genus"]
        ),

        "family": get_value(
            data,
            ["family"]
        ),

        "order": get_value(
            data,
            ["order"]
        ),

        "class": get_value(
            data,
            [
                "class",
                "class_name"
            ]
        ),

        "phylum": get_value(
            data,
            ["phylum"]
        ),

        "kingdom": get_value(
            data,
            ["kingdom"]
        ),

        "score": score,

        "score_percent": round(
            score_percent,
            2
        )
    }


# =========================================================
# SCORE EXPLANATION
# =========================================================

def explain_score(score):

    if score >= 80:

        return (
            "Strong AI match",
            """
            The model found a strong similarity between the
            uploaded image and this taxonomic candidate.
            Verification is still recommended for scientific use.
            """
        )

    elif score >= 50:

        return (
            "Moderate AI match",
            """
            The model found a reasonable match, but visually
            similar organisms may also be possible. Review the
            alternative predictions.
            """
        )

    else:

        return (
            "Uncertain AI match",
            """
            The model is less certain about this identification.
            Image quality, angle, lighting, species similarity,
            or limited visual evidence may affect the result.
            """
        )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🌿 BioSight AI")

    st.markdown("---")

    st.subheader("Why did we build this?")

    st.write(
        """
        Earth contains millions of species, but identifying
        organisms manually often requires specialist knowledge.

        BioSight AI explores how artificial intelligence can
        support faster biodiversity observation, education
        and environmental awareness.
        """
    )

    st.markdown("---")

    st.subheader("How it works")

    st.markdown(
        """
        **1.** Upload a biodiversity image

        **2.** BioCLIP analyses the visual features

        **3.** The image is compared against the Tree of Life

        **4.** Likely taxonomic matches are returned

        **5.** BioSight explains the prediction
        """
    )

    st.markdown("---")

    st.warning(
        """
        AI predictions are estimates and should not replace
        expert taxonomic identification.
        """
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">
<div class="hero-title">🌿 BioSight AI</div>
<div class="hero-subtitle">
AI-powered biodiversity intelligence for exploring and understanding life on Earth.
<br><br>
Upload an image of an animal, bird, insect, plant, fungus or another organism and explore its predicted taxonomic identity.
</div>
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# WHY IT MATTERS
# =========================================================

st.markdown("## Why this application matters")

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("""
    <div class="info-card">
        <h3>🔍 Faster Identification</h3>
        <p>
        AI can help researchers, students and citizens
        narrow down possible species from photographs.
        </p>
    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="info-card">
        <h3>🌍 Biodiversity Awareness</h3>
        <p>
        Understanding the organisms around us helps us
        better understand ecosystems and biodiversity.
        </p>
    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown("""
    <div class="info-card">
        <h3>📊 Scalable Monitoring</h3>
        <p>
        AI identification can support future camera-trap,
        ecological survey and biodiversity monitoring systems.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# UPLOAD
# =========================================================

st.markdown("## Analyse a biodiversity image")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# =========================================================
# PROCESS IMAGE
# =========================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    image_path = save_uploaded_image(
        uploaded_file
    )

    try:

        with st.spinner(
            "BioSight AI is searching the Tree of Life..."
        ):

            raw_predictions = run_prediction(
                image_path
            )


        # Take top 5 after prediction
        raw_predictions = raw_predictions[:5]


        predictions = [

            normalize_prediction(result)

            for result in raw_predictions

        ]


        if len(predictions) == 0:

            st.warning(
                "The AI model did not return any predictions."
            )

            st.stop()


        best = predictions[0]


        # =================================================
        # IMAGE + RESULT
        # =================================================

        image_col, result_col = st.columns(
            [1, 1],
            gap="large"
        )


        with image_col:

            st.markdown(
                "### Uploaded observation"
            )

            st.image(
                image,
                use_container_width=True
            )


        with result_col:

            st.markdown(
                "### AI biodiversity analysis"
            )


            # =============================================
            # MAIN PREDICTION CARD
            # =============================================

            st.markdown(f"""<div class="prediction-card">

<h1 style="margin-bottom:8px;">🌿 {best["common_name"]}</h1>

<h3 style="color:#b9e8cf; margin-top:0;"><i>{best["species"]}</i></h3>

<hr style="border:0;border-top:1px solid rgba(255,255,255,0.15);margin:15px 0;">

<p style="font-size:16px;"><strong>Family:</strong> {best["family"]}</p>

</div>""", unsafe_allow_html=True)


            # =============================================
            # METRICS
            # =============================================

            metric1, metric2 = st.columns(2)


            with metric1:

                st.metric(
                    "Model Match Score",
                    f"{best['score_percent']}%"
                )


            with metric2:

                st.metric(
                    "Biological Class",
                    best["class"]
                )


            # =============================================
            # SCORE INTERPRETATION
            # =============================================

            score_title, score_description = explain_score(
                best["score_percent"]
            )


            if best["score_percent"] >= 80:

                st.success(
                    f"**{score_title}**\n\n"
                    f"{score_description}"
                )


            elif best["score_percent"] >= 50:

                st.warning(
                    f"**{score_title}**\n\n"
                    f"{score_description}"
                )


            else:

                st.info(
                    f"**{score_title}**\n\n"
                    f"{score_description}"
                )


        # =================================================
        # EXPLAIN RESULT
        # =================================================

        st.markdown("---")

        st.markdown(
            "## Understanding the AI result"
        )


        st.info(
            f"""
            BioSight AI's most likely taxonomic match is
            **{best['common_name']}**
            (*{best['species']}*).

            The model match score is **{best['score_percent']}%**.

            This score represents how strongly the AI model
            matched the uploaded image with this candidate
            relative to the available taxonomic candidates.

            **It is not the same as scientific certainty.**
            """
        )


        # =================================================
        # TAXONOMY
        # =================================================

        st.markdown(
            "## Taxonomic classification"
        )


        taxonomy_data = pd.DataFrame({

            "Taxonomic Rank": [

                "Kingdom",
                "Phylum",
                "Class",
                "Order",
                "Family",
                "Genus",
                "Species"

            ],

            "AI Prediction": [

                best["kingdom"],
                best["phylum"],
                best["class"],
                best["order"],
                best["family"],
                best["genus"],
                best["species"]

            ]

        })


        st.dataframe(

            taxonomy_data,

            use_container_width=True,

            hide_index=True

        )


        # =================================================
        # EXPLAIN TAXONOMY
        # =================================================

        with st.expander(
            "What does the taxonomy mean?"
        ):

            st.markdown(
                """
                Biological taxonomy organizes life from broad
                groups to increasingly specific groups.

                **Kingdom** → Broad biological group

                **Phylum** → Major body or evolutionary group

                **Class** → More specific biological grouping

                **Order** → Related families

                **Family** → Related genera

                **Genus** → Closely related species

                **Species** → The most specific identification
                predicted by the AI
                """
            )


        # =================================================
        # ALTERNATIVE PREDICTIONS
        # =================================================

        st.markdown("---")

        st.markdown(
            "## Alternative AI matches"
        )

        st.write(
            """
            These are other taxonomic candidates considered
            by the model. Similar scores may indicate uncertainty
            between visually similar organisms.
            """
        )


        for index, prediction in enumerate(
            predictions,
            start=1
        ):

            title = (
                f"{index}. "
                f"{prediction['common_name']} "
                f"— {prediction['species']} "
                f"({prediction['score_percent']}%)"
            )


            with st.expander(title):

                st.write(
                    f"**Common Name:** "
                    f"{prediction['common_name']}"
                )

                st.write(
                    f"**Scientific Name:** "
                    f"*{prediction['species']}*"
                )

                st.write(
                    f"**Kingdom:** "
                    f"{prediction['kingdom']}"
                )

                st.write(
                    f"**Class:** "
                    f"{prediction['class']}"
                )

                st.write(
                    f"**Order:** "
                    f"{prediction['order']}"
                )

                st.write(
                    f"**Family:** "
                    f"{prediction['family']}"
                )

                st.write(
                    f"**Genus:** "
                    f"{prediction['genus']}"
                )

                st.write(
                    f"**Model Match Score:** "
                    f"{prediction['score_percent']}%"
                )


        # =================================================
        # CONSERVATION STATUS PLACEHOLDER
        # =================================================

        st.markdown("---")

        st.markdown(
            "## Conservation intelligence"
        )

        st.info(
            f"""
            **Predicted scientific name:** {best['species']}

            The next version of BioSight AI will use the predicted
            scientific name to retrieve current conservation
            information from an authoritative biodiversity data source.

            This can include:

            - Conservation category
            - Threat level
            - Population trend
            - Known threats
            - Conservation actions

            Conservation status is intentionally not hard-coded because
            biodiversity assessments can change over time.
            """
        )


        # =================================================
        # RESPONSIBLE USE
        # =================================================

        st.markdown(
            "## Important interpretation"
        )

        st.warning(
            """
            BioSight AI is an AI-assisted identification tool.

            A prediction may be affected by image quality,
            lighting, viewing angle, geographic location,
            life stage and similarities between related species.

            For scientific research, conservation decisions or
            official species records, the result should be verified
            using expert review and authoritative biodiversity data.
            """
        )


    except Exception as error:

        st.error(
            "The image could not be analysed."
        )

        st.code(
            str(error)
        )


    finally:

        if os.path.exists(
            image_path
        ):

            os.remove(
                image_path
            )


else:

    st.info(
        "Upload a biodiversity image to begin the AI analysis."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""<div class="footer">
<strong>BioSight AI</strong><br>
Biodiversity Intelligence Prototype<br><br>
Powered by BioCLIP and the Tree of Life
</div>""", unsafe_allow_html=True)