# from flask import Flask, render_template, request
# import socket
# import requests
# import tldextract
# import ipinfo

# app = Flask(__name__)

# # IPinfo Token (optional)
# access_token = ''  # ← চাইলে ipinfo.io থেকে token বসাও
# handler = ipinfo.getHandler(access_token)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     result = ""
#     url = request.form.get('url')
#     ip_input = request.form.get('ip')

#     if url:
#         try:
#             ext = tldextract.extract(url)
#             domain = f"{ext.domain}.{ext.suffix}"
#             ip = socket.gethostbyname(domain)
#             response = requests.get(url, timeout=5)
#             status_code = response.status_code
#             details = handler.getDetails(ip)

#             result += f"🔍 URL: {url}<br>"
#             result += f"🌐 Domain: {domain}<br>"
#             result += f"🧠 IP Address: {ip}<br>"
#             result += f"📶 HTTP Status: {status_code}<br>"
#             result += f"📍 Country: {details.country_name}<br>"
#             result += f"🏙 City: {details.city}<br>"
#             result += f"🏢 ISP: {details.org}<br><br>"

#         except Exception as e:
#             result += f"<b>URL Analysis Error:</b> {e}<br><br>"

#     if ip_input:
#         try:
#             url = f"http://ip-api.com/json/{ip_input}"
#             response = requests.get(url)
#             data = response.json()

#             result += f"🔍 IP Address: {ip_input}<br>"
#             result += f"📍 Country: {data['country']}<br>"
#             result += f"🏙 Region: {data['regionName']}<br>"
#             result += f"🌆 City: {data['city']}<br>"
#             result += f"🏢 ISP: {data['isp']}<br>"
#             result += f"🕒 Timezone: {data['timezone']}<br>"
#             result += f"📌 Coordinates: {data['lat']}, {data['lon']}<br>"

#         except Exception as e:
#             result += f"<b>IP Tracking Error:</b> {e}"

#     return render_template('index.html', result=result)

# if __name__ == '__main__':
#     app.run(debug=True)








from flask import Flask, render_template, request
import socket
import requests
import tldextract
import ipinfo

app = Flask(__name__)

# IPinfo Token (optional)
access_token = ''  # ← চাইলে ipinfo.io থেকে token বসাও
handler = ipinfo.getHandler(access_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    result = ""
    url = request.form.get('url')
    ip_input = request.form.get('ip')

    if url:
        try:
            # যদি URL-এ http:// বা https:// না থাকে, তাহলে নিজেরা যোগ করি
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url

            ext = tldextract.extract(url)
            domain = f"{ext.domain}.{ext.suffix}"
            ip = socket.gethostbyname(domain)
            response = requests.get(url, timeout=5)
            status_code = response.status_code
            details = handler.getDetails(ip)

            result += f"🔍 URL: {url}<br>"
            result += f"🌐 Domain: {domain}<br>"
            result += f"🧠 IP Address: {ip}<br>"
            result += f"📶 HTTP Status: {status_code}<br>"
            result += f"📍 Country: {details.country_name}<br>"
            result += f"🏙 City: {details.city}<br>"
            result += f"🏢 ISP: {details.org}<br><br>"

        except Exception as e:
            result += f"<b>URL Analysis Error:</b> {e}<br><br>"

    if ip_input:
        try:
            url = f"http://ip-api.com/json/{ip_input}"
            response = requests.get(url)
            data = response.json()

            if data['status'] == 'fail':
                result += f"<b>IP Tracking Error:</b> {data['message']}<br>"
            else:
                result += f"🔍 IP Address: {ip_input}<br>"
                result += f"📍 Country: {data.get('country', 'N/A')}<br>"
                result += f"🏙 Region: {data.get('regionName', 'N/A')}<br>"
                result += f"🌆 City: {data.get('city', 'N/A')}<br>"
                result += f"🏢 ISP: {data.get('isp', 'N/A')}<br>"
                result += f"🕒 Timezone: {data.get('timezone', 'N/A')}<br>"
                result += f"📌 Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}<br>"

        except Exception as e:
            result += f"<b>IP Tracking Error:</b> {e}<br>"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
