from flask import Flask, render_template, request
import math

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        if self.top:
            new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        else:
            popped_node = self.top
            self.top = self.top.next
            popped_node.next = None
            return popped_node.data

    def peek(self):
        if self.top:
            return self.top.data
        else:
            return None

    def print_stack(self):
        if self.top is None:
            print("Stack is empty")
        else:
            current = self.top
            print("Stack elements (top → bottom):")
            while current:
                print(current.data)
                current = current.next

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def remove_beginning(self):
        if not self.head:
            return None
        removed_data = self.head.data
        self.head = self.head.next
        return removed_data

    def remove_at_end(self):
        if not self.head:
            return None
        if not self.head.next:
            removed_data = self.head.data
            self.head = None
            return removed_data
        current = self.head
        while current.next.next:
            current = current.next
        removed_data = current.next.data
        current.next = None
        return removed_data

    def remove_at(self, data):
        if not self.head:
            return None
        if self.head.data == data:
            return self.remove_beginning()
        current = self.head
        while current.next and current.next.data != data:
            current = current.next
        if current.next:
            removed_data = current.next.data
            current.next = current.next.next
            return removed_data
        return None

    def get_items(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items

    def display(self):
        items = self.get_items()
        return " -> ".join(items) if items else "Empty list"

linked_list = LinkedList()
sushi_steps = ["cut fish", "wash rice", "prepare to assemble", "roll sushi", "eat sushi"]
for step in sushi_steps:
    linked_list.add(step)

def infix_to_postfix(infix):
    stack = Stack()
    postfix = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    
    for char in infix:
        if char.isalnum():  
            postfix.append(char)
        elif char == '(':
            stack.push(char)
        elif char == ')':
            while stack.peek() != '(':
                postfix.append(stack.pop())
            stack.pop()  
        else:  
            while stack.peek() and stack.peek() != '(' and precedence.get(char, 0) <= precedence.get(stack.peek(), 0):
                postfix.append(stack.pop())
            stack.push(char)
    
    while stack.peek():
        postfix.append(stack.pop())
    
    return ''.join(postfix)

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
        base_input = request.form.get('base', '').strip()  
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
                    result = f"The area is {area:.2f} square units."  
            except ValueError:
                result = "Error: Only numbers allowed for base and height (e.g., 10 or 5.5; no letters or symbols)."
    return render_template('triangle.html', result=result)

@app.route('/works/linkedlist', methods=['GET', 'POST'])
def linkedlist():
    result = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            data_input = request.form.get('data', '').strip()
            if not data_input:
                result = "Error: Data cannot be empty."
            else:
                linked_list.add(data_input)
                result = f"Added '{data_input}'."
        elif action == 'remove_beginning':
            removed = linked_list.remove_beginning()
            result = f"Removed from beginning: '{removed}'" if removed is not None else "List is empty."
        elif action == 'remove_end':
            removed = linked_list.remove_at_end()
            result = f"Removed from end: '{removed}'" if removed is not None else "List is empty."
        elif action == 'remove_at':
            data_input = request.form.get('data', '').strip()
            if not data_input:
                result = "Error: Data to remove cannot be empty."
            else:
                removed = linked_list.remove_at(data_input)
                result = f"Removed: '{removed}'" if removed is not None else f"'{data_input}' not found."
    return render_template('linkedlist.html', result=result, list_items=linked_list.get_items())

@app.route('/works/infixtopostfix', methods=['GET', 'POST'])
def infixtopostfix():
    result = None
    postfix_list = []
    if request.method == 'POST':
        infix_input = request.form.get('infix', '').strip()
        if not infix_input:
            result = "Error: Infix expression cannot be empty."
        else:
            try:
                postfix = infix_to_postfix(infix_input)
                result = f"Postfix: {postfix}"
                postfix_list = list(postfix)  
            except:
                result = "Error: Invalid infix expression (check operators/parentheses)."
    return render_template('infixtopostfix.html', result=result, postfix_list=postfix_list)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)