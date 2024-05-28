**Image to Schedule Converter**

This project is a Python-based application that allows users to upload an image containing a schedule or timetable, and it automatically extracts the event details, including titles and dates, from the image. The extracted information is then stored in a CSV file and displayed in a user-friendly Tkinter GUI.

**Features**

1. Upload an image containing a schedule or timetable
2. Automatic image processing and event extraction using computer vision and natural language processing techniques
3. Store extracted event details (title, date, and formatted date) in a CSV file
4. Display the extracted events in a Tkinter GUI with options to edit, delete, and add new events
5. Calculate the remaining time for each event and display it in the GUI

**Requirements**

Python 3.x
OpenCV
Pandas
Pillow
Tkinter
Google Generative AI API (requires an API key)

**Installation**

1. Clone the repository or download the source code.
2. Install the required dependencies by running pip install -r requirements.txt.
3. Obtain a Google Generative AI API key and set it as an environment variable named GOOGLE_API_KEY.

**Usage**

> Run the `ui.py` script to launch the application.
 Click the "Upload Image" button and select the image file containing the schedule or timetable.
 The application will process the image, extract the event details, and display them in the GUI.
 Use the provided buttons to edit, delete, or add new events.
 The remaining time for each event will be calculated and displayed in the GUI.

**Contributing**

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
