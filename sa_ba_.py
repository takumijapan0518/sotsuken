from flask import Flask, render_template_string, send_from_directory, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>位置情報を取得</title>
    
    <style>
        /* ボディ全体のフォントサイズと中央寄せ */
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        
        h1 {
            font-size: 40px; /* タイトルを大きく */
            margin-bottom: 20px;
        }
        
        h2 {
            font-size: 32px; /* 説明文のフォントサイズ */
            color: red;
            margin-bottom: 30px;
        }

        #demo {
            font-size: 18px; /* 結果表示用テキストを大きく */
            margin-top: 20px;
        }

        /* ボタンのスタイル */
        button {
            font-size: 24px; /* ボタン内の文字を大きく */
            padding: 15px 30px; /* ボタン全体を大きく */
            margin-top: 20px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3; /* ホバー時の色変更 */
        }
    </style>
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
                console.log(data);
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
        if not data or 'lat' not in data or 'lon' not in data:
            return jsonify({"status": "error", "message": "Invalid JSON data, 'lat' and 'lon' are required"})

        lat = data.get("lat")
        lon = data.get("lon")

        file_path = os.path.join(os.getcwd(), "location.json")
        with open(file_path, "w") as f:
            json.dump({"latitude": lat, "longitude": lon}, f)

        script_path = 'new now.py'
        result = subprocess.run(['python', script_path], capture_output=True, text=True)

        if result.returncode != 0:
            app.logger.error(f"Script error: {result.stderr or result.stdout}")
            return jsonify({"status": "error", "message": "Script execution failed.", "details": result.stderr or result.stdout})

        app.logger.info(result.stdout)
        return jsonify({"status": "success", "message": "位置情報が保存されました。マップを表示します。"})

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"status": "error", "message": f"Error occurred: {str(e)}"})

@app.route("/map")
def serve_map():
    try:
        return send_from_directory('static', 'map_with_path.html')
    except Exception as e:
        app.logger.error(f"Error serving map: {str(e)}")
        return f"エラーが発生しました: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
