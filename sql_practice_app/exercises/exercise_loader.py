"""
Exercise Loader for SQL Practice Generator
Loads and manages exercise templates
"""
import json
import os
import random
from typing import List, Dict, Any, Optional
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SKILL_LEVELS


class ExerciseLoader:
    """Loads exercise templates from JSON files"""

    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.templates_dir = templates_dir
        self.templates = {}
        self._load_templates()

    def _load_templates(self):
        """Load all exercise templates from the templates directory"""
        self.templates = self._get_built_in_templates()

        # Also load from JSON files if they exist
        if os.path.exists(self.templates_dir):
            for filename in os.listdir(self.templates_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.templates_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                for template in data:
                                    self.templates[template['id']] = template
                            elif isinstance(data, dict) and 'id' in data:
                                self.templates[data['id']] = data
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Warning: Could not load template from {filename}: {e}")

    def _get_built_in_templates(self) -> Dict[str, Dict]:
        """Return built-in exercise templates"""
        templates = {}

        # Level 1: Foundation (SELECT, WHERE, basic operators)
        level1_templates = [
            {
                "id": "l1_select_basic_001",
                "level": 1,
                "difficulty": "easy",
                "skills": ["SELECT"],
                "scenario": "ecommerce",
                "problem": "Select all columns from the customers table.",
                "tables": ["customers"],
                "solution": "SELECT * FROM customers",
                "hints": [
                    "Use SELECT * to get all columns",
                    "The table name is 'customers'"
                ]
            },
            {
                "id": "l1_select_columns_001",
                "level": 1,
                "difficulty": "easy",
                "skills": ["SELECT"],
                "scenario": "ecommerce",
                "problem": "Select only the first_name and last_name columns from the customers table.",
                "tables": ["customers"],
                "solution": "SELECT first_name, last_name FROM customers",
                "hints": [
                    "List the columns you want separated by commas",
                    "You need first_name and last_name"
                ]
            },
            {
                "id": "l1_where_equals_001",
                "level": 1,
                "difficulty": "easy",
                "skills": ["SELECT", "WHERE", "OPERATORS"],
                "scenario": "ecommerce",
                "problem": "Find all customers who are not active (is_active = 0).",
                "tables": ["customers"],
                "solution": "SELECT * FROM customers WHERE is_active = 0",
                "hints": [
                    "Use WHERE to filter rows",
                    "is_active column contains 0 for inactive customers"
                ]
            },
            {
                "id": "l1_where_greater_001",
                "level": 1,
                "difficulty": "easy",
                "skills": ["SELECT", "WHERE", "OPERATORS"],
                "scenario": "ecommerce",
                "problem": "Find all products with a price greater than 100.",
                "tables": ["products"],
                "solution": "SELECT * FROM products WHERE price > 100",
                "hints": [
                    "Use the > operator for 'greater than'",
                    "Filter on the price column"
                ]
            },
            {
                "id": "l1_between_001",
                "level": 1,
                "difficulty": "medium",
                "skills": ["SELECT", "WHERE", "BETWEEN"],
                "scenario": "ecommerce",
                "problem": "Find all products with a price between 50 and 200 (inclusive).",
                "tables": ["products"],
                "solution": "SELECT * FROM products WHERE price BETWEEN 50 AND 200",
                "hints": [
                    "BETWEEN includes both endpoints",
                    "Syntax: column BETWEEN low AND high"
                ]
            },
            {
                "id": "l1_in_001",
                "level": 1,
                "difficulty": "medium",
                "skills": ["SELECT", "WHERE", "IN"],
                "scenario": "ecommerce",
                "problem": "Find all orders with status 'pending', 'processing', or 'shipped'.",
                "tables": ["orders"],
                "solution": "SELECT * FROM orders WHERE status IN ('pending', 'processing', 'shipped')",
                "hints": [
                    "IN allows you to specify multiple values",
                    "Syntax: column IN (value1, value2, ...)"
                ]
            },
            {
                "id": "l1_like_001",
                "level": 1,
                "difficulty": "medium",
                "skills": ["SELECT", "WHERE", "LIKE"],
                "scenario": "ecommerce",
                "problem": "Find all customers whose email ends with 'gmail.com'.",
                "tables": ["customers"],
                "solution": "SELECT * FROM customers WHERE email LIKE '%gmail.com'",
                "hints": [
                    "% is a wildcard matching any characters",
                    "Use % before the pattern to match anything at the start"
                ]
            },
            {
                "id": "l1_limit_001",
                "level": 1,
                "difficulty": "easy",
                "skills": ["SELECT", "LIMIT"],
                "scenario": "ecommerce",
                "problem": "Select the first 10 products from the products table.",
                "tables": ["products"],
                "solution": "SELECT * FROM products LIMIT 10",
                "hints": [
                    "LIMIT restricts the number of rows returned",
                    "Put LIMIT at the end of your query"
                ]
            },
            {
                "id": "l1_offset_001",
                "level": 1,
                "difficulty": "medium",
                "skills": ["SELECT", "LIMIT", "OFFSET"],
                "scenario": "ecommerce",
                "problem": "Select 5 products starting from the 11th product (skip the first 10).",
                "tables": ["products"],
                "solution": "SELECT * FROM products LIMIT 5 OFFSET 10",
                "hints": [
                    "OFFSET skips a number of rows",
                    "Combine LIMIT and OFFSET for pagination"
                ]
            },
            {
                "id": "l1_and_or_001",
                "level": 1,
                "difficulty": "hard",
                "skills": ["SELECT", "WHERE", "OPERATORS"],
                "scenario": "ecommerce",
                "problem": "Find all active customers (is_active = 1) from the state 'CA' or 'NY' with more than 1000 loyalty points.",
                "tables": ["customers"],
                "solution": "SELECT * FROM customers WHERE is_active = 1 AND (state = 'CA' OR state = 'NY') AND loyalty_points > 1000",
                "hints": [
                    "Use AND to combine conditions that must all be true",
                    "Use OR for conditions where any can be true",
                    "Use parentheses to group OR conditions"
                ]
            },
            # HR scenario templates
            {
                "id": "l1_hr_select_001",
                "level": 1,
                "difficulty": "easy",
                "skills": ["SELECT"],
                "scenario": "hr",
                "problem": "Select all employees from the employees table.",
                "tables": ["employees"],
                "solution": "SELECT * FROM employees",
                "hints": [
                    "Use SELECT * to get all columns",
                    "The table name is 'employees'"
                ]
            },
            {
                "id": "l1_hr_where_001",
                "level": 1,
                "difficulty": "medium",
                "skills": ["SELECT", "WHERE", "OPERATORS"],
                "scenario": "hr",
                "problem": "Find all employees with a salary greater than 100000.",
                "tables": ["employees"],
                "solution": "SELECT * FROM employees WHERE salary > 100000",
                "hints": [
                    "Use the > operator for comparison",
                    "Filter on the salary column"
                ]
            },
            {
                "id": "l1_hr_like_001",
                "level": 1,
                "difficulty": "hard",
                "skills": ["SELECT", "WHERE", "LIKE", "OPERATORS"],
                "scenario": "hr",
                "problem": "Find all employees whose job title contains 'Manager' and who have been active (is_active = 1).",
                "tables": ["employees"],
                "solution": "SELECT * FROM employees WHERE job_title LIKE '%Manager%' AND is_active = 1",
                "hints": [
                    "Use LIKE with % wildcards on both sides",
                    "Combine conditions with AND"
                ]
            },
            # Finance scenario
            {
                "id": "l1_finance_select_001",
                "level": 1,
                "difficulty": "easy",
                "skills": ["SELECT", "WHERE"],
                "scenario": "finance",
                "problem": "Find all accounts with a balance greater than 10000.",
                "tables": ["accounts"],
                "solution": "SELECT * FROM accounts WHERE balance > 10000",
                "hints": [
                    "Use WHERE to filter",
                    "Use > for greater than"
                ]
            },
            {
                "id": "l1_finance_between_001",
                "level": 1,
                "difficulty": "medium",
                "skills": ["SELECT", "WHERE", "BETWEEN"],
                "scenario": "finance",
                "problem": "Find all transactions with an amount between -1000 and -100 (withdrawals in that range).",
                "tables": ["transactions"],
                "solution": "SELECT * FROM transactions WHERE amount BETWEEN -1000 AND -100",
                "hints": [
                    "Negative amounts represent withdrawals",
                    "BETWEEN works with negative numbers too"
                ]
            },
            # Social media scenario
            {
                "id": "l1_social_select_001",
                "level": 1,
                "difficulty": "easy",
                "skills": ["SELECT"],
                "scenario": "social_media",
                "problem": "Select all posts from the posts table.",
                "tables": ["posts"],
                "solution": "SELECT * FROM posts",
                "hints": [
                    "Use SELECT * to get all columns"
                ]
            },
            {
                "id": "l1_social_where_001",
                "level": 1,
                "difficulty": "medium",
                "skills": ["SELECT", "WHERE", "OPERATORS"],
                "scenario": "social_media",
                "problem": "Find all users who are verified (is_verified = 1).",
                "tables": ["users"],
                "solution": "SELECT * FROM users WHERE is_verified = 1",
                "hints": [
                    "is_verified is a boolean column (0 or 1)",
                    "Use = for equality comparison"
                ]
            },
            # Healthcare scenario
            {
                "id": "l1_health_select_001",
                "level": 1,
                "difficulty": "easy",
                "skills": ["SELECT"],
                "scenario": "healthcare",
                "problem": "Select all patients from the patients table.",
                "tables": ["patients"],
                "solution": "SELECT * FROM patients",
                "hints": [
                    "Use SELECT * to get all columns"
                ]
            },
            {
                "id": "l1_health_in_001",
                "level": 1,
                "difficulty": "medium",
                "skills": ["SELECT", "WHERE", "IN"],
                "scenario": "healthcare",
                "problem": "Find all patients with blood type 'A+', 'A-', or 'O+'.",
                "tables": ["patients"],
                "solution": "SELECT * FROM patients WHERE blood_type IN ('A+', 'A-', 'O+')",
                "hints": [
                    "Use IN for multiple values",
                    "Blood types are stored as text"
                ]
            },
            # Education scenario
            {
                "id": "l1_edu_select_001",
                "level": 1,
                "difficulty": "easy",
                "skills": ["SELECT"],
                "scenario": "education",
                "problem": "Select all students from the students table.",
                "tables": ["students"],
                "solution": "SELECT * FROM students",
                "hints": [
                    "Use SELECT * to get all columns"
                ]
            },
            {
                "id": "l1_edu_where_001",
                "level": 1,
                "difficulty": "medium",
                "skills": ["SELECT", "WHERE", "OPERATORS"],
                "scenario": "education",
                "problem": "Find all students with a GPA greater than or equal to 3.5.",
                "tables": ["students"],
                "solution": "SELECT * FROM students WHERE gpa >= 3.5",
                "hints": [
                    "Use >= for greater than or equal to",
                    "GPA is a decimal value"
                ]
            },
        ]

        # Level 2: Sorting & Uniqueness
        level2_templates = [
            {
                "id": "l2_orderby_001",
                "level": 2,
                "difficulty": "easy",
                "skills": ["SELECT", "ORDER_BY"],
                "scenario": "ecommerce",
                "problem": "Select all products ordered by price from lowest to highest.",
                "tables": ["products"],
                "solution": "SELECT * FROM products ORDER BY price ASC",
                "hints": [
                    "ORDER BY sorts results",
                    "ASC means ascending (lowest to highest)"
                ]
            },
            {
                "id": "l2_orderby_desc_001",
                "level": 2,
                "difficulty": "easy",
                "skills": ["SELECT", "ORDER_BY"],
                "scenario": "ecommerce",
                "problem": "Select all customers ordered by loyalty_points from highest to lowest.",
                "tables": ["customers"],
                "solution": "SELECT * FROM customers ORDER BY loyalty_points DESC",
                "hints": [
                    "DESC means descending (highest to lowest)"
                ]
            },
            {
                "id": "l2_distinct_001",
                "level": 2,
                "difficulty": "easy",
                "skills": ["SELECT", "DISTINCT"],
                "scenario": "ecommerce",
                "problem": "Find all distinct (unique) states where customers are located.",
                "tables": ["customers"],
                "solution": "SELECT DISTINCT state FROM customers",
                "hints": [
                    "DISTINCT removes duplicate values",
                    "Put DISTINCT after SELECT"
                ]
            },
            {
                "id": "l2_upper_001",
                "level": 2,
                "difficulty": "medium",
                "skills": ["SELECT", "UPPER"],
                "scenario": "ecommerce",
                "problem": "Select customer first_name and last_name with the last_name in uppercase.",
                "tables": ["customers"],
                "solution": "SELECT first_name, UPPER(last_name) as last_name FROM customers",
                "hints": [
                    "UPPER() converts text to uppercase",
                    "Use an alias to name the result column"
                ]
            },
            {
                "id": "l2_round_001",
                "level": 2,
                "difficulty": "medium",
                "skills": ["SELECT", "ROUND"],
                "scenario": "ecommerce",
                "problem": "Select product name and price rounded to the nearest whole number.",
                "tables": ["products"],
                "solution": "SELECT name, ROUND(price) as rounded_price FROM products",
                "hints": [
                    "ROUND() rounds a number",
                    "Without a second argument, it rounds to a whole number"
                ]
            },
            {
                "id": "l2_orderby_multi_001",
                "level": 2,
                "difficulty": "hard",
                "skills": ["SELECT", "WHERE", "ORDER_BY", "LIMIT"],
                "scenario": "ecommerce",
                "problem": "Find the top 10 most expensive products that are active (is_active = 1), ordered by price descending, then by name ascending.",
                "tables": ["products"],
                "solution": "SELECT * FROM products WHERE is_active = 1 ORDER BY price DESC, name ASC LIMIT 10",
                "hints": [
                    "ORDER BY can use multiple columns",
                    "Second column is used when first column has ties"
                ]
            },
            {
                "id": "l2_hr_orderby_001",
                "level": 2,
                "difficulty": "medium",
                "skills": ["SELECT", "ORDER_BY", "WHERE"],
                "scenario": "hr",
                "problem": "Find all active employees ordered by salary descending. Show only the top 20.",
                "tables": ["employees"],
                "solution": "SELECT * FROM employees WHERE is_active = 1 ORDER BY salary DESC LIMIT 20",
                "hints": [
                    "Combine WHERE, ORDER BY, and LIMIT",
                    "Filter first, then sort, then limit"
                ]
            },
            {
                "id": "l2_finance_distinct_001",
                "level": 2,
                "difficulty": "medium",
                "skills": ["SELECT", "DISTINCT", "ORDER_BY"],
                "scenario": "finance",
                "problem": "Find all distinct transaction categories, ordered alphabetically.",
                "tables": ["transactions"],
                "solution": "SELECT DISTINCT category FROM transactions ORDER BY category",
                "hints": [
                    "DISTINCT with ORDER BY",
                    "NULL values may appear in results"
                ]
            },
            {
                "id": "l2_length_001",
                "level": 2,
                "difficulty": "hard",
                "skills": ["SELECT", "LENGTH", "WHERE", "ORDER_BY"],
                "scenario": "social_media",
                "problem": "Find all posts where the content length is greater than 200 characters, showing the post id, content, and content length. Order by content length descending.",
                "tables": ["posts"],
                "solution": "SELECT id, content, LENGTH(content) as content_length FROM posts WHERE LENGTH(content) > 200 ORDER BY content_length DESC",
                "hints": [
                    "LENGTH() returns the number of characters",
                    "You can use LENGTH() in both SELECT and WHERE"
                ]
            },
            {
                "id": "l2_substr_001",
                "level": 2,
                "difficulty": "hard",
                "skills": ["SELECT", "SUBSTR", "WHERE"],
                "scenario": "ecommerce",
                "problem": "Find all products whose SKU starts with 'SKU-0001' (the first 8 characters). Show the product name and SKU.",
                "tables": ["products"],
                "solution": "SELECT name, sku FROM products WHERE SUBSTR(sku, 1, 8) = 'SKU-0001'",
                "hints": [
                    "SUBSTR(string, start, length) extracts a substring",
                    "First position is 1, not 0"
                ]
            },
        ]

        # Level 3: Aggregation Basics
        level3_templates = [
            {
                "id": "l3_count_001",
                "level": 3,
                "difficulty": "easy",
                "skills": ["SELECT", "COUNT"],
                "scenario": "ecommerce",
                "problem": "Count the total number of customers in the customers table.",
                "tables": ["customers"],
                "solution": "SELECT COUNT(*) as total_customers FROM customers",
                "hints": [
                    "COUNT(*) counts all rows",
                    "Use an alias for clarity"
                ]
            },
            {
                "id": "l3_sum_001",
                "level": 3,
                "difficulty": "easy",
                "skills": ["SELECT", "SUM"],
                "scenario": "ecommerce",
                "problem": "Calculate the total amount of all orders.",
                "tables": ["orders"],
                "solution": "SELECT SUM(total_amount) as total_sales FROM orders",
                "hints": [
                    "SUM() adds up all values in a column"
                ]
            },
            {
                "id": "l3_avg_001",
                "level": 3,
                "difficulty": "easy",
                "skills": ["SELECT", "AVG", "ROUND"],
                "scenario": "ecommerce",
                "problem": "Calculate the average price of all products, rounded to 2 decimal places.",
                "tables": ["products"],
                "solution": "SELECT ROUND(AVG(price), 2) as avg_price FROM products",
                "hints": [
                    "AVG() calculates the mean",
                    "ROUND(value, 2) rounds to 2 decimal places"
                ]
            },
            {
                "id": "l3_groupby_001",
                "level": 3,
                "difficulty": "medium",
                "skills": ["SELECT", "GROUP_BY", "COUNT"],
                "scenario": "ecommerce",
                "problem": "Count the number of products in each category. Show category_id and product count.",
                "tables": ["products"],
                "solution": "SELECT category_id, COUNT(*) as product_count FROM products GROUP BY category_id",
                "hints": [
                    "GROUP BY groups rows with the same value",
                    "Aggregations are calculated per group"
                ]
            },
            {
                "id": "l3_having_001",
                "level": 3,
                "difficulty": "medium",
                "skills": ["SELECT", "GROUP_BY", "HAVING", "COUNT"],
                "scenario": "ecommerce",
                "problem": "Find categories with more than 5 products. Show category_id and product count.",
                "tables": ["products"],
                "solution": "SELECT category_id, COUNT(*) as product_count FROM products GROUP BY category_id HAVING COUNT(*) > 5",
                "hints": [
                    "HAVING filters groups (like WHERE for aggregations)",
                    "HAVING comes after GROUP BY"
                ]
            },
            {
                "id": "l3_minmax_001",
                "level": 3,
                "difficulty": "medium",
                "skills": ["SELECT", "MIN", "MAX"],
                "scenario": "ecommerce",
                "problem": "Find the minimum and maximum price of products.",
                "tables": ["products"],
                "solution": "SELECT MIN(price) as min_price, MAX(price) as max_price FROM products",
                "hints": [
                    "MIN() and MAX() find extreme values",
                    "You can use multiple aggregations in one query"
                ]
            },
            {
                "id": "l3_groupby_multi_001",
                "level": 3,
                "difficulty": "hard",
                "skills": ["SELECT", "GROUP_BY", "COUNT", "AVG", "ORDER_BY"],
                "scenario": "ecommerce",
                "problem": "For each order status, find the count of orders and the average order amount. Order by count descending.",
                "tables": ["orders"],
                "solution": "SELECT status, COUNT(*) as order_count, ROUND(AVG(total_amount), 2) as avg_amount FROM orders GROUP BY status ORDER BY order_count DESC",
                "hints": [
                    "Group by status",
                    "Use multiple aggregations",
                    "ORDER BY works after GROUP BY"
                ]
            },
            {
                "id": "l3_hr_salary_001",
                "level": 3,
                "difficulty": "hard",
                "skills": ["SELECT", "GROUP_BY", "AVG", "HAVING", "ORDER_BY"],
                "scenario": "hr",
                "problem": "Find departments (by department_id) where the average salary is greater than 80000. Show department_id and average salary. Order by average salary descending.",
                "tables": ["employees"],
                "solution": "SELECT department_id, ROUND(AVG(salary), 2) as avg_salary FROM employees GROUP BY department_id HAVING AVG(salary) > 80000 ORDER BY avg_salary DESC",
                "hints": [
                    "Use HAVING to filter by aggregate values",
                    "You can use the aggregate in both SELECT and HAVING"
                ]
            },
            {
                "id": "l3_finance_trans_001",
                "level": 3,
                "difficulty": "hard",
                "skills": ["SELECT", "GROUP_BY", "SUM", "COUNT", "WHERE"],
                "scenario": "finance",
                "problem": "For each account_id, calculate the total deposit amount (positive amounts only) and count of deposits. Only include accounts with total deposits over 5000.",
                "tables": ["transactions"],
                "solution": "SELECT account_id, SUM(amount) as total_deposits, COUNT(*) as deposit_count FROM transactions WHERE amount > 0 GROUP BY account_id HAVING SUM(amount) > 5000",
                "hints": [
                    "Filter positive amounts with WHERE",
                    "Then group and apply HAVING"
                ]
            },
            {
                "id": "l3_social_posts_001",
                "level": 3,
                "difficulty": "medium",
                "skills": ["SELECT", "GROUP_BY", "COUNT", "ORDER_BY", "LIMIT"],
                "scenario": "social_media",
                "problem": "Find the top 5 users with the most posts. Show user_id and post count.",
                "tables": ["posts"],
                "solution": "SELECT user_id, COUNT(*) as post_count FROM posts GROUP BY user_id ORDER BY post_count DESC LIMIT 5",
                "hints": [
                    "Group by user_id",
                    "Count and order to find top posters"
                ]
            },
        ]

        # Level 4: Basic Joins
        level4_templates = [
            {
                "id": "l4_inner_join_001",
                "level": 4,
                "difficulty": "easy",
                "skills": ["SELECT", "INNER_JOIN"],
                "scenario": "ecommerce",
                "problem": "List all orders with customer information. Show order id, order_date, and customer first_name and last_name.",
                "tables": ["orders", "customers"],
                "solution": "SELECT o.id, o.order_date, c.first_name, c.last_name FROM orders o INNER JOIN customers c ON o.customer_id = c.id",
                "hints": [
                    "INNER JOIN combines matching rows from both tables",
                    "Use table aliases (o, c) for shorter syntax",
                    "ON specifies the join condition"
                ]
            },
            {
                "id": "l4_inner_join_002",
                "level": 4,
                "difficulty": "easy",
                "skills": ["SELECT", "INNER_JOIN"],
                "scenario": "ecommerce",
                "problem": "List all products with their category names. Show product name and category name.",
                "tables": ["products", "categories"],
                "solution": "SELECT p.name as product_name, c.name as category_name FROM products p INNER JOIN categories c ON p.category_id = c.id",
                "hints": [
                    "Join products and categories tables",
                    "Use aliases to distinguish column names"
                ]
            },
            {
                "id": "l4_join_where_001",
                "level": 4,
                "difficulty": "medium",
                "skills": ["SELECT", "INNER_JOIN", "WHERE"],
                "scenario": "ecommerce",
                "problem": "Find all orders placed by customers from California (state = 'CA'). Show order id, order_date, and customer name.",
                "tables": ["orders", "customers"],
                "solution": "SELECT o.id, o.order_date, c.first_name, c.last_name FROM orders o INNER JOIN customers c ON o.customer_id = c.id WHERE c.state = 'CA'",
                "hints": [
                    "First join the tables",
                    "Then filter with WHERE"
                ]
            },
            {
                "id": "l4_join_groupby_001",
                "level": 4,
                "difficulty": "medium",
                "skills": ["SELECT", "INNER_JOIN", "GROUP_BY", "COUNT"],
                "scenario": "ecommerce",
                "problem": "Count the number of products in each category. Show category name and product count.",
                "tables": ["products", "categories"],
                "solution": "SELECT c.name as category_name, COUNT(p.id) as product_count FROM categories c INNER JOIN products p ON c.id = p.category_id GROUP BY c.name",
                "hints": [
                    "Join categories with products",
                    "Group by category name",
                    "Count the products"
                ]
            },
            {
                "id": "l4_join_agg_001",
                "level": 4,
                "difficulty": "hard",
                "skills": ["SELECT", "INNER_JOIN", "GROUP_BY", "SUM", "ORDER_BY"],
                "scenario": "ecommerce",
                "problem": "Calculate the total revenue per customer. Show customer name and total amount spent. Order by total spent descending, show top 10.",
                "tables": ["orders", "customers"],
                "solution": "SELECT c.first_name, c.last_name, SUM(o.total_amount) as total_spent FROM customers c INNER JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.first_name, c.last_name ORDER BY total_spent DESC LIMIT 10",
                "hints": [
                    "Join customers with orders",
                    "Sum the order amounts per customer",
                    "GROUP BY customer identifier"
                ]
            },
            {
                "id": "l4_hr_join_001",
                "level": 4,
                "difficulty": "medium",
                "skills": ["SELECT", "INNER_JOIN", "WHERE"],
                "scenario": "hr",
                "problem": "List all employees with their department names. Show employee first_name, last_name, and department name. Only include active employees.",
                "tables": ["employees", "departments"],
                "solution": "SELECT e.first_name, e.last_name, d.name as department_name FROM employees e INNER JOIN departments d ON e.department_id = d.id WHERE e.is_active = 1",
                "hints": [
                    "Join employees and departments",
                    "Filter for active employees"
                ]
            },
            {
                "id": "l4_finance_join_001",
                "level": 4,
                "difficulty": "hard",
                "skills": ["SELECT", "INNER_JOIN", "GROUP_BY", "SUM", "HAVING"],
                "scenario": "finance",
                "problem": "Find customers who have accounts with total balance over 50000. Show customer name and total balance across all their accounts.",
                "tables": ["customers", "accounts"],
                "solution": "SELECT c.first_name, c.last_name, SUM(a.balance) as total_balance FROM customers c INNER JOIN accounts a ON c.id = a.customer_id GROUP BY c.id, c.first_name, c.last_name HAVING SUM(a.balance) > 50000",
                "hints": [
                    "Join customers with accounts",
                    "Sum balances per customer",
                    "Filter with HAVING"
                ]
            },
            {
                "id": "l4_health_join_001",
                "level": 4,
                "difficulty": "medium",
                "skills": ["SELECT", "INNER_JOIN", "ORDER_BY"],
                "scenario": "healthcare",
                "problem": "List all appointments with patient and doctor names. Show appointment date, patient name, and doctor name. Order by appointment date.",
                "tables": ["appointments", "patients", "doctors"],
                "solution": "SELECT a.appointment_date, p.first_name || ' ' || p.last_name as patient_name, d.first_name || ' ' || d.last_name as doctor_name FROM appointments a INNER JOIN patients p ON a.patient_id = p.id INNER JOIN doctors d ON a.doctor_id = d.id ORDER BY a.appointment_date",
                "hints": [
                    "You need two joins: appointments to patients, appointments to doctors",
                    "Use || to concatenate names"
                ]
            },
            {
                "id": "l4_edu_join_001",
                "level": 4,
                "difficulty": "hard",
                "skills": ["SELECT", "INNER_JOIN", "GROUP_BY", "AVG", "ORDER_BY"],
                "scenario": "education",
                "problem": "Find the average GPA by department (major). Show department name and average GPA, rounded to 2 decimals. Order by average GPA descending.",
                "tables": ["students", "departments"],
                "solution": "SELECT d.name as department, ROUND(AVG(s.gpa), 2) as avg_gpa FROM students s INNER JOIN departments d ON s.major_department_id = d.id GROUP BY d.id, d.name ORDER BY avg_gpa DESC",
                "hints": [
                    "Join students with departments on major_department_id",
                    "Calculate average GPA per department"
                ]
            },
        ]

        # Level 5: Advanced Joins
        level5_templates = [
            {
                "id": "l5_left_join_001",
                "level": 5,
                "difficulty": "easy",
                "skills": ["SELECT", "LEFT_JOIN"],
                "scenario": "ecommerce",
                "problem": "List all customers and their orders. Include customers who have never placed an order (they should show NULL for order columns).",
                "tables": ["customers", "orders"],
                "solution": "SELECT c.id, c.first_name, c.last_name, o.id as order_id, o.order_date FROM customers c LEFT JOIN orders o ON c.id = o.customer_id",
                "hints": [
                    "LEFT JOIN keeps all rows from the left table",
                    "Unmatched rows get NULL for right table columns"
                ]
            },
            {
                "id": "l5_left_join_null_001",
                "level": 5,
                "difficulty": "medium",
                "skills": ["SELECT", "LEFT_JOIN", "WHERE"],
                "scenario": "ecommerce",
                "problem": "Find all customers who have never placed an order.",
                "tables": ["customers", "orders"],
                "solution": "SELECT c.* FROM customers c LEFT JOIN orders o ON c.id = o.customer_id WHERE o.id IS NULL",
                "hints": [
                    "Use LEFT JOIN and filter for NULL",
                    "Check if the order id IS NULL"
                ]
            },
            {
                "id": "l5_self_join_001",
                "level": 5,
                "difficulty": "medium",
                "skills": ["SELECT", "SELF_JOIN"],
                "scenario": "hr",
                "problem": "List all employees with their manager's name. Show employee name and manager name.",
                "tables": ["employees"],
                "solution": "SELECT e.first_name || ' ' || e.last_name as employee_name, m.first_name || ' ' || m.last_name as manager_name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id",
                "hints": [
                    "A self-join joins a table to itself",
                    "Use different aliases for the same table",
                    "LEFT JOIN to include employees without managers"
                ]
            },
            {
                "id": "l5_multiple_joins_001",
                "level": 5,
                "difficulty": "hard",
                "skills": ["SELECT", "MULTIPLE_JOINS", "GROUP_BY", "SUM"],
                "scenario": "ecommerce",
                "problem": "Calculate the total revenue per product category. Show category name and total revenue (sum of quantity * unit_price from order_items).",
                "tables": ["categories", "products", "order_items"],
                "solution": "SELECT c.name as category, SUM(oi.quantity * oi.unit_price) as total_revenue FROM categories c INNER JOIN products p ON c.id = p.category_id INNER JOIN order_items oi ON p.id = oi.product_id GROUP BY c.id, c.name ORDER BY total_revenue DESC",
                "hints": [
                    "Join categories -> products -> order_items",
                    "Calculate revenue as quantity * unit_price",
                    "Sum by category"
                ]
            },
            {
                "id": "l5_full_join_001",
                "level": 5,
                "difficulty": "hard",
                "skills": ["SELECT", "FULL_JOIN"],
                "scenario": "hr",
                "problem": "Create a report showing all employees and all projects, matched where assignments exist. Include employees with no projects and projects with no employees.",
                "tables": ["employees", "projects", "project_assignments"],
                "solution": "SELECT e.first_name, e.last_name, p.name as project_name FROM employees e LEFT JOIN project_assignments pa ON e.id = pa.employee_id LEFT JOIN projects p ON pa.project_id = p.id UNION SELECT e.first_name, e.last_name, p.name FROM projects p LEFT JOIN project_assignments pa ON p.id = pa.project_id LEFT JOIN employees e ON pa.employee_id = e.id WHERE e.id IS NULL",
                "hints": [
                    "SQLite doesn't have FULL OUTER JOIN directly",
                    "Use UNION of two LEFT JOINs",
                    "Or use LEFT JOIN and filter appropriately"
                ]
            },
            {
                "id": "l5_cross_join_001",
                "level": 5,
                "difficulty": "medium",
                "skills": ["SELECT", "CROSS_JOIN", "LIMIT"],
                "scenario": "ecommerce",
                "problem": "Generate all possible combinations of the first 5 products and first 5 categories (25 combinations total).",
                "tables": ["products", "categories"],
                "solution": "SELECT p.name as product, c.name as category FROM (SELECT * FROM products LIMIT 5) p CROSS JOIN (SELECT * FROM categories LIMIT 5) c",
                "hints": [
                    "CROSS JOIN produces a Cartesian product",
                    "Every row from first table paired with every row from second"
                ]
            },
            {
                "id": "l5_left_join_agg_001",
                "level": 5,
                "difficulty": "hard",
                "skills": ["SELECT", "LEFT_JOIN", "GROUP_BY", "COUNT", "COALESCE"],
                "scenario": "ecommerce",
                "problem": "For each customer, count their total orders. Include customers with zero orders (show 0 for them).",
                "tables": ["customers", "orders"],
                "solution": "SELECT c.first_name, c.last_name, COUNT(o.id) as order_count FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.first_name, c.last_name ORDER BY order_count DESC",
                "hints": [
                    "LEFT JOIN to keep all customers",
                    "COUNT(o.id) returns 0 when no orders",
                    "COUNT(*) would count 1 for NULL rows"
                ]
            },
            {
                "id": "l5_social_joins_001",
                "level": 5,
                "difficulty": "hard",
                "skills": ["SELECT", "LEFT_JOIN", "GROUP_BY", "COUNT"],
                "scenario": "social_media",
                "problem": "Find all users and their follower count. Include users with 0 followers.",
                "tables": ["users", "follows"],
                "solution": "SELECT u.username, u.display_name, COUNT(f.follower_id) as follower_count FROM users u LEFT JOIN follows f ON u.id = f.following_id GROUP BY u.id, u.username, u.display_name ORDER BY follower_count DESC",
                "hints": [
                    "follows table has follower_id and following_id",
                    "You want users being followed (following_id)"
                ]
            },
        ]

        # Level 6: Subqueries
        level6_templates = [
            {
                "id": "l6_subquery_where_001",
                "level": 6,
                "difficulty": "easy",
                "skills": ["SELECT", "SUBQUERY_WHERE"],
                "scenario": "ecommerce",
                "problem": "Find all products with a price higher than the average product price.",
                "tables": ["products"],
                "solution": "SELECT * FROM products WHERE price > (SELECT AVG(price) FROM products)",
                "hints": [
                    "The subquery calculates the average",
                    "The outer query uses it for comparison"
                ]
            },
            {
                "id": "l6_subquery_in_001",
                "level": 6,
                "difficulty": "medium",
                "skills": ["SELECT", "SUBQUERY_WHERE", "IN"],
                "scenario": "ecommerce",
                "problem": "Find all customers who have placed at least one order.",
                "tables": ["customers", "orders"],
                "solution": "SELECT * FROM customers WHERE id IN (SELECT DISTINCT customer_id FROM orders)",
                "hints": [
                    "Subquery returns list of customer IDs with orders",
                    "Use IN to match against the list"
                ]
            },
            {
                "id": "l6_subquery_from_001",
                "level": 6,
                "difficulty": "medium",
                "skills": ["SELECT", "SUBQUERY_FROM", "GROUP_BY"],
                "scenario": "ecommerce",
                "problem": "Find the average number of orders per customer. (First calculate orders per customer, then average that.)",
                "tables": ["orders"],
                "solution": "SELECT AVG(order_count) as avg_orders_per_customer FROM (SELECT customer_id, COUNT(*) as order_count FROM orders GROUP BY customer_id) as customer_orders",
                "hints": [
                    "Inner query: count orders per customer",
                    "Outer query: average the counts",
                    "Subquery in FROM needs an alias"
                ]
            },
            {
                "id": "l6_exists_001",
                "level": 6,
                "difficulty": "medium",
                "skills": ["SELECT", "EXISTS"],
                "scenario": "ecommerce",
                "problem": "Find all customers who have placed at least one order (using EXISTS).",
                "tables": ["customers", "orders"],
                "solution": "SELECT * FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)",
                "hints": [
                    "EXISTS checks if subquery returns any rows",
                    "The subquery references the outer query (correlated)"
                ]
            },
            {
                "id": "l6_not_exists_001",
                "level": 6,
                "difficulty": "medium",
                "skills": ["SELECT", "NOT_EXISTS"],
                "scenario": "ecommerce",
                "problem": "Find all customers who have never placed an order (using NOT EXISTS).",
                "tables": ["customers", "orders"],
                "solution": "SELECT * FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)",
                "hints": [
                    "NOT EXISTS is true when subquery returns no rows",
                    "Good for finding missing relationships"
                ]
            },
            {
                "id": "l6_correlated_001",
                "level": 6,
                "difficulty": "hard",
                "skills": ["SELECT", "CORRELATED_SUBQUERY"],
                "scenario": "ecommerce",
                "problem": "For each product, find its price and the average price in its category. Show product name, price, and category average.",
                "tables": ["products"],
                "solution": "SELECT p.name, p.price, (SELECT AVG(p2.price) FROM products p2 WHERE p2.category_id = p.category_id) as category_avg FROM products p",
                "hints": [
                    "The subquery references p.category_id from outer query",
                    "This is a correlated subquery - runs for each row"
                ]
            },
            {
                "id": "l6_subquery_select_001",
                "level": 6,
                "difficulty": "hard",
                "skills": ["SELECT", "SUBQUERY_SELECT", "INNER_JOIN"],
                "scenario": "hr",
                "problem": "List all employees with their department name and the count of employees in their department.",
                "tables": ["employees", "departments"],
                "solution": "SELECT e.first_name, e.last_name, d.name as department, (SELECT COUNT(*) FROM employees e2 WHERE e2.department_id = e.department_id) as dept_employee_count FROM employees e INNER JOIN departments d ON e.department_id = d.id",
                "hints": [
                    "Use a scalar subquery in SELECT",
                    "The subquery counts employees in same department"
                ]
            },
            {
                "id": "l6_nested_subquery_001",
                "level": 6,
                "difficulty": "hard",
                "skills": ["SELECT", "SUBQUERY_WHERE", "GROUP_BY", "HAVING"],
                "scenario": "ecommerce",
                "problem": "Find customers who have spent more than the average customer spending (total order amounts).",
                "tables": ["customers", "orders"],
                "solution": "SELECT c.first_name, c.last_name, SUM(o.total_amount) as total_spent FROM customers c INNER JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.first_name, c.last_name HAVING SUM(o.total_amount) > (SELECT AVG(customer_total) FROM (SELECT customer_id, SUM(total_amount) as customer_total FROM orders GROUP BY customer_id))",
                "hints": [
                    "First calculate total per customer",
                    "Then average those totals",
                    "Compare each customer's total to that average"
                ]
            },
        ]

        # Level 7: Conditional Logic
        level7_templates = [
            {
                "id": "l7_case_simple_001",
                "level": 7,
                "difficulty": "easy",
                "skills": ["SELECT", "CASE"],
                "scenario": "ecommerce",
                "problem": "Categorize products by price: 'Budget' (< 50), 'Standard' (50-200), 'Premium' (> 200). Show product name and category.",
                "tables": ["products"],
                "solution": "SELECT name, price, CASE WHEN price < 50 THEN 'Budget' WHEN price <= 200 THEN 'Standard' ELSE 'Premium' END as price_category FROM products",
                "hints": [
                    "CASE WHEN ... THEN ... ELSE ... END",
                    "Conditions are evaluated in order"
                ]
            },
            {
                "id": "l7_case_count_001",
                "level": 7,
                "difficulty": "medium",
                "skills": ["SELECT", "CASE", "SUM", "GROUP_BY"],
                "scenario": "ecommerce",
                "problem": "For each category, count how many products are in each price tier (Budget/Standard/Premium).",
                "tables": ["products", "categories"],
                "solution": "SELECT c.name as category, SUM(CASE WHEN p.price < 50 THEN 1 ELSE 0 END) as budget_count, SUM(CASE WHEN p.price >= 50 AND p.price <= 200 THEN 1 ELSE 0 END) as standard_count, SUM(CASE WHEN p.price > 200 THEN 1 ELSE 0 END) as premium_count FROM products p INNER JOIN categories c ON p.category_id = c.id GROUP BY c.id, c.name",
                "hints": [
                    "Use CASE inside SUM to count conditionally",
                    "CASE returns 1 or 0 for counting"
                ]
            },
            {
                "id": "l7_coalesce_001",
                "level": 7,
                "difficulty": "easy",
                "skills": ["SELECT", "COALESCE"],
                "scenario": "hr",
                "problem": "List all employees with their commission percentage. If commission is NULL, display 0.",
                "tables": ["employees"],
                "solution": "SELECT first_name, last_name, salary, COALESCE(commission_pct, 0) as commission_pct FROM employees",
                "hints": [
                    "COALESCE returns the first non-NULL value",
                    "COALESCE(column, default_value)"
                ]
            },
            {
                "id": "l7_nullif_001",
                "level": 7,
                "difficulty": "medium",
                "skills": ["SELECT", "NULLIF"],
                "scenario": "ecommerce",
                "problem": "Calculate the discount rate (discount_percent / 100), but avoid division by zero. If discount is 0, treat it as NULL.",
                "tables": ["order_items"],
                "solution": "SELECT id, order_id, quantity, unit_price, discount_percent, unit_price / NULLIF((100 - discount_percent) / 100.0, 0) as original_price FROM order_items",
                "hints": [
                    "NULLIF(a, b) returns NULL if a = b",
                    "Use it to convert 0 to NULL before division"
                ]
            },
            {
                "id": "l7_case_groupby_001",
                "level": 7,
                "difficulty": "hard",
                "skills": ["SELECT", "CASE", "GROUP_BY", "COUNT"],
                "scenario": "ecommerce",
                "problem": "Create a report showing orders by status grouped into three categories: 'Active' (pending, processing), 'Completed' (delivered, shipped), 'Cancelled' (cancelled). Show the category and count.",
                "tables": ["orders"],
                "solution": "SELECT CASE WHEN status IN ('pending', 'processing') THEN 'Active' WHEN status IN ('delivered', 'shipped') THEN 'Completed' ELSE 'Cancelled' END as status_category, COUNT(*) as order_count FROM orders GROUP BY status_category ORDER BY order_count DESC",
                "hints": [
                    "Use CASE to create status categories",
                    "Group by the CASE expression"
                ]
            },
            {
                "id": "l7_case_orderby_001",
                "level": 7,
                "difficulty": "hard",
                "skills": ["SELECT", "CASE", "ORDER_BY"],
                "scenario": "hr",
                "problem": "List employees ordered by priority: first managers (job_title contains 'Manager'), then engineers (job_title contains 'Engineer'), then others. Within each group, order by salary descending.",
                "tables": ["employees"],
                "solution": "SELECT first_name, last_name, job_title, salary FROM employees ORDER BY CASE WHEN job_title LIKE '%Manager%' THEN 1 WHEN job_title LIKE '%Engineer%' THEN 2 ELSE 3 END, salary DESC",
                "hints": [
                    "CASE can be used in ORDER BY",
                    "Return different numbers for different priorities"
                ]
            },
            {
                "id": "l7_iif_001",
                "level": 7,
                "difficulty": "medium",
                "skills": ["SELECT", "IIF"],
                "scenario": "ecommerce",
                "problem": "Show products with an 'In Stock' or 'Out of Stock' indicator based on inventory quantity > 0.",
                "tables": ["products", "inventory"],
                "solution": "SELECT p.name, i.quantity, IIF(i.quantity > 0, 'In Stock', 'Out of Stock') as stock_status FROM products p INNER JOIN inventory i ON p.id = i.product_id",
                "hints": [
                    "IIF(condition, true_value, false_value)",
                    "It's a shorthand for simple CASE"
                ]
            },
        ]

        # Level 8: Window Functions
        level8_templates = [
            {
                "id": "l8_row_number_001",
                "level": 8,
                "difficulty": "easy",
                "skills": ["SELECT", "ROW_NUMBER"],
                "scenario": "ecommerce",
                "problem": "List all products with a row number, ordered by price descending.",
                "tables": ["products"],
                "solution": "SELECT ROW_NUMBER() OVER (ORDER BY price DESC) as row_num, name, price FROM products",
                "hints": [
                    "ROW_NUMBER() assigns unique sequential numbers",
                    "OVER() defines the window (ordering/partitioning)"
                ]
            },
            {
                "id": "l8_rank_001",
                "level": 8,
                "difficulty": "easy",
                "skills": ["SELECT", "RANK"],
                "scenario": "ecommerce",
                "problem": "Rank products by price descending. Products with the same price should have the same rank.",
                "tables": ["products"],
                "solution": "SELECT RANK() OVER (ORDER BY price DESC) as price_rank, name, price FROM products",
                "hints": [
                    "RANK() gives same rank for ties",
                    "It skips numbers after ties (1,1,3 not 1,1,2)"
                ]
            },
            {
                "id": "l8_dense_rank_001",
                "level": 8,
                "difficulty": "medium",
                "skills": ["SELECT", "DENSE_RANK"],
                "scenario": "ecommerce",
                "problem": "Assign a dense rank to products by price descending. (No gaps in ranking for ties.)",
                "tables": ["products"],
                "solution": "SELECT DENSE_RANK() OVER (ORDER BY price DESC) as price_rank, name, price FROM products",
                "hints": [
                    "DENSE_RANK() gives same rank for ties",
                    "No gaps (1,1,2 instead of 1,1,3)"
                ]
            },
            {
                "id": "l8_partition_001",
                "level": 8,
                "difficulty": "medium",
                "skills": ["SELECT", "ROW_NUMBER", "INNER_JOIN"],
                "scenario": "ecommerce",
                "problem": "For each category, number the products by price (1 = most expensive in that category).",
                "tables": ["products", "categories"],
                "solution": "SELECT c.name as category, p.name as product, p.price, ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY p.price DESC) as rank_in_category FROM products p INNER JOIN categories c ON p.category_id = c.id",
                "hints": [
                    "PARTITION BY restarts numbering for each group",
                    "Like doing ROW_NUMBER per category"
                ]
            },
            {
                "id": "l8_lag_001",
                "level": 8,
                "difficulty": "medium",
                "skills": ["SELECT", "LAG", "ORDER_BY"],
                "scenario": "finance",
                "problem": "For each transaction, show the previous transaction amount for the same account.",
                "tables": ["transactions"],
                "solution": "SELECT id, account_id, transaction_date, amount, LAG(amount) OVER (PARTITION BY account_id ORDER BY transaction_date) as prev_amount FROM transactions",
                "hints": [
                    "LAG() gets value from previous row",
                    "Partition by account to get previous within same account"
                ]
            },
            {
                "id": "l8_lead_001",
                "level": 8,
                "difficulty": "medium",
                "skills": ["SELECT", "LEAD"],
                "scenario": "finance",
                "problem": "For each transaction, show the next transaction amount for the same account.",
                "tables": ["transactions"],
                "solution": "SELECT id, account_id, transaction_date, amount, LEAD(amount) OVER (PARTITION BY account_id ORDER BY transaction_date) as next_amount FROM transactions",
                "hints": [
                    "LEAD() gets value from next row",
                    "Returns NULL for last row in partition"
                ]
            },
            {
                "id": "l8_running_sum_001",
                "level": 8,
                "difficulty": "hard",
                "skills": ["SELECT", "WINDOW_AGGREGATE"],
                "scenario": "finance",
                "problem": "Calculate a running total of transaction amounts for each account, ordered by date.",
                "tables": ["transactions"],
                "solution": "SELECT id, account_id, transaction_date, amount, SUM(amount) OVER (PARTITION BY account_id ORDER BY transaction_date ROWS UNBOUNDED PRECEDING) as running_total FROM transactions",
                "hints": [
                    "SUM() OVER() with ORDER BY creates running total",
                    "ROWS UNBOUNDED PRECEDING means all rows up to current"
                ]
            },
            {
                "id": "l8_ntile_001",
                "level": 8,
                "difficulty": "hard",
                "skills": ["SELECT", "NTILE"],
                "scenario": "ecommerce",
                "problem": "Divide products into 4 price quartiles (1 = cheapest 25%, 4 = most expensive 25%).",
                "tables": ["products"],
                "solution": "SELECT name, price, NTILE(4) OVER (ORDER BY price) as price_quartile FROM products",
                "hints": [
                    "NTILE(n) divides rows into n equal groups",
                    "Groups are numbered 1 to n"
                ]
            },
            {
                "id": "l8_window_avg_001",
                "level": 8,
                "difficulty": "hard",
                "skills": ["SELECT", "WINDOW_AGGREGATE", "INNER_JOIN"],
                "scenario": "ecommerce",
                "problem": "For each product, show its price and the average price in its category (using window function).",
                "tables": ["products", "categories"],
                "solution": "SELECT c.name as category, p.name as product, p.price, ROUND(AVG(p.price) OVER (PARTITION BY p.category_id), 2) as category_avg_price FROM products p INNER JOIN categories c ON p.category_id = c.id",
                "hints": [
                    "AVG() OVER (PARTITION BY ...) calculates average per partition",
                    "Every row gets the average of its group"
                ]
            },
        ]

        # Level 9: CTEs
        level9_templates = [
            {
                "id": "l9_cte_basic_001",
                "level": 9,
                "difficulty": "easy",
                "skills": ["SELECT", "CTE_BASIC"],
                "scenario": "ecommerce",
                "problem": "Using a CTE, find all customers with more than 5 orders.",
                "tables": ["customers", "orders"],
                "solution": "WITH customer_order_counts AS (SELECT customer_id, COUNT(*) as order_count FROM orders GROUP BY customer_id) SELECT c.first_name, c.last_name, coc.order_count FROM customers c INNER JOIN customer_order_counts coc ON c.id = coc.customer_id WHERE coc.order_count > 5",
                "hints": [
                    "WITH name AS (subquery) defines the CTE",
                    "Then use the CTE name like a table"
                ]
            },
            {
                "id": "l9_cte_multiple_001",
                "level": 9,
                "difficulty": "medium",
                "skills": ["SELECT", "CTE_MULTIPLE", "INNER_JOIN"],
                "scenario": "ecommerce",
                "problem": "Using two CTEs: First calculate total revenue per category, then calculate average product price per category. Join them to show category name, total revenue, and average price.",
                "tables": ["categories", "products", "order_items"],
                "solution": "WITH category_revenue AS (SELECT p.category_id, SUM(oi.quantity * oi.unit_price) as total_revenue FROM products p INNER JOIN order_items oi ON p.id = oi.product_id GROUP BY p.category_id), category_avg_price AS (SELECT category_id, AVG(price) as avg_price FROM products GROUP BY category_id) SELECT c.name, ROUND(cr.total_revenue, 2) as revenue, ROUND(cap.avg_price, 2) as avg_price FROM categories c INNER JOIN category_revenue cr ON c.id = cr.category_id INNER JOIN category_avg_price cap ON c.id = cap.category_id",
                "hints": [
                    "Define multiple CTEs separated by commas",
                    "WITH cte1 AS (...), cte2 AS (...) SELECT ..."
                ]
            },
            {
                "id": "l9_cte_chained_001",
                "level": 9,
                "difficulty": "hard",
                "skills": ["SELECT", "CTE_CHAINED"],
                "scenario": "hr",
                "problem": "Using chained CTEs: 1) Get employee salaries, 2) Calculate department averages, 3) Find employees earning above their department average.",
                "tables": ["employees", "departments"],
                "solution": "WITH emp_salaries AS (SELECT id, first_name, last_name, department_id, salary FROM employees WHERE is_active = 1), dept_avg AS (SELECT department_id, AVG(salary) as avg_salary FROM emp_salaries GROUP BY department_id), above_avg AS (SELECT e.*, d.avg_salary FROM emp_salaries e INNER JOIN dept_avg d ON e.department_id = d.department_id WHERE e.salary > d.avg_salary) SELECT aa.first_name, aa.last_name, aa.salary, ROUND(aa.avg_salary, 2) as dept_avg FROM above_avg aa",
                "hints": [
                    "Each CTE can reference previous CTEs",
                    "Build up the logic step by step"
                ]
            },
            {
                "id": "l9_cte_window_001",
                "level": 9,
                "difficulty": "hard",
                "skills": ["SELECT", "CTE_BASIC", "ROW_NUMBER"],
                "scenario": "ecommerce",
                "problem": "Using a CTE with a window function, find the top 3 products by price in each category.",
                "tables": ["products", "categories"],
                "solution": "WITH ranked_products AS (SELECT p.*, c.name as category_name, ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY p.price DESC) as rn FROM products p INNER JOIN categories c ON p.category_id = c.id) SELECT category_name, name as product_name, price FROM ranked_products WHERE rn <= 3",
                "hints": [
                    "CTE can contain window functions",
                    "Filter the CTE results in outer query"
                ]
            },
        ]

        # Level 10: Advanced CTEs
        level10_templates = [
            {
                "id": "l10_recursive_001",
                "level": 10,
                "difficulty": "medium",
                "skills": ["SELECT", "CTE_RECURSIVE"],
                "scenario": "hr",
                "problem": "Using a recursive CTE, find the management chain for employee with id=50 (show all managers up the chain).",
                "tables": ["employees"],
                "solution": "WITH RECURSIVE management_chain AS (SELECT id, first_name, last_name, manager_id, 1 as level FROM employees WHERE id = 50 UNION ALL SELECT e.id, e.first_name, e.last_name, e.manager_id, mc.level + 1 FROM employees e INNER JOIN management_chain mc ON e.id = mc.manager_id) SELECT * FROM management_chain",
                "hints": [
                    "WITH RECURSIVE enables recursive CTEs",
                    "Has base case (anchor) and recursive case",
                    "UNION ALL combines results"
                ]
            },
            {
                "id": "l10_recursive_hierarchy_001",
                "level": 10,
                "difficulty": "hard",
                "skills": ["SELECT", "CTE_RECURSIVE"],
                "scenario": "ecommerce",
                "problem": "Using a recursive CTE, show the category hierarchy. For each category, show its full path (parent > child > grandchild).",
                "tables": ["categories"],
                "solution": "WITH RECURSIVE category_path AS (SELECT id, name, parent_category_id, name as full_path, 1 as depth FROM categories WHERE parent_category_id IS NULL UNION ALL SELECT c.id, c.name, c.parent_category_id, cp.full_path || ' > ' || c.name, cp.depth + 1 FROM categories c INNER JOIN category_path cp ON c.parent_category_id = cp.id) SELECT id, name, full_path, depth FROM category_path ORDER BY full_path",
                "hints": [
                    "Start with root categories (no parent)",
                    "Recursively join children",
                    "Build path string with concatenation"
                ]
            },
            {
                "id": "l10_complex_cte_001",
                "level": 10,
                "difficulty": "hard",
                "skills": ["SELECT", "CTE_COMPLEX", "WINDOW_AGGREGATE"],
                "scenario": "finance",
                "problem": "Create a complex analysis: 1) Calculate monthly transaction totals per account, 2) Add running balance, 3) Flag months where balance dropped below zero.",
                "tables": ["transactions", "accounts"],
                "solution": "WITH monthly_totals AS (SELECT account_id, strftime('%Y-%m', transaction_date) as month, SUM(amount) as monthly_total FROM transactions GROUP BY account_id, strftime('%Y-%m', transaction_date)), with_running AS (SELECT *, SUM(monthly_total) OVER (PARTITION BY account_id ORDER BY month) as running_balance FROM monthly_totals), flagged AS (SELECT *, CASE WHEN running_balance < 0 THEN 'ALERT' ELSE 'OK' END as status FROM with_running) SELECT * FROM flagged ORDER BY account_id, month",
                "hints": [
                    "Chain multiple CTEs for complex analysis",
                    "strftime extracts date parts in SQLite",
                    "Use window function for running total"
                ]
            },
        ]

        # Level 11: Optimization
        level11_templates = [
            {
                "id": "l11_explain_001",
                "level": 11,
                "difficulty": "easy",
                "skills": ["EXPLAIN"],
                "scenario": "ecommerce",
                "problem": "Use EXPLAIN QUERY PLAN to analyze a query that finds all orders for a specific customer.",
                "tables": ["orders"],
                "solution": "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 1",
                "hints": [
                    "EXPLAIN QUERY PLAN shows how SQLite will execute",
                    "Look for SCAN vs SEARCH (index usage)"
                ]
            },
            {
                "id": "l11_index_analysis_001",
                "level": 11,
                "difficulty": "medium",
                "skills": ["EXPLAIN", "INDEX_USAGE"],
                "scenario": "ecommerce",
                "problem": "Compare two queries with EXPLAIN: one filtering by indexed column (id) and one by non-indexed column (status). What's the difference?",
                "tables": ["orders"],
                "solution": "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE id = 1; EXPLAIN QUERY PLAN SELECT * FROM orders WHERE status = 'pending'",
                "hints": [
                    "Run EXPLAIN on both queries",
                    "SEARCH indicates index use, SCAN means full table scan",
                    "id is typically indexed (primary key)"
                ]
            },
        ]

        # Level 12: Data Manipulation
        level12_templates = [
            {
                "id": "l12_insert_001",
                "level": 12,
                "difficulty": "easy",
                "skills": ["INSERT"],
                "scenario": "ecommerce",
                "problem": "Insert a new customer with first_name 'John', last_name 'Doe', email 'john.doe@example.com', and join_date of today.",
                "tables": ["customers"],
                "solution": "INSERT INTO customers (first_name, last_name, email, join_date) VALUES ('John', 'Doe', 'john.doe@example.com', DATE('now'))",
                "hints": [
                    "INSERT INTO table (columns) VALUES (values)",
                    "DATE('now') gives today's date in SQLite"
                ]
            },
            {
                "id": "l12_update_001",
                "level": 12,
                "difficulty": "medium",
                "skills": ["UPDATE", "WHERE"],
                "scenario": "ecommerce",
                "problem": "Update all products in category_id 1 to increase their price by 10%.",
                "tables": ["products"],
                "solution": "UPDATE products SET price = price * 1.10 WHERE category_id = 1",
                "hints": [
                    "UPDATE table SET column = value WHERE condition",
                    "You can use expressions in SET"
                ]
            },
            {
                "id": "l12_delete_001",
                "level": 12,
                "difficulty": "medium",
                "skills": ["DELETE", "WHERE"],
                "scenario": "ecommerce",
                "problem": "Delete all reviews with a rating of 1 and no helpful_votes.",
                "tables": ["reviews"],
                "solution": "DELETE FROM reviews WHERE rating = 1 AND helpful_votes = 0",
                "hints": [
                    "DELETE FROM table WHERE condition",
                    "Be careful - always use WHERE with DELETE"
                ]
            },
            {
                "id": "l12_upsert_001",
                "level": 12,
                "difficulty": "hard",
                "skills": ["INSERT_OR_REPLACE"],
                "scenario": "ecommerce",
                "problem": "Insert a product with id=1, or if it exists, update its name and price. Name='Updated Product', price=99.99, category_id=1.",
                "tables": ["products"],
                "solution": "INSERT OR REPLACE INTO products (id, name, price, category_id) VALUES (1, 'Updated Product', 99.99, 1)",
                "hints": [
                    "INSERT OR REPLACE works like UPSERT",
                    "If the key exists, it replaces the row"
                ]
            },
        ]

        # Level 13: Advanced Topics
        level13_templates = [
            {
                "id": "l13_view_001",
                "level": 13,
                "difficulty": "medium",
                "skills": ["CREATE_VIEW"],
                "scenario": "ecommerce",
                "problem": "Create a view called 'customer_order_summary' that shows customer name, total orders, and total amount spent.",
                "tables": ["customers", "orders"],
                "solution": "CREATE VIEW customer_order_summary AS SELECT c.id, c.first_name, c.last_name, COUNT(o.id) as total_orders, COALESCE(SUM(o.total_amount), 0) as total_spent FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.first_name, c.last_name",
                "hints": [
                    "CREATE VIEW name AS SELECT ...",
                    "Views act like virtual tables"
                ]
            },
            {
                "id": "l13_datetime_001",
                "level": 13,
                "difficulty": "hard",
                "skills": ["DATETIME_FUNCTIONS"],
                "scenario": "ecommerce",
                "problem": "Find all orders placed in the last 30 days, grouped by day. Show date and order count.",
                "tables": ["orders"],
                "solution": "SELECT DATE(order_date) as order_day, COUNT(*) as order_count FROM orders WHERE order_date >= DATE('now', '-30 days') GROUP BY DATE(order_date) ORDER BY order_day",
                "hints": [
                    "DATE('now', '-30 days') is 30 days ago",
                    "DATE() extracts just the date part"
                ]
            },
            {
                "id": "l13_temp_table_001",
                "level": 13,
                "difficulty": "hard",
                "skills": ["TEMP_TABLE"],
                "scenario": "hr",
                "problem": "Create a temporary table with top earners (salary > 100000), then query it to find their departments.",
                "tables": ["employees", "departments"],
                "solution": "CREATE TEMPORARY TABLE top_earners AS SELECT * FROM employees WHERE salary > 100000; SELECT t.first_name, t.last_name, t.salary, d.name as department FROM top_earners t INNER JOIN departments d ON t.department_id = d.id",
                "hints": [
                    "CREATE TEMPORARY TABLE creates session-scoped table",
                    "Temp tables are deleted when connection closes"
                ]
            },
        ]

        # Combine all templates
        all_templates = (level1_templates + level2_templates + level3_templates +
                        level4_templates + level5_templates + level6_templates +
                        level7_templates + level8_templates + level9_templates +
                        level10_templates + level11_templates + level12_templates +
                        level13_templates)

        for template in all_templates:
            templates[template['id']] = template

        return templates

    def get_template(self, template_id: str) -> Optional[Dict]:
        """Get a specific template by ID"""
        return self.templates.get(template_id)

    def get_templates_by_level(self, level: int) -> List[Dict]:
        """Get all templates for a specific level"""
        return [t for t in self.templates.values() if t['level'] == level]

    def get_templates_by_difficulty(self, difficulty: str) -> List[Dict]:
        """Get all templates for a specific difficulty"""
        return [t for t in self.templates.values() if t['difficulty'] == difficulty]

    def get_templates_by_scenario(self, scenario: str) -> List[Dict]:
        """Get all templates for a specific scenario"""
        return [t for t in self.templates.values() if t.get('scenario') == scenario]

    def get_templates_filtered(self, levels: List[int] = None,
                               difficulties: List[str] = None,
                               scenarios: List[str] = None) -> List[Dict]:
        """Get templates matching multiple filters"""
        templates = list(self.templates.values())

        if levels:
            templates = [t for t in templates if t['level'] in levels]
        if difficulties:
            templates = [t for t in templates if t['difficulty'] in difficulties]
        if scenarios:
            templates = [t for t in templates if t.get('scenario') in scenarios]

        return templates

    def get_random_template(self, level: int = None, difficulty: str = None,
                           scenario: str = None) -> Optional[Dict]:
        """Get a random template matching the criteria"""
        templates = self.get_templates_filtered(
            levels=[level] if level else None,
            difficulties=[difficulty] if difficulty else None,
            scenarios=[scenario] if scenario else None
        )
        return random.choice(templates) if templates else None

    def get_all_levels(self) -> List[int]:
        """Get all available levels"""
        return sorted(set(t['level'] for t in self.templates.values()))

    def get_all_difficulties(self) -> List[str]:
        """Get all available difficulties"""
        return list(set(t['difficulty'] for t in self.templates.values()))

    def get_all_scenarios(self) -> List[str]:
        """Get all available scenarios"""
        return list(set(t.get('scenario') for t in self.templates.values() if t.get('scenario')))

    def get_template_count(self) -> int:
        """Get total number of templates"""
        return len(self.templates)

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the template collection"""
        templates = list(self.templates.values())
        return {
            'total': len(templates),
            'by_level': {level: len([t for t in templates if t['level'] == level])
                        for level in range(1, 14)},
            'by_difficulty': {diff: len([t for t in templates if t['difficulty'] == diff])
                             for diff in ['easy', 'medium', 'hard']},
            'by_scenario': {scenario: len([t for t in templates if t.get('scenario') == scenario])
                           for scenario in self.get_all_scenarios()}
        }
