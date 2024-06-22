import streamlit as st
import pandas as pd
import altair as alt

# Set the page configuration to wide
st.set_page_config(layout="wide")

def traffic1():
    # Streamlit app title
    st.title('회선 트래픽 분석 (2024년 5월)')

    # File uploader for CSV files
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the uploaded CSV file
        data = pd.read_csv(uploaded_file)

        # Removing leading and trailing spaces from column names
        data.columns = data.columns.str.strip()

        # Adding new columns for average and maximum bps in mbps
        data['inmbps'] = data['inbps'] / 1000000
        data['outmbps'] = data['outbps'] / 1000000

        # Sidebar multiselect for 'type' column
        st.sidebar.header('Filter options')
        types = data['type'].unique()
        all_types_option = '모두 선택'
        selected_types = st.sidebar.multiselect('Select types to filter', [all_types_option] + list(types), default=[all_types_option])

        # If '모두 선택' is selected, select all types
        if all_types_option in selected_types:
            selected_types = types

        # Filter data based on selected types
        filtered_data = data[data['type'].isin(selected_types)]

        # Grouping by type, category1, category2, category3, category4 and calculating mean for inmbps and outmbps
        original_grouped_df = filtered_data.groupby(['type', 'category1', 'category2', 'category3', 'category4'], observed=False).agg(
            average_inmbps=('inmbps', 'mean'),
            average_outmbps=('outmbps', 'mean'),
            max_inmbps=('inmbps', 'max'),
            max_outmbps=('outmbps', 'max')
        ).reset_index()

        # Formatting the numeric columns to two decimal places
        original_grouped_df['average_inmbps'] = original_grouped_df['average_inmbps'].round(2)
        original_grouped_df['average_outmbps'] = original_grouped_df['average_outmbps'].round(2)
        original_grouped_df['max_inmbps'] = original_grouped_df['max_inmbps'].round(2)
        original_grouped_df['max_outmbps'] = original_grouped_df['max_outmbps'].round(2)

        # Display the grouped dataframe using Streamlit for original data
        st.subheader('회선 유형별 데이터')
        st.dataframe(original_grouped_df)

        # Grouping by the day column and calculating mean for inmbps and outmbps
        grouped_df = filtered_data.groupby(['day'], observed=False).agg(
            average_inmbps=('inmbps', 'mean'),
            average_outmbps=('outmbps', 'mean'),
            max_inmbps=('inmbps', 'max'),
            max_outmbps=('outmbps', 'max')
        ).reset_index()

        # Formatting the numeric columns to two decimal places
        grouped_df['average_inmbps'] = grouped_df['average_inmbps'].round(2)
        grouped_df['average_outmbps'] = grouped_df['average_outmbps'].round(2)
        grouped_df['max_inmbps'] = grouped_df['max_inmbps'].round(2)
        grouped_df['max_outmbps'] = grouped_df['max_outmbps'].round(2)

        
        with st.expander("일자별"):
            # Create columns for displaying dataframe and chart side by side for 일자별 평균 데이터
            st.subheader('1_일자별 평균 데이터')

            # Create columns for displaying metrics side by side
            metric_col1, metric_col2 = st.columns([1, 1])

            # Display metrics for overall average and max inmbps in the first column
            overall_avg_inmbps = grouped_df['average_inmbps'].mean().round(2)
            overall_max_inmbps = grouped_df['max_inmbps'].max().round(2)
            metric_col1.metric(label="Overall Average InMbps", value=f"{overall_avg_inmbps:.2f} Mbps", delta=f"MAX: {overall_max_inmbps:.2f} Mbps")

            # Display metrics for overall average and max outmbps in the second column
            overall_avg_outmbps = grouped_df['average_outmbps'].mean().round(2)
            overall_max_outmbps = grouped_df['max_outmbps'].max().round(2)
            metric_col2.metric(label="Overall Average OutMbps", value=f"{overall_avg_outmbps:.2f} Mbps", delta=f"MAX: {overall_max_outmbps:.2f} Mbps")

            col1, col2 = st.columns([1, 2])  # Adjust the width ratio as needed

            # Display the grouped dataframe in the first column
            col1.dataframe(grouped_df)

            # Creating a line chart for inmbps and outmbps average values by day in the second column
            day_chart = alt.Chart(grouped_df).transform_fold(
                ['average_inmbps', 'average_outmbps'],
                as_=['Measurement', 'Mbps']
            ).mark_line().encode(
                x=alt.X('day:Q', title='Day'),
                y=alt.Y('Mbps:Q', title='Mbps'),
                color=alt.Color('Measurement:N', title='Measurement'),
                tooltip=['day', 'Measurement:N', 'Mbps:Q']
            ).interactive()

            col2.altair_chart(day_chart, use_container_width=True)


        # Grouping by the weekday2 column and calculating mean for inmbps and outmbps
        weekday_order = ['월', '화', '수', '목', '금', '토', '일']
        filtered_data['weekday2'] = pd.Categorical(filtered_data['weekday2'], categories=weekday_order, ordered=True)
        
        weekday_grouped_df = filtered_data.groupby(['weekday2'], observed=False).agg(
            average_inmbps=('inmbps', 'mean'),
            average_outmbps=('outmbps', 'mean'),
            max_inmbps=('inmbps', 'max'),
            max_outmbps=('outmbps', 'max')
        ).reset_index().sort_values(by='weekday2')

        # Formatting the numeric columns to two decimal places
        weekday_grouped_df['average_inmbps'] = weekday_grouped_df['average_inmbps'].round(2)
        weekday_grouped_df['average_outmbps'] = weekday_grouped_df['average_outmbps'].round(2)
        weekday_grouped_df['max_inmbps'] = weekday_grouped_df['max_inmbps'].round(2)
        weekday_grouped_df['max_outmbps'] = weekday_grouped_df['max_outmbps'].round(2)

        
        with st.expander("요일별"):
            # Create columns for displaying dataframe and chart side by side for 요일별 평균 데이터
            st.subheader('2_요일별 평균 데이터')

            # Create columns for displaying metrics side by side for 요일별 평균 데이터
            metric_col3, metric_col4 = st.columns([1, 1])

            # Display metrics for overall average and max inmbps by weekday in the first column
            overall_avg_inmbps_weekday = weekday_grouped_df['average_inmbps'].mean().round(2)
            overall_max_inmbps_weekday = weekday_grouped_df['max_inmbps'].max().round(2)
            metric_col3.metric(label="Overall Average InMbps (Weekday)", value=f"{overall_avg_inmbps_weekday:.2f} Mbps", delta=f"MAX: {overall_max_inmbps_weekday:.2f} Mbps")

            # Display metrics for overall average and max outmbps by weekday in the second column
            overall_avg_outmbps_weekday = weekday_grouped_df['average_outmbps'].mean().round(2)
            overall_max_outmbps_weekday = weekday_grouped_df['max_outmbps'].max().round(2)
            metric_col4.metric(label="Overall Average OutMbps (Weekday)", value=f"{overall_avg_outmbps_weekday:.2f} Mbps", delta=f"MAX: {overall_max_outmbps_weekday:.2f} Mbps")

            col3, col4 = st.columns([1, 2])  # Adjust the width ratio as needed

            # Display the grouped dataframe in the first column
            col3.dataframe(weekday_grouped_df)

            # Creating a line chart for inmbps and outmbps average values by weekday in the second column
            weekday_chart = alt.Chart(weekday_grouped_df).transform_fold(
                ['average_inmbps', 'average_outmbps'],
                as_=['Measurement', 'Mbps']
            ).mark_line().encode(
                x=alt.X('weekday2:N', title='Weekday', sort=weekday_order),
                y=alt.Y('Mbps:Q', title='Mbps'),
                color=alt.Color('Measurement:N', title='Measurement'),
                tooltip=['weekday2:N', 'Measurement:N', 'Mbps:Q']
            ).interactive()

            col4.altair_chart(weekday_chart, use_container_width=True)

        # Grouping by the hour column and calculating mean for inmbps and outmbps
        hourly_grouped_df = filtered_data.groupby(['hour'], observed=False).agg(
            average_inmbps=('inmbps', 'mean'),
            average_outmbps=('outmbps', 'mean'),
            max_inmbps=('inmbps', 'max'),
            max_outmbps=('outmbps', 'max')
        ).reset_index()

        # Formatting the numeric columns to two decimal places
        hourly_grouped_df['average_inmbps'] = hourly_grouped_df['average_inmbps'].round(2)
        hourly_grouped_df['average_outmbps'] = hourly_grouped_df['average_outmbps'].round(2)
        hourly_grouped_df['max_inmbps'] = hourly_grouped_df['max_inmbps'].round(2)
        hourly_grouped_df['max_outmbps'] = hourly_grouped_df['max_outmbps'].round(2)

        
        with st.expander("시간별"):
            # Create columns for displaying dataframe and chart side by side for 시간대별 평균 데이터
            st.subheader('3_시간대별 평균 데이터')

            # Create columns for displaying metrics side by side for 시간대별 평균 데이터
            metric_col5, metric_col6 = st.columns([1, 1])

            # Display metrics for overall average and max inmbps by hour in the first column
            overall_avg_inmbps_hour = hourly_grouped_df['average_inmbps'].mean().round(2)
            overall_max_inmbps_hour = hourly_grouped_df['max_inmbps'].max().round(2)
            metric_col5.metric(label="Overall Average InMbps (Hour)", value=f"{overall_avg_inmbps_hour:.2f} Mbps", delta=f"MAX: {overall_max_inmbps_hour:.2f} Mbps")

            # Display metrics for overall average and max outmbps by hour in the second column
            overall_avg_outmbps_hour = hourly_grouped_df['average_outmbps'].mean().round(2)
            overall_max_outmbps_hour = hourly_grouped_df['max_outmbps'].max().round(2)
            metric_col6.metric(label="Overall Average OutMbps (Hour)", value=f"{overall_avg_outmbps_hour:.2f} Mbps", delta=f"MAX: {overall_max_outmbps_hour:.2f} Mbps")

            col5, col6 = st.columns([1, 2])  # Adjust the width ratio as needed

            # Display the grouped dataframe in the first column
            col5.dataframe(hourly_grouped_df)

            # Creating a line chart for inmbps and outmbps average values by hour in the second column
            hour_chart = alt.Chart(hourly_grouped_df).transform_fold(
                ['average_inmbps', 'average_outmbps'],
                as_=['Measurement', 'Mbps']
            ).mark_line().encode(
                x=alt.X('hour:Q', title='Hour'),
                y=alt.Y('Mbps:Q', title='Mbps'),
                color=alt.Color('Measurement:N', title='Measurement'),
                tooltip=['hour:Q', 'Measurement:N', 'Mbps:Q']
            ).interactive()

            col6.altair_chart(hour_chart, use_container_width=True)

    else:
        st.write("Please upload a CSV file to proceed.")

#if __name__ == "__main__":
#    traffic1()
