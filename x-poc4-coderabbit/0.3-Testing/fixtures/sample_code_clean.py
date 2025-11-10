"""
Sample Python code with NO issues - follows all Hana-X standards.

This file demonstrates clean code that passes all quality checks:
- No security vulnerabilities
- SOLID principles compliant
- Type hints present
- Docstrings present
- Low complexity
- Well-structured

Author: Julia Santos - Testing & QA Specialist
Date: 2025-11-10
"""

import os
from typing import List, Dict, Optional, Protocol
from abc import ABC, abstractmethod


# ==============================================================================
# CLEAN: Environment variables for secrets (Security Best Practice)
# ==============================================================================

def get_api_key() -> str:
    """
    Retrieve API key from environment variables.

    Returns:
        str: API key from environment

    Raises:
        ValueError: If API_KEY not set in environment
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")
    return api_key


# ==============================================================================
# CLEAN: SOLID - Single Responsibility Principle
# Each class has ONE clear responsibility
# ==============================================================================

class UserRepository:
    """Handles ONLY database operations for users."""

    def save(self, user: "User") -> None:
        """
        Save user to database.

        Args:
            user: User object to save
        """
        # Database save logic only
        pass

    def find_by_id(self, user_id: int) -> Optional["User"]:
        """
        Find user by ID.

        Args:
            user_id: User identifier

        Returns:
            User object if found, None otherwise
        """
        # Database query logic only
        pass


class EmailService:
    """Handles ONLY email operations."""

    def send_welcome_email(self, email: str) -> None:
        """
        Send welcome email to user.

        Args:
            email: Recipient email address
        """
        # Email sending logic only
        pass


class UserValidator:
    """Handles ONLY user validation."""

    def validate(self, user: "User") -> bool:
        """
        Validate user data.

        Args:
            user: User object to validate

        Returns:
            True if valid, False otherwise
        """
        # Validation logic only
        return True


# ==============================================================================
# CLEAN: SOLID - Open-Closed Principle
# Extensible without modification via polymorphism
# ==============================================================================

class Shape(ABC):
    """Abstract base class for shapes."""

    @abstractmethod
    def calculate_area(self) -> float:
        """Calculate shape area."""
        pass


class Circle(Shape):
    """Circle shape implementation."""

    def __init__(self, radius: float) -> None:
        """
        Initialize circle.

        Args:
            radius: Circle radius
        """
        self.radius = radius

    def calculate_area(self) -> float:
        """
        Calculate circle area.

        Returns:
            float: Circle area
        """
        return 3.14159 * self.radius ** 2


class Rectangle(Shape):
    """Rectangle shape implementation."""

    def __init__(self, width: float, height: float) -> None:
        """
        Initialize rectangle.

        Args:
            width: Rectangle width
            height: Rectangle height
        """
        self.width = width
        self.height = height

    def calculate_area(self) -> float:
        """
        Calculate rectangle area.

        Returns:
            float: Rectangle area
        """
        return self.width * self.height


# Adding new shapes doesn't require modifying existing code!
class Triangle(Shape):
    """Triangle shape implementation."""

    def __init__(self, base: float, height: float) -> None:
        """
        Initialize triangle.

        Args:
            base: Triangle base
            height: Triangle height
        """
        self.base = base
        self.height = height

    def calculate_area(self) -> float:
        """
        Calculate triangle area.

        Returns:
            float: Triangle area
        """
        return 0.5 * self.base * self.height


# ==============================================================================
# CLEAN: SOLID - Liskov Substitution Principle
# Subtypes honor base type contracts
# ==============================================================================

class Bird(ABC):
    """Abstract bird base class."""

    @abstractmethod
    def move(self) -> str:
        """How the bird moves."""
        pass


class Sparrow(Bird):
    """Sparrow - can fly."""

    def move(self) -> str:
        """
        Sparrow movement.

        Returns:
            str: Movement description
        """
        return "Flying"


class Penguin(Bird):
    """Penguin - cannot fly, but honors Bird contract."""

    def move(self) -> str:
        """
        Penguin movement.

        Returns:
            str: Movement description
        """
        return "Swimming"  # Honors contract without raising exceptions


# ==============================================================================
# CLEAN: SOLID - Interface Segregation Principle
# Focused, specific interfaces
# ==============================================================================

class Readable(Protocol):
    """Interface for readable objects."""

    def read(self) -> str:
        """Read data."""
        ...


class Writable(Protocol):
    """Interface for writable objects."""

    def write(self, data: str) -> None:
        """Write data."""
        ...


# Clients depend only on interfaces they need (not fat interfaces)


# ==============================================================================
# CLEAN: SOLID - Dependency Inversion Principle
# Depend on abstractions, not concretions
# ==============================================================================

class IMailer(Protocol):
    """Abstract mailer interface."""

    def send(self, to: str, subject: str, body: str) -> None:
        """Send email."""
        ...


class NotificationService:
    """Service that depends on abstraction (IMailer), not concrete implementation."""

    def __init__(self, mailer: IMailer) -> None:
        """
        Initialize with mailer dependency.

        Args:
            mailer: Mailer implementation (injected)
        """
        self.mailer = mailer  # Depends on abstraction

    def notify_user(self, email: str, message: str) -> None:
        """
        Send notification to user.

        Args:
            email: User email
            message: Notification message
        """
        self.mailer.send(email, "Notification", message)


# ==============================================================================
# CLEAN: Type hints, docstrings, low complexity
# ==============================================================================

def process_data(
    input_data: List[Dict[str, str]],
    config: Dict[str, bool]
) -> List[Dict[str, str]]:
    """
    Process input data according to configuration.

    Args:
        input_data: List of data items to process
        config: Configuration dictionary

    Returns:
        List of processed data items

    Example:
        >>> data = [{"name": "Alice"}, {"name": "Bob"}]
        >>> config = {"uppercase": True}
        >>> process_data(data, config)
        [{"name": "ALICE"}, {"name": "BOB"}]
    """
    result = []
    for item in input_data:
        processed = _process_single_item(item, config)
        result.append(processed)
    return result


def _process_single_item(
    item: Dict[str, str],
    config: Dict[str, bool]
) -> Dict[str, str]:
    """
    Process a single data item.

    Args:
        item: Single data item
        config: Configuration dictionary

    Returns:
        Processed data item
    """
    # Low complexity - simple, focused logic
    if config.get("uppercase", False):
        return {k: v.upper() for k, v in item.items()}
    return item


# ==============================================================================
# CLEAN: Main entry point
# ==============================================================================

def main() -> None:
    """Main entry point for the module."""
    # Clean, simple main function
    api_key = get_api_key()
    print(f"API key loaded: {api_key[:5]}...")


if __name__ == "__main__":
    main()
