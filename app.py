from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open("model_loan.pkl", "rb"))
encoders = pickle.load(open("encoders_loan.pkl", "rb"))

@app.route("/")
def home():
    return render_template("loan.html")

@app.route("/predict", methods=["POST"])
def predict():

    age = int(request.form["age"])
    gender = request.form["gender"]
    marital_status = request.form["marital_status"]
    employment_status = request.form["employment_status"]
    annual_income = float(request.form["annual_income"])
    loan_amount = float(request.form["loan_amount"])
    credit_score = int(request.form["credit_score"])
    num_dependents = int(request.form["num_dependents"])
    existing_loans_count = int(request.form["existing_loans_count"])

    # Encode categorical
    gender = encoders["gender"].transform([gender])[0]
    marital_status = encoders["marital_status"].transform([marital_status])[0]
    employment_status = encoders["employment_status"].transform([employment_status])[0]

    input_data = [[
        age,
        gender,
        marital_status,
        annual_income,
        loan_amount,
        credit_score,
        num_dependents,
        existing_loans_count,
        employment_status
    ]]

    prediction = model.predict(input_data)[0]

    result = "Approved" if prediction == 1 else "Rejected"

    return render_template("result.html", result=result)

if name == "main":
    app.run(host="0.0.0.0", port=5000)
