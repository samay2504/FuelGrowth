```markdown
# Influencer Performance Analysis and Face Detection System

This project involves analyzing influencer performance metrics from videos. The process integrates video downloading, face detection, and performance linking using a CSV input. The repository includes scripts for data processing, visualization, and generating reports in HTML format. The following sections describe each step and function in detail.

---

## Table of Contents

1. [Setup and Requirements](#setup-and-requirements)
2. [Functionality Overview](#functionality-overview)
3. [Scripts Breakdown](#scripts-breakdown)
    - [Main Script](#main-script)
    - [Data Cleaning Script](#data-cleaning-script)
    - [Visualization Script](#visualization-script)
    - [HTML Table Generator Script](#html-table-generator-script)
4. [Execution Steps](#execution-steps)
5. [Sample Output](#sample-output)
6. [Future Enhancements](#future-enhancements)

---

## Setup and Requirements

### Prerequisites
Ensure you have the following installed:
- Python 3.7+
- Required Python libraries:
  ```bash
  pip install pandas opencv-python insightface sklearn matplotlib seaborn
  ```
- Colab environment (if running on Google Colab)
- CSV file containing influencer data (with columns `Video URL` and `Performance`).

---

## Functionality Overview

The workflow processes influencer videos to detect unique faces and calculates their average performance:
1. **Upload CSV**: Load influencer data.
2. **Download Videos**: Fetch video files using their URLs.
3. **Extract Faces**: Detect and save unique faces with embeddings.
4. **Link Metrics**: Link faces to their performance metrics.
5. **Visualize Data**: Generate bar charts and performance distributions.
6. **Generate HTML Report**: Display influencers’ faces and metrics in an HTML table.

---

## Scripts Breakdown

### Main Script

The **main script** processes videos to extract influencer faces and associates them with performance metrics.

#### Key Steps
1. **Setup Directories**:
   - Creates `videos` and `frames` directories for downloaded videos and extracted faces.
2. **Load Data**:
   - Uploads the CSV file and removes duplicate video URLs.
3. **Download Videos**:
   - Downloads videos from URLs in the CSV file using `wget`.
4. **Extract Faces**:
   - Processes videos frame-by-frame using `InsightFace` to detect unique faces based on cosine similarity.
5. **Aggregate Results**:
   - Links detected faces with performance metrics and calculates average performance per face.
6. **Export Results**:
   - Saves the results to a CSV and downloads face images as a ZIP file.

#### Functions
- `load_data()`: Handles CSV upload and preprocessing.
- `download_video(video_url, save_dir)`: Downloads a video from a URL.
- `extract_faces_from_video(video_path, video_name, output_dir)`: Extracts unique faces and saves them with unified filenames.
- `process_videos(data, video_dir, frame_dir)`: Processes all videos in the dataset.
- `calculate_average_performance(influencer_faces)`: Computes the average performance for each unique influencer face.
- `download_all_faces(frame_dir, local_path)`: Zips and downloads extracted face images.

---

### Data Cleaning Script

The **data cleaning script** removes duplicate influencers based on similar performance and face embeddings.

#### Steps
1. **Upload Data**:
   - Upload and load the results CSV.
2. **Remove Duplicates**:
   - Drops duplicate rows with identical performance metrics.
3. **Save Cleaned Data**:
   - Exports the cleaned dataset to a new CSV file.

#### Key Functions
- Uses Pandas `drop_duplicates()` for efficient duplicate removal.

---

### Visualization Script

The **visualization script** generates plots to analyze influencer performance metrics.

#### Steps
1. **Load Data**:
   - Reads the cleaned influencer performance CSV.
2. **Generate Bar Chart**:
   - Visualizes the top 20 influencers by performance using Seaborn.
3. **Performance Distribution**:
   - Plots the distribution of all performance metrics.
4. **Save Output**:
   - Saves the plots as PNG files.

#### Key Libraries
- **Matplotlib**: For creating plots.
- **Seaborn**: For aesthetically pleasing visualizations.

---

### HTML Table Generator Script

The **HTML table generator script** creates a table showcasing influencer faces and their average performance.

#### Steps
1. **Load Data**:
   - Reads the cleaned CSV and face images.
2. **Generate HTML Table**:
   - Embeds images and performance metrics into an interactive HTML file.
3. **Save HTML**:
   - Outputs the table to a specified file.

#### Key Features
- Uses Base64 encoding to embed face images directly in the HTML file.

---

## Execution Steps

1. **Run the Main Script**:
   - Upload the CSV and let the script process the videos to generate the initial performance data.
2. **Clean the Data**:
   - Use the data cleaning script to remove duplicates.
3. **Visualize the Data**:
   - Run the visualization script to generate performance insights.
4. **Generate the HTML Report**:
   - Create an HTML table using the HTML table generator script.

---

## Sample Output

### CSV Results
|           Face Image            | Average Performance |
|---------------------------------|---------------------|
| `face_1_hd-999607261342550.jpg` |   1.06636506947943  |
| `face_1_hd-997580728807604.jpg` |   1.500649605075    |

### Visualizations
 **Top Influencers Bar Chart and Performance Distribution**
   ![Plot](https://github.com/user-attachments/assets/d9c7e3d9-22de-4f7a-b17e-ddc7762b8b46)

### HTML Report
An interactive table displaying influencer faces and their average performance.

---

## Future Enhancements

1. Add advanced face clustering for better uniqueness detection.
2. Enable multi-threaded video processing for faster execution.
3. Integrate cloud storage for large datasets.
4. Improve visualization with interactivity using tools like Plotly.

---

## Author
Samay Mehar  
*BTech in Artificial Intelligence and Data Science, IIT Jodhpur*  
[GitHub Repository](https://github.com/samay2504/FuelGrowth) (Optional: Placeholder for repository link)
```

This README is detailed enough for any user to set up and run the project while understanding each script's purpose and functionality.
