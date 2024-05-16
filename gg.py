import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from user_agents import parse

def get_public_ip_address():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"Failed to retrieve public IP address: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_location(ip_address):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        if response.status_code == 200:
            data = response.json()
            return data.get('city', 'Unknown'), data.get('region', 'Unknown'), data.get('country', 'Unknown')
        else:
            print(f"Failed to retrieve location: {response.status_code}")
            return 'Unknown', 'Unknown', 'Unknown'
    except Exception as e:
        print(f"Error: {e}")
        return 'Unknown', 'Unknown', 'Unknown'

def get_device_type(user_agent_string):
    user_agent = parse(user_agent_string)
    if user_agent.is_mobile:
        return "Mobile"
    elif user_agent.is_tablet:
        return "Tablet"
    elif user_agent.is_pc:
        return "PC"
    else:
        return "Unknown"

def send_email(sender_email, sender_password, recipient_email, username, user_agent_string):
    ip_address = get_public_ip_address()
    if ip_address:
        city, region, country = get_location(ip_address)
        device_type = get_device_type(user_agent_string)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        subject = "Login Alert"
        body = (f"Hello {username}, we noticed a login to your account. Please check if this was you. "
                f"If not, we recommend changing your password.\n\n"
                f"Your device's public IP address: {ip_address}\n"
                f"Approximate Location: {city}, {region}, {country}\n"
                f"Device Type: {device_type}\n"
                f"Time of the login: {current_time}")

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")

# Your Flask app
from flask import Flask, request

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email_from_flask():
    username = request.form.get('username')
    sender_email = "yesssziif@gmail.com"
    sender_password = "uhey jgpf otmx afrj"
    recipient_email = "mohamedidrisshamadi@gmail.com"
    user_agent_string = request.headers.get('User-Agent')
    
    send_email(sender_email, sender_password, recipient_email, username, user_agent_string)
    
    return "Email sent successfully!"

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
