
import streamlit as st
import pandas as pd
import plotly.express as px


def visitor_df(df):
    df_vis = df.groupby('IP').size()
    df_1 = pd.DataFrame({'IP': df_vis.index, 'count': df_vis.values})
    fig = px.pie(df_1, names=df_1["IP"], values=df_1["count"], title="Frequent Visitors")
    st.title('Frequent Visitors')
    st.plotly_chart(fig)
    var=df.IP.nunique()
    st.caption("Total number of unique visitors: "+str(var))


def error(df):
    df_er = df[df['Status_code'] == '404']



    st.title('404 ERROR CODES')
    st.dataframe(df_er)

    st.header("Total number of 404 response codes: "+str(df_er.shape[0]))
    df_viser = df_er.groupby('IP').size()
    df_2 = pd.DataFrame({'IP': df_viser.index, 'count': df_viser.values})

    st.header('Frequent Number of Client Errors')
    fig2 = px.pie(df_2, names=df_2["IP"], values=df_2["count"])
    st.plotly_chart(fig2)

    df_server = df_er.groupby('Request').size()
    st.header("404 Code End Points")
    df_3 = pd.DataFrame({'Request': df_server.index, 'count': df_server.values})
    fig3 = px.pie(df_3, names=df_3["Request"], values=df_3["count"], title="Frequent Error pages")
    st.plotly_chart(fig3)






def visitor_length(df):
    IP = st.radio("Select the user IP",('10.131.0.1', '10.131.2.1', '10.128.2.1','10.129.2.1'))
    vis_date=st.radio("Select the date of visitor",('2017-11-29','2017-11-30'))
    user_1 = df[df['IP'] == IP]
    user_1_data= user_1[user_1['Timestamp'] == pd.to_datetime(vis_date)]
    user_1_data.Timestamp.sort_values()



def main():
    st.title("Online Image Compressor")


    menu = ["Frequent Visitors","404 Codes"]
    choice = st.sidebar.selectbox("Metrics", menu)
    header_list = ['IP', 'Timestamp', 'Request', 'Status_code']
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file,names=header_list)


        df.dropna()
        del_val = ['chmod:', 'rm:', 'timeout:', "sh:"]
        df.drop(df[df["IP"].isin(del_val)].index, axis=0, inplace=True)
        df = df.iloc[:-7, 0:].copy()
        df["Timestamp"] = df["Timestamp"].apply(lambda x: x[1:])
        df["Timestamp"] = df["Timestamp"].apply(lambda x: x.replace(':', ' ', 1))
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        if choice == "Frequent Visitors":
                visitor_df(df)

        if choice=="404 Codes":
            error(df)












if __name__ == '__main__':
    main()
