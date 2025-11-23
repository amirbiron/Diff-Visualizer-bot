#!/usr/bin/env python3
"""
Test script for Diff Visualizer
Demonstrates the diff functionality without Telegram
"""

from diff_bot import DiffGenerator

def test_diff():
    """Test the diff generator with sample code"""
    
    print("🎨 Diff Visualizer - Local Test")
    print("=" * 50)
    print()
    
    # Sample code 1
    code1 = """def hello():
    print("Hello World")
    return True"""
    
    # Sample code 2
    code2 = """def hello(name):
    print(f"Hello {name}!")
    return True"""
    
    print("📝 Original Code:")
    print("-" * 50)
    print(code1)
    print()
    
    print("📝 Modified Code:")
    print("-" * 50)
    print(code2)
    print()
    
    # Generate diff
    diff_gen = DiffGenerator()
    
    print("🔍 Text Diff:")
    print("=" * 50)
    text_diff = diff_gen.generate_text_diff(code1, code2)
    print(text_diff)
    print()
    
    # Generate HTML
    print("📄 Generating HTML diff...")
    html_diff = diff_gen.generate_html_diff(code1, code2)
    
    # Save to file
    with open('test_diff.html', 'w', encoding='utf-8') as f:
        f.write(html_diff)
    
    print("✅ HTML diff saved to: test_diff.html")
    print("💡 Open the file in your browser to see the colored diff!")
    print()
    
    # Another example with more changes
    print("\n" + "=" * 50)
    print("📝 Example 2: More Complex Changes")
    print("=" * 50)
    print()
    
    code3 = """class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        result = a * b
        return result"""
    
    code4 = """class Calculator:
    def add(self, a, b):
        \"\"\"Add two numbers\"\"\"
        return a + b
    
    def subtract(self, a, b):
        \"\"\"Subtract b from a\"\"\"
        return a - b
    
    def multiply(self, a, b):
        \"\"\"Multiply two numbers\"\"\"
        return a * b"""
    
    text_diff2 = diff_gen.generate_text_diff(code3, code4)
    print(text_diff2)


if __name__ == '__main__':
    test_diff()
