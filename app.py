import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, flash, redirect, url_for
from Database import *
import pickle

app = Flask(__name__)

global filename
filename = ""

app.secret_key = os.environ.get('SECRET_KEY', 'super-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Lazy-load model so app starts even if numpy/sklearn not ready
_loaded_model = None

def get_model():
    global _loaded_model
    if _loaded_model is None:
        path = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(path, 'models', 'rf_classifier.pkl')
        _loaded_model = pickle.load(open(model_path, 'rb'))
    return _loaded_model

@app.route("/")
def index():
    return render_template("index.html", xx=-1)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', xx=-1)

@app.route('/index')
def index1():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/register', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        mobile = 0
        InsertData(username, email, password, mobile)
        return render_template('login.html')
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        passw = request.form['password']
        resp = read_cred(email, passw)
        if resp != None:
            return redirect("/dashboard")
        else:
            message = "Username and/or Password incorrect. You have not registered yet. Go to Register page."
            return "<script type='text/javascript'>alert('{}');</script>".format(message)
    return render_template('login.html')

# {'Dos': 0, 'Probe': 1, 'R2L': 2, 'U2R': 3, 'normal': 4}
def decode(output):
    if output == 0:
        return 'Dos Attack Found in Packet'
    elif output == 1:
        return 'Probe Attack Found in Packet'
    elif output == 2:
        return 'R2L Attack Found in Packet'
    elif output == 3:
        return 'U2R Attack Found in Packet'
    elif output == 4:
        return 'Normal Packet'

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            input_data = [
                float(request.form["duration"]),
                int(request.form["protocol_type"]),
                int(request.form["service"]),
                int(request.form["flag"]),
                float(request.form["src_bytes"]),
                float(request.form["dst_bytes"]),
                float(request.form["land"]),
                float(request.form["wrong_fragment"]),
                float(request.form["urgent"]),
                float(request.form["hot"]),
                float(request.form["num_failed_logins"]),
                float(request.form["logged_in"]),
                float(request.form["num_compromised"]),
                float(request.form["root_shell"]),
                float(request.form["su_attempted"]),
                float(request.form["num_file_creations"]),
                float(request.form["num_shells"]),
                float(request.form["num_access_files"]),
                float(request.form["num_outbound_cmds"]),
                float(request.form["is_host_login"]),
                float(request.form["is_guest_login"]),
                float(request.form["count"]),
                float(request.form["srv_count"]),
                float(request.form["serror_rate"]),
                float(request.form["rerror_rate"]),
                float(request.form["same_srv_rate"]),
                float(request.form["diff_srv_rate"]),
            ]
            attack_type = decode(get_model().predict([input_data])[0])
            if attack_type == "Normal Packet":
                return render_template("dashboard.html", attack=attack_type, safe='yes')
            else:
                return render_template("dashboard.html", attack=attack_type)
        except Exception as e:
            return render_template("dashboard.html", attack=f"Error: {str(e)}")
    return render_template("dashboard.html", xx=-1)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', error='No selected file')
        try:
            import pandas as pd
            df = pd.read_csv(file)
            has_actual_label = 'label' in df.columns
            actual_labels = None
            if has_actual_label:
                actual_labels = df['label'].tolist()
                df = df.drop('label', axis=1)
            predictions = get_model().predict(df)
            label_mapping = {0: 'Dos', 1: 'Probe', 2: 'R2L', 3: 'U2R', 4: 'normal'}
            reverse_mapping = {'Dos': 0, 'Probe': 1, 'R2L': 2, 'U2R': 3, 'normal': 4}
            response = []
            for i, pred in enumerate(predictions):
                class_index = int(pred)
                result = {'sr_no': i+1, 'class_index': class_index, 'class_name': label_mapping[class_index]}
                if has_actual_label:
                    actual = actual_labels[i]
                    if isinstance(actual, (int, float)) or (isinstance(actual, str) and actual.isdigit()):
                        actual = int(actual)
                        actual_name = label_mapping.get(actual, f"Unknown ({actual})")
                    else:
                        actual_name = actual
                        actual = reverse_mapping.get(actual, -1)
                    result['actual_index'] = actual
                    result['actual_name'] = actual_name
                    result['match'] = class_index == actual
                response.append(result)
            return render_template('upload.html', predictions=response, has_actual=has_actual_label)
        except Exception as e:
            return render_template('upload.html', error=str(e))
    return render_template('upload.html', error=None)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
