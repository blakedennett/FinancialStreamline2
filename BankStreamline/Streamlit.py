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

categories = ['All', 'food', 'amazon', 'shopping', 'misc', 'wmt', 'tithing', 'subscriptions', 'progressive', 'fun', 'power', 'gas', 'water', 'internet', 'rent', 'car']
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

# =======================================================================================

st.header('Goals Section')

current_quarter = (now.month - 1) // 3 + 1
current_yr = now.year
quarters = [1, 2, 3, 4]
quarters = [current_quarter] + [q for q in quarters if q != current_quarter]

selected_quarter = st.selectbox("Select a quarter", key=5, options=(quarters), label_visibility='hidden')


food = 150 * 3
amazon = 180 * 3
shopping = 60 * 3
wmt = 600 * 3

st.write(f'Food: ${food}')
st.write(f'Amazon: ${amazon}')
st.write(f'Shopping: ${shopping}')
st.write(f'WMT: ${wmt}')

f3 = df.filter((pl.col('category').is_in(['food', 'amazon', 'shopping', 'wmt'])) & (pl.col('quarter') == selected_quarter) & (pl.col('year') == current_yr))

f3 = f3.group_by(['category', 'quarter']).agg(pl.sum('cost'))


f3 = f3.with_columns(value_difference = pl.when(pl.col('category') == 'food').then(food - pl.col('cost'))
                                        .when(pl.col('category') == 'amazon').then(amazon - pl.col('cost'))
                                        .when(pl.col('category') == 'wmt').then(wmt - pl.col('cost'))
                                        .when(pl.col('category') == 'shopping').then(shopping - pl.col('cost'))) \
        # .with_columns(color = pl.when(pl.col('value_difference') >= 0).then(pl.lit('green')).otherwise(pl.lit('red')))

fig3 = go.Figure()

fig3 = go.Figure(go.Indicator(
    mode = "number+gauge+delta", value = f3.filter(pl.col('category') == 'food')['cost'].max(),
    # domain = {'x': [0.1, 1], 'y': [0, 1]},
    title = {'text' :"<b>Food</b>"},
    # delta = {'reference': 450},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 600]},
        'threshold': {
            'line': {'color': "green", 'width': 2},
            'thickness': 1,
            'value': food},
        'steps': [
            {'range': [0, 150], 'color': "lightgray"},
            {'range': [150, 300], 'color': "darkgray"},
            {'range': [300, 450], 'color': "gray"},
            {'range': [450, 600], 'color': "black"},
            ]}))

fig4 = go.Figure()

fig4 = go.Figure(go.Indicator(
    mode = "number+gauge+delta", value = f3.filter(pl.col('category') == 'wmt')['cost'].max(),
    # domain = {'x': [0.1, 1], 'y': [0.5, 1]},
    title = {'text' :"<b>WMT</b>"},
    # delta = {'reference': 450},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 2400]},
        'threshold': {
            'line': {'color': "green", 'width': 2},
            'thickness': 1,
            'value': wmt},
        'steps': [
            {'range': [0, 600], 'color': "lightgray"},
            {'range': [600, 1200], 'color': "darkgray"},
            {'range': [1200, 1800], 'color': "gray"},
            {'range': [1800, 2400], 'color': "black"},
            ]}))


fig5 = go.Figure()

fig5 = go.Figure(go.Indicator(
    mode = "number+gauge+delta", value = f3.filter(pl.col('category') == 'amazon')['cost'].max(),
    # domain = {'x': [0.1, 1], 'y': [0.5, 1]},
    title = {'text' :"<b>amazon</b>"},
    # delta = {'reference': 450},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 720]},
        'threshold': {
            'line': {'color': "green", 'width': 2},
            'thickness': 1,
            'value': amazon},
        'steps': [
            {'range': [0, 180], 'color': "lightgray"},
            {'range': [180, 360], 'color': "darkgray"},
            {'range': [360, 540], 'color': "gray"},
            {'range': [540, 720], 'color': "black"},
            ]}))

fig6 = go.Figure()

fig6 = go.Figure(go.Indicator(
    mode = "number+gauge+delta", value = round(f3.filter(pl.col('category') == 'shopping')['cost'].max(), 0),
    # domain = {'x': [0.1, 1], 'y': [0.5, 1]},
    title = {'text' :"<b>Shopping</b>"},
    # delta = {'reference': 450},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 240]},
        'threshold': {
            'line': {'color': "green", 'width': 2},
            'thickness': 1,
            'value': shopping},
        'steps': [
            {'range': [0, 60], 'color': "lightgray"},
            {'range': [60, 120], 'color': "darkgray"},
            {'range': [120, 180], 'color': "gray"},
            {'range': [180, 240], 'color': "black"},
            ]}))


fig3.update_layout(height = 250, title='Food', title_font_size=20)
fig4.update_layout(height = 250, title='WMT', title_font_size=20)
fig5.update_layout(height = 250, title='Amazon', title_font_size=20)
fig6.update_layout(height = 250, title='Shopping', title_font_size=20)
 
st.plotly_chart(fig3)
st.plotly_chart(fig4)
st.plotly_chart(fig5)
st.plotly_chart(fig6)
st.table(f3)
# =======================================================================================

st.subheader('Select a column to sort by')
columns = ['date', 'category', 'description', 'cost', 'controllable', 'monthName', 'month', 'day', 'year', 'weekDay', 'cardType']
chosen_column = st.selectbox("", key=6, options=(columns), label_visibility='hidden')

directions = ['Highest at the top', 'Lowest at the top']
chosen_direction = st.selectbox("Sorting Direction", key=7, options=(directions), label_visibility='hidden')

last_month = EndOfLastMonth.month
correct_yr = EndOfLastMonth.year

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
date_filter = st.checkbox('Filter dates', key=8, value=False)

if date_filter:
    chosen_month = st.selectbox('Month Filter', key=9, options=months, label_visibility='hidden')
    chosen_year = st.selectbox('year Filter', key=10, options=sorted(list(df['year'].unique()), reverse = True), label_visibility='hidden')
    tf = df.filter((pl.col('monthName') == chosen_month) & (pl.col('year') == chosen_year))
else:
    tf = df

# tf = df.filter((pl.col('month') == last_month) & (pl.col('year') == correct_yr))

if chosen_direction == 'Highest at the top':
    tf = tf.sort(chosen_column, descending=True)
else:
    tf = tf.sort(chosen_column, descending=False)
    

if selected_category != 'All':
    tf = tf.filter(pl.col('category') == selected_category)
else:
    tf = tf

st.table(tf)