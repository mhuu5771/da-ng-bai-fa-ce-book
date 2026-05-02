from flask import Flask, render_template, request, jsonify
import requests
import logging

app = Flask(__name__)

# --- CẤU HÌNH FACEBOOK ---
# Nhập ID Fanpage của bạn vào đây
FB_PAGE_ID = 'YOUR_FACEBOOK_PAGE_ID'
FB_API_VERSION = 'v19.0'

# Cấu hình Logging để kiểm tra lỗi trên Terminal
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    """Hiển thị thẳng Dashboard M2V"""
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def handle_post():
    """Nhận nội dung từ 2 ô và đẩy lên Facebook"""
    data = request.json
    slot_1 = data.get('slot_1', '').strip()
    slot_2 = data.get('slot_2', '').strip()
    fb_token = data.get('access_token')

    # Kiểm tra điều kiện đầu vào
    if not fb_token:
        return jsonify({"status": "error", "error": "Vui lòng kết nối Facebook trước!"}), 400
    
    if not slot_1 or not slot_2:
        return jsonify({"status": "error", "error": "Nội dung không được để trống."}), 400

    # Hợp nhất nội dung với đường kẻ ngăn cách chuyên nghiệp
    combined_message = f"{slot_1}\n\n━━━━━━━━━━━━━━━\n\n{slot_2}"

    # Gửi tới Facebook Graph API
    fb_url = f"https://graph.facebook.com/{FB_API_VERSION}/{FB_PAGE_ID}/feed"
    payload = {
        'message': combined_message,
        'access_token': fb_token
    }

    try:
        response = requests.post(fb_url, data=payload, timeout=10)
        result = response.json()

        if response.status_code == 200 and 'id' in result:
            logging.info(f"Đăng bài thành công: {result['id']}")
            return jsonify({"status": "success", "message": "Đã đăng bài lên Fanpage thành công!"})
        else:
            fb_error = result.get('error', {}).get('message', 'Lỗi API Facebook')
            return jsonify({"status": "error", "error": f"FB: {fb_error}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": f"Lỗi hệ thống: {str(e)}"}), 500

if __name__ == '__main__':
    # Chạy trên localhost:5000
    app.run(host='0.0.0.0', port=5001, debug=True)