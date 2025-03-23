import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import time
import plotly.express as px

# set session
if "gaming_button" not in st.session_state:
    st.session_state.gaming_button = False
if "movies_button" not in st.session_state:
    st.session_state.movies_button = False
if "music_button" not in st.session_state:
    st.session_state.music_button = False
if 'load_app' not in st.session_state:
    st.session_state.load_app = False
def reset_all_tabs():
    st.session_state.gaming_button = False
    st.session_state.movies_button = False
    st.session_state.music_button = False



# set page
st.set_page_config(page_title="YouTube Dashboard", page_icon="🎬", layout="wide")
# set tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📑 Introduction", "🎮 Gaming", "📽️ Movies", "🎵 Music", "🔏 Improvement"])



#################################################  Sidebar  ###################################################
# read data
df_gaming = pd.read_csv("OneDrive/桌面/python/streamlit_project/pages/data/gaming.csv")
df_movies = pd.read_csv("OneDrive/桌面/python/streamlit_project/pages/data/movies.csv")
df_music = pd.read_csv("OneDrive/桌面/python/streamlit_project/pages/data/music.csv")




















#################################################  Intro  ###################################################
with tab1:
    # Application introduction
    st.title("🎬 YouTube Data Analysis Dashboard")
    st.write("""
    Welcome to the **YouTube Data Analysis App**!  
    This application provides insights into YouTube videos across different categories, helping users understand trends, engagement metrics, and popular content.
    """)

    # Dataset overview
    st.markdown("---")
    st.header("Dataset Explanation")
    st.write("""
    The dataset used in this analysis comes from YouTube and contains key attributes such as:
    - **title:** title of the video
    - **description:** description of the vide
    - **publishedDate:** the date when the video is published 
    - **channelName:** the channel that published the video
    - **views:** the number of views
    - **duration:** the length of the video (seconds)
    - **isShort:** if the video is categorized as shorts
    """)

    st.markdown("---")
    st.header("Dataset Statistics")   
    col1, col2, col3 = st.columns(3)
    with col1:
        # Dataset statistics
        st.write(df_gaming.describe())
        # Dataset size
        st.write(f"🔹 Total Videos: {df_gaming.shape[0]}")
        st.write(f"🔹 Total Columns: {df_gaming.shape[1]}")
    with col2:
        # Dataset statistics
        st.write(df_movies.describe())

        # Dataset size
        st.write(f"🔹 Total Videos: {df_movies.shape[0]}")
        st.write(f"🔹 Total Columns: {df_movies.shape[1]}")
    with col3:
        # Dataset statistics
        st.write(df_music.describe())

        # Dataset size
        st.write(f"🔹 Total Videos: {df_music.shape[0]}")
        st.write(f"🔹 Total Columns: {df_music.shape[1]}")


    # Preview data
    st.markdown("---")
    st.header("Dataset Preview") 
    st.write("Gaming Dataset")
    st.dataframe(df_gaming.head())

    st.write("Movie Dataset")
    st.dataframe(df_movies.head())

    st.write("Music Dataset")
    st.dataframe(df_music.head())



















#################################################  Gaming  ###################################################
with tab2:
    st.session_state.active_tab = "gaming"

    # header
    st.header("Trend Overview")

    # publishedDate to date
    df_gaming["publishedDate"] = pd.to_datetime(df_gaming["publishedDate"]).dt.date

    # card
    col1, col2, col3 = st.columns(3)
    with col1:
        ttl_video = df_gaming["title"].count()
        st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}", delta="+5%")
    with col2:
        ttl_duration = df_gaming["duration"].sum()
        st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}", delta="-1%")
    with col3: 
        ttl_view = df_gaming["views"].sum()
        st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}", delta="-1%")


    # line: avg view vs. date
    df_gaming_1 = df_gaming.groupby("publishedDate")["views"].mean().reset_index()
    overall_avg = df_gaming["views"].mean()
    g1 = px.line(df_gaming_1,
                x="publishedDate",
                y="views", 
                title="Average Views")
    # avg line
    g1.add_hline(y=overall_avg, 
                line_color="#ec5353",
                line_dash="dash",
                annotation_text=f"Overall Mean: {overall_avg:.2f}",
                annotation_position="top right")
    st.plotly_chart(g1, use_container_width=True)


    # subplots
    col1, col2 = st.columns(2)

    # small plot left
    with col1: 
        st.subheader("📊 Top Views Channel")    
        # slidebar
        df_gaming_2 = df_gaming.groupby("channelName")["views"].sum().reset_index()
        df_gaming_2 = df_gaming_2.sort_values("views", ascending=False)

        max_channels_views_gaming = min(len(df_gaming_2), 20)
        num_channels_views_gaming = st.slider("Number of Gaming Channel_views",
                                                min_value = 1,
                                                max_value = max_channels_views_gaming,
                                                value = 5, 
                                                key = "slider_gaming_1")
        top_channelview = df_gaming_2.head(num_channels_views_gaming)

        # g2
        g2 = px.bar(top_channelview, x = "views", y = "channelName", orientation = "h",
                labels = {"views": "Total Views", "channelName": "Channel Name"},
                color="channelName",
                color_discrete_sequence = px.colors.qualitative.Pastel)
        g2.update_layout(showlegend=False)
        st.plotly_chart(g2, use_container_width=True)


    with col2:
        st.subheader("📊 Top Video Published Channel")
        # slidebar
        df_gaming_3 = df_gaming["channelName"].value_counts().reset_index()
        df_gaming_3 = df_gaming_3.sort_values("count", ascending=False)
        df_gaming_3 = df_gaming_3.rename(columns={"count":"Num of Video"})

        max_channels_count_gaming = min(len(df_gaming_3), 20)
        num_channels_count_gaming = st.slider("Number of Gaming Channel_count",
                                              min_value = 1,
                                              max_value = max_channels_count_gaming,
                                              value = 5, 
                                              key = "slider_gaming_2")
        top_channels = df_gaming_3.head(num_channels_count_gaming)

        # g3
        g3 = px.bar(top_channels, x = "Num of Video", y = "channelName", orientation = "h",
                labels = {"Num of Video": "Count", "channelName": "Channel Name"},
                color="channelName",
                color_discrete_sequence = px.colors.qualitative.Pastel)
        g3.update_layout(showlegend=False)
        st.plotly_chart(g3, use_container_width = True) 


    #######################################  Gaming Button  #######################################


    # button 
    #def click_button_gaming():
    #    st.session_state.my_button = True
    # button for detailed nalysis
    #st.button('Read More', on_click=click_button_gaming, key="button_gaming")

    if st.button("Detailed Analysis - Gaming", key="gaming_analysis"):
        reset_all_tabs()
        st.session_state.gaming_button = True

    if st.session_state.gaming_button:
        st.header("Channel Analysis")
        # select date
        start_date = df_gaming["publishedDate"].min()
        end_date = df_gaming["publishedDate"].max()
        options_date = st.sidebar.date_input("Publish Date",
                            (start_date, end_date),
                            start_date, end_date,
                            key = "gaming_date")
        # select channel
        df_gaming_uni_channel = df_gaming.drop_duplicates("channelName")
        channel_option = df_gaming_uni_channel.sort_values("channelName", ascending=True)["channelName"]
        options_channel = st.sidebar.selectbox("Channel Name", channel_option)

        # views & duration
        with st.sidebar.expander("More Filtering", expanded=False):
            min_views = int(df_gaming["views"].min())
            max_views = int(df_gaming["views"].max())
            min_views_formatted = f"{min_views:,}"
            max_views_formatted = f"{max_views:,}"
            min_views = st.number_input("Min Views", min_value=int(min_views), value=int(min_views))
            max_views = st.number_input("Max Views", max_value=int(max_views), value=int(max_views))

            min_duration = df_gaming["duration"].min()
            max_duration = df_gaming["duration"].max()
            min_duration = st.number_input("Min Duration (seconds)", min_value=int(min_duration), value=int(min_duration))
            max_duration = st.number_input("Max Duration (seconds)", max_value=int(max_duration), value=int(max_duration))

        
        # detail card
        col1, col2, col3 = st.columns(3)
        mask = df_gaming["publishedDate"].between(options_date[0], options_date[1]) &\
               df_gaming["channelName"].isin([options_channel])
        df_filtered_0 = df_gaming[mask]

        with col1:
            ttl_video = df_filtered_0["title"].count()
            st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}")
        with col2:
            ttl_duration = df_filtered_0["duration"].sum()
            st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}")
        with col3: 
            ttl_view = df_filtered_0["views"].sum()
            st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}")



        # plot1: top view per day
        if options_date and options_channel:
            mask = df_gaming["publishedDate"].between(options_date[0], options_date[1]) &\
                    df_gaming["channelName"].isin([options_channel])
            df_filtered_1 = df_gaming[mask]

            df_gaming_1 = df_filtered_1.groupby(["publishedDate", "channelName"])["views"].mean().reset_index()
            g4 = px.line(df_gaming_1,
                        x="publishedDate",
                        y="views")
            g4.add_hline(y=overall_avg, 
                         line_color="#ec5353",
                         line_dash="dash",
                         annotation_text=f"Overall Mean: {overall_avg:.2f}",
                         annotation_position="top right")
            st.plotly_chart(g4, use_container_width=True)
                
        if options_date and not options_channel:
            mask = df_gaming["publishedDate"].between(options_date[0], options_date[1])
            df_filtered_1 = df_gaming[mask]

            df_gaming_1 = df_filtered_1.groupby(["publishedDate"])["views"].mean().reset_index()
            g4 = px.line(df_gaming_1,
                        x="publishedDate",
                            y="views")
            g4.add_hline(y=overall_avg, 
                            line_color="#ec5353",
                            line_dash="dash",
                            annotation_text=f"Overall Mean: {overall_avg:.2f}",
                            annotation_position="top right")
            st.plotly_chart(g4, use_container_width=True)

    # two small graphs
    if st.session_state.gaming_button:
        col1, col2 = st.columns([3, 2])
        # top 10 video per channel
        with col1:
            mask = df_gaming["channelName"].isin([options_channel])
            df_filtered_2 = df_gaming[mask]
            top_videos = df_filtered_2.sort_values("views", ascending=False).head(10)
            g5 = px.bar(top_videos, x="views", y="title",
                        title="🔥 Top 10 Videos by View")
            st.plotly_chart(g5, use_container_width=True)
        
        with col2:
            mask = df_gaming["channelName"].isin([options_channel])
            df_filtered_3 = df_gaming[mask]
            g6 = px.scatter(df_filtered_3, x="duration", y="views",
                            title="⏳ Duration vs. Views",
                            size="views")
            st.plotly_chart(g6, use_container_width=True)

    # table
    if st.session_state.gaming_button:
        mask = df_gaming["channelName"].isin([options_channel])
        df_filtered_4 = df_gaming[mask].drop(columns=["channelName"])

        st.subheader('Gaming Dataset')
        st.dataframe(df_filtered_4)



















#################################################  Movies  ###################################################
with tab3:
    st.session_state.active_tab = "movies"
    
    # header
    st.header("Trend Overview")

    # publishedDate to date
    df_movies["publishedDate"] = pd.to_datetime(df_gaming["publishedDate"]).dt.date


    # card
    col1, col2, col3 = st.columns(3)
    with col1:
        ttl_video = df_movies["title"].count()
        st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}", delta="+5%")
    with col2:
        ttl_duration = df_movies["duration"].sum()
        st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}", delta="-1%")
    with col3: 
        ttl_view = df_movies["views"].sum()
        st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}", delta="-1%")


    # line: avg view vs. date
    df_movies_1 = df_movies.groupby("publishedDate")["views"].mean().reset_index()
    overall_avg = df_movies["views"].mean()
    g1 = px.line(df_movies_1,
                x="publishedDate",
                y="views", 
                title="Average Views")
    # avg line
    g1.add_hline(y=overall_avg, 
                line_color="#ec5353",
                line_dash="dash",
                annotation_text=f"Overall Mean: {overall_avg:.2f}",
                annotation_position="top right")
    st.plotly_chart(g1, use_container_width=True)


    # subplots
    col1, col2 = st.columns(2)
    with col1: 
        st.subheader("📊 Top Views Channel") 
        # slidebar
        df_movies_2 = df_movies.groupby("channelName")["views"].sum().reset_index()
        df_movies_2 = df_movies_2.sort_values("views", ascending=False)

        max_channels_views_gaming = min(len(df_movies_2), 20)
        num_channels_views_gaming = st.slider("Number of Gaming Channel_views",
                                                min_value = 1,
                                                max_value = max_channels_views_gaming,
                                                value = 5, 
                                                key = "slider_movies_1")
        top_channelview = df_movies_2.head(num_channels_views_gaming)   

        # g5
        g2 = px.bar(top_channelview, x = "views", y = "channelName", orientation = "h",
                labels = {"views": "Total Views", "channelName": "Channel Name"},
                color="channelName",
                color_discrete_sequence = px.colors.qualitative.Pastel)
        g2.update_layout(showlegend=False)
        st.plotly_chart(g2, use_container_width=True)

    with col2: 
        st.subheader("📊 Top Video Published Channel")      
        # slidebar
        df_movies_3 = df_movies["channelName"].value_counts().reset_index()
        df_movies_3 = df_movies_3.sort_values("count", ascending=False)
        df_movies_3 = df_movies_3.rename(columns={"count":"Num of Video"})

        max_channels_count_gaming = min(len(df_movies_3), 20)
        num_channels_count_gaming = st.slider("Number of Gaming Channel_count",
                                              min_value = 1,
                                              max_value = max_channels_count_gaming,
                                              value = 5, 
                                              key = "slider_movies_2")
        top_channels = df_movies_3.head(num_channels_count_gaming)

        # g3
        g3 = px.bar(top_channels, x = "Num of Video", y = "channelName", orientation = "h",
                labels = {"Num of Video": "Count", "channelName": "Channel Name"},
                color="channelName",
                color_discrete_sequence = px.colors.qualitative.Pastel)
        g3.update_layout(showlegend=False)
        st.plotly_chart(g3, use_container_width = True) 

    #######################################  Movies Button  #######################################


    # button 
    #def click_button_movies():
    #    st.session_state.movies_button = True
    # button for detailed nalysis
    #st.button('Read More', on_click=click_button_movies, key="button_movies")

    if st.button("Detailed Analysis - Movies", key="movies_analysis"):
        reset_all_tabs()
        st.session_state.movies_button = True


    if st.session_state.movies_button:
        st.header("Channel Analysis")
        # select date
        start_date = df_movies["publishedDate"].min()
        end_date = df_movies["publishedDate"].max()
        options_date = st.sidebar.date_input("Publish Date",
                            (start_date, end_date),
                            start_date, end_date,
                            key = "movies_date")
        
        # select channel
        df_movies_uni_channel = df_movies.drop_duplicates("channelName")
        channel_option = df_movies_uni_channel.sort_values("channelName", ascending=True)["channelName"]
        options_channel = st.sidebar.selectbox("Movie Channel", channel_option)

        with st.sidebar.expander("More Filtering", expanded=False):
            min_views = int(df_movies["views"].min())
            max_views = int(df_movies["views"].max())
            min_views_formatted = f"{min_views:,}"
            max_views_formatted = f"{max_views:,}"
            min_views = st.number_input("Min Views", min_value=int(min_views), value=int(min_views))
            max_views = st.number_input("Max Views", max_value=int(max_views), value=int(max_views))

            min_duration = df_movies["duration"].min()
            max_duration = df_movies["duration"].max()
            min_duration = st.number_input("Min Duration (seconds)", min_value=int(min_duration), value=int(min_duration))
            max_duration = st.number_input("Max Duration (seconds)", max_value=int(max_duration), value=int(max_duration))

        # detail card
        col1, col2, col3 = st.columns(3)
        mask = df_movies["publishedDate"].between(options_date[0], options_date[1]) &\
               df_movies["channelName"].isin([options_channel])
        df_filtered_0 = df_movies[mask]

        with col1:
            ttl_video = df_filtered_0["title"].count()
            st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}")
        with col2:
            ttl_duration = df_filtered_0["duration"].sum()
            st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}")
        with col3: 
            ttl_view = df_filtered_0["views"].sum()
            st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}")

        # plot1: top view per day
        if options_date and options_channel:
            mask = df_movies["publishedDate"].between(options_date[0], options_date[1]) &\
                    df_movies["channelName"].isin([options_channel])
            df_filtered_1 = df_movies[mask]

            df_movies_1 = df_filtered_1.groupby(["publishedDate", "channelName"])["views"].mean().reset_index()
            g4 = px.line(df_movies_1,
                        x="publishedDate",
                        y="views")
            g4.add_hline(y=overall_avg, 
                         line_color="#ec5353",
                         line_dash="dash",
                         annotation_text=f"Overall Mean: {overall_avg:.2f}",
                         annotation_position="top right")
            st.plotly_chart(g4, use_container_width=True)
                
        if options_date and not options_channel:
            mask = df_movies["publishedDate"].between(options_date[0], options_date[1])
            df_filtered_1 = df_movies[mask]

            df_movies_1 = df_filtered_1.groupby(["publishedDate"])["views"].mean().reset_index()
            g4 = px.line(df_movies_1,
                        x="publishedDate",
                            y="views")
            g4.add_hline(y=overall_avg, 
                            line_color="#ec5353",
                            line_dash="dash",
                            annotation_text=f"Overall Mean: {overall_avg:.2f}",
                            annotation_position="top right")
            st.plotly_chart(g4, use_container_width=True)

    # two small graphs
    if st.session_state.movies_button:
        col1, col2 = st.columns([3, 2])
        # top 10 video per channel
        with col1:
            mask = df_movies["channelName"].isin([options_channel])
            df_filtered_2 = df_movies[mask]
            top_videos = df_filtered_2.sort_values("views", ascending=False).head(10)
            g5 = px.bar(top_videos, x="views", y="title",
                        title="🔥 Top 10 Videos by View")
            g5.update_layout(showlegend=False)
            st.plotly_chart(g5, use_container_width=True)
        
        with col2:
            mask = df_movies["channelName"].isin([options_channel])
            df_filtered_3 = df_movies[mask]
            g6 = px.scatter(df_filtered_3, x="duration", y="views",
                            title="⏳ Duration vs. Views",
                            size="views")
            g6.update_layout(showlegend=False)
            st.plotly_chart(g6, use_container_width=True)

    # table
    if st.session_state.movies_button:
        mask = df_movies["channelName"].isin([options_channel])
        df_filtered_4 = df_movies[mask].drop(columns=["channelName"])

        st.subheader('Movie Dataset')
        st.dataframe(df_filtered_4)




















#################################################  Music  ###################################################
with tab4:
    st.session_state.active_tab = "music"

    # header
    st.header("Trend Overview")

    # publishedDate to date
    df_music["publishedDate"] = pd.to_datetime(df_gaming["publishedDate"]).dt.date


    # card
    col1, col2, col3 = st.columns(3)
    with col1:
        ttl_video = df_music["title"].count()
        st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}", delta="+5%")
    with col2:
        ttl_duration = df_music["duration"].sum()
        st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}", delta="-1%")
    with col3: 
        ttl_view = df_music["views"].sum()
        st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}", delta="-1%")


    # line: avg view vs. date
    df_music_1 = df_music.groupby("publishedDate")["views"].mean().reset_index()
    overall_avg = df_music["views"].mean()
    g1 = px.line(df_music_1,
                x="publishedDate",
                y="views", 
                title="Average Views")
    # avg line
    g1.add_hline(y=overall_avg, 
                line_color="#ec5353", 
                line_dash="dash",
                annotation_text=f"Overall Mean: {overall_avg:.2f}",
                annotation_position="top right")
    st.plotly_chart(g1, use_container_width=True)


    # subplots
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1: 
        st.subheader("📊 Top Views Channel")  
        # slidebar
        df_music_2 = df_music.groupby("channelName")["views"].sum().reset_index()
        df_music_2 = df_music_2.sort_values("views", ascending=False)

        max_channels_views_gaming = min(len(df_music_2), 20)
        num_channels_views_gaming = st.slider("Number of Gaming Channel_views",
                                                min_value = 1,
                                                max_value = max_channels_views_gaming,
                                                value = 5, 
                                                key = "slider_music_1")
        top_channelview = df_music_2.head(num_channels_views_gaming)  

        # g5
        g5 = px.bar(top_channelview, x = "views", y = "channelName", orientation = "h",
                labels = {"views": "Total Views", "channelName": "Channel Name"},
                color="channelName",
                color_discrete_sequence = px.colors.qualitative.Pastel)
        g5.update_layout(showlegend=False)
        st.plotly_chart(g5, use_container_width=True)

    with col2:    
        st.subheader("📊 Top Video Published Channel")   
        # slidebar
        df_music_3 = df_music["channelName"].value_counts().reset_index()
        df_music_3 = df_music_3.sort_values("count", ascending=False)
        df_music_3 = df_music_3.rename(columns={"count":"Num of Video"})

        max_channels_count_gaming = min(len(df_music_3), 20)
        num_channels_count_gaming = st.slider("Number of Gaming Channel_count",
                                              min_value = 1,
                                              max_value = max_channels_count_gaming,
                                              value = 5, 
                                              key = "slider_music_2")
        top_channels = df_music_3.head(num_channels_count_gaming)

        # g6
        g6 = px.bar(top_channels, x = "Num of Video", y = "channelName", orientation = "h",
                labels = {"Num of Video": "Count", "channelName": "Channel Name"},
                color="channelName",
                color_discrete_sequence = px.colors.qualitative.Pastel)
        g6.update_layout(showlegend=False)
        st.plotly_chart(g6, use_container_width = True) 



    #######################################  Music Button  #######################################

    

    # button
    #def click_button_music():
    #    st.session_state.my_button = True
    # button for detailed nalysis
    #st.button("Read More", on_click=click_button_music, key="button_music")

    if st.button("Detailed Analysis - Music", key="music_analysis"):
        reset_all_tabs()
        st.session_state.music_button = True

    if st.session_state.music_button:
        st.header("Channel Analysis")
        # select date
        start_date = df_music["publishedDate"].min()
        end_date = df_music["publishedDate"].max()
        options_date = st.sidebar.date_input("Publish Date",
                            (start_date, end_date),
                            start_date, end_date,
                            key = "music_date")
        
        # select channel
        df_music_uni_channel = df_music.drop_duplicates("channelName")
        channel_option = df_music_uni_channel.sort_values("channelName", ascending=True)["channelName"]
        options_channel = st.sidebar.selectbox("Music Channel", channel_option)

        with st.sidebar.expander("More Filtering", expanded=False):
            min_views = int(df_music["views"].min())
            max_views = int(df_music["views"].max())
            min_views_formatted = f"{min_views:,}"
            max_views_formatted = f"{max_views:,}"
            min_views = st.number_input("Min Views", min_value=int(min_views), value=int(min_views))
            max_views = st.number_input("Max Views", max_value=int(max_views), value=int(max_views))

            min_duration = df_music["duration"].min()
            max_duration = df_music["duration"].max()
            min_duration = st.number_input("Min Duration (seconds)", min_value=int(min_duration), value=int(min_duration))
            max_duration = st.number_input("Max Duration (seconds)", max_value=int(max_duration), value=int(max_duration))

        # detail card
        col1, col2, col3 = st.columns(3)
        mask = df_music["publishedDate"].between(options_date[0], options_date[1]) &\
               df_music["channelName"].isin([options_channel])
        df_filtered_0 = df_movies[mask]

        with col1:
            ttl_video = df_filtered_0["title"].count()
            st.metric(label="📹 Total Video Published", value=f"{ttl_video:,}")
        with col2:
            ttl_duration = df_filtered_0["duration"].sum()
            st.metric(label="⏳ Total Video Duration (second)", value=f"{ttl_duration:,}")
        with col3: 
            ttl_view = df_filtered_0["views"].sum()
            st.metric(label="👁️ Total Number of Views", value=f"{ttl_view:,}")

        # plot1: top view per day
        if options_date and options_channel:
            mask = df_music["publishedDate"].between(options_date[0], options_date[1]) &\
                    df_music["channelName"].isin([options_channel])
            df_filtered_1 = df_music[mask]
            df_music_1 = df_filtered_1.groupby(["publishedDate", "channelName"])["views"].mean().reset_index()
            # g4
            g4 = px.line(df_music_1,
                        x="publishedDate",
                        y="views")
            g4.add_hline(y=overall_avg, 
                         line_color="#ec5353",
                         line_dash="dash",
                         annotation_text=f"Overall Mean: {overall_avg:.2f}",
                         annotation_position="top right")
            st.plotly_chart(g4, use_container_width=True)
                
        if options_date and not options_channel:
            mask = df_music["publishedDate"].between(options_date[0], options_date[1])
            df_filtered_1 = df_music[mask]
            df_music_1 = df_filtered_1.groupby(["publishedDate"])["views"].mean().reset_index()
            # g4
            g4 = px.line(df_music,
                        x="publishedDate",
                            y="views")
            g4.add_hline(y=overall_avg, 
                            line_color="#ec5353",
                            line_dash="dash",
                            annotation_text=f"Overall Mean: {overall_avg:.2f}",
                            annotation_position="top right")
            st.plotly_chart(g4, use_container_width=True) 

    # two small graphs
    st.markdown("---")
    if st.session_state.music_button:
        col1, col2 = st.columns([3, 2])
        # top 10 video per channel
        with col1:
            mask = df_music["channelName"].isin([options_channel])
            df_filtered_2 = df_music[mask]
            top_videos = df_filtered_2.sort_values("views", ascending=False).head(10)
            g5 = px.bar(top_videos, x="views", y="title",
                        title="🔥 Top 10 Videos by View")
            g5.update_layout(showlegend=False)
            st.plotly_chart(g5, use_container_width=True)
        
        with col2:
            mask = df_music["channelName"].isin([options_channel])
            df_filtered_3 = df_music[mask]
            g6 = px.scatter(df_filtered_3, x="duration", y="views",
                            title="⏳ Duration vs. Views",
                            size="views")
            g6.update_layout(showlegend=False)
            st.plotly_chart(g6, use_container_width=True)

    # table
    if st.session_state.music_button:
        mask = df_music["channelName"].isin([options_channel])
        df_filtered_4 = df_music[mask].drop(columns=["channelName"])

        st.subheader('Music Dataset')
        st.dataframe(df_filtered_4)


















#################################################  Improvement  ###################################################
with tab5:
    st.title("🛠️ Opportunities for Dashboard Enhancement")

    st.markdown("""
    While the current version of the YouTube Dashboard provides a solid foundation for data exploration, 
    there are several areas for potential improvement to enhance functionality, usability, and analytical depth:
    """)

    st.markdown("#### 1. Incomplete Data Coverage")
    st.markdown("""
    The dataset retrieved from Kaggle exhibits gaps in its temporal coverage. 
    Some dates are missing, which may affect the accuracy of time-series analysis. 
    Future versions could incorporate a more complete dataset or implement data imputation methods.
    """)

    st.markdown("#### 2. Channel Comparison Functionality")
    st.markdown("""
    Enable users to select and compare multiple channels within the same time-series chart. 
    This would allow for more intuitive benchmarking of content performance across creators.
    """)

    st.markdown("#### 3. Description-Based Text Analysis")
    st.markdown("""
    Since the dataset contains video descriptions, a new tab can be introduced for 
    Natural Language Processing (NLP) to extract insights from textual content (e.g., keyword trends, topic modeling).
    """)

    st.markdown("#### 4. Viewer Sentiment Analysis")
    st.markdown("""
    If future datasets include user comments or likes/dislikes, sentiment analysis can be applied 
    to better understand audience reactions and their relationship to video performance.
    """)

    st.markdown("#### 5. Predictive Modeling Capabilities")
    st.markdown("""
    Introduce machine learning models (e.g., regression, classification) to predict video success 
    based on metadata such as publish date, video length, or keywords in the description.
    """)

    st.markdown("#### 6. Sidebar Context Management")
    st.markdown("""
    When switching between tabs, the sidebar currently retains filters from previous tabs. 
    Future iterations should dynamically clear or update sidebar components to match the active tab.
    """)
