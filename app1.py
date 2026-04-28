import streamlit as st
import pandas as pd

# ---------------- SESSION ----------------
if "step" not in st.session_state:
    st.session_state.step = 1

# ---------------- STEP 1 ----------------
if st.session_state.step == 1:
    st.title("Step 1: Upload CSV")

    file = st.file_uploader("Upload CSV")

    if file:
        df = pd.read_csv(file)
        st.session_state.df = df

    if "df" in st.session_state:
        st.dataframe(st.session_state.df.head())

        if st.button("Next ➡️"):
            st.session_state.step = 2

# ---------------- STEP 2 ----------------
elif st.session_state.step == 2:
    st.title("Step 2: Column Mapping")

    df = st.session_state.df
    st.dataframe(df.head())

    columns = df.columns.tolist()

    user_id = st.selectbox("Select User_ID column", columns)
    amount = st.selectbox("Select Amount column", columns)

    st.session_state.mapping = {
        "User_ID": user_id,
        "Amount": amount
    }

    col1, col2 = st.columns(2)

    if col1.button("⬅️ Back"):
        st.session_state.step = 1

    if col2.button("Next ➡️"):
        st.session_state.step = 3

# ---------------- STEP 3 ----------------
elif st.session_state.step == 3:
    st.title("Step 3: Apply Mapping")

    df = st.session_state.df.copy()
    mapping = st.session_state.mapping

    # Rename columns
    df = df.rename(columns={
        mapping["User_ID"]: "User_ID",
        mapping["Amount"]: "Amount"
    })

    st.session_state.transformed_df = df

    st.write("After Mapping 👇")
    st.dataframe(df.head())

    col1, col2 = st.columns(2)

    if col1.button("⬅️ Back"):
        st.session_state.step = 2

    if col2.button("Next ➡️"):
        st.session_state.step = 4

# ---------------- STEP 4 ----------------
elif st.session_state.step == 4:
    st.title("Step 4: Download")

    df = st.session_state.transformed_df

    st.dataframe(df.head())

    csv = df.to_csv(index=False)

    st.download_button(
        "Download CSV",
        data=csv,
        file_name="processed.csv"
    )

    if st.button("⬅️ Back"):
        st.session_state.step = 3