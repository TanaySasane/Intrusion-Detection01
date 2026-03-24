import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, flash, redirect, url_for
from Database import *
import pickle
import pandas as pd

app = Flask(__name__)

global filename
filename = ""

app.secret_key = os.environ.get('SECRET_KEY', 'super-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html", xx= -1)

@app.route('/dashboard')
def dashboard():
   return render_template('dashboard.html', xx= -1)

@app.route('/index')
def index1():
   return render_template('index.html')


@app.route('/home')
def home():
   return render_template('index.html')


@app.route('/aboutus')
def aboutus():
   return render_template('aboutus.html')

@app.route('/register',methods = ['POST','GET'])
def registration():
	if request.method=="POST":
		username = request.form["username"]
		email = request.form["email"]
		password = request.form["password"]
		mobile = 0
		InsertData(username,email,password,mobile)
		return render_template('login.html')
		
	return render_template('register.html')


@app.route('/login',methods = ['POST','GET'])
def login():
   if request.method=="POST":
        email = request.form['email']
        passw = request.form['password']
        resp = read_cred(email, passw)
        if resp != None:
            return redirect("/dashboard")
        else:
            message = "Username and/or Password incorrect.\\n        Yo have not registered Yet \\nGo to Register page and do Registration";
            return "<script type='text/javascript'>alert('{}');</script>".format(message)

   return render_template('login.html')


# {'Dos': 0, 'Probe': 1, 'R2L': 2, 'U2R': 3, 'normal': 4}
def decode(output):
    print(output)
    if output ==0:
        return 'Dos Attack Found in Packet'
    elif output ==1:
        return 'Probe Attack Found in Packet'
    elif output ==2:
        return 'R2L Attack Found in Packet'
    elif output ==3:
        return 'U2R Attack Found in Packet'
    elif output ==4:
        return 'Normal Packet'


import pickle
import os
path = os.getcwd()
model_path = os.path.join(path, 'models', 'rf_classifier.pkl')
loaded_model = pickle.load(open(model_path, 'rb'))


@app.route("/predict", methods=["GET", "POST"])
def predict():
	global filename
	if request.method == "POST":
		duration  = request.form["duration"]
		protocol_type  = request.form["protocol_type"]
		service  = request.form["service"]
		flag  = request.form["flag"]
		src_bytes  = request.form["src_bytes"]
		dst_bytes  = request.form["dst_bytes"]
		land  = request.form["land"]
		wrong_fragment  = request.form["wrong_fragment"]
		urgent  = request.form["urgent"]
		hot  = request.form["hot"]
		num_failed_logins  = request.form["num_failed_logins"]
		logged_in  = request.form["logged_in"]
		num_compromised  = request.form["num_compromised"]
		root_shell  = request.form["root_shell"]
		su_attempted  = request.form["su_attempted"]
		num_file_creations  = request.form["num_file_creations"]
		num_shells  = request.form["num_shells"]
		num_access_files  = request.form["num_access_files"]
		num_outbound_cmds  = request.form["num_outbound_cmds"]
		is_host_login  = request.form["is_host_login"]
		is_guest_login  = request.form["is_guest_login"]
		count  = request.form["count"]
		srv_count  = request.form["srv_count"]
		serror_rate  = request.form["serror_rate"]
		rerror_rate  = request.form["rerror_rate"]
		same_srv_rate  = request.form["same_srv_rate"]
		diff_srv_rate  = request.form["diff_srv_rate"]

		print('\nduration:', duration,'\nprotocol_type:', protocol_type,'\nservice:', service,'\nflag:', flag,'\nsrc_bytes:', src_bytes,'\ndst_bytes:', dst_bytes,'\nland:', land,'\nwrong_fragment:', wrong_fragment,'\nurgent:', urgent,'\nhot:', hot,'\nnum_failed_logins:', num_failed_logins,'\nlogged_in:', logged_in,'\nnum_compromised:', num_compromised,'\nroot_shell:', root_shell,'\nsu_attempted:', su_attempted,'\nnum_file_creations:', num_file_creations,'\nnum_shells:', num_shells,'\nnum_access_files:', num_access_files,'\nnum_outbound_cmds:', num_outbound_cmds,'\nis_host_login:', is_host_login,'\nis_guest_login:', is_guest_login,'\ncount:', count,'\nsrv_count:', srv_count,'\nserror_rate:', serror_rate,'\nrerror_rate:', rerror_rate,'\nsame_srv_rate:', same_srv_rate,'\ndiff_srv_rate:', diff_srv_rate)
		
		print("\n************************************************************")
		input_data = []
		input_data.append(float(duration))
		input_data.append(int(protocol_type))
		input_data.append(int(service))
		input_data.append(int(flag))
		input_data.append(float(src_bytes))
		input_data.append(float(dst_bytes))
		input_data.append(float(land))
		input_data.append(float(wrong_fragment))
		input_data.append(float(urgent))
		input_data.append(float(hot))
		input_data.append(float(num_failed_logins))
		input_data.append(float(logged_in))
		input_data.append(float(num_compromised))
		input_data.append(float(root_shell))
		input_data.append(float(su_attempted))
		input_data.append(float(num_file_creations))
		input_data.append(float(num_shells))
		input_data.append(float(num_access_files))
		input_data.append(float(num_outbound_cmds))
		input_data.append(float(is_host_login))
		input_data.append(float(is_guest_login))
		input_data.append(float(count))
		input_data.append(float(srv_count))
		input_data.append(float(serror_rate))
		input_data.append(float(rerror_rate))
		input_data.append(float(same_srv_rate))
		input_data.append(float(diff_srv_rate))

		attack_type = decode(loaded_model.predict([input_data])[0])
		print("\n**************** RESULT *********************\n")
		print('Attack Type Resut = ',attack_type)

		if attack_type=="Normal Packet":
			return render_template("dashboard.html",attack=attack_type,safe='yes')
		else:
			return render_template("dashboard.html",attack=attack_type)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', error='No file part')
        file = request.files['file']
        # If the user does not select a file, the browser also
        # submits an empty file without a filename
        if file.filename == '':
            return render_template('upload.html', error='No selected file')
        try:
            # Read the CSV file
            df = pd.read_csv(file)
            
            # Check if the file has a label column
            has_actual_label = 'label' in df.columns
            
            # Store actual labels if they exist
            actual_labels = None
            if has_actual_label:
                actual_labels = df['label'].tolist()
                df = df.drop('label', axis=1)
            
            # Make predictions using the loaded model
            predictions = loaded_model.predict(df)
            
            # Label encoding mapping
            label_mapping = {0: 'Dos', 1: 'Probe', 2: 'R2L', 3: 'U2R', 4: 'normal'}
            
            # Reverse mapping (if actual labels are numerical)
            reverse_mapping = {'Dos': 0, 'Probe': 1, 'R2L': 2, 'U2R': 3, 'normal': 4}
            
            # Prepare the response with class index, name, and actual label if available
            response = []
            for i, pred in enumerate(predictions):
                class_index = int(pred)
                class_name = label_mapping[class_index]
                
                result = {
                    'sr_no': i+1,
                    'class_index': class_index,
                    'class_name': class_name
                }
                
                # Add actual label if available
                if has_actual_label:
                    actual = actual_labels[i]
                    # Convert actual label to name if it's numeric
                    if isinstance(actual, (int, float)) or (isinstance(actual, str) and actual.isdigit()):
                        actual = int(actual)
                        actual_name = label_mapping.get(actual, f"Unknown ({actual})")
                    else:
                        # If actual is already a string label
                        actual_name = actual
                        actual = reverse_mapping.get(actual, -1)
                    
                    result['actual_index'] = actual
                    result['actual_name'] = actual_name
                    result['match'] = class_index == actual
                
                response.append(result)
                
            # Return the HTML page with predictions
            return render_template('upload.html', predictions=response, has_actual=has_actual_label)
        except Exception as e:
            return render_template('upload.html', error=str(e))
    return render_template('upload.html', error=None)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)