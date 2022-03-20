
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,date


def visitor_df(df):
    df_vis = df.groupby('IP').size()
    df_1 = pd.DataFrame({'IP': df_vis.index, 'count': df_vis.values})
    fig = px.pie(df_1, names=df_1["IP"], values=df_1["count"], title="Frequent Visitors",height=600)
    st.title('Frequent Visitors')
    st.plotly_chart(fig)
    var=df.IP.nunique()
    st.subheader("Total number of unique visitors: "+str(var))


def error(df):
    df_er = df[df['Status_code'] == '404']



    st.title('404 ERROR CODES')
    st.dataframe(df_er)

    st.subheader("Total number of 404 response codes: "+str(df_er.shape[0]))
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

    df_4=df_er.groupby('Dates').size()
    df_4_res = pd.DataFrame({'Date': df_4.index, 'count': df_4.values})
    st.header("404 Response Code per Day")
    fig4=px.bar(df_4_res,x="Date",y="count")
    st.plotly_chart(fig4)



def popular_pages(df):
    st.title('Top 10 Popular pages')
    df_req = df.groupby('Request').size()
    df_4 = pd.DataFrame({'Request': df_req.index, 'count': df_req.values})
    df_4_sort=df_4.sort_values(by='count',ascending=False)
    df_4_res=df_4_sort[:10]
    fig4 = px.bar(df_4_res, x="Request", y="count", title="Popular pages",width=1000,height=800)
    st.plotly_chart(fig4)









def visitor_length(df):
    IP = st.radio("Select the user IP",('10.131.0.1', '10.131.2.1', '10.128.2.1','10.129.2.1'))
    vis_date=st.radio("Select the date of visitor",('2017-11-29','2017-11-30'))
    user_1 = df[df['IP'] == IP]
    user_1_data= user_1[user_1['Dates'] == pd.to_datetime(vis_date)]

    user_1_data.sort_values('datetime',axis=0,ascending=True,inplace=True)
    st.write(user_1_data)
    today = date.today()
    d_end = datetime.datetime.combine(today,df.iloc[-1]['Time'])
    d_start = datetime.datetime.combine(today, df.iloc[0]['Time'])

    len=d_end-d_start

    st.subheader("Time spent by the user in the website: "+ str(len))




def main():
    st.title("WEB ANALYTICS TOOL")


    menu = ["Frequent Visitors","Visitor Length","404 Codes","Popular Pages"]
    choice = st.sidebar.selectbox("Metrics", menu)
    header_list = ['IP', 'Timestamp', 'Request', 'Status_code']
    uploaded_file = st.file_uploader("Choose a CSV file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file,names=header_list)


        df.dropna()
        del_val = ['chmod:', 'rm:', 'timeout:', "sh:"]
        df.drop(df[df["IP"].isin(del_val)].index, axis=0, inplace=True)
        df = df.iloc[:-7, 0:].copy()
        # df["Timestamp"] = df["Timestamp"].apply(lambda x: x[1:])
        # df["Timestamp"] = df["Timestamp"].apply(lambda x: x.replace(':', ' ', 1))

        # if data['URL'].str.contains('.js').any():
        #   data['URL_new'] = data['URL'].str.split('/').str[3]

        from datetime import datetime
        df["datetime"] = df["Timestamp"].apply(lambda x: datetime.strptime(x, "[%d/%b/%Y:%H:%M:%S"))
        #df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        df['Dates'] = pd.to_datetime(df['datetime']).dt.date
        df['Time'] = pd.to_datetime(df['datetime']).dt.time

        if choice == "Frequent Visitors":
                visitor_df(df)

        if choice=="Visitor Length":
            visitor_length(df)

        if choice=="404 Codes":
            error(df)

        if choice=="Popular pages":
            popular_pages(df)














if __name__ == '__main__':
    main()
