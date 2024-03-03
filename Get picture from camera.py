import requests

# URL of the picture
picture_url = "http://192.168.1.185/capture"

# Send a GET request to the URL
response = requests.get(picture_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Specify the file path to save the image
    file_path = "captured_picture.jpg"

    # Save the image content to a file
    with open(file_path, "wb") as f:
        f.write(response.content)

    print("Picture saved successfully as:", file_path)
else:
    print("Failed to fetch picture. Status code:", response.status_code)
