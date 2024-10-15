import streamlit as st 
import joblib
import numpy as np 
import mysql.connector

model =joblib.load("social.pkl")
# connect data base
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Change this
        password="Raja@3182",  # Change this
        database="social_meadia"
    )


    #streamlit app
    st.title("Socialmedia product purchase prdiction")

    #use inputs
user_id=st.number_input("Enter use ID",min_value=1)
gender=st.selectbox("gender(0:Male,1:Female)",[0,1])

age=st.number_input("enter age0",min_value=18)
salary=st.number_input("enter you salary",min_value=15000)



    # Prediction button
if st.button('Predict'):
    # Prepare data for prediction
    user_data = np.array([[user_id,gender,age,salary]])
    
    # Make prediction
    prediction = model.predict(user_data)[0] # [1 or 0]  [0]
    
    st.write(f"Prediction: {'he/she can purchase' if prediction == 1 else 'he/she cant'}")
    
    # Store user input and prediction in the database
    db = connect_to_db() # mysql.conector.connect.cursor()
    cursor = db.cursor()
    
    query = """
    INSERT INTO user_inputs (User_id,Gender,age,estimate_salary,purchased)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query,(user_id,gender,age,salary ,int(prediction)))
    db.commit()
    
    st.write("Data saved to the database.")
    
    cursor.close()
    db.close()