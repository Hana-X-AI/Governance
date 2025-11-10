"""
Sample Python code with known issues for testing.

This file intentionally contains multiple code quality issues
for testing the CodeRabbit parser's detection capabilities.
"""

# SECURITY ISSUE: Hardcoded secret (P0)
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "MySecretPassword123"


# SECURITY ISSUE: SQL injection vulnerability (P0)
def get_user_by_id(user_id):
    """Retrieve user from database - UNSAFE"""
    cursor.execute('SELECT * FROM users WHERE id = ' + user_id)
    return cursor.fetchone()


# SOLID VIOLATION: Single Responsibility Principle (P1)
class UserManager:
    """
    Handles too many responsibilities:
    - Database operations
    - Email sending
    - Data validation
    - Logging
    """
    def save_user(self, user):
        # Database operation
        db.save(user)
        # Email sending
        send_email(user.email, "Welcome")
        # Validation
        if not user.is_valid():
            raise ValueError("Invalid user")
        # Logging
        log.info(f"User {user.id} saved")


# SOLID VIOLATION: Open-Closed Principle (P1)
def calculate_area(shape):
    """Calculate area - must modify for new shapes"""
    if isinstance(shape, Circle):
        return 3.14 * shape.radius ** 2
    elif isinstance(shape, Rectangle):
        return shape.width * shape.height
    elif isinstance(shape, Triangle):
        return 0.5 * shape.base * shape.height
    # Must modify this function to add new shape types!


# SOLID VIOLATION: Liskov Substitution Principle (P1)
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def fly(self):
        # Violates contract! Penguins can't fly
        raise Exception("Penguins can't fly")


# CODE QUALITY: Missing type hints (P2)
def process_data(input, config):
    """Process data without type hints"""
    result = []
    for item in input:
        if config.validate(item):
            result.append(config.transform(item))
    return result


# CODE QUALITY: Missing docstring (P2)
def complex_function():
    x = 10
    y = 20
    z = x + y
    return z * 2


# CODE QUALITY: High complexity (P2)
def complex_workflow(data, options):
    """Function with high cyclomatic complexity"""
    if data is None:
        return None

    if options.get('validate'):
        if not data.is_valid():
            if options.get('strict'):
                raise ValueError("Invalid data")
            else:
                if options.get('log_errors'):
                    log.error("Validation failed")
                return None

    if options.get('transform'):
        if data.needs_transformation():
            if options.get('parallel'):
                result = parallel_transform(data)
            else:
                result = sequential_transform(data)
        else:
            result = data
    else:
        result = data

    if options.get('persist'):
        if result.is_complete():
            save_to_database(result)
        else:
            save_to_cache(result)

    return result


# SOLID VIOLATION: Dependency Inversion Principle (P1)
class EmailService:
    """Directly depends on concrete SMTP implementation"""
    def __init__(self):
        # Depends on concrete class, not abstraction
        self.mailer = SmtpMailer("smtp.gmail.com", 587)

    def send(self, to, subject, body):
        # Tightly coupled to SMTP implementation
        self.mailer.connect()
        self.mailer.authenticate("user", "pass")
        self.mailer.send_message(to, subject, body)
        self.mailer.disconnect()
