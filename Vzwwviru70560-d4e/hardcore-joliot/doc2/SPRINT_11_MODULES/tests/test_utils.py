"""
Tests — Utilitaires
"""

import pytest
from utils.helpers import slugify, truncate, mask_email, bytes_to_human
from utils.validators import (
    is_valid_email, is_valid_phone, is_valid_password, is_valid_uuid
)
from utils.formatters import format_currency, format_phone


class TestHelpers:
    """Tests helpers"""
    
    def test_slugify(self):
        assert slugify("Hello World") == "hello-world"
        assert slugify("Café au lait") == "cafe-au-lait"
        assert slugify("Test--Multiple---Dashes") == "test-multiple-dashes"
    
    def test_truncate(self):
        assert truncate("Hello", 10) == "Hello"
        assert truncate("Hello World Test", 10) == "Hello W..."
        assert truncate("Test", 10, suffix="…") == "Test"
    
    def test_mask_email(self):
        assert mask_email("test@gmail.com") == "t***@g***.com"
        assert mask_email("user@example.org") == "u***@e***.org"
    
    def test_bytes_to_human(self):
        assert bytes_to_human(500) == "500.0 B"
        assert bytes_to_human(1024) == "1.0 KB"
        assert bytes_to_human(1048576) == "1.0 MB"


class TestValidators:
    """Tests validateurs"""
    
    def test_is_valid_email(self):
        assert is_valid_email("test@example.com") == True
        assert is_valid_email("user.name@domain.co.uk") == True
        assert is_valid_email("invalid-email") == False
        assert is_valid_email("@nodomain.com") == False
    
    def test_is_valid_phone(self):
        assert is_valid_phone("514-555-1234") == True
        assert is_valid_phone("(514) 555-1234") == True
        assert is_valid_phone("+1 514 555 1234") == True
        assert is_valid_phone("123") == False
    
    def test_is_valid_password(self):
        valid, msg = is_valid_password("SecurePass123")
        assert valid == True
        
        valid, msg = is_valid_password("weak")
        assert valid == False
        assert "8 caractères" in msg
        
        valid, msg = is_valid_password("nouppercase123")
        assert valid == False
    
    def test_is_valid_uuid(self):
        assert is_valid_uuid("550e8400-e29b-41d4-a716-446655440000") == True
        assert is_valid_uuid("not-a-uuid") == False


class TestFormatters:
    """Tests formateurs"""
    
    def test_format_currency(self):
        from decimal import Decimal
        assert format_currency(Decimal("1234.56"), "CAD", "fr") == "1 234,56 $"
        assert format_currency(Decimal("1234.56"), "USD", "en") == "$1,234.56"
    
    def test_format_phone(self):
        assert format_phone("5145551234") == "(514) 555-1234"
        assert format_phone("+15145551234", "international") == "+1 (514) 555-1234"
