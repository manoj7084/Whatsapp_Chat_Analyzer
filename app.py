import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Load the custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply the custom CSS
local_css("style.css")

# st.title("Please Upload a Whatsapp Chat File")
# uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files=True)
# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     data = bytes_data.decode("utf-8")
#     # st.write("filename:", uploaded_file.name)
#     # st.write(data)
#     df = preprocessor.preprocess(data)
#     st.title("Whatsapp Data Loaded Successfully")
#     st.dataframe(df)


# Define a placeholder for the dataframe
df = None

# Title when no file is uploaded
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files=True)

# Check if files have been uploaded
if uploaded_files:
    st.session_state['uploaded_files'] = uploaded_files
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

    if df is not None:
        st.title("Whatsapp Chat File Upload Successfully")
        st.dataframe(df)
else:
    st.title("Please Upload a Whatsapp Chat File")

# Example usage of the dataframe after ensuring it is loaded
if df is not None:
    # df = df[df['user'] != 'group_notification']
    # user_list = df['user'].unique().tolist()
    #
    # user_df = pd.DataFrame(user_list, columns=['users'])
    #
    #
    # # st.header("User List:")
    # # st.dataframe(user_df)


    #fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("User Analysis", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,words,num_media_messages, url = helper.fetch_stats(selected_user,df)
        st.title("Top Statics....")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_media_messages)
        with col4:
            st.header("Total URL")
            st.title(url)
        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_time_line(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])  # x-axis is timeline['time'] and y-axis is timeline['message']
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_time_line(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        week_activity_map = helper.week_activity_map(selected_user,df)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index, busy_day.values)

            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            X, user_m_percentage = helper.most_busy_users(df)
            colm1, colm2 = st.columns(2)
            with colm1:
                fig, ax = plt.subplots()
                ax.bar(X.index, X.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with colm2:
                st.dataframe(user_m_percentage)
        # Wordcloud

        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        # Most Common Words.................
        most_common_df = helper.most_common_word(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common words ")
        st.pyplot(fig)

        # st.dataframe(most_common_df)

        emoji_df = helper.emoji_helper(selected_user, df)
        emoji_counts = emoji_df['emoji'].explode().value_counts()
        st.title("Emoji Analysis")
        st.dataframe(emoji_counts)