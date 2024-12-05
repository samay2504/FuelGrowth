import os
import pandas as pd
import base64

def generate_html_table_with_faces(csv_path, frames_dir, output_html):
    """
    Creates an HTML table displaying each unique influencer's face alongside their average performance.

    Args:
        csv_path (str): Path to the influencer performance CSV file.
        frames_dir (str): Path to the folder containing influencer face images.
        output_html (str): Path to save the generated HTML file.
    """
    # Load the CSV file
    influencer_data = pd.read_csv(csv_path)

    # Initialize an HTML table
    table_html = """
    <html>
    <head>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                text-align: center;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
            }
            img {
                max-width: 100px;
                max-height: 100px;
            }
        </style>
    </head>
    <body>
        <h2>Influencer Performance Table</h2>
        <table>
            <tr>
                <th>Face</th>
                <th>Average Performance</th>
            </tr>
    """

    # Iterate through each row in the CSV
    for _, row in influencer_data.iterrows():
        face_image_path = row['Face Image']
        avg_performance = row['Average Performance']

        # Resolve the full path for the face image
        face_full_path = os.path.join(frames_dir, os.path.basename(face_image_path))

        # Check if the image exists
        if not os.path.exists(face_full_path):
            print(f"File not found: {face_full_path}")
            continue

        # Read and encode the image to base64 for embedding in HTML
        with open(face_full_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Append a row to the HTML table
        table_html += f"""
        <tr>
            <td><img src="data:image/jpeg;base64,{image_base64}" alt="Face"></td>
            <td>{avg_performance:.2f}</td>
        </tr>
        """

    # Close the table and HTML structure
    table_html += """
        </table>
    </body>
    </html>
    """

    # Write the HTML to a file
    with open(output_html, "w") as html_file:
        html_file.write(table_html)

    print(f"HTML table saved to {output_html}")

# Example usage
csv_path = r"D:\Projects\FuelGrowth\name convention\cleaned_influencer_performance.csv" # Path to the influencer performance CSV
frames_dir = r"D:\Projects\FuelGrowth\name convention\frames"  # Path to the frames folder
output_html = r"D:\Projects\FuelGrowth\name convention\influencer_performance_table.html"  # Path to save the HTML table

generate_html_table_with_faces(csv_path, frames_dir, output_html)
