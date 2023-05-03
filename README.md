# GrabIt 📺
A REST API to download Youtube videos.

## Example Usage

In order to download a Youtube video using 2 separate GET requests.

You can send the first `GET` request to `https://grab-it.onrender.com/youtube?url=<youtube-video-url>` where `<youtube-video-url>` is the URL to the Youtube video you want to download.
Since the server will retrieve the video when it receives the request, it can take a while depending on the size of the video.

The data will contain multiple fields representing the data of the video, but the field you need the most is `download_file_id` in order to download the file with the second `GET` request.

```json
{
  "success": false,
  "data": {
    ...
    "download_file_id": "01e15d35-d074-4ca7-9eaa-0acf9ecdf702",
    "duration": 12,
    "duration_string": "12",
    "dynamic_range": "SDR",
    "ext": "webm",
    "filesize_approx": 616626,
    "format": "248 - 1920x1080 (1080p)+251 - audio only (medium)",
    "format_id": "248+251",
    "format_note": "1080p+medium",
    "fps": 25,
    "fulltitle": "10 Seconds Timer with Music",
    "height": 1080,
    ...
  }
}
```
You will then need to grab the value at `download_file_id` send the second request to the endpoint `https://grab-it.onrender.com/download/<download_file_id>`.
The server will send back the downloaded Youtube file. The following is an example to download the file in Python:

```python
import wget # pip install wget

download_file_id = "01e15d35-d074-4ca7-9eaa-0acf9ecdf702"
endpoint = "https://grab-it.onrender.com/download/" + download_file_id

wget.download(endpoint, "C:/Users/hoang/Downloads/my_video.webm")
```
