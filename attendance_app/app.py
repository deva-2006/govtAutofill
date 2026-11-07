import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
import random


# ============================================================
# CONFIGURATION
# ============================================================

STUDENT_FOLDER = "students"
MODEL_FOLDER = "models"
CSV_FILE = "students.csv"

YUNET_MODEL = os.path.join(
    MODEL_FOLDER,
    "face_detection_yunet_2026may.onnx"
)

SFACE_MODEL = os.path.join(
    MODEL_FOLDER,
    "face_recognition_sface_2021dec.onnx"
)

# Face recognition threshold
# SFace cosine similarity:
# higher = more similar
FACE_THRESHOLD = 0.363


# ============================================================
# 20 SEATS
# ============================================================

SEATS = [
    "M1", "M2",
    "M3", "M4",
    "M5", "M6",
    "M7", "M8",
    "M9", "M10",
    "M11", "M12",
    "M13", "M14",
    "M15", "M16",
    "M17", "M18",
    "M19", "M20"
]


# Each pair represents two students sitting together.
# Male + Female in the same pair is NOT allowed.

SEAT_PAIRS = [
    ("M1", "M2"),
    ("M3", "M4"),
    ("M5", "M6"),
    ("M7", "M8"),
    ("M9", "M10"),
    ("M11", "M12"),
    ("M13", "M14"),
    ("M15", "M16"),
    ("M17", "M18"),
    ("M19", "M20")
]


# ============================================================
# STREAMLIT PAGE
# ============================================================

st.set_page_config(
    page_title="Student Attendance Monitoring",
    page_icon="🎓",
    layout="wide"
)

st.title("Student Attendance Monitoring System")

st.caption(
    "Face Recognition • Student Identification • "
    "Gender-Based Seat Allocation"
)


# ============================================================
# SESSION STATE
# ============================================================

if "seat_allocations" not in st.session_state:
    st.session_state.seat_allocations = {}

if "last_student" not in st.session_state:
    st.session_state.last_student = None

if "last_gender" not in st.session_state:
    st.session_state.last_gender = None

if "last_seat" not in st.session_state:
    st.session_state.last_seat = None

if "last_score" not in st.session_state:
    st.session_state.last_score = None


# ============================================================
# CHECK FILES
# ============================================================

missing_files = []

if not os.path.exists(CSV_FILE):
    missing_files.append(CSV_FILE)

if not os.path.exists(YUNET_MODEL):
    missing_files.append(YUNET_MODEL)

if not os.path.exists(SFACE_MODEL):
    missing_files.append(SFACE_MODEL)

if not os.path.exists(STUDENT_FOLDER):
    missing_files.append(STUDENT_FOLDER)


if missing_files:

    st.error("❌ Required files/folders are missing:")

    for item in missing_files:
        st.write(f"- `{item}`")

    st.stop()


# ============================================================
# LOAD CSV
# ============================================================

try:

    students = pd.read_csv(CSV_FILE)

except Exception as e:

    st.error("❌ Could not read students.csv")

    st.exception(e)

    st.stop()


# Clean CSV

students["name"] = (
    students["name"]
    .astype(str)
    .str.strip()
)

students["gender"] = (
    students["gender"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# ============================================================
# FIND STUDENT IMAGE
# ============================================================

def find_student_image(name):

    extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".JPG",
        ".JPEG",
        ".PNG"
    ]

    # Exact filename first
    for ext in extensions:

        path = os.path.join(
            STUDENT_FOLDER,
            name + ext
        )

        if os.path.isfile(path):

            return path


    # Case-insensitive fallback
    try:

        files = os.listdir(STUDENT_FOLDER)

        target = name.lower()

        for filename in files:

            base, ext = os.path.splitext(filename)

            if (
                base.lower() == target
                and ext.lower() in [
                    ".jpg",
                    ".jpeg",
                    ".png"
                ]
            ):

                return os.path.join(
                    STUDENT_FOLDER,
                    filename
                )

    except Exception:
        pass


    return None


# ============================================================
# LOAD OPENCV MODELS
# ============================================================

@st.cache_resource
def load_models():

    detector = cv2.FaceDetectorYN.create(
        YUNET_MODEL,
        "",
        (320, 320),

        # Lower score threshold
        # so weaker faces can also be detected
        0.5,

        # NMS threshold
        0.3,

        # Maximum detections
        5000
    )

    recognizer = cv2.FaceRecognizerSF.create(
        SFACE_MODEL,
        ""
    )

    return detector, recognizer


try:

    detector, recognizer = load_models()

except Exception as e:

    st.error("❌ Could not load OpenCV face models.")

    st.exception(e)

    st.stop()


# ============================================================
# FACE DETECTION FUNCTION
# ============================================================

def detect_best_face(image):

    """
    Try several preprocessing methods.
    Return:
        processed_image, face
    """

    if image is None:

        return None, None


    attempts = []


    # --------------------------------------------------------
    # Attempt 1: Original image
    # --------------------------------------------------------

    attempts.append(image)


    # --------------------------------------------------------
    # Attempt 2: Resize if image is large
    # --------------------------------------------------------

    h, w = image.shape[:2]

    max_dimension = 1600

    if max(h, w) > max_dimension:

        scale = max_dimension / max(h, w)

        resized = cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA
        )

        attempts.append(resized)


    # --------------------------------------------------------
    # Attempt 3: Enlarged image
    # --------------------------------------------------------

    enlarged = cv2.resize(
        image,
        None,
        fx=1.5,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    attempts.append(enlarged)


    # --------------------------------------------------------
    # Attempt 4: Slight contrast enhancement
    # --------------------------------------------------------

    lab = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2LAB
    )

    l_channel, a_channel, b_channel = cv2.split(
        lab
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    l_channel = clahe.apply(
        l_channel
    )

    enhanced = cv2.merge(
        [l_channel, a_channel, b_channel]
    )

    enhanced = cv2.cvtColor(
        enhanced,
        cv2.COLOR_LAB2BGR
    )

    attempts.append(enhanced)


    # --------------------------------------------------------
    # Try detection
    # --------------------------------------------------------

    best_face = None
    best_image = None
    best_area = 0

    for attempt in attempts:

        h, w = attempt.shape[:2]

        detector.setInputSize(
            (w, h)
        )

        _, faces = detector.detect(
            attempt
        )

        if faces is None:

            continue

        for face in faces:

            x, y, fw, fh = face[:4]

            area = fw * fh

            if area > best_area:

                best_area = area

                best_face = face

                best_image = attempt


    return best_image, best_face


# ============================================================
# BUILD FACE DATABASE
# ============================================================

def build_face_database():

    database = []
    skipped = []

    for _, row in students.iterrows():

        name = str(row["name"]).strip()

        gender = str(row["gender"]).strip().upper()


        # ----------------------------------------------------
        # Find image
        # ----------------------------------------------------

        image_path = find_student_image(
            name
        )

        if image_path is None:

            skipped.append({
                "name": name,
                "reason": "Image not found"
            })

            continue


        # ----------------------------------------------------
        # Read image
        # ----------------------------------------------------

        image = cv2.imread(
            image_path
        )

        if image is None:

            skipped.append({
                "name": name,
                "reason": "Image could not be read"
            })

            continue


        # ----------------------------------------------------
        # Detect face
        # ----------------------------------------------------

        processed_image, face = detect_best_face(
            image
        )

        if face is None:

            skipped.append({
                "name": name,
                "reason": "Face not detected"
            })

            continue


        try:

            # ------------------------------------------------
            # Align face
            # ------------------------------------------------

            aligned_face = recognizer.alignCrop(
                processed_image,
                face
            )


            # ------------------------------------------------
            # Generate face feature
            # ------------------------------------------------

            feature = recognizer.feature(
                aligned_face
            )


            database.append({
                "name": name,
                "gender": gender,
                "feature": feature,
                "image": image_path
            })


        except Exception as e:

            skipped.append({
                "name": name,
                "reason": f"Feature error: {str(e)}"
            })


    return database, skipped


# ============================================================
# BUILD DATABASE
# ============================================================

with st.spinner(
    "🔄 Building student face database..."
):

    face_database, skipped = build_face_database()


# ============================================================
# DATABASE STATUS
# ============================================================

st.divider()

st.subheader("📊 Student Database")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Students in CSV",
        len(students)
    )

with col2:

    st.metric(
        "Faces Loaded",
        len(face_database)
    )

with col3:

    st.metric(
        "Seats",
        20
    )


# ============================================================
# SHOW DATABASE DETAILS
# ============================================================

with st.expander(
    "👥 View loaded students"
):

    for student in face_database:

        st.write(
            f"✅ {student['name']} "
            f"— {student['gender']}"
        )


# ============================================================
# SHOW SKIPPED STUDENTS
# ============================================================

if skipped:

    with st.expander(
        f"⚠️ {len(skipped)} students need attention"
    ):

        for item in skipped:

            st.warning(
                f"{item['name']} — "
                f"{item['reason']}"
            )


if len(face_database) == 0:

    st.error(
        "❌ No faces were loaded from the student database."
    )

    st.stop()


# ============================================================
# SEAT HELPER FUNCTIONS
# ============================================================

def get_other_seat(seat):

    for seat_a, seat_b in SEAT_PAIRS:

        if seat == seat_a:

            return seat_b

        if seat == seat_b:

            return seat_a

    return None


def get_student_on_seat(seat):

    for student, allocated_seat in (
        st.session_state.seat_allocations.items()
    ):

        if allocated_seat == seat:

            return student

    return None


def get_gender(student_name):

    matches = students[
        students["name"] == student_name
    ]

    if len(matches) == 0:

        return None

    return str(
        matches.iloc[0]["gender"]
    ).upper()


def is_seat_valid(seat, gender):

    # --------------------------------------------------------
    # Seat must be empty
    # --------------------------------------------------------

    if seat in (
        st.session_state
        .seat_allocations
        .values()
    ):

        return False


    # --------------------------------------------------------
    # Find neighboring seat
    # --------------------------------------------------------

    other_seat = get_other_seat(
        seat
    )

    if other_seat is None:

        return True


    other_student = get_student_on_seat(
        other_seat
    )

    # Empty neighboring seat
    if other_student is None:

        return True


    # --------------------------------------------------------
    # Check gender
    # --------------------------------------------------------

    other_gender = get_gender(
        other_student
    )

    if other_gender is None:

        return False


    # Male + Female = NOT ALLOWED
    if other_gender != gender:

        return False


    return True


# ============================================================
# ALLOCATE SEAT
# ============================================================

def allocate_seat(student_name, gender):

    # --------------------------------------------------------
    # Already allocated?
    # --------------------------------------------------------

    if student_name in (
        st.session_state.seat_allocations
    ):

        return (
            st.session_state
            .seat_allocations[student_name]
        )


    # --------------------------------------------------------
    # Find valid seats
    # --------------------------------------------------------

    valid_seats = []

    for seat in SEATS:

        if is_seat_valid(
            seat,
            gender
        ):

            valid_seats.append(
                seat
            )


    # --------------------------------------------------------
    # No seat
    # --------------------------------------------------------

    if not valid_seats:

        return None


    # --------------------------------------------------------
    # Random selection
    # --------------------------------------------------------

    selected_seat = random.choice(
        valid_seats
    )


    # --------------------------------------------------------
    # Save allocation
    # --------------------------------------------------------

    st.session_state.seat_allocations[
        student_name
    ] = selected_seat


    return selected_seat


# ============================================================
# CAMERA SECTION
# ============================================================

st.divider()

camera_col, result_col = st.columns(
    [1.5, 1]
)


# ============================================================
# CAMERA
# ============================================================

with camera_col:

    st.subheader(
        "📷 Entrance Camera"
    )

    camera_image = st.camera_input(
        "Scan Student"
    )


# ============================================================
# RECOGNITION
# ============================================================

if camera_image is not None:

    # --------------------------------------------------------
    # Convert camera image
    # --------------------------------------------------------

    image_bytes = camera_image.getvalue()

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    frame = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )


    # --------------------------------------------------------
    # Detect face
    # --------------------------------------------------------

    processed_frame, face = detect_best_face(
        frame
    )


    with result_col:

        if face is None:

            st.error(
                "❌ No face detected."
            )

            st.info(
                "Try facing the camera directly "
                "and use better lighting."
            )


        else:

            try:

                # ------------------------------------------------
                # Align live face
                # ------------------------------------------------

                aligned_face = recognizer.alignCrop(
                    processed_frame,
                    face
                )


                # ------------------------------------------------
                # Feature
                # ------------------------------------------------

                live_feature = recognizer.feature(
                    aligned_face
                )


                # ------------------------------------------------
                # Compare against database
                # ------------------------------------------------

                best_student = None

                best_score = -1


                for student in face_database:

                    score = recognizer.match(
                        live_feature,
                        student["feature"],
                        cv2.FaceRecognizerSF_FR_COSINE
                    )


                    if score > best_score:

                        best_score = score

                        best_student = student


                # ------------------------------------------------
                # Recognition result
                # ------------------------------------------------

                if (
                    best_student is not None
                    and best_score >= FACE_THRESHOLD
                ):

                    student_name = (
                        best_student["name"]
                    )

                    gender = (
                        best_student["gender"]
                    )


                    # --------------------------------------------
                    # Allocate seat
                    # --------------------------------------------

                    seat = allocate_seat(
                        student_name,
                        gender
                    )


                    # --------------------------------------------
                    # Save latest result
                    # --------------------------------------------

                    st.session_state.last_student = (
                        student_name
                    )

                    st.session_state.last_gender = (
                        gender
                    )

                    st.session_state.last_seat = (
                        seat
                    )

                    st.session_state.last_score = (
                        best_score
                    )


                    # --------------------------------------------
                    # Display student
                    # --------------------------------------------

                    st.success(
                        "✅ STUDENT RECOGNIZED"
                    )

                    st.markdown(
                        f"## 👤 {student_name}"
                    )

                    st.write(
                        f"**Gender:** {gender}"
                    )

                    st.write(
                        f"**Similarity:** "
                        f"{best_score:.4f}"
                    )


                    # --------------------------------------------
                    # Seat result
                    # --------------------------------------------

                    if seat is not None:

                        st.success(
                            f"🪑 **{seat}** allocated "
                            f"to **{student_name}**"
                        )

                        st.markdown(
                            f"### 🎫 Your Seat: **{seat}**"
                        )

                    else:

                        st.error(
                            "❌ No valid seat available."
                        )

                        st.info(
                            "All remaining seats would "
                            "violate the gender seating rule."
                        )


                else:

                    st.error(
                        "❌ UNKNOWN STUDENT"
                    )

                    if best_student is not None:

                        st.write(
                            f"Closest match: "
                            f"{best_student['name']}"
                        )

                        st.write(
                            f"Similarity: "
                            f"{best_score:.4f}"
                        )

                    st.info(
                        "The face did not reach "
                        "the recognition threshold."
                    )


            except Exception as e:

                st.error(
                    "❌ Error during face recognition."
                )

                st.exception(e)


# ============================================================
# CURRENT ALLOCATIONS
# ============================================================

st.divider()

st.subheader(
    "🎫 Current Seat Allocations"
)


if len(
    st.session_state.seat_allocations
) == 0:

    st.info(
        "No seats allocated yet."
    )

else:

    allocation_data = []


    for student, seat in (
        st.session_state
        .seat_allocations
        .items()
    ):

        gender = get_gender(
            student
        )

        allocation_data.append({
            "Student": student,
            "Gender": gender,
            "Seat": seat
        })


    allocation_df = pd.DataFrame(
        allocation_data
    )


    st.dataframe(
        allocation_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SEAT MAP
# ============================================================

st.divider()

st.subheader(
    "🪑 Live Seat Map"
)

st.caption(
    "🟢 Available    🔴 Occupied"
)


for seat_a, seat_b in SEAT_PAIRS:

    col1, col2 = st.columns(2)


    # ========================================================
    # SEAT A
    # ========================================================

    student_a = get_student_on_seat(
        seat_a
    )


    with col1:

        if student_a:

            gender_a = get_gender(
                student_a
            )

            st.error(
                f"🔴 **{seat_a}**\n\n"
                f"👤 {student_a}\n\n"
                f"Gender: {gender_a}"
            )

        else:

            st.success(
                f"🟢 **{seat_a}**\n\n"
                "Available"
            )


    # ========================================================
    # SEAT B
    # ========================================================

    student_b = get_student_on_seat(
        seat_b
    )


    with col2:

        if student_b:

            gender_b = get_gender(
                student_b
            )

            st.error(
                f"🔴 **{seat_b}**\n\n"
                f"👤 {student_b}\n\n"
                f"Gender: {gender_b}"
            )

        else:

            st.success(
                f"🟢 **{seat_b}**\n\n"
                "Available"
            )


# ============================================================
# RESET BUTTON
# ============================================================

st.divider()

if st.button(
    "🔄 Reset All Seat Allocations",
    type="primary"
):

    st.session_state.seat_allocations = {}

    st.session_state.last_student = None

    st.session_state.last_gender = None

    st.session_state.last_seat = None

    st.session_state.last_score = None

    st.rerun()