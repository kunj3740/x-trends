from flask import Flask, render_template_string
from social_scraper import SocialMediaScraper
import json

app = Flask(__name__)
social_tracker = SocialMediaScraper()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Social Media Pulse</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #4b0082 0%, #2e006e 100%);
            color: #e4e4e4;
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
        }

        .dashboard-container {
            max-width: 500px;
            margin: auto;
            background: rgba(63, 81, 181, 0.95);
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 20px;
        }

        .dashboard-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            color: #fff;
            text-align: center;
            letter-spacing: 0.5px;
        }

        .topic-card {
            padding: 16px 24px;
            margin: 8px 0;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 500;
            color: #fff;
            background: rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
            cursor: pointer;
            display: flex;
            align-items: center;
        }

        .topic-card:before {
            content: "#";
            margin-right: 10px;
            color: #1d9bf0;
            font-weight: 700;
        }

        .topic-card:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }

        .update-btn {
            background: linear-gradient(45deg, #1d9bf0 0%, #1a8cd8 100%);
            color: white;
            border: none;
            padding: 16px 32px;
            border-radius: 30px;
            cursor: pointer;
            font-weight: 600;
            margin-top: 30px;
            font-size: 16px;
            width: 100%;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(29, 155, 240, 0.2);
        }

        .update-btn:hover {
            background: linear-gradient(45deg, #1a8cd8 0%, #1577b8 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(29, 155, 240, 0.3);
        }

        .last-update {
            font-size: 14px;
            color: #8b949e;
            margin-top: 25px;
            text-align: center;
            font-weight: 500;
        }

        .data-section {
            max-width: 500px;
            margin: 20px auto;
            background: rgba(63, 81, 181, 0.95);
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .data-header {
            font-size: 18px;
            color: #8b949e;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        }

        .data-content {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            font-family: monospace;
            white-space: pre-wrap;
            word-break: break-word;
            color: #e4e4e4;
            font-size: 14px;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .topic-card {
            animation: slideIn 0.5s ease forwards;
            animation-delay: calc(var(--index) * 0.1s);
            opacity: 0;
        }

        @media (max-width: 600px) {
            .dashboard-container, .data-section {
                margin: 10px;
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="dashboard-title">Social Media Trends</div>
        {% if result %}
            {% for i in range(1, 6) %}
                {% set topic = result["topicname" ~ i] %}
                {% if topic != "No topic available" %}
                    <div class="topic-card" style="--index: {{ i }}">{{ topic }}</div>
                {% endif %}
            {% endfor %}
            <button onclick="window.location.href='/update'" class="update-btn">Refresh Feed</button>
            <div class="last-update">Updated: {{ result.timestamp.strftime('%Y-%m-%d %H:%M:%S') }}</div>
        {% else %}
            <button onclick="window.location.href='/update'" class="update-btn">Load Topics</button>
        {% endif %}
    </div>

    {% if result %}
    <div class="data-section">
        <div class="data-header">Database Record</div>
        <div class="data-content">
{
    "_id": "{{ result._id }}",
    "topicname1": "{{ result.topicname1 }}",
    "topicname2": "{{ result.topicname2 }}",
    "topicname3": "{{ result.topicname3 }}",
    "topicname4": "{{ result.topicname4 }}",
    "timestamp": "{{ result.timestamp.strftime('%Y-%m-%d %H:%M:%S') }}",
    "ip_address": "{{ result.ip_address }}"
}</div>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/update')
def update_topics():
    result = social_tracker.fetch_trending_topics()
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(debug=True)