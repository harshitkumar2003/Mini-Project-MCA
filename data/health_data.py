DOCTORS = [
    {"id": 1, "name": "Dr. Sarah Johnson", "specialization": "Cardiologist", "available": ["Mon", "Wed", "Fri"], "image": "assets/doctor1.png"},
    {"id": 2, "name": "Dr. Michael Chen", "specialization": "Neurologist", "available": ["Tue", "Thu", "Sat"], "image": "assets/doctor2.png"},
    {"id": 3, "name": "Dr. Emily Wilson", "specialization": "Dermatologist", "available": ["Mon", "Wed", "Fri"], "image": "assets/doctor3.png"},
    {"id": 4, "name": "Dr. Robert Taylor", "specialization": "Orthopedic Surgeon", "available": ["Mon", "Wed", "Fri", "Sat"], "image": "assets/doctor4.png"},
    {"id": 5, "name": "Dr. Priya Patel", "specialization": "Pediatrician", "available": ["Mon", "Tue", "Thu"], "image": "assets/doctor5.png"},
    {"id": 6, "name": "Dr. James Wilson", "specialization": "General Physician", "available": ["Mon", "Tue", "Wed", "Thu", "Fri"], "image": "assets/doctor1.png"},
    {"id": 7, "name": "Dr. Lisa Wong", "specialization": "Gynecologist", "available": ["Mon", "Wed", "Fri"], "image": "assets/doctor2.png"},
    {"id": 8, "name": "Dr. David Kim", "specialization": "ENT Specialist", "available": ["Tue", "Thu", "Sat"], "image": "assets/doctor3.png"}
]

DISEASES = {
    "Common Cold": {
        "symptoms": ["cough", "sore throat", "runny nose", "sneezing", "congestion"],
        "doctor": "General Physician",
        "medication": ["Acetaminophen", "Ibuprofen", "Decongestants"],
        "advice": "Get plenty of rest and stay hydrated."
    },
    "Influenza (Flu)": {
        "symptoms": ["fever", "muscle aches", "fatigue", "headache", "chills"],
        "doctor": "General Physician",
        "medication": ["Oseltamivir (Tamiflu)", "Zanamivir (Relenza)", "Pain relievers"],
        "advice": "Get plenty of rest and drink fluids. Stay home to avoid spreading the virus."
    },
    "Migraine": {
        "symptoms": ["severe headache", "nausea", "sensitivity to light", "sensitivity to sound"],
        "doctor": "Neurologist",
        "medication": ["Triptans", "NSAIDs", "Anti-nausea medications"],
        "advice": "Rest in a quiet, dark room. Avoid triggers like stress and certain foods."
    },
    "Allergic Rhinitis": {
        "symptoms": ["sneezing", "itchy/watery eyes", "nasal congestion", "runny nose"],
        "doctor": "Allergist",
        "medication": ["Antihistamines", "Nasal corticosteroids", "Decongestants"],
        "advice": "Avoid allergens when possible. Use air purifiers and keep windows closed during high pollen seasons."
    },
    "Gastroenteritis": {
        "symptoms": ["diarrhea", "nausea", "vomiting", "abdominal pain", "fever"],
        "doctor": "Gastroenterologist",
        "medication": ["Oral rehydration solutions", "Anti-nausea medications", "Antidiarrheal medications"],
        "advice": "Stay hydrated with clear fluids. Follow the BRAT diet (Bananas, Rice, Applesauce, Toast) as you recover."
    },
    "Urinary Tract Infection (UTI)": {
        "symptoms": ["painful urination", "frequent urination", "urge to urinate", "cloudy urine"],
        "doctor": "Urologist",
        "medication": ["Antibiotics (e.g., Ciprofloxacin, Nitrofurantoin)", "Pain relievers"],
        "advice": "Drink plenty of water. Urinate frequently and empty your bladder completely."
    },
    "Bronchitis": {
        "symptoms": ["persistent cough", "mucus production", "fatigue", "chest discomfort"],
        "doctor": "Pulmonologist",
        "medication": ["Cough medicine", "Bronchodilators", "Anti-inflammatory drugs"],
        "advice": "Get plenty of rest. Use a humidifier and drink warm fluids to soothe your throat."
    },
    "Sinusitis": {
        "symptoms": ["facial pain/pressure", "nasal congestion", "thick nasal discharge", "reduced sense of smell"],
        "doctor": "ENT Specialist",
        "medication": ["Nasal corticosteroids", "Decongestants", "Pain relievers"],
        "advice": "Use a saline nasal spray and apply warm compresses to your face to relieve pain."
    },
    "Anxiety Disorder": {
        "symptoms": ["excessive worry", "restlessness", "difficulty concentrating", "irritability"],
        "doctor": "Psychiatrist",
        "medication": ["SSRIs", "Benzodiazepines", "Beta-blockers"],
        "advice": "Practice relaxation techniques like deep breathing and meditation. Maintain a regular sleep schedule."
    },
    "Hypertension (High Blood Pressure)": {
        "symptoms": ["headaches", "shortness of breath", "nosebleeds", "dizziness"],
        "doctor": "Cardiologist",
        "medication": ["ACE inhibitors", "Beta-blockers", "Diuretics"],
        "advice": "Maintain a healthy diet low in sodium, exercise regularly, and monitor your blood pressure at home."
    }
}
