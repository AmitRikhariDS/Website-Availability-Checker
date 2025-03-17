from flask import Flask, render_template, request, redirect, url_for
import smtplib
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
sent = 0  # Global flag to track if the email was sent

SENDER_EMAIL = "techyink011@gmail.com"
SENDER_PASSWORD = "fyze kbcu spvp lzgf"
# RECEIVER_EMAIL = "amitrikhari011@gmail.com"

def setup_driver():
    """Initialize and return a headless Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def send_email(url,RECEIVER_EMAIL):
    """Send an email notification when the website is up."""
    subject = "Website is UP!"
    body = f"The website {url} is now accessible. You can check it."

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

def check_website(url,RECEIVER_EMAIL):
    """Check if the website is up (Max retries: 10)."""
    global sent  # Correct way to use global variables
    driver = setup_driver()
    max_retries = 10

    for _ in range(max_retries):
        try:
            driver.get(url)
            if driver.title:  # If page loads, title is non-empty
                print(f"🎉 Website {url} is UP!")
                send_email(url,RECEIVER_EMAIL)  # Send email notification
                sent = 1  # Update global flag
                driver.quit()
                return True
        except WebDriverException:
            print(f"⏳ {url} is DOWN... Retrying in 30 seconds.")
        
        time.sleep(30)  # Wait before retrying

    driver.quit()
    return False

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        url = request.form['websiteUrl']
        RECEIVER_EMAIL = request.form['RECEIVER_EMAIL']

        return redirect(url_for('result', url=url,RECEIVER_EMAIL=RECEIVER_EMAIL))
    return render_template("index.html")

@app.route("/result")
def result():
    url = request.args.get("url")
    RECEIVER_EMAIL=request.args.get("RECEIVER_EMAIL")
    
    if not url:
        return render_template("error.html", message="No URL provided!"), 400

    status = check_website(url,RECEIVER_EMAIL)
    
    return render_template("success.html", url=url, sent=sent) if status else render_template("failure.html", url=url, sent=sent)

if __name__ == "__main__":
    app.run(debug=True)
