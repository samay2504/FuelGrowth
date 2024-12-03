# -*- coding: utf-8 -*-
"""Round 2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-4IjnQ6qhT0ki-v9CMlYUx3g6gBWdCJg
"""

import torch
print("GPU Available:", torch.cuda.is_available())

!pip install insightface onnxruntime onnxruntime-gpu opencv-python-headless

import os
import cv2
import pandas as pd
from insightface.app import FaceAnalysis
import shutil
from google.colab import files

# Step 3: Setup Directories in Colab
video_dir = "/content/videos/"
frame_dir = "/content/frames/"
os.makedirs(video_dir, exist_ok=True)
os.makedirs(frame_dir, exist_ok=True)

# Step 4: Load Data
def load_data():
    """
    Uploads and loads the CSV file into a DataFrame.

    Returns:
        DataFrame: Cleaned data with video URLs and performance metrics.
    """
    uploaded = files.upload()
    file_name = list(uploaded.keys())[0]
    data = pd.read_csv(file_name)
    data_cleaned = data.drop_duplicates(subset="Video URL").reset_index(drop=True)
    return data_cleaned

# Step 5: Download Videos
def download_video(video_url, save_dir):
    """
    Downloads a video from the given URL and saves it in the specified directory.

    Args:
        video_url (str): URL of the video to download.
        save_dir (str): Directory to save the video.

    Returns:
        str: Path to the downloaded video.
    """
    video_path = os.path.join(save_dir, os.path.basename(video_url))
    os.system(f"wget -q -O {video_path} {video_url}")
    return video_path

# Step 6: Extract Unique Faces Using InsightFace
def extract_faces_from_video(video_path, output_dir):
    """
    Extracts unique faces from a video using InsightFace and saves them as images.

    Args:
        video_path (str): Path to the video file.
        output_dir (str): Directory to save face images.

    Returns:
        list: List of unique face embeddings found in the video.
    """
    app = FaceAnalysis(allowed_modules=['detection', 'recognition'])
    app.prepare(ctx_id=0, det_thresh=0.5)  # GPU (ctx_id=0), or CPU (ctx_id=-1)

    cap = cv2.VideoCapture(video_path)
    face_embeddings = []
    frame_count = 0
    skipped_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process every 10th frame
        if frame_count % 10 == 0:
            try:
                faces = app.get(frame)
                for face in faces:
                    embedding = face.normed_embedding
                    if not any((embedding == x).all() for x in face_embeddings):
                        face_embeddings.append(embedding)
                        x1, y1, x2, y2 = [int(v) for v in face.bbox]
                        face_image = frame[y1:y2, x1:x2]
                        if face_image.size > 0:
                            face_path = os.path.join(output_dir, f"face_{len(face_embeddings)}.jpg")
                            cv2.imwrite(face_path, face_image)
            except Exception as e:
                print(f"Error processing frame {frame_count}: {e}")

        frame_count += 1

    cap.release()
    print(f"Skipped frames in {os.path.basename(video_path)}: {skipped_frames}")
    return face_embeddings

# Step 7: Process Videos and Link Faces to Performance
def process_videos(data, video_dir, frame_dir):
    """
    Processes videos to detect faces and link them to performance metrics.

    Args:
        data (DataFrame): Cleaned DataFrame with video URLs and performance.
        video_dir (str): Directory to save downloaded videos.
        frame_dir (str): Directory to save detected face images.

    Returns:
        dict: Dictionary containing unique faces and associated performance.
    """
    influencer_faces = {}

    for idx, row in data.iterrows():
        video_url = row['Video URL']
        performance = row['Performance']

        print(f"Processing video {idx + 1}/{len(data)}...")

        try:
            # Download the video
            video_path = download_video(video_url, video_dir)
            # Extract faces
            faces = extract_faces_from_video(video_path, frame_dir)
            # Link performance to unique faces
            for face in faces:
                face_id = str(face.tolist())  # Convert embedding to a unique string
                if face_id not in influencer_faces:
                    influencer_faces[face_id] = {
                        "performance": [],
                        "face_path": os.path.join(frame_dir, f"face_{len(influencer_faces)+1}.jpg")
                    }
                influencer_faces[face_id]["performance"].append(performance)
        except Exception as e:
            print(f"Error processing {video_url}: {e}")
            continue

    return influencer_faces

# Step 8: Aggregate Results and Create the Table
def calculate_average_performance(influencer_faces):
    """
    Calculates the average performance for each unique influencer.

    Args:
        influencer_faces (dict): Dictionary of face embeddings and performance metrics.

    Returns:
        DataFrame: DataFrame containing face image paths and average performance.
    """
    results = []
    for face_id, info in influencer_faces.items():
        print(f"Performance List for Face {face_id}: {info['performance']}")  # Debugging
        avg_performance = sum(info['performance']) / len(info['performance'])
        results.append({"Face Image": info["face_path"], "Average Performance": avg_performance})
    return pd.DataFrame(results)

# Step 10: Zip Frames and Download
def download_frames(frame_dir, local_path):
    """
    Zips the frames directory and downloads it locally.

    Args:
        frame_dir (str): Directory containing the saved frames.
        local_path (str): Path to save the frames locally (e.g., Downloads).
    """
    # Zip the frames directory
    zip_path = "/content/frames.zip"
    shutil.make_archive("/content/frames", 'zip', frame_dir)

    # Download the zip file
    print(f"Downloading frames to {local_path}...")
    files.download(zip_path)

if __name__ == "__main__":
    # Load data from uploaded CSV file
    data_cleaned = load_data()

    # Process videos
    influencer_faces = process_videos(data_cleaned, video_dir, frame_dir)

    # Calculate average performance
    results_df = calculate_average_performance(influencer_faces)

    # Save results CSV
    results_csv = "/content/influencer_performance.csv"
    results_df.to_csv(results_csv, index=False)
    print(f"Results saved to {results_csv}")

    # Download results CSV
    files.download(results_csv)

    # Download frames locally
    download_frames(frame_dir, r"C:\Users\Samay Mehar\Downloads\frames")

import pandas as pd
from google.colab import files

# Step 1: Upload the CSV File
uploaded = files.upload()

# Step 2: Load the CSV File
file_name = list(uploaded.keys())[0]
data = pd.read_csv(file_name)

# Step 3: Clean Data by Removing Duplicate Influencers
# Drop duplicates based on similar average performance and same "Face Image"
# Assuming the "Face Image" names might differ slightly but unique embeddings exist
data_cleaned = data.drop_duplicates(subset=["Average Performance"], keep="first").reset_index(drop=True)

# Debugging output
print(f"Original Data Size: {data.shape[0]} rows")
print(f"Cleaned Data Size: {data_cleaned.shape[0]} rows")

# Step 4: Save the Cleaned Data to a New CSV File
cleaned_file_name = "cleaned_influencer_performance.csv"
data_cleaned.to_csv(cleaned_file_name, index=False)

print(f"Cleaned CSV saved as {cleaned_file_name}")

# Step 5: Optional - Download the Cleaned File
files.download(cleaned_file_name)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files

uploaded = files.upload()

file_name = list(uploaded.keys())[0]
data = pd.read_csv(file_name)

unique_data = data.drop_duplicates(subset=['Face Image']).reset_index(drop=True)

unique_data['Face Image Short'] = unique_data['Face Image'].apply(lambda x: x.split('/')[-1])

unique_data_sorted = unique_data.sort_values(by="Average Performance", ascending=False)

plt.figure(figsize=(16, 10))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 16), gridspec_kw={'height_ratios': [3, 1]})

top_20_data = unique_data_sorted.head(20)

palette = sns.color_palette("coolwarm", n_colors=20)

sns.barplot(
    x="Average Performance",
    y="Face Image Short",
    data=top_20_data,
    palette=palette,
    ax=ax1,
    orient='h',
    hue="Face Image Short",
    legend=False
)

ax1.set_title("Top 20 Influencers Performance", fontsize=16, fontweight='bold')
ax1.set_xlabel("Average Performance", fontsize=12)
ax1.set_ylabel("Influencer", fontsize=12)

for i, v in enumerate(top_20_data['Average Performance']):
    ax1.text(v, i, f' {v:.2f}', va='center', fontsize=10, color='gray')

sns.histplot(
    unique_data_sorted['Average Performance'],
    kde=True,
    color='skyblue',
    ax=ax2
)
ax2.set_title("Distribution of Influencer Performances", fontsize=14)
ax2.set_xlabel("Average Performance", fontsize=10)
ax2.set_ylabel("Frequency", fontsize=10)

plt.tight_layout()

print("\nPerformance Insights:")
print(f"Total Influencers: {len(unique_data)}")
print(f"Mean Performance: {unique_data['Average Performance'].mean():.2f}")
print(f"Median Performance: {unique_data['Average Performance'].median():.2f}")
print(f"Top Performer: {top_20_data.iloc[0]['Face Image Short']} (Performance: {top_20_data.iloc[0]['Average Performance']:.2f})")
print(f"Bottom Performer: {unique_data_sorted.iloc[-1]['Face Image Short']} (Performance: {unique_data_sorted.iloc[-1]['Average Performance']:.2f})")

plt.savefig('influencer_performance.png', dpi=300, bbox_inches='tight')

plt.show()