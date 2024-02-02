from json_to_df import JSON2DF

import pandas as pd 
from matplotlib import pyplot as plt

import streamlit as st 
st.set_page_config(layout="wide")

st.title("Instagram Chat Analyzer :")
st.text("get insights on your personal and group chat")

# input json file from user
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # df = pd.read_csv("./main.csv") # eventually going to remove it

    json_to_df = JSON2DF(data)

    # working on json to df converter -> on file name json_to_df.py
    df = json_to_df.converter() # this method will run and gives output in Dataframe format

    total_users = sorted(json_to_df.total_users())
    total_users.insert(0, "None")
    total_users.insert(1, "Overall")

    # ==================================================================

    user = st.sidebar.selectbox(label="Select User", options=total_users)

    if user != "None":
        col1, col2 = st.columns(spec=2)

        if user != "Overall":
            df = df[df['users'] == user]

        # Summery
        with col1:
            st.header("Message Count")
            st.text(len(df['word_count']))

            st.header("Word Count")
            st.text(sum(df['word_count']))
        with col2:
            st.header("Reel Shared")
            st.text(len(df[df['msgs'] == "reel"]))

            st.header("Media Shared")
            st.text(len(df[df['msgs'] == "media"]))

        # most active user
        if user == "Overall":
            col3, col4, col5= st.columns(spec=3)
            with col3:
                st.header("Activity bar")
                active = df['users'].value_counts()
                fig, ax = plt.subplots()
                ax.bar(active.index, height=active.values)
                plt.xticks(rotation=90)
                fig.set_size_inches(5.5, 2.5)
                st.pyplot(fig)

            with col4:
                st.header("Plot")
                fig, ax = plt.subplots()
                ax.plot(active)
                plt.xticks(rotation=90)
                fig.set_size_inches(5.5, 2.5)
                st.pyplot(fig)

            with col5:
                st.header("Active Percentage")
                st.dataframe(round((df['users'].value_counts() / df.shape[0])*100,2).reset_index().rename(columns={"count" : "percentage"}))

        # most common word used
        col5, col6 = st.columns(spec=2)
        with col5:
            common = json_to_df.most_common_words(df, 10)
            st.header("Most Common Word Used")
            st.dataframe(common)

            x = common['words']
            y = common['count']

            fig,ax = plt.subplots()
            ax.barh(x, width=y)
            fig.set_size_inches(5.5, 2.5)
            plt.xticks(rotation=90)
            st.pyplot(fig)
        
        with col6:
            pass


    if st.button("View Dataset"):
        st.dataframe(df,hide_index=True)

