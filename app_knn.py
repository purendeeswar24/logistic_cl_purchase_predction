import streamlit as st
import mysql.connector
import  numpy as np
import joblib

model=joblib.load("media.pkl")

def connect_to_db():
  return mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Raja@3182",
    database='social_meadia');

st.title("Socil_Media_Product Prediction")


user_id=st.number_input("enter User_id",min_value=1)
gender=st.selectbox('select_gender(0:Female,1:Male)',[0,1])

age=st.number_input("enter_age",min_value=18)

salary=st.number_input("enter salary",min_value=15000)

# Prediction button
if st.button('Predict'):
    # Prepare data for prediction
    user_data = np.array([[user_id, gender, age, salary]])
    
    # Make prediction
    prediction = model.predict(user_data)[0] # [1 or 0]  [0]
    
    st.write(f"Prediction: {'he/she can purchase' if prediction == 1 else 'he/she Will not purchase'}")
    
    # Store user input and prediction in the database
    db = connect_to_db() # mysql.conector.connect.cursor()
    cursor = db.cursor()
    
    query = """
    INSERT INTO user_inputs (Userid, Gender, age, estimate_salary, purchased)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, gender, age, salary, int(prediction)))
    db.commit()
    
    st.write("Data saved to the database.")
    
    cursor.close()
    db.close()