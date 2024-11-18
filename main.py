from flask import Flask, render_template, request, redirect, session,  url_for
import pymysql, secrets, random, string


# db connection
local_server = True
app = Flask(__name__)

app.secret_key = b'tq34tq'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'organpage',
}
#-------------------------------------------------------------------------------------------
def insert_into_database(data):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # SQL query to insert data into the database
            sql = "INSERT INTO registration (Name, Aadhar_No, Date_of_Birth, Email, Password, Phone_Number) VALUES (%s, %s, %s, %s, %s, %s)"
            # Execute the SQL query with the data tuple
            cursor.execute(sql,data)
            connection.commit()
    except Exception as e:
        # Handle any exceptions that occur during database operation
        print("Error:", e)  # Print the full exception message for debugging
    finally:
        # Close database connection
        connection.close()
#-----------------------------------------------------
def authenticate_user(aadhar_no, password):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Query database to check if user exists with given Aadhar number and password
            sql = "SELECT * FROM registration WHERE Aadhar_No = %s AND Password = %s"
            cursor.execute(sql, (aadhar_no, password))
            user = cursor.fetchone()
            return user
    finally:
        connection.close()
#-------------------------------------------------------------------------------------------
# Login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        aadhar_no = request.form['Aadhar_No']
        password = request.form['Password']
        user = authenticate_user(aadhar_no, password)
        if user:
            # Set session for the authenticated user
            session['user_id'] = user[0]  # Assuming 'id' is the first element in the tuple
            return redirect('/dashboard')
        else:
            error = 'Invalid Aadhar number or password. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')
#-------------------------------------------------------------------------------------------
# Dashboard route (accessible only after login)
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Fetch user details from the database using the session user_id
        user_id = session['user_id']
        # Query the database to fetch user details based on user_id
        # Render dashboard template with user details
        return render_template('index.html')
    else:
        return redirect('/login')
#-------------------------------------------------------------------------------------------
# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')
#-------------------------------------------------------------------------------------------
@app.route('/submit-form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Extract form data from the request
        data = (
            request.form['Name'],
            request.form['Aadhar_No'],
            request.form['Date_of_Birth'],
            request.form['Email'],
            request.form['Password'],
            request.form['Phone_Number']
        )
        # Insert form data into the database
        insert_into_database(data)
        return 'Form submitted successfully'
    else:
        return 'Invalid request method'
#-------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')
#-------------------------------------------------------------------------------------------
@app.route('/BloodSlot')
def BloodSlot():
    return render_template('BloodSlot.html')
# Function to generate a random Slot_ID
def generate_slot_id(length=5):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=length))
#------------------------------------------------------------------------------------------
# Define the generate_slot_id function
def generate_slot_id():
    characters = string.ascii_lowercase + string.digits
    slot_id = ''.join(secrets.choice(characters) for _ in range(4))
    print("Generated Slot ID:", slot_id)  # Print the generated slot_id for debugging
    return slot_id
# Submit route
@app.route('/submit', methods=['POST'])
def submit():
    # Generate a unique Slot_ID
    slot_id = generate_slot_id()
    
    name = request.form['Name']
    aadhar_no = request.form['Aadhar_No']
    gender = request.form['Gender']
    age = request.form['Age']
    blood_group = request.form['Blood_Group']
    selected_slot = request.form['Selected_Slot']
    date = request.form['Date']

    # Insert the data into the database
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # SQL query to insert data into the database
            sql = "INSERT INTO Slots (Slot_ID, Name, Aadhar_No, Gender, Age, Blood_Group, Selected_Slot, Date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (slot_id, name, aadhar_no, gender, age, blood_group,selected_slot, date))
            # Commit changes to the database
            connection.commit()
    except Exception as e:
        # Handle any exceptions that occur during database operation
        print("Error:", e)
    finally:
        # Close database connection
        connection.close()

    # Render the confirmation page with the Slot_ID
    return 'Form submitted successfully'
    return render_template('confirmation.html', message=message, redirect_delay=5)
#-------------------------------------------------------------------------------------------
@app.route('/Login')
def Login():
    return render_template('Login.html')
#-------------------------------------------------------------------------------------------
@app.route('/Signup')
def Signup():
    return render_template('Signup.html')
#---------------------------------------------------------------------------------------------
def insert_into_database(data):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # SQL query to insert data into the database
            sql = """INSERT INTO OrganDonationRegistration (First_Name, Middle_Name, Last_Name, 
                                                        Mothers_Fathers_Name, Current_Residential_Address,
                                                        Address_Line_2, City, District, State, PIN_Code, 
                                                        Mobile_Number, Occupation, Email, Date_Of_Birth, Age,
                                                        Gender, Blood_Group, Emergency_Contact_Name,
                                                        Emergency_Contact_Address, Identity_Card_Type,
                                                        Identity_Card_Number, Organs_To_Donate)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            # Print SQL query and data tuple for debugging
            print("SQL query:", sql)
            print("Data tuple:", data)
            
            # Execute the SQL query
            cursor.execute(sql, data)
            
            # Commit changes to the database
            connection.commit()
            return True  # Indicate success
    except pymysql.Error as e:
        # Log the error
        print("Error:", e)
        return False  # Indicate failure
    finally:
        # Close database connection
        connection.close()
@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        mothers_fathers_name = request.form.get('mother_father_name')
        current_residential_address = request.form.get('current_address')
        address_line_2 = request.form.get('address_line_2')
        city = request.form.get('city')
        district = request.form.get('district')
        state = request.form.get('state')
        pin_code = request.form.get('pin_code')
        mobile_number = request.form.get('mobile_number')
        occupation = request.form.get('occupation')
        email = request.form.get('email')
        date_of_birth = request.form.get('dob')
        age = request.form.get('age')
        gender = request.form.get('gender')
        blood_group = request.form.get('blood_group')
        emergency_contact_name = request.form.get('emergency_contact_name')
        emergency_contact_address = request.form.get('emergency_contact_address')
        identity_card_type = request.form.get('identity_card')
        identity_card_number = request.form.get('identity_card_number')
        organs_to_donate = ', '.join(request.form.getlist('organs_to_donate'))

        # Store form data in a tuple
        data = (first_name, middle_name, last_name, mothers_fathers_name,
                current_residential_address, address_line_2, city, district,
                state, pin_code, mobile_number, occupation, email, date_of_birth,
                age, gender, blood_group, emergency_contact_name,
                emergency_contact_address, identity_card_type,
                identity_card_number, organs_to_donate)
        
        # Insert data into the database
        success = insert_into_database(data)

        if success:
            # Render the thank you page template
            return render_template('thankyou.html')
        else:
            # Display an error message
            error_message = "Failed to submit donation form. Please try again later."
            return render_template('error.html', error_message=error_message)
            
    else:
        # Render the donation form template
        return render_template('donate.html')

#------------------------------------------------------------------------------------------
@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')

# Define a function to insert volunteer details into the database
# Function to insert volunteer details into the database
# Function to insert volunteer details into the database
# Function to insert volunteer details into the database
def insert_volunteer_details(aadhar_no, event_selected):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # SQL query to insert data into the database
            sql = "INSERT INTO Volunteer (Aadhar_No, Event_selected) VALUES (%s, %s)"
            cursor.execute(sql, (aadhar_no, event_selected))
            # Commit changes to the database
            connection.commit()
            print("Volunteer details inserted successfully.")
    except pymysql.Error as e:
        # Handle any errors that occur during database operation
        print("Error:", e)
    finally:
        # Close database connection
        connection.close()



# Define a route to handle the form submission for volunteer details
@app.route('/submit_volunteer_details', methods=['POST'])
def submit_volunteer_details():
    if request.method == 'POST':
        # Extract form data from the request
        aadhar_no = request.form['Aadhar_No']
        event_selected = request.form['event']  # Ensure the correct name is used
        
        # Call the function to insert volunteer details into the database
        # Since Volunteer_ID is auto-incremented, you don't need to pass it explicitly
        insert_volunteer_details(aadhar_no, event_selected)

        # Optionally, you can return a response or redirect to another page
        return 'Volunteer details submitted successfully'

#-------------------------------------------------------------------------------------------
# Function to insert organ request data into the database
def insert_organ_request(data):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # SQL query to insert data into the database
            sql = "INSERT INTO OrganRequest (PatientName, Aadhar_No, PatientAge, Relationship, RequiredOrgans, UrgencyLevel, ContactName, ContactNumber, AdditionalInfo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, data)
            # Commit changes to the database
            connection.commit()
    except pymysql.Error as e:
        # Handle any errors that occur during database operation
        print("Error:", e)
    finally:
        # Close database connection
        connection.close()

# Route to handle organ request form submission
@app.route('/submit_organ_request', methods=['POST'])
def submit_organ_request():
    if request.method == 'POST':
        # Extract form data from the request
        data = (
            request.form['patient_name'],
            request.form['Aadhar_No'],
            request.form['patient_age'],
            request.form['Relationship'],
            request.form['required_organs'],
            request.form['urgency_level'],
            request.form['contact_name'],
            request.form['contact_number'],
            request.form['additional_info']
        )
        # Insert form data into the database
        success1 = insert_organ_request(data)
        
        if success1:
            # Render the thank you page template
            return render_template('thankyou.html')
        else:
            # Display an error message
            error_message = "Failed to submit organ request. Please try again later."
            return render_template('error.html', error_message=error_message)

# Function to insert organ request data into the database
def insert_organ_request(data):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # SQL query to insert data into the database
            sql = "INSERT INTO OrganRequest (PatientName, Aadhar_No, PatientAge, Relationship, RequiredOrgans, UrgencyLevel, ContactName, ContactNumber, AdditionalInfo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, data)
            # Commit changes to the database
            connection.commit()
            return True  # Return True if insertion is successful
    except pymysql.Error as e:
        # Handle any errors that occur during database operation
        print("Error:", e)
        return False  # Return False if insertion fails
    finally:
        # Close database connection
        connection.close()

# Route to render the organ request page
@app.route('/request_page')
def request_page():
    return render_template('request.html')

#-------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
