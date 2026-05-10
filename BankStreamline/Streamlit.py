# type this: cd "BankStreamline"
# then to run type: streamlit run Streamlit.py
import streamlit as st
import polars as pl
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


st.header('Financial Data Analysis')


# df = pd.read_csv(r'https://raw.githubusercontent.com/blakedennett/FinancialStreamline2/refs/heads/main/BankStreamline/Data/BankDataProd.csv?token=GHSAT0AAAAAADDLKTTFA5OTUWAX5YB6OCWI2AZCKEQ')
df = pd.read_csv(r'https://raw.githubusercontent.com/blakedennett/FinancialStreamline2/refs/heads/main/BankStreamline/Data/BankDataProd.csv')
df = pl.DataFrame(df)


df = df.with_columns(
    pl.col("date").str.strptime(pl.Date, "%Y-%m-%d", strict=False)
)


# End date
days_backward = time.localtime().tm_mday
now = datetime.now()
EndOfLastMonth = now - timedelta(days=days_backward)
# Start date
LastYear = EndOfLastMonth - relativedelta(years=1)
StartDate = LastYear + relativedelta(months=1)
StartDate = StartDate.replace(day=1).date()


df = df.filter(pl.col("date") >= pl.date(StartDate.year, StartDate.month, StartDate.day)) \
        .filter(pl.col("date") <= pl.date(EndOfLastMonth.year, EndOfLastMonth.month, EndOfLastMonth.day))


# ============================================================================================================


month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

df = df.sort("month")

categories = ['All', 'food', 'amazon', 'shopping', 'misc', 'wmt', 'tithing', 'subscriptions', 'progressive', 'fun', 'power', 'gas', 'water', 'internet', 'rent', 'car', 'natural gas', 'home improvement']
selected_category = st.selectbox("Select a category", key=1, options=(categories), label_visibility='hidden')

if selected_category != 'All':
    f1 = df.filter(pl.col('category') == selected_category)
else:
    f1 = df

controllable = st.checkbox('Controllables only?', key=2, value=False)

smooth = st.checkbox('Smooth?', key=3, value=False)

if smooth:
    trxn_count = st.checkbox('Transaction Count?', key=4, value=False)
else:
    trxn_count = 0

if controllable:
    f1 = f1.filter(pl.col('controllable') > 0)

fig = px.bar(f1.to_pandas(), x="monthName", y="cost", color="category", hover_data=['description', 'cardType', 'day'],
             title="Total Expense by Month",
             category_orders={"monthName": month_order},
             template='plotly_dark',
             labels={'monthName':''},
             text_auto=True,
             height=450,
             width=800)

# this graph is shown at end of next section
# st.plotly_chart(fig)

# ============================================================================================================


if selected_category != 'All':
    f2 = df.filter(pl.col('category') == selected_category)
else:
    f2 = df

if controllable:
    f2 = f2.filter(pl.col('controllable') > 0)

if trxn_count:
    f2 = f2.group_by(["monthName", 'month']).agg(pl.count())
    y_col = 'count'
else: 
    f2 = f2.group_by(["monthName", 'month']).agg(pl.sum("cost")) 
    y_col = 'cost'

f2 = f2.sort("month")


fig2 = px.bar(f2.to_pandas(), x="monthName", y=y_col,
             title="Total Expense by Month",
             template='plotly_dark',
             labels={'monthName':''},
             color_discrete_sequence=['#228B22'])
            #  category_orders={"monthName": month_order},
            #  text_auto=True)  # This adds text labels on top of the bars

fig2.add_trace(go.Scatter(
    x=f2["monthName"], 
    y=f2[y_col],
    text=f2[y_col].to_pandas().round(0).astype(int),
    mode='text',  
    textposition="top center", 
    showlegend=False
))

avg_cost = f2[y_col].mean()

fig2.add_shape(
    type="line",
    x0=month_order[0], x1=month_order[-1], 
    y0=avg_cost, y1=avg_cost,
    line=dict(color="white", width=2, dash="dash")
)

fig2.add_annotation(
    x=month_order[-1], y=avg_cost + (avg_cost * .1),
    text=f"Avg: {avg_cost:.0f}",
    showarrow=False,
    font=dict(size=12, color="white")
)

if smooth:
    st.plotly_chart(fig2)
else:
    st.plotly_chart(fig)

# st.text('Note: April 2026 returned $209 on Amazon', size=10)

st.markdown("<p style='font-size:14px;'>Note: April 2026 returned $209 on Amazon</p>", unsafe_allow_html=True)

