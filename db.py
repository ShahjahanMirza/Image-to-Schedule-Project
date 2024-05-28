from image_processing import transform_image
from image_read import chat_with_image_gemini

import pandas as pd

# input_image_path = 'schedule.jpg'
# transform_image(input_image_path)
# output_image_path = 'output_image.jpg'
# events = chat_with_image_gemini(output_image_path)


def update_db(events):
    try:
        df = pd.read_csv('events.csv', header=0)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Title', 'Date', 'Formatted_Date'])

    titles = events.get('Title', [])
    dates = events.get('Date', [])
    formatted_dates = events.get('Formatted_Date', [])

    if len(titles) != len(dates) or len(titles) != len(formatted_dates):
        raise ValueError("The lengths of the 'Title', 'Date', and 'Formatted_Date' lists are not equal.")

    new = pd.DataFrame({'Title': titles, 'Date': dates, 'Formatted_Date': formatted_dates})
    

    df = df._append(new, ignore_index=True)

    df.to_csv('events.csv', index=False)


# print(df)

# for index, row in df.iterrows():
#     title = row['Title']
#     date = row['Date']
#     f_date = row['Formatted_Date']
#     print(f"Title: {title}")
#     print(f"Date: {date}")
#     print(f"Formatted Date: {f_date}")
#     print()  # Add an empty line for better readability

# print(df)


# df.drop('Release of Moot Problem', axis=0,inplace=True)

# print(df)