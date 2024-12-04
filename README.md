# README: Face Analysis from Videos with Performance Metrics Integration

This project aims to analyze faces from videos, link detected faces with their performance metrics, and calculate average performance for unique individuals. The workflow involves extracting face embeddings from videos using the `InsightFace` library, associating them with performance data, and exporting the results for further analysis.

---

## Table of Contents
1. [Project Setup](#project-setup)
2. [Workflow Overview](#workflow-overview)
3. [Code Explanation](#code-explanation)
   - [Step 1: Setup Directories](#step-1-setup-directories)
   - [Step 2: Load Data](#step-2-load-data)
   - [Step 3: Download Videos](#step-3-download-videos)
   - [Step 4: Extract Faces](#step-4-extract-faces)
   - [Step 5: Process Videos](#step-5-process-videos)
   - [Step 6: Calculate Average Performance](#step-6-calculate-average-performance)
   - [Step 7: Zip and Download Face Images](#step-7-zip-and-download-face-images)
4. [How to Run the Code](#how-to-run-the-code)
5. [Requirements](#requirements)
6. [Potential Errors and Troubleshooting](#potential-errors-and-troubleshooting)
7. [Results and Output](#results-and-output)

---

## Project Setup

### **Directory Structure**
- **`/content/videos/`**: Stores downloaded videos.
- **`/content/frames/`**: Stores face images extracted from videos.

### **Dependencies**
The following Python libraries are required:
- `os`: For directory and file handling.
- `cv2` (OpenCV): For video frame processing.
- `pandas`: For data handling.
- `insightface`: For face detection and recognition.
- `scikit-learn`: For cosine similarity calculations.
- `shutil`: For zipping files.
- `google.colab`: For uploading/downloading files in Google Colab.

---

## Workflow Overview

1. **Upload CSV Data**: Provide a CSV containing video URLs and performance metrics.
2. **Download Videos**: Videos from the given URLs are downloaded.
3. **Extract Faces**: Faces are detected in each video frame and saved as images.
4. **Identify Unique Faces**: Using face embeddings and cosine similarity, unique faces are identified.
5. **Link Faces to Performance**: Performance metrics from the CSV are linked to each unique face.
6. **Calculate Average Performance**: Computes the average performance metric for each unique face.
7. **Export Results**: Results are saved in a CSV and face images are zipped for download.

---

## Code Explanation

### Step 1: Setup Directories
```python
video_dir = "/content/videos/"
frame_dir = "/content/frames/"
os.makedirs(video_dir, exist_ok=True)
os.makedirs(frame_dir, exist_ok=True)
```
Creates directories to store videos and extracted face images.

---

### Step 2: Load Data
```python
def load_data():
    uploaded = files.upload()
    file_name = list(uploaded.keys())[0]
    data = pd.read_csv(file_name)
    data_cleaned = data.drop_duplicates(subset="Video URL").reset_index(drop=True)
    return data_cleaned
```
- **Purpose**: Uploads a CSV file containing video URLs and performance data.
- **Output**: Returns a cleaned DataFrame with no duplicate URLs.

---

### Step 3: Download Videos
```python
def download_video(video_url, save_dir):
    video_path = os.path.join(save_dir, os.path.basename(video_url))
    os.system(f"wget -q -O {video_path} {video_url}")
    return video_path
```
- **Purpose**: Downloads videos from provided URLs.
- **Output**: Saves the video file in the `/content/videos/` directory.

---

### Step 4: Extract Faces
```python
def extract_faces_from_video(video_path, output_dir):
    app = FaceAnalysis(allowed_modules=['detection', 'recognition'])
    app.prepare(ctx_id=0, det_thresh=0.5)
    ...
    return face_embeddings
```
- **Purpose**: Extracts faces from video frames using `InsightFace`.
- **Key Features**:
  - Processes every 10th frame for efficiency.
  - Saves all detected face images (both unique and duplicate).
  - Identifies unique faces using **cosine similarity** (threshold: 0.85).
- **Output**: Saves face images and returns a list of unique face embeddings.

---

### Step 5: Process Videos
```python
def process_videos(data, video_dir, frame_dir):
    influencer_faces = {}
    ...
    return influencer_faces
```
- **Purpose**: Processes all videos, extracts faces, and associates them with performance metrics.
- **Output**: Returns a dictionary of unique face embeddings and associated performance data.

---

### Step 6: Calculate Average Performance
```python
def calculate_average_performance(influencer_faces):
    results = []
    ...
    return pd.DataFrame(results)
```
- **Purpose**: Calculates the average performance metric for each unique face.
- **Output**: Returns a DataFrame with face image paths and average performance.

---

### Step 7: Zip and Download Face Images
```python
def download_all_faces(frame_dir, local_path):
    zip_path = "/content/frames.zip"
    shutil.make_archive("/content/frames", 'zip', frame_dir)
    files.download(zip_path)
```
- **Purpose**: Zips all face images and downloads them locally.

---

## How to Run the Code

1. **Set up Google Colab**:
   - Upload the code to a Colab notebook.
2. **Upload CSV File**:
   - Upload a CSV containing `Video URL` and `Performance` columns.
3. **Run the Code**:
   - Execute the provided script in Colab.
4. **Download Results**:
   - Results are saved as a CSV and face images are provided as a zipped file.

---

## Requirements

Install the required Python libraries:
```bash
pip install opencv-python pandas insightface scikit-learn
```

---

## Potential Errors and Troubleshooting

1. **`InsightFace` Initialization Error**:
   - Ensure GPU is available or set `ctx_id=-1` for CPU.
2. **Invalid Video URL**:
   - Verify URLs in the CSV file.
3. **Frame Skipping**:
   - The code logs skipped frames to handle processing errors gracefully.

---

## Results and Output

1. **`influencer_performance.csv`**:
   - Contains face image paths and their average performance metrics.
2. **Zipped Face Images**:
   - All face images extracted from the videos.
