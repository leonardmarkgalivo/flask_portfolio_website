from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('projects.html')

@app.route('/works/uppercase', methods=['GET', 'POST'])
def uppercase():
    result = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '').strip()  
        if not input_string:
            result = "Error: Input cannot be empty."
        elif not input_string.isalpha():  
            result = "Error: Only letters are allowed (no numbers, symbols, or spaces)."
        else:
            result = input_string.upper() 
    return render_template('touppercase.html', result=result)

@app.route('/works/area/circle', methods=['GET', 'POST'])
def area_of_circle():
    result = None
    if request.method == 'POST':
        input_radius = request.form.get('radius', '').strip()  
        if not input_radius:
            result = "Error: Radius cannot be empty."
        else:
            try:
                radius = float(input_radius)
                if radius < 0:
                    result = "Error: Radius cannot be negative (use positive numbers only)."
                else:
                    area = math.pi * (radius ** 2)
                    result = f"The area is {area:.2f} square units."  # Format as string (2 decimals)
            except ValueError:
                result = "Error: Only numbers allowed for radius (e.g., 5 or 3.14; no letters or symbols)."
    return render_template('circle.html', result=result)

@app.route('/works/area/triangle', methods=['GET', 'POST'])
def area_of_triangle():
    result = None
    if request.method == 'POST':
        base_input = request.form.get('base', '').strip()  # Strip whitespace
        height_input = request.form.get('height', '').strip()
        if not base_input or not height_input:
            result = "Error: Both base and height cannot be empty."
        else:
            try:
                base_val = float(base_input)
                height_val = float(height_input)
                if base_val < 0 or height_val < 0:
                    result = "Error: Base and height cannot be negative (use positive numbers only)."
                else:
                    area = 0.5 * base_val * height_val
                    result = f"The area is {area:.2f} square units."  # Format as string (2 decimals)
            except ValueError:
                result = "Error: Only numbers allowed for base and height (e.g., 10 or 5.5; no letters or symbols)."
    return render_template('triangle.html', result=result)

@app.route('/contact')
def contact():
    return render_template('contacts.html')

if __name__ == "__main__":
    app.run(debug=True)