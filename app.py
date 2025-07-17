import streamlit as st
import pandas as pd
import base64

# Page configuration
st.set_page_config(page_title="Civil Getaway '25", layout="centered")

# Session state setup
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "emp_id" not in st.session_state:
    st.session_state.emp_id = ""
if "emp_name" not in st.session_state:
    st.session_state.emp_name = ""
if "team" not in st.session_state:
    st.session_state.team = ""

# Function to set background GIF
def set_bg_gif(gif_path):
    with open(gif_path, "rb") as f:
        data_url = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/gif;base64,{data_url}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center top;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

# Load Excel data
@st.cache_data
def load_data():
    df = pd.read_excel("employees.xlsx", engine="openpyxl")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Search function
def show_results(emp_id):
    df["Employee_ID"] = df["Employee_ID"].astype(str)
    result = df[df["Employee_ID"] == emp_id.strip()]
    if not result.empty:
        st.session_state.emp_name = result.iloc[0]["Employee_Name"]
        st.session_state.team = result.iloc[0]["Team_Name"]
        st.session_state.show_result = True
        st.rerun()
    else:
        st.error("❌ No employee found with this ID.")

# ----------------------------
# PAGE 1 – Search Input
# ----------------------------
# PAGE 1 – Employee ID Input (Mobile Optimized)
if not st.session_state.show_result:
    set_bg_gif("page1.gif")  # Keep your background as-is

    st.markdown("""
        <style>
        header, footer { visibility: hidden; }
        .block-container {
            padding: 0rem 1rem;
        }

        .title {
            font-size: 28px;
            text-align: center;
            font-weight: bold;
            color: #FFD700;
            text-shadow: 1px 1px 2px black;
            margin-top: 10vh;
            font-family: 'Copperplate', sans-serif;
        }

        .input-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 6vh;
        }

        .stTextInput>div>input {
            text-align: center;
            font-size: 18px;
        }

        .stButton button {
            background-color: #FFA500;
            color: white;
            font-weight: bold;
            padding: 10px 24px;
            font-size: 16px;
            border-radius: 8px;
            margin-top: 20px;
        }

        @media (max-width: 600px) {
            .title { font-size: 22px; margin-top: 7vh; }
            .stTextInput>div>input { font-size: 16px; }
            .stButton button { font-size: 14px; padding: 8px 18px; }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>Employee Team Lookup</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='input-container'>", unsafe_allow_html=True)
        emp_id = st.text_input("Enter your Employee ID", key="input_emp_id")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Search"):
            if emp_id:
                df = pd.read_excel("employee_data.xlsx")
                matched_row = df[df["Employee ID"] == emp_id]

                if not matched_row.empty:
                    st.session_state.emp_name = matched_row["Employee Name"].values[0]
                    st.session_state.team = matched_row["Team Name"].values[0]
                    st.session_state.show_result = True
                    st.session_state.emp_id = emp_id
                    st.rerun()
                else:
                    st.error("Employee ID not found.")
            else:
                st.warning("Please enter your Employee ID.")

# ----------------------------
# PAGE 2 – Show Results
# ----------------------------
if st.session_state.show_result:
    set_bg_gif("page2.gif")

    # Place employee name beside "Dear"
    st.markdown(f"""
                    <style>
                    header, footer {{ visibility: hidden; }}
                    .block-container {{
                        padding: 0rem 1rem;
                        margin-top: 3vh;
                    }}
                    </style>
                """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <style>
            .emp-name {{
                position: absolute;
                top: 21px;         /* Adjust vertically */
                left: 255px;       /* Adjust right of "Dear" */
                font-size: 32px;
                font-weight: bold;
                color: pink;
                font-family: 'Brush Script MT', serif;
                text-shadow: 0 0 0.5px #ffffff, 0 0 0px #00f0ff;
            }}

            .team-name {{
                position: absolute;
                top: 250px;        /* Align with "You Belong To" */
                left: 220px;       /* Align after "You Belong To" */
                font-size: 30px;
                font-weight: 600;
                color: orange;
                width: 225px;
                text-align: center;
                font-family: 'Algerian', serif;
                text-shadow: 0 0 1px #FFD700, 0 0 2px #FFB800;
            }}
        </style>

        <div class="emp-name">{st.session_state.emp_name},</div>
        <div class="team-name">{st.session_state.team}</div>
        """,
        unsafe_allow_html=True
    )

    # Map team names to logo file paths
    team_logos = {
        "NERUPU DAA NERUNGU DAA PAAPOM": "neruppu.png",
        "GANGERS": "gangers.png",
        "PORKANDA SINGAM": "porkanda.png",
        "TIGER KA HUKUM": "tiger.png",
    }

    # Get the team name
    team_name = st.session_state.team.strip()

    # Default logo_path
    logo_path = team_logos.get(team_name)

    # Display logo if found
    def get_image_base64(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()


    def centered_logo(logo_path):
        logo_base64 = get_image_base64(logo_path)
        st.markdown(
            f"""
            <div style='display: flex; justify-content: center; align-items: center; margin-top: 385px; margin-bottom: 20px;'>
                <img src="data:image/png;base64,{logo_base64}" style="width: 170px; height: auto; border-radius: 15px;" />
            </div>
            """,
            unsafe_allow_html=True
        )


    # 🔥 Call this function where you want to display the logo
    centered_logo(logo_path)

