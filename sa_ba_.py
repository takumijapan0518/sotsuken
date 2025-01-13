from flask import Flask, render_template_string, send_from_directory, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

# HTMLテンプレート
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>位置情報を取得</title>
</head>
<body>
    <h1>位置情報を取得</h1>
    <h2><font color="red">※表示後、最新のマップを閲覧したい場合はこのページに戻り、もう一度下のボタンを押してください！！</font></h2>
    
    <button onclick="getLocation()">位置情報を取得してマップを表示</button>
    <p id="demo"></p>
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition, showError);
            } else {
                document.getElementById("demo").innerHTML = "Geolocation is not supported by this browser.";
            }
        }

        function showPosition(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            fetch(`/location`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ lat: latitude, lon: longitude })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);  // レスポンス確認
                document.getElementById("demo").innerHTML = data.message;
                if (data.status === "success") {
                    window.location.href = "/map?_=" + new Date().getTime();
                }
            });
        }

        function showError(error) {
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    document.getElementById("demo").innerHTML = "User denied the request for Geolocation.";
                    break;
                case error.POSITION_UNAVAILABLE:
                    document.getElementById("demo").innerHTML = "Location information is unavailable.";
                    break;
                case error.TIMEOUT:
                    document.getElementById("demo").innerHTML = "The request to get user location timed out.";
                    break;
                case error.UNKNOWN_ERROR:
                    document.getElementById("demo").innerHTML = "An unknown error occurred.";
                    break;
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/location", methods=["POST"])
def location():
    try:
        data = request.json
        lat = data.get("lat")
        lon = data.get("lon")

        with open("location.json", "w") as f:
            json.dump({"latitude": lat, "longitude": lon}, f)

        script_path = 'new now.py'
        result = subprocess.run(['python', script_path], capture_output=True, text=True)

        if result.returncode != 0:
            app.logger.error(f"Script error: {result.stderr}")
            return jsonify({"status": "error", "message": "Script execution failed.", "details": result.stderr})

        app.logger.info(result.stdout)
        return jsonify({"status": "success", "message": "Script executed successfully and map generated."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error occurred: {str(e)}"})

@app.route("/map")
def serve_map():
    try:
        file_path = os.path.join('static', 'map_with_path.html')
        if not os.path.exists(file_path):
            return "マップが生成されていません。スクリプトを確認してください。"
        return send_from_directory('static', 'map_with_path.html')
    except Exception as e:
        app.logger.error(f"Error serving map: {str(e)}")
        return f"エラーが発生しました: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)