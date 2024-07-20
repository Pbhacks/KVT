import pandas as pd
import os

# Define the CSV file path
csv_file_path = 'email_phishing_dataset.csv'

# Load the existing dataset
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
else:
    print(f"Error: The file {csv_file_path} does not exist.")
    exit()

# Define new data to add
new_data = [
    {"email_content": "Dear user, please verify your account by clicking here.", "label": 1},
    {"email_content": "Meeting at 10 AM tomorrow. Don't forget the report.", "label": 0},
    {"email_content": "Your account has been compromised. Reset your password.", "label": 1},
    {"email_content": "Lunch with Sarah at 1 PM today. See you there!", "label": 0},
    {"email_content": "Your payment has been received. Thank you!", "label": 0},
    {"email_content": "Urgent: Update your payment information immediately.", "label": 1},
    {"email_content": "Dear Customer, We have noticed suspicious activity on your account and need you to verify your information immediately. Please click the link below to update your account details: http://fakebank.com/verify Failure to do so within 24 hours will result in your account being locked. Thank you, Customer Support", "label": 1},
    {"email_content": "Hi, We detected a suspicious login attempt to your account from an unknown device. If this was not you, please reset your password immediately to secure your account. Click here to reset your password: http://fakesocialmedia.com/reset If you do not take action, your account may be at risk. Best, The Security Team", "label": 1},
    {"email_content": "Dear Customer, Thank you for your recent purchase. We need to verify your payment information to process your order. Please confirm your payment details by clicking the link below: http://fakeretailer.com/confirm If we do not receive a response within 48 hours, your order will be canceled. Regards, Customer Service", "label": 1},
    {"email_content": "Dear Taxpayer, You are eligible for a tax refund. To process your refund, please click the link below and fill out the necessary information: http://fakegovernment.com/refund This refund is time-sensitive and must be claimed within the next 7 days. Sincerely, Tax Department", "label": 1}
]

# Convert new data to DataFrame
try:
    new_df = pd.DataFrame(new_data)
except ValueError as e:
    print(f"Error converting new data to DataFrame: {e}")
    exit()

# Append new data to existing DataFrame
df = pd.concat([df, new_df], ignore_index=True)

# Save the updated DataFrame to CSV
df.to_csv(csv_file_path, index=False)
print(f"Updated data has been saved to {csv_file_path}.")
