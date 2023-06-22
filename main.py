from flask import Flask, render_template, request, jsonify
from datetime import datetime
from configs import configs
import psycopg2
import os
import matplotlib.pyplot as plt
import numpy as np
from googleapiclient.discovery import build
from google.oauth2 import service_account
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# credentials = service_account.Credentials.from_service_account_file('path/to/service_account.json')
#scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/webmasters.readonly'])
#service = build('webmasters', 'v3', credentials=scoped_credentials)



@app.route('/')
def landing():
  return render_template("landing.html")

@app.route('/home')
def index():
    is_admin = request.args.get('admin')  # Check if 'admin' parameter is present in the URL
    if is_admin:
        return render_template('admin_dashboard.html', is_admin=True)
    else:
        return render_template('index.html')

# Function to fetch search visibility data from Google Search Console API
def fetch_search_visibility():
    # Specify your website's URL
    site_url = 'https://example.com/'

    # Fetch search analytics data from the API
    response = service.searchanalytics().query(
        siteUrl=site_url,
        body={
            'startDate': '2023-06-01',
            'endDate': '2023-06-30',
            'dimensions': ['query'],
            'rowLimit': 10
        }
    ).execute()

    # Process the API response and extract visibility data
    visibility_data = response.get('rows', [])
    search_engines = []
    visibility_counts = []

    for data in visibility_data:
        search_engines.append(data['keys'][0])
        visibility_counts.append(data['clicks'])

    return search_engines, visibility_counts






# Route for the detailspage
@app.route('/listing')
def listing():
    return render_template('listing.html')

# Route to fetch all posts
@app.route('/posts')
def get_posts():
    conn = psycopg2.connect(
        host=configs.db_host, dbname=configs.db_name, user=configs.db_user, password=configs.db_password
    )
    cursor = conn.cursor()
    create_script='''
            CREATE TABLE IF NOT EXISTS posts(
                id SERIAL PRIMARY KEY,
                username VARCHAR (50),
                image TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_admin BOOLEAN DEFAULT FALSE

            )
    '''

    select_query = "SELECT * FROM posts"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    posts = []
    for row in rows:
        post_id, username, image, description, created_at, is_admin = row
        posts.append({
            'id': post_id,
            'username': username,
            'image': image,
            'description': description,
            'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_admin': is_admin
        })

    cursor.close()
    conn.close()

    return jsonify(posts)

# Route to edit a post
@app.route('/edit_post/<int:post_id>', methods=['POST'])
def edit_post(post_id):
    new_description = request.json['description']

    conn = psycopg2.connect(
        host=db_host, dbname=db_name, user=db_user, password=db_password
    )
    cursor = conn.cursor()

    update_query = "UPDATE posts SET description = %s WHERE id = %s"
    cursor.execute(update_query, (new_description, post_id))

    conn.commit()
    cursor.close()
    conn.close()

    return {'message': 'Post updated successfully'}

# Route to delete a post
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    conn = psycopg2.connect(
        host=db_host, dbname=db_name, user=db_user, password=db_password
    )
    cursor = conn.cursor()

    delete_query = "DELETE FROM posts WHERE id = %s"
    cursor.execute(delete_query, (post_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return {'message': 'Post deleted successfully'}

@app.route('/admin')
def admin_dashboard():
    conn = psycopg2.connect(
        host=configs.db_host, dbname=configs.db_name, user=configs.db_user, password=configs.db_password
    )
    cursor = conn.cursor()
    # Visitor count
    # cursor.execute("SELECT COUNT(*) FROM visitors")
    # visitor_count = cursor.fetchone()[0]

    # Fetch posts
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()

    # Google search visibility pie chart
    search_engines, visibility_counts = fetch_search_visibility()

    # Render admin dashboard template
    return render_template('admin_dashboard.html', visitor_count=visitor_count, posts=posts, search_engines=search_engines, visibility_counts=visibility_counts)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')


# Submit contact form route
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    email = request.form['email']
    name = request.form['name']
    comment = request.form['comment']

    # Send email to admin
    send_email(email, name, comment)

    # Redirect to thank you page
    return render_template('thank_you.html')

# Function to send email to admin
def send_email(email, name, comment):
    admin_email = 'ssebugenyimaluufu@gmail.com'  # Replace with admin's email address
    smtp_server = 'smtp.gmail.com'  # Replace with SMTP server address
    smtp_port = 587  # Replace with SMTP server port number
    smtp_username = 'ssebugenyimaluufu@gmail.com'  # Replace with SMTP server username
    smtp_password = 'Ssebugenyijuma95'  # Replace with SMTP server password

    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\n\nComment or Question:\n{comment}")

    msg['Subject'] = f"New Contact Form Submission from {name}"
    msg['From'] = admin_email
    msg['To'] = admin_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


if __name__ == '__main__':
    app.run(debug=True)
