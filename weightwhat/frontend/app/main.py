import datetime
import json

import altair as alt
import pandas as pd
import requests
import streamlit as st

st.title("Weightwhat?")
st.write("Weight tracking and analysis")


def preprocess_data(raw_data):
    data = raw_data.sort_values(by="created_at", ascending=True).reset_index(drop=True)
    data = data[["id", "weight", "created_at"]]
    data["timestamp"] = pd.to_datetime(data["created_at"])
    data["date"] = data["timestamp"].dt.date
    data["year_month"] = data["timestamp"].dt.strftime("%Y-%m")
    data["year_week"] = data["timestamp"].dt.strftime("%Y-%W")
    data["month_of_year"] = data["timestamp"].dt.month
    data["week_of_year"] = data["timestamp"].dt.week
    data["day_of_week"] = data["timestamp"].dt.dayofweek
    data["day_name"] = data["timestamp"].dt.day_name()
    data["diff"] = data.groupby("year_month")["weight"].diff().fillna(0)
    return data


@st.cache
def load_data():
    response = requests.get("http://api:8000/api/weights")
    raw_data = pd.DataFrame(response.json())
    data = preprocess_data(raw_data)
    return data


data = load_data()

st.sidebar.title("Options")
st.sidebar.subheader("Show raw data")
show_raw_data = st.sidebar.checkbox("Show raw data")

if show_raw_data:
    st.dataframe(data[["id", "weight", "created_at"]])

d = pd.to_datetime(st.date_input("Weight loss since:", data.timestamp.min()), utc=True)

c1 = (
    alt.Chart(data[data.timestamp > d])
    .mark_line(color="#282a36", size=1)
    .encode(
        alt.Y(
            "weight",
            scale=alt.Scale(domain=[data.weight.max() * 0.8, data.weight.max()]),
            title="weight in kg",
        ),
        x="date:T",
        tooltip=["id", "weight"],
    )
    .properties(height=400, width=300)
    .interactive()
)

c2 = (
    alt.Chart(data[data.timestamp > d].groupby("year_week")["diff"].sum().reset_index())
    .mark_bar()
    .encode(
        y=alt.Y("year_week", title="week"),
        x=alt.X("diff:Q", title="difference to day before (in kg)"),
        color=alt.condition(
            alt.datum.diff < 0,
            alt.value("#50fa7b"),  # The positive color
            alt.value("#ff5555"),  # The negative color
        ),
        tooltip=["diff"],
    )
    .properties(height=400, width=200)
    .interactive()
)

c3 = c1 | c2

st.altair_chart(c3, use_container_width=True)

weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

options = st.selectbox(
    "Weight loss by week:",
    data.year_week.unique().tolist(),
    index=data.year_week.unique().tolist().index(data.year_week.unique().tolist()[-1]),
)

c4 = (
    alt.Chart(data[data.year_week == options])
    .mark_circle(color="black")
    .encode(
        y=alt.Y(
            "weight",
            scale=alt.Scale(
                domain=[
                    data[data.year_week == options].weight.max() * 0.95,
                    data[data.year_week == options].weight.max(),
                ]
            ),
            title="weight in kg",
        ),
        x=alt.X("day_name", sort=weekdays, title="day of week"),
        tooltip=["weight", "created_at"],
    )
    .interactive()
)

st.altair_chart(c4, use_container_width=True)

c5 = (
    alt.Chart(data)
    .mark_circle(color="black")
    .encode(
        x=alt.X("diff", title="difference to day before (in kg)"),
        y=alt.Y("day_name", sort=weekdays, title="day of week"),
        color=alt.condition(
            alt.datum.diff < 0,
            alt.value("#50fa7b"),  # The positive color
            alt.value("#ff5555"),  # The negative color
        ),
    )
    .configure_mark(opacity=0.3)
)


st.altair_chart(c5, use_container_width=True)

st.sidebar.subheader("Add weight")
weight = st.sidebar.number_input("Weight")
date = st.sidebar.date_input("Measured at:")
date = datetime.datetime(date.year, date.month, date.day)


if st.sidebar.button("add"):
    response = requests.post(
        "http://api:8000/api/weight",
        data=json.dumps({"weight": weight, "created_at": str(date)}),
    )
    if response.status_code == 201:
        st.sidebar.success("Weight added")
    else:
        st.sidebar.exception(RuntimeError("Weight could not be added"))


st.sidebar.subheader("Delete weight")
del_id = int(st.sidebar.number_input("ID"))

if st.sidebar.button("delete"):
    response = requests.delete(f"http://api:8000/api/weight/{del_id}")
    if response.status_code == 200:
        st.sidebar.success("Weight deleted")
    else:
        st.sidebar.exception(
            RuntimeError(f"No Weight found at id:{del_id} could not be deleted")
        )
