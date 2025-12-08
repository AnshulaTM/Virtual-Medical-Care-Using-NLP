import psycopg2
from datetime import date

try:
    illness_conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='pixel3105',
        database='illness_db'
    )

    

    def create_tables():
        illness_cursor = illness_conn.cursor()

        illness_cursor.execute('DROP TABLE IF EXISTS medical_history CASCADE')
        illness_cursor.execute('DROP TABLE IF EXISTS patients CASCADE')
        illness_cursor.execute('DROP TABLE IF EXISTS illnesses CASCADE')
        
        

        # Create symptoms table
        illness_cursor.execute('''
            CREATE TABLE IF NOT EXISTS illnesses (
                    id SERIAL PRIMARY KEY,
                    illness_name TEXT NOT NULL,
                    possible_symptoms TEXT NOT NULL,
                    treatment_plan TEXT NOT NULL,
                    common_causes TEXT NOT NULL,
                    recommended_tests TEXT NOT NULL
                )
        ''')

        illness_cursor.execute('''
                               CREATE TABLE IF NOT EXISTS patients (
                               id SERIAL PRIMARY KEY,
                               first_name TEXT NOT NULL,
                               last_name TEXT NOT NULL,
                               date_of_birth DATE NOT NULL,
                               gender TEXT NOT NULL,
                               contact_info TEXT NOT NULL,
                               address TEXT NOT NULL
                               )
        ''')


        illness_cursor.execute('''
                               CREATE TABLE IF NOT EXISTS medical_history(
                               id SERIAL PRIMARY KEY,
                               patient_id INT REFERENCES patients(id) ON DELETE CASCADE,
                               illness_id INT REFERENCES illnesses(id) ON DELETE CASCADE,
                               diagnosis TEXT NOT NULL,
                               diagnosis_date DATE NOT NULL,
                               treatment_details TEXT NOT NULL,
                               visit_count INT DEFAULT 1
                               )
        ''')
       

        # Commit and close the cursors
        illness_conn.commit()
        illness_cursor.close()

    # Populate `symptoms_db`
    def populate_illness_db():
        illness_cursor = illness_conn.cursor()
        illness_cursor.executemany('''
            INSERT INTO illnesses (illness_name, possible_symptoms, treatment_plan, common_causes, recommended_tests)
                VALUES (%s, %s, %s, %s, %s)
            ''', [
                ('Migraine', 'headache,nausea,sensitivity to light', 
                 'Rest in a dark room, painkillers, hydration', 
                 'Stress, dehydration, lack of sleep', 'MRI, CT scan'),
                
                ('Pneumonia', 'fever,cough,chest pain,shortness of breath', 
                 'Antibiotics, rest, hydration', 
                 'Bacterial or viral infection, weakened immunity', 'Chest X-ray, sputum test'),
                
                ('Anemia', 'fatigue,dizziness,pale skin', 
                 'Iron supplements, a balanced diet', 
                 'Iron deficiency, blood loss', 'Complete Blood Count (CBC) test'),
                
                ('Diabetes', 'frequent urination,thirst,weight loss,fatigue', 
                 'Insulin therapy, dietary changes, exercise', 
                 'Genetics, obesity, inactivity', 'Blood glucose test, HbA1c test'),
                
                ('Bronchitis', 'cough,shortness of breath,fever', 
                 'Hydration, rest, anti-inflammatory medications', 
                 'Viral infection, smoking, air pollution', 'Chest X-ray, sputum test'),
                
                ('Heart Attack', 'chest pain,shortness of breath,nausea,weakness', 
                 'Emergency care, angioplasty, medication', 
                 'Blocked arteries, high cholesterol, stress', 'ECG, angiogram'),
                
                ('Food Poisoning', 'nausea,vomiting,diarrhea,stomach pain', 
                 'Hydration, antiemetics, rest', 
                 'Contaminated food, bacteria like Salmonella', 'Stool test'),
                
                ('Flu', 'fever,cough,body ache,headache', 
                 'Rest, fluids, antiviral medications', 
                 'Viral infection', 'Rapid influenza diagnostic test'),

                 ('Asthma', 'shortness of breath,wheezing,chest tightness,cough', 
                 'Inhalers, bronchodilators, avoid triggers', 
                 'Allergens, pollution, exercise', 'Pulmonary function test'),
                 
                ('Hypertension', 'headache,blurred vision,chest pain,shortness of breath', 
                 'Antihypertensive medications, dietary changes, exercise', 
                 'Stress, high sodium diet, obesity', 'Blood pressure measurement'),
                 
                ('Kidney Stones', 'severe abdominal pain,nausea,blood in urine,frequent urination', 
                 'Pain relievers, hydration, lithotripsy', 
                 'Dehydration, high oxalate diet', 'Ultrasound, CT scan'),
                 
                ('Appendicitis', 'abdominal pain,loss of appetite,nausea,fever', 
                 'Surgical removal of appendix', 
                 'Infection, blockage in appendix', 'CT scan, ultrasound'),
                 
                ('Stroke', 'sudden numbness,weakness in limbs,confusion,blurred vision', 
                 'Emergency care, clot-busting medications', 
                 'Blocked or burst blood vessel in brain', 'CT scan, MRI, angiography'),
                 
                ('Tuberculosis', 'persistent cough,weight loss,fever,night sweats', 
                 'Antibiotics for 6-9 months', 
                 'Bacterial infection (Mycobacterium tuberculosis)', 'Chest X-ray, sputum test'),
                 
                ('Skin Allergy', 'rash,redness,itching,swelling', 
                 'Antihistamines, topical creams', 
                 'Allergens, insect bites, chemicals', 'Patch test, skin prick test'),
                 
                ('Gastroenteritis', 'diarrhea,nausea,abdominal cramps,fever', 
                 'Hydration, antiemetics, rest', 
                 'Viral or bacterial infection, contaminated food', 'Stool culture'),
                 
                ('COVID-19', 'fever,cough,loss of taste or smell,shortness of breath', 
                 'Isolation, antiviral drugs, supportive care', 
                 'SARS-CoV-2 virus', 'PCR test, antigen test'),
                 
                ('Arthritis', 'joint pain,stiffness,swelling,limited range of motion', 
                 'Pain relief, physical therapy, anti-inflammatory drugs', 
                 'Age, wear and tear, autoimmune conditions', 'X-ray, blood tests'),
                 
                ('Depression', 'persistent sadness,fatigue,loss of interest,changes in sleep or appetite', 
                 'Psychotherapy, antidepressant medications, lifestyle changes', 
                 'Genetics, trauma, hormonal changes', 'Psychological evaluation'),
                 
                ('Epilepsy', 'seizures,loss of consciousness,confusion,uncontrollable movements', 
                 'Antiepileptic drugs, surgery (in some cases)', 
                 'Brain injury, infections, genetic factors', 'EEG, MRI'),
                 
                ('Obesity', 'excessive weight gain,fatigue,shortness of breath', 
                 'Dietary changes, exercise, weight-loss surgery', 
                 'Overeating, sedentary lifestyle, genetics', 'BMI calculation, blood tests'),
                 
                ('Hypothyroidism', 'fatigue,weight gain,dry skin,depression', 
                 'Thyroid hormone replacement therapy', 
                 'Autoimmune disorders, iodine deficiency', 'TSH, T4 blood tests'),
                 
                ('Allergic Rhinitis', 'sneezing,runny nose,itchy eyes,congestion', 
                 'Antihistamines, nasal sprays, allergen avoidance', 
                 'Pollen, dust mites, animal dander', 'Allergy testing'),
                 
                ('Gout', 'joint pain,swelling,redness,limited mobility', 
                 'Pain relievers, anti-inflammatory drugs, dietary changes', 
                 'High uric acid levels, alcohol consumption', 'Joint fluid analysis, blood test'),
                 
                ('Liver Cirrhosis', 'jaundice,fatigue,abdominal swelling,confusion', 
                 'Lifestyle changes, medications, liver transplant (severe cases)', 
                 'Alcohol abuse, hepatitis, fatty liver disease', 'Liver function tests, ultrasound'),
                 
                ('Parkinson’s Disease', 'tremors,stiffness,slowed movement,impaired posture', 
                 'Medications, physical therapy, deep brain stimulation', 
                 'Genetic factors, aging, environmental toxins', 'Neurological exam, MRI')
            ])
        illness_conn.commit()
        illness_cursor.close()

    # Populate `patient_records_db`
    def populate_patients_db():
        illness_cursor = illness_conn.cursor()
        illness_cursor.executemany('''
            INSERT INTO patients(first_name, last_name, date_of_birth, gender, contact_info, address)
            VALUES(%s, %s, %s, %s, %s, %s)
            ''', [
                ('John', 'Doe', '1985-06-15', 'Male', '123-456-7890', '123 Elm Street, CA'),
                ('Chappel', 'Smith', '1992-08-24', 'Female', '987-654-3210', '456 Maple Drive, NY'),
                ('Sirisha', 'Johnson', '1978-09-28', 'Female', '555-666-7777', '900 Woodland Ave, CO'),
                ('Michael', 'Brown', '1990-12-05', 'Male', '444-987-6543', '321 Pine Street, FL')
        ])
        illness_conn.commit()
        illness_cursor.close()

    def populate_medical_history_db():
        illness_cursor = illness_conn.cursor()
        illness_cursor.executemany('''
        INSERT INTO medical_history(patient_id, illness_id, diagnosis, diagnosis_date, treatment_details)
        VALUES(%s, %s, %s, %s, %s)
    ''', [
        (1, 1, 'Type 2 Diabetes', '2022-01-10', 'Patient diagnosed with Type 2 Diabetes. Needs lifestyle changes.'),
        (2, 2, 'Hypertension', '2023-05-15', 'Blood pressure consistently high. Medication prescribed.'),
        (3, 3, 'Asthma', '2021-09-30', 'Asthma symptoms managed with inhaler.'),
        (4, 4, 'Epilepsy', '2024-06-27', 'Recieved emergency care and antiepileptic drugs')
    ])
    

        illness_conn.commit()
        illness_cursor.close()
    
      

    # Main script execution
    create_tables()  # Create the necessary tables
    populate_illness_db()  # Populate the symptoms database
    populate_patients_db()
    populate_medical_history_db()
    
    # Close the connections
    illness_conn.close()
    

except Exception as e:
    print("Error:", e)
 
