import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
#Storing dataframes in sql
#mysql server connection
import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",password="")
mycursor = mydb.cursor(buffered=True)
#Getting data from sql and creating a dataframe
#Agg_Trans
mycursor.execute("use phonepe")
mycursor.execute("select * from Agg_Trans")
AT=mycursor.fetchall()
Agg_Trans=pd.DataFrame(AT,columns=("State","Year","Quarter","Transaction_type","Transaction_count","Transaction_amount"))
#Agg_uesr
mycursor.execute("select * from Agg_user")
Au=mycursor.fetchall()
Agg_user=pd.DataFrame(Au,columns=("State","Year","Quarter","User_brand","User_count","User_percentage"))
#map_Trans
mycursor.execute("select * from map_Trans")
mT=mycursor.fetchall()
map_Trans=pd.DataFrame(mT,columns=("State","Year","Quarter","Transaction_region","Transaction_count","Transaction_amount"))
#map_user
mycursor.execute("select * from map_user")
mu=mycursor.fetchall()
map_user=pd.DataFrame(mu,columns=("State","Year","Quarter","User_region","User_count"))
#Top_Trans
mycursor.execute("select * from Top_Trans")
TT=mycursor.fetchall()
Top_Trans=pd.DataFrame(TT,columns=("State","Year","Quarter","Transaction_type","Transaction_count","Transaction_amount"))
#Top_user
mycursor.execute("select * from Top_user")
Tu=mycursor.fetchall()
Top_user=pd.DataFrame(Tu,columns=("State","Year","Quarter","User_region","User_count"))
def map_1(year,agg_type):
    if(agg_type=="Aggregated_Transaction"):
        type=Agg_Trans
        count="Transaction_count"
        name='Transaction_type'
        amount="Transaction_amount"
    elif(agg_type=="Map_Transaction"):
        type=map_Trans
        count="Transaction_count"
        name="Transaction_region"
        amount="Transaction_amount"
    elif(agg_type=="Map_User"):
        type=map_user
        count="User_count"
        name="User_region"
        amount="User_count"
    elif(agg_type=="Top_Transaction"):
        type=Top_Trans
        count="Transaction_count"
        name="Transaction_type"
        amount="Transaction_amount"
    elif(agg_type=="Top_User"):
        type=Top_user
        count="User_count"
        name="User_region"
        amount="User_count"
    else:
        type=Agg_user
        count="User_count"
        name="User_brand"
        amount="User_percentage"
    a=type[type["Year"]==year]
    a.reset_index(drop=True,inplace=True)
    b=a.groupby("State")[[count]].sum()
    b.reset_index(inplace=True)
    c=a.groupby("State")[[amount]].sum()
    c.reset_index(inplace=True)
    import pandas as pd
    import plotly.express as px
    df = b
    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color=count,
        title=f"{count} Distribution",
        color_continuous_scale='Reds',
        height=900,  # Set the height of the chart
        width=900
    )
    fig.update_geos(fitbounds="locations", visible=False)
    
    df = c
    fig_1 = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color=amount,
        title=f"{amount} Distribution",
        color_continuous_scale="YlGnBu",
        height=900,  # Set the height of the chart
        width=900
    )
    fig_1.update_geos(fitbounds="locations", visible=False)
    df = a
    #sunburst
    fig_2 = px.sunburst(df, 
                    path=['Year', 'State', 'Quarter',name,count], 
                    values=amount,
                    color_discrete_sequence=px.colors.qualitative.Prism,  # Example color palette
                    maxdepth=3,  # Limit the depth of the sunburst to make it clearer
                    labels={amount},  # Update labels for clarity
                    title="Sunburst Chart for Transactions",  # Add a title
                    height=850,  # Set the height of the chart
                    width=850,  # Set the width of the chart
                    )
    fig_2.update_traces(textfont=dict(size=12), insidetextorientation='radial')  # Adjust font size and text orientation
    fig_2.update_layout(margin=dict(t=0, l=0, r=0, b=0),  # Remove unnecessary margins
                    plot_bgcolor='rgba(0,0,0,0)')  # Set transparent background
    fig_list=[fig_2,fig,fig_1]
    return fig_list
def map_2(agg_type):
    if(agg_type=="Aggregated_Transaction"):
        type=Agg_Trans
        count="Transaction_count"
        name='Transaction_type'
        amount="Transaction_amount"
    elif(agg_type=="Map_Transaction"):
        type=map_Trans
        count="Transaction_count"
        name="Transaction_region"
        amount="Transaction_amount"
    elif(agg_type=="Top_Transaction"):
        type=Top_Trans
        count="Transaction_count"
        name="Transaction_type"
        amount="Transaction_amount"
    else:
        type=Agg_user
        count="User_count"
        name="User_brand"
        amount="User_percentage"

    a=type.groupby(name)[[count,amount]].sum()
    a.reset_index(inplace=True)

    z=a.sort_values(by=count)
    fig_1 = px.bar(z.head(5),y=count,x=name, title=f'Bottom 5 Overall {name} Distribution by {count}')

    y=a.sort_values(by=amount)
    fig_2 = px.bar(y.head(5),y=amount,x=name, title=f'Bottom 5 Overall {name} Distribution by {amount}')
    
    z=a.sort_values(by=count,ascending=False)
    fig_3 = px.bar(z.head(5),y=count,x=name, title=f'Top 5 Overall {name} Distribution by {count}')
    
    y=a.sort_values(by=amount,ascending=False)
    fig_4 = px.bar(y.head(5),y=amount,x=name, title=f'Top 5 Overall {name} Distribution by {amount}')
    
    list=[fig_1,fig_2,fig_3,fig_4]



    b=type.groupby("State")[[count,amount]].sum()
    b.reset_index(inplace=True)
    z=b.sort_values(by=count,ascending=False)
    fig_1 = px.pie(b,values=count,names="State", title=f'State wise {count} Distribution')

    fig_2 = px.bar(z.head(5),y=count,x="State", title=f'Top 5 States by {count}')

    z=b.sort_values(by=amount,ascending=False)
    fig_3 = px.pie(b,values=amount,names="State", title=f'State wise {amount} Distribution')
    
    fig_4 = px.bar(z.head(5),y=amount,x="State", title=f'Top 5 States by {amount}')
    list2=[fig_1,fig_2,fig_3,fig_4]

    # b=type.groupby("State")[[count,amount]].sum()
    # b.reset_index(inplace=True)
    # fig_1 = px.pie(b,values=count,names="State", title='Transaction Type Distribution count')
    # fig_2 = px.pie(b,values=amount,names="State", title='Transaction Type Distribution count')
    # list2=[fig_1,fig_2]
    c=type.groupby("Year")[[count,amount]].sum()
    c.reset_index(inplace=True)
    fig_1 = px.bar(c,y=count,x="Year", title=f'{count} each Year')
    fig_2 = px.bar(c,y=amount,x="Year", title=f'{amount} each Year')
    list3=[fig_1,fig_2]
    total_list=[list,list2,list3]
    return total_list

def map_3(agg_type):
    if(agg_type=="Map_User"):
        type=map_user
    elif(agg_type=="Top_User"):
        type=Top_user

    b=type.groupby("State")[["User_count"]].sum()
    b.reset_index(inplace=True)
    z=b.sort_values(by="User_count",ascending=False)
    fig_3 = px.pie(b,values="User_count",names="State", title=f'State wise User count Distribution')
    fig_4 = px.bar(z.head(5),y="User_count",x="State", title=f'Top 5 States by User count Distribution')
    z=b.sort_values(by="User_count",ascending=True)
    fig_2= px.bar(z.head(5),y="User_count",x="State", title=f'Bottom 5 States by User count Distribution')



    b=type.groupby("User_region")[["User_count"]].sum()
    b.reset_index(inplace=True)
    z=b.sort_values(by="User_count",ascending=False)
    fig_1 = px.pie(b,values="User_count",names="User_region", title=f'User Count Distribution by Region')
    fig_5 = px.bar(z.head(5),y="User_count",x="User_region", title=f'Top 5 Region by User count Distribution')
    z=b.sort_values(by="User_count",ascending=True)
    fig_6= px.bar(z.head(5),y="User_count",x="User_region", title=f'Bottom 5 States by User count Distribution')

    o=type.groupby("Year")[["User_count"]].sum()
    o.reset_index(inplace=True)
    fig_7= px.bar(o,y="User_count",x="Year",title='User Count Distribution each Region')

    list2=[fig_3,fig_4,fig_2,fig_1,fig_5,fig_6,fig_7]

    return list2



def map_4(agg_type):
    if(agg_type=="Aggregated_Transaction"):
        type=Agg_Trans
        count="Transaction_count"
        name='Transaction_type'
        amount="Transaction_amount"
        color='sunset'
        year=[2018,2019,2020,2021,2022]
    elif(agg_type=="Map_Transaction"):
        type=map_Trans
        count="Transaction_count"
        name="Transaction_region"
        amount="Transaction_amount"
        color='earth'
        year=[2018,2019,2020,2021,2022]
    elif(agg_type=="Top_Transaction"):
        type=Top_Trans
        count="Transaction_count"
        name="Transaction_type"
        amount="Transaction_amount"
        color='balance'
        year=[2018,2019,2020,2021,2022]
    else:
        type=Agg_user
        count="User_count"
        name="User_brand"
        amount="User_percentage"
        color='plotly3'
        year=[2018,2019,2020,2021]
    fig_list=[]
    fig_list1=[]
    fig_list2=[]

    for i in year:
        a = type[type["Year"] == i]
        quater=[1,2,3,4]
        for j in quater:
            b = a[a["Quarter"] == j]
            c=b.groupby("State")[[count]].sum()
            c.reset_index(inplace=True)
            fig = px.choropleth(
                c,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color=count,
                title=f"year {i} Quarter {j}",
                color_continuous_scale=color,
                range_color=(0,b[count].max()),  # Define the range of colors
                height=700,
                width=700
            )
            fig.update_geos(fitbounds="locations", visible=False)



            d=c.sort_values(by=count,ascending=False)
            fig_4 = px.bar(d.head(5),y=count,x="State", title=f'In the {j} quarter of {i}, the top five {count}')
            fig_list1.append(fig)
            fig_list2.append(fig_4)
    fig_list=[fig_list1,fig_list2]
    return fig_list










#streamli page
st.set_page_config(layout="wide")
#creating sidebar
with st.sidebar:
    select_option=option_menu("Menu",["About","Maps","Chart"])
if select_option=="About":
        # Title and Introduction
        st.title("PhonePe Pulse Data Visualization and Exploration")
        st.header("",divider='rainbow')
        col1, col2 = st.columns(2)

            # Chart 1: Bar chart
        with col1:
            st.write("Welcome to the PhonePe Pulse Data Visualization and Exploration platform. Explore digital transaction trends and insights!")

            # Chart 2: Pie chart
        with col2:
            st.image("https://pbs.twimg.com/card_img/1785669921055367169/qtL8NNzS?format=jpg&name=large", width=600)

        # Description of PhonePe
        st.header("About PhonePe",divider='rainbow')
        col1, col2 = st.columns(2)
        with col2:
            st.write("PhonePe is a leading digital payments platform in India, offering a wide range of services including UPI payments, bill payments, recharges, and more. It is known for its user-friendly interface and secure transactions.")
        with col1:
            st.image("https://cdn.zeebiz.com/sites/default/files/styles/zeebiz_850x478/public/2023/02/07/225973-phonepe-upi.png?itok=XRUCFnK4", caption='Phonepe', use_column_width=True)


        # Data Visualization Section
        st.header("PhonePe Pulse Data Visualization",divider='rainbow')
        st.write("Explore digital transaction trends and insights with interactive visualizations in Maps and Chart pages.")

        # Placeholder for Data Visualization (Replace with actual visualizations)
        # Add your code to generate interactive visualizations here

        # # Exploration Features
        # st.header("Exploration Features")
        # st.write("Customize your exploration with interactive features.")

        # # Placeholder for Filters and Interactive Features (Replace with actual features)
        # # Add your code to provide interactive filters and features here

        # Photo and Video Gallery
        st.header("Photo and Video Gallery",divider='rainbow')
        st.write("Experience PhonePe's features with photos and videos.")

        # Add images from URLs
        image_urls = [
            "https://assets.entrepreneur.com/content/3x2/2000/1675756974-Untitleddesign-2023-02-07T132945518.jpg",
            "https://pbs.twimg.com/media/GG8TY2XawAA46SC?format=jpg&name=4096x4096",
            "https://d6xcmfyh68wv8.cloudfront.net/blog-content/uploads/2022/03/Phonepe.png"
        ]
            # Add videos from URLs
        video_urls = [
            "https://youtu.be/zGlDkrNxDU8?feature=shared",
            "https://youtu.be/_Tr05iT2IWI?feature=shared",
            "https://youtu.be/7opLEEi7StU?feature=shared"
        ]


        col1,col3= st.columns(2)
        with col1:
            st.image(image_urls[0],use_column_width=True)
        with col3:
            st.markdown(f'<img src="{image_urls[2]}" style="height:450px;">', unsafe_allow_html=True)
        col1,col3= st.columns(2)
        with col1:
            st.markdown(f'<img src="{image_urls[1]}" style="height:650px;">', unsafe_allow_html=True)
        with col3:
            st.video(video_urls[0])
        col1,col3= st.columns(2)
        with col1:
            st.video(video_urls[1])
        with col3:
            st.video(video_urls[2])
        # Conclusion
        st.header("Conclusion",divider='rainbow')
        st.write("Thank you for exploring PhonePe Pulse data with us. Try out PhonePe for yourself and experience the convenience of digital payments.")






elif select_option=="Maps":
    st.header("Phonepe Maps")
    t1,t2,t3=st.tabs(["Aggregated","Map","Top"])
    with t1:
        select_tab=st.radio("select one",["Aggregated_Transaction","Aggregated_User"])
        if select_tab=="Aggregated_Transaction":
            select_year=st.selectbox("year",["2018","2019","2020","2021","2022","2023"])
            st.write(f"{select_year} Data Sunburst: Distribution Across All Categories of {select_tab}")
            for i in map_1(int(select_year),select_tab):
                                st.plotly_chart(i)
        elif select_tab=="Aggregated_User":
            select_year=st.selectbox("year",["2018","2019","2020","2021","2022","2023"])
            st.write(f"{select_year} Data Sunburst: Distribution Across All Categories of {select_tab}")
            for i in map_1(int(select_year),select_tab):
                                st.plotly_chart(i)
    with t2:
        select_tab=st.radio("select one",["Map_Transaction","Map_User"])
        if select_tab=="Map_Transaction":
            select_year=st.selectbox("years",["2018","2019","2020","2021","2022","2023"])
            st.write(f"{select_year} Data Sunburst: Distribution Across All Categories of {select_tab}")
            for i in map_1(int(select_year),select_tab):
                st.plotly_chart(i)
        elif select_tab=="Map_User":
            select_year=st.selectbox("years",["2018","2019","2020","2021","2022","2023"])
            st.write(f"{select_year} Data Sunburst: Distribution Across All Categories of {select_tab}")
            var_cou=0
            for i in map_1(int(select_year),select_tab):
                var_cou+=1
                if(var_cou==3):
                    break
                st.plotly_chart(i)
    with t3:
        select_tab=st.radio("select one",["Top_Transaction","Top_User"])
        if select_tab=="Top_Transaction":
            select_year=st.selectbox("Years",["2018","2019","2020","2021","2022","2023"])
            st.write(f"{select_year} Data Sunburst: Distribution Across All Categories of {select_tab}")
            for i in map_1(int(select_year),select_tab):
                            st.plotly_chart(i)
        elif select_tab=="Top_User":
            select_year=st.selectbox("Years",["2018","2019","2020","2021","2022","2023"])
            st.write(f"{select_year} Data Sunburst: Distribution Across All Categories of {select_tab}")
            var_cou=0
            for i in map_1(int(select_year),select_tab):
                var_cou+=1
                if(var_cou==3):
                    break
                st.plotly_chart(i)







elif select_option=="Chart":
    st.header("Phonepe Charts")
    t=st.selectbox("queston",["Insights on Aggregated Transaction","Insights on Aggregated User","Insights on Map Transaction","Insights on Top Transaction","Insights on Map User",'Insights on Top User',"Quater wise transaction in Aggregated Transaction","Quater wise transaction in Map Transaction","Quater wise transaction in Top Transaction","Quater wise transaction in Aggregated User"])
    if t=="Insights on Aggregated Transaction":
            a=map_2("Aggregated_Transaction")
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[0][2])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[0][3])
            # Create two columns
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[1][0])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[1][1])

            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[1][2])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[1][3])

            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[2][0])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[2][1])
    elif t=="Insights on Map Transaction":
            a=map_2("Map_Transaction")
            # Create two columns
            col1, col2 = st.columns(2)
            with col1:
                t1,t2=st.tabs(["top 5","buttom 5"])

                # Chart 1: Bar chart
                with t2:
                        st.plotly_chart(a[0][0])

                    # Chart 2: Pie chart
                with t1:
                        st.plotly_chart(a[0][2])
            with col2:
                t1,t2=st.tabs(["top 5","buttom 5"])

                # Chart 1: Bar chart
                with t2:
                        st.plotly_chart(a[0][1])

                    # Chart 2: Pie chart
                with t1:
                        st.plotly_chart(a[0][3])

            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[1][0])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[1][1])

            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[1][2])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[1][3])

            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[2][0])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[2][1])
    elif t=="Insights on Top Transaction":
            a=map_2("Top_Transaction")
            # Create two columns
            col1, col2 = st.columns(2)
            with col1:
                t1,t2=st.tabs(["top 5","buttom 5"])

                # Chart 1: Bar chart
                with t2:
                        st.plotly_chart(a[0][0])

                    # Chart 2: Pie chart
                with t1:
                        st.plotly_chart(a[0][2])
            with col2:
                t1,t2=st.tabs(["top 5","buttom 5"])

                # Chart 1: Bar chart
                with t2:
                        st.plotly_chart(a[0][1])

                    # Chart 2: Pie chart
                with t1:
                        st.plotly_chart(a[0][3])

            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[1][0])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[1][1])

            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[1][2])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[1][3])

            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[2][0])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[2][1])
    elif t=="Insights on Aggregated User":
            a=map_2("Aggregated_user")
            # Create two columns
                        # Create two columns
            col1, col2 = st.columns(2)
            with col1:
                t1,t2=st.tabs(["top 5","buttom 5"])

                # Chart 1: Bar chart
                with t2:
                        st.plotly_chart(a[0][0])

                    # Chart 2: Pie chart
                with t1:
                        st.plotly_chart(a[0][2])
            with col2:
                t1,t2=st.tabs(["top 5","buttom 5"])

                # Chart 1: Bar chart
                with t2:
                        st.plotly_chart(a[0][1])

                    # Chart 2: Pie chart
                with t1:
                        st.plotly_chart(a[0][3])
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[1][0])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[1][1])

            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[1][2])

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(a[1][3])

            st.plotly_chart(a[2][0])
    elif t=="Insights on Map User":
            a=map_3("Map_User")
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[0])

            # Chart 2: Pie chart
            with col2:
                t1,t2=st.tabs(["top 5","buttom 5"])
                with t1:
                    st.plotly_chart(a[1])
                with t2:
                    st.plotly_chart(a[2])
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[3])

            # Chart 2: Pie chart
            with col2:
                t1,t2=st.tabs(["top 5","buttom 5"])
                with t1:
                    st.plotly_chart(a[4])
                with t2:
                    st.plotly_chart(a[5])
            st.plotly_chart(a[6])

    elif t=='Insights on Top User':
            a=map_3("Top_User")
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[0])

            # Chart 2: Pie chart
            with col2:
                t1,t2=st.tabs(["top 5","buttom 5"])
                with t1:
                    st.plotly_chart(a[1])
                with t2:
                    st.plotly_chart(a[2])
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(a[3])

            # Chart 2: Pie chart
            with col2:
                t1,t2=st.tabs(["top 5","buttom 5"])
                with t1:
                    st.plotly_chart(a[4])
                with t2:
                    st.plotly_chart(a[5])
            st.plotly_chart(a[6])
    elif t=="Quater wise transaction in Aggregated Transaction":
        a=map_4("Aggregated_Transaction")
        for i,j in zip(a[0],a[1]):
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(i)

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(j)
    elif t=="Quater wise transaction in Map Transaction":
        a=map_4("Map_Transaction")
        for i,j in zip(a[0],a[1]):
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(i)

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(j)    
    elif t=="Quater wise transaction in Top Transaction":
        a=map_4("Top_Transaction")
        for i,j in zip(a[0],a[1]):
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(i)

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(j)    
    elif t=="Quater wise transaction in Aggregated User":
        a=map_4("Aggregated_User")
        for i,j in zip(a[0],a[1]):
            col1, col2 = st.columns(2)

            # Chart 1: Bar chart
            with col1:
                st.plotly_chart(i)

            # Chart 2: Pie chart
            with col2:
                st.plotly_chart(j)