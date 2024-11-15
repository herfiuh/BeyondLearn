from flask import Flask, render_template, request, jsonify

app = Flask(_name_)

# Chatbot response logic
def chatbot_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input:
        return "Hi there! How can I help you?"
    elif "bye" in user_input:
        return "Goodbye! Have a nice day!"
    else:
        return "I'm not sure how to respond to that. Can you rephrase?"

# Route for serving the HTML page
@app.route('/')
def home():
    return render_template('index.html')  # This serves the HTML frontend

# Route for chatbot API
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    if user_input:
        response = chatbot_response(user_input)
        return jsonify({"response": response})
    else:
        return jsonify({"error": "No message provided"}), 400

if _name_ == '_main_':
    app.run(debug=True)