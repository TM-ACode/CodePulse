"""
Example code to test CodePulse analysis engines.
This file intentionally contains issues for testing.
"""

def calculate_total(a, b, c, d, e, f, g):  # Long parameter list
    """Calculate total with many parameters."""
    result = 0
    for i in range(100):
        for j in range(100):  # Nested loop - O(n²)
            result += i * j
    
    x = 1
    y = 2  # Unused variable
    
    return result


class UserManager:  # God class - too many responsibilities
    """Manages everything about users."""
    
    def __init__(self):
        self.users = []
        self.cache = {}
        self.db = None
    
    def validate_user(self, user):
        if user.email:
            if "@" in user.email:  # Nested if
                if "." in user.email:
                    return True
        return False
    
    def save_user(self, user):
        # Database logic
        self.db.save(user)
    
    def send_email(self, user):
        # Email logic
        pass
    
    def generate_report(self, user):
        # Reporting logic
        pass
    
    def validate_password(self, password):
        # Validation logic
        pass
    
    def hash_password(self, password):
        # Hashing logic
        pass


# Duplicate code (clone)
def process_data_1(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result


def process_data_2(items):  # Same as above with different names
    output = []
    for element in items:
        if element > 0:
            output.append(element * 2)
    return output


# Feature Envy - uses 'other' more than 'self'
class Calculator:
    def __init__(self):
        self.name = "Calculator"
    
    def complex_calculation(self, other_obj):
        # Uses other_obj extensively
        x = other_obj.value1
        y = other_obj.value2
        z = other_obj.value3
        result = other_obj.method1() + other_obj.method2()
        return result


# Dead code after return
def unreachable_example():
    return 42
    x = 100  # Unreachable
    print("This will never execute")


# Infinite loop
def infinite_loop_example():
    while True:
        pass  # No break condition
