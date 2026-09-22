from flask import Flask, request, jsonify
from dotenv import load_dotenv
from functools import wraps
from flask_cors import CORS
import os
import requests
import traceback

load_dotenv() #Setting environmental variables - in this case link and anon key to the database

app = Flask(__name__)
CORS(app)

#Declare link and anon key of the database
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

#Create clients for Supabase database server
from supabase import create_client, Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#Creating an uniformed request header
HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

#Defining the routing path for each request
def api_url(path):
    return f"{SUPABASE_URL}/rest/v1/{path}"

#Confirming the login status of user
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #Check for user's access token in header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Please login first.'}), 401 #Returning error message when user tries to access contents for logged in users as guest
        try:
            token = token.replace('Bearer ', '') #Checking the user's access token
            user = supabase.auth.get_user(token)
            request.user = user
            request.token = token

            user_id = user.user.id
            profile_resp = requests.get(
                api_url(f'profiles?id=eq.{user_id}&select=role'),
                headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer{token}'}
            )
            if profile_resp.status_code == 200 and profile_resp.json():
                request.user_role = profile_resp.json()[0]['role']
            else:
                request.user_role = 'user'
        except Exception as e: #Returning error message when token is invalid or expired
            traceback.print_exc()
            return jsonify({'error': 'Access token invalid or expired'}), 401
        return f(*args, **kwargs)             
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': '请先登录'}), 401
        try:
            token = auth_header.replace('Bearer ', '')
            user = supabase.auth.get_user(token)
            request.user = user
            request.token = token

            user_id = user.user.id
            profile_resp = requests.get(
                api_url(f'profiles?id=eq.{user_id}&select=role'),
                headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {token}'}
            )
            if profile_resp.status_code == 200 and profile_resp.json():
                role = profile_resp.json()[0]['role']
            else:
                role = 'user'

            if role != 'admin':
                return jsonify({'error': '需要管理员权限'}), 403

            request.user_role = role
        except Exception as e:
            traceback.print_exc()
            return jsonify({'error': '令牌无效或已过期'}), 401
        return f(*args, **kwargs)
    return decorated_function



#data fetching test with welcome message
@app.route('/api/welcome', methods=['GET'])
def welcome():
    return jsonify('Hello, world! Man, what can I say?')

# Get all articles
@app.route('/api/articles', methods=['GET'])
def get_articles():
    try:
        #Select all articles in database
        resp = requests.get(api_url('article?select=*'), headers=HEADERS) 
        #Check status of request
        resp.raise_for_status()
        return jsonify(resp.json()) #Return the articles as jsonified data
    except requests.exceptions.RequestException as e: #Returning error message when an error happens.
        return jsonify({'error': str (e)}), 500

#Get individual articles by ID
@app.route('/api/articles/<int:id>', methods=['GET'])
def get_article(id):
    try:
        #Select articles by ID
        resp = requests.get(api_url(f'article?id=eq.{id}'), headers=HEADERS)
        #Check status of request
        resp.raise_for_status()
        data = resp.json()
        #Returning error message when article with chosen ID is not found
        if not data:
            return jsonify({'error': 'Article not found'}), 404
        return jsonify(data[0])
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

#Creating new articles
@app.route('/api/articles', methods=['POST'])
@admin_required
def create_article():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'The title and content cannot be blank!'}), 400
    try:
        resp = requests.post(
            api_url('article'),
            json=data,
            headers={**HEADERS, 'prefer': 'return=representation'}
        )
        resp.raise_for_status()
        return jsonify(resp.json()), 201
    except requests.exceptions.RequestException as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

#Updating existing articles
@app.route('/api/articles/<int:id>', methods=['PUT'])
@admin_required
def update_article(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'The body cannot be empty.'}), 400
    try:
        resp = requests.patch(
            api_url(f'article?id=eq.{id}'),
            json=data,
            headers={**HEADERS, 'Prefer': 'return=representation'}
        )
        if resp.status_code == 200 and resp.json():
            return jsonify(resp.json()[0])
        else:
            return jsonify({'error': 'Article not found.'}), 404
    except requests.exceptions.RequestException as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

#Deleting articles
@app.route('/api/articles/<int:id>', methods=['DELETE'])
@admin_required
def delete_article(id):
    try:
        resp = requests.delete(api_url(f'article?id=eq.{id}'), headers=HEADERS)
        if resp.status_code == 204:
            return '', 204
        else:
            return jsonify({'error': 'Article not found.'}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

#User registration
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password cannot be blank!'}), 400

    try:
        res = supabase.auth.sign_up({'email': email, 'password': password})
        return jsonify({
            'message': 'Registration successful, check your email for confirmation link' if res.user.identities else 'Registration successful',
            'user':{
                'id': res.user.id,
                'email': res.user.email
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

#User login
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password cannot be blank!'}), 400

    try:
        res = supabase.auth.sign_in_with_password({'email': email, 'password': password})
        return jsonify({
            'message': 'Registration successful',
            'access_token': res.session.access_token,
            'user':{
                'id': res.user.id,
                'email': res.user.email
            }
        }), 200
    except Exception as e:
        return jsonify({'error': 'Incorrect email or password!'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=3000)

