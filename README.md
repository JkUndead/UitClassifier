## File Structure
* app_name
  * app.py: Flask API application
  * requirements.txt: list of packages that the app will import
  * models: directory that contains the pickled/json model files



## Testing the API
1. Run the Flask API locally for testing. Go to directory with `app.py`.

```bash
python app.py
```


2. In a new terminal window, use HTTPie to make a GET request at the URL of the API.

```bash
http http://127.0.0.1:5000/ query=="Nguyễn Thị Minh Khai"
```


3. Example of successful output.

```bash
HTTP/1.0 200 OK
Content-Length: 57
Content-Type: application/json
Date: Tue, 21 Aug 2018 19:04:04 GMT
Server: Werkzeug/0.14.1 Python/3.6.3

{
    "prediction": "Female",
    "confidence": 99.68,
}
```