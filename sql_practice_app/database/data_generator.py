"""
Data Generator for SQL Practice Generator
Generates realistic data for each scenario
"""
import random
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any
from faker import Faker
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import EXERCISE_DB_PATH
from database.schema_generator import SchemaGenerator


class DataGenerator:
    """Generates realistic data for practice scenarios"""

    def __init__(self, db_path: str = EXERCISE_DB_PATH):
        self.db_path = db_path
        self.fake = Faker()
        Faker.seed(42)
        random.seed(42)

    def _get_connection(self):
        """Get database connection"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _execute_script(self, conn, script: str):
        """Execute a SQL script"""
        conn.executescript(script)

    def _insert_many(self, conn, table: str, columns: List[str], data: List[tuple]):
        """Insert multiple rows into a table"""
        placeholders = ', '.join(['?' for _ in columns])
        columns_str = ', '.join(columns)
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        conn.executemany(query, data)

    def generate_all_scenarios(self):
        """Generate data for all scenarios"""
        conn = self._get_connection()
        try:
            for scenario in ['ecommerce', 'hr', 'finance', 'social_media', 'healthcare', 'education']:
                self._execute_script(conn, SchemaGenerator.get_schema(scenario))
                self._generate_scenario_data(conn, scenario)
            conn.commit()
        finally:
            conn.close()

    def _generate_scenario_data(self, conn, scenario: str):
        """Generate data for a specific scenario"""
        generators = {
            'ecommerce': self._generate_ecommerce_data,
            'hr': self._generate_hr_data,
            'finance': self._generate_finance_data,
            'social_media': self._generate_social_media_data,
            'healthcare': self._generate_healthcare_data,
            'education': self._generate_education_data
        }
        if scenario in generators:
            generators[scenario](conn)

    def _generate_ecommerce_data(self, conn):
        """Generate e-commerce data"""
        # Categories
        categories = [
            ('Electronics', 'Electronic devices and accessories', None),
            ('Clothing', 'Apparel and fashion items', None),
            ('Books', 'Physical and digital books', None),
            ('Home & Garden', 'Home improvement and garden supplies', None),
            ('Sports', 'Sports equipment and apparel', None),
            ('Toys', 'Toys and games', None),
            ('Beauty', 'Beauty and personal care', None),
            ('Food & Grocery', 'Food items and groceries', None),
            ('Smartphones', 'Mobile phones and accessories', 1),
            ('Laptops', 'Laptop computers', 1),
            ('Cameras', 'Digital cameras', 1),
            ("Men's Clothing", 'Clothing for men', 2),
            ("Women's Clothing", 'Clothing for women', 2),
            ('Fiction', 'Fiction books', 3),
            ('Non-Fiction', 'Non-fiction books', 3),
        ]
        self._insert_many(conn, 'categories',
                         ['name', 'description', 'parent_category_id'], categories)

        # Customers (100 customers)
        customers = []
        for i in range(100):
            join_date = self.fake.date_between(start_date='-3y', end_date='today')
            customers.append((
                self.fake.first_name(),
                self.fake.last_name(),
                f"customer{i+1}@{self.fake.free_email_domain()}",
                self.fake.phone_number()[:15],
                self.fake.street_address(),
                self.fake.city(),
                self.fake.state_abbr(),
                'USA',
                self.fake.zipcode(),
                str(join_date),
                random.choice([1, 1, 1, 0]),
                random.randint(0, 5000)
            ))
        self._insert_many(conn, 'customers',
                         ['first_name', 'last_name', 'email', 'phone', 'address',
                          'city', 'state', 'country', 'zip_code', 'join_date',
                          'is_active', 'loyalty_points'], customers)

        # Products (150 products)
        product_names = {
            9: ['iPhone 15', 'Samsung Galaxy S24', 'Google Pixel 8', 'OnePlus 12', 'Xiaomi 14'],
            10: ['MacBook Pro', 'Dell XPS 15', 'HP Spectre', 'Lenovo ThinkPad', 'ASUS ZenBook'],
            11: ['Canon EOS R5', 'Sony A7 IV', 'Nikon Z8', 'Fujifilm X-T5', 'Panasonic Lumix'],
            12: ['Dress Shirt', 'Jeans', 'Polo Shirt', 'Chinos', 'Blazer', 'T-Shirt', 'Shorts'],
            13: ['Summer Dress', 'Blouse', 'Skirt', 'Cardigan', 'Jumpsuit', 'Leggings'],
            14: ['The Great Gatsby', '1984', 'To Kill a Mockingbird', 'Pride and Prejudice'],
            15: ['Atomic Habits', 'Thinking Fast and Slow', 'Sapiens', 'The Power of Habit'],
            4: ['Garden Hose', 'Plant Pots', 'LED Lights', 'Throw Pillows', 'Wall Art'],
            5: ['Basketball', 'Tennis Racket', 'Yoga Mat', 'Dumbbells', 'Running Shoes'],
            6: ['LEGO Set', 'Board Game', 'Puzzle', 'Remote Control Car', 'Doll'],
            7: ['Moisturizer', 'Lipstick', 'Perfume', 'Face Mask', 'Shampoo'],
            8: ['Organic Coffee', 'Dark Chocolate', 'Olive Oil', 'Protein Bars', 'Green Tea']
        }

        products = []
        product_id = 0
        for cat_id, names in product_names.items():
            for name in names:
                product_id += 1
                price = round(random.uniform(10, 2000), 2)
                products.append((
                    name,
                    self.fake.text(max_nb_chars=200),
                    cat_id,
                    price,
                    round(price * random.uniform(0.3, 0.7), 2),
                    f"SKU-{product_id:05d}",
                    round(random.uniform(0.1, 20), 2),
                    random.choice([1, 1, 1, 1, 0])
                ))
        self._insert_many(conn, 'products',
                         ['name', 'description', 'category_id', 'price', 'cost',
                          'sku', 'weight', 'is_active'], products)

        # Inventory
        inventory = []
        for i in range(1, len(products) + 1):
            inventory.append((
                i,
                random.randint(0, 500),
                f"Warehouse-{random.choice(['A', 'B', 'C'])}-{random.randint(1, 50)}",
                str(self.fake.date_between(start_date='-1y', end_date='today')),
                random.randint(5, 50)
            ))
        self._insert_many(conn, 'inventory',
                         ['product_id', 'quantity', 'warehouse_location',
                          'last_restocked', 'reorder_level'], inventory)

        # Orders (300 orders)
        orders = []
        for i in range(300):
            customer_id = random.randint(1, 100)
            order_date = self.fake.date_time_between(start_date='-2y', end_date='now')
            status = random.choices(
                ['pending', 'processing', 'shipped', 'delivered', 'cancelled'],
                weights=[10, 15, 20, 50, 5]
            )[0]
            orders.append((
                customer_id,
                str(order_date),
                status,
                self.fake.street_address(),
                self.fake.city(),
                self.fake.state_abbr(),
                self.fake.zipcode(),
                round(random.uniform(0, 25), 2),
                round(random.uniform(0, 100), 2),
                0,  # Will update after order_items
                random.choice(['credit_card', 'debit_card', 'paypal', 'bank_transfer']),
                self.fake.text(max_nb_chars=100) if random.random() > 0.7 else None
            ))
        self._insert_many(conn, 'orders',
                         ['customer_id', 'order_date', 'status', 'shipping_address',
                          'shipping_city', 'shipping_state', 'shipping_zip',
                          'shipping_cost', 'tax_amount', 'total_amount',
                          'payment_method', 'notes'], orders)

        # Order items (1-5 items per order)
        order_items = []
        for order_id in range(1, 301):
            num_items = random.randint(1, 5)
            product_ids = random.sample(range(1, len(products) + 1), num_items)
            total = 0
            for product_id in product_ids:
                quantity = random.randint(1, 5)
                price = products[product_id - 1][3]
                discount = random.choice([0, 0, 0, 5, 10, 15, 20])
                total += quantity * price * (1 - discount / 100)
                order_items.append((order_id, product_id, quantity, price, discount))
            # Update order total
            conn.execute(
                "UPDATE orders SET total_amount = ? WHERE id = ?",
                (round(total, 2), order_id)
            )
        self._insert_many(conn, 'order_items',
                         ['order_id', 'product_id', 'quantity', 'unit_price',
                          'discount_percent'], order_items)

        # Reviews (200 reviews)
        reviews = []
        for i in range(200):
            product_id = random.randint(1, len(products))
            customer_id = random.randint(1, 100)
            rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 15, 30, 40])[0]
            reviews.append((
                product_id,
                customer_id,
                rating,
                self.fake.sentence(nb_words=6),
                self.fake.text(max_nb_chars=300),
                str(self.fake.date_time_between(start_date='-1y', end_date='now')),
                random.randint(0, 50),
                random.choice([0, 1])
            ))
        self._insert_many(conn, 'reviews',
                         ['product_id', 'customer_id', 'rating', 'title', 'comment',
                          'review_date', 'helpful_votes', 'verified_purchase'], reviews)

        # Coupons
        coupons = [
            ('SAVE10', 'percentage', 10, 0, 1000, 0, '2024-01-01', '2025-12-31', 1),
            ('SAVE20', 'percentage', 20, 50, 500, 0, '2024-01-01', '2025-12-31', 1),
            ('FLAT25', 'fixed', 25, 100, 200, 0, '2024-06-01', '2025-06-01', 1),
            ('WELCOME', 'percentage', 15, 0, None, 0, '2024-01-01', '2025-12-31', 1),
            ('EXPIRED', 'percentage', 30, 0, 100, 100, '2023-01-01', '2023-12-31', 0),
        ]
        self._insert_many(conn, 'coupons',
                         ['code', 'discount_type', 'discount_value', 'min_order_amount',
                          'max_uses', 'uses_count', 'start_date', 'end_date', 'is_active'],
                         coupons)

    def _generate_hr_data(self, conn):
        """Generate HR data"""
        # Departments
        departments = [
            ('Engineering', 'Software and hardware engineering', 5000000, 'Building A'),
            ('Sales', 'Sales and business development', 3000000, 'Building B'),
            ('Marketing', 'Marketing and communications', 2000000, 'Building B'),
            ('Human Resources', 'HR and talent management', 1500000, 'Building C'),
            ('Finance', 'Financial operations', 2500000, 'Building C'),
            ('Operations', 'Business operations', 3000000, 'Building A'),
            ('Customer Support', 'Customer service', 1800000, 'Building D'),
            ('Research', 'R&D department', 4000000, 'Building A'),
            ('Legal', 'Legal affairs', 1200000, 'Building C'),
            ('IT', 'Information technology', 2800000, 'Building A'),
        ]
        self._insert_many(conn, 'departments',
                         ['name', 'description', 'budget', 'location'], departments)

        # Employees (150 employees)
        job_titles = {
            1: ['Software Engineer', 'Senior Engineer', 'Staff Engineer', 'Engineering Manager', 'Tech Lead'],
            2: ['Sales Representative', 'Account Executive', 'Sales Manager', 'VP Sales'],
            3: ['Marketing Specialist', 'Content Writer', 'Marketing Manager', 'Brand Manager'],
            4: ['HR Specialist', 'Recruiter', 'HR Manager', 'HR Director'],
            5: ['Accountant', 'Financial Analyst', 'Finance Manager', 'CFO'],
            6: ['Operations Analyst', 'Operations Manager', 'COO'],
            7: ['Support Agent', 'Support Lead', 'Support Manager'],
            8: ['Research Scientist', 'Research Lead', 'Director of Research'],
            9: ['Legal Counsel', 'Paralegal', 'General Counsel'],
            10: ['IT Specialist', 'System Administrator', 'IT Manager', 'CTO'],
        }

        salary_ranges = {
            'Engineer': (80000, 180000),
            'Manager': (100000, 200000),
            'Director': (150000, 300000),
            'VP': (200000, 400000),
            'C': (250000, 500000),
            'default': (50000, 120000)
        }

        employees = []
        for i in range(150):
            dept_id = random.randint(1, 10)
            title = random.choice(job_titles[dept_id])
            hire_date = self.fake.date_between(start_date='-10y', end_date='today')

            # Determine salary based on title
            for key, range_vals in salary_ranges.items():
                if key in title:
                    salary = round(random.uniform(*range_vals), 2)
                    break
            else:
                salary = round(random.uniform(*salary_ranges['default']), 2)

            manager_id = random.randint(1, max(1, i)) if i > 0 else None

            employees.append((
                self.fake.first_name(),
                self.fake.last_name(),
                f"employee{i+1}@company.com",
                self.fake.phone_number()[:15],
                str(hire_date),
                title,
                dept_id,
                manager_id,
                salary,
                round(random.uniform(0, 0.15), 2) if 'Sales' in title else None,
                1 if random.random() > 0.05 else 0,
                str(self.fake.date_of_birth(minimum_age=22, maximum_age=65)),
                self.fake.street_address(),
                self.fake.city(),
                self.fake.state_abbr()
            ))
        self._insert_many(conn, 'employees',
                         ['first_name', 'last_name', 'email', 'phone', 'hire_date',
                          'job_title', 'department_id', 'manager_id', 'salary',
                          'commission_pct', 'is_active', 'birth_date', 'address',
                          'city', 'state'], employees)

        # Update department managers
        for dept_id in range(1, 11):
            manager_id = random.randint(1, 150)
            conn.execute(
                "UPDATE departments SET manager_id = ? WHERE id = ?",
                (manager_id, dept_id)
            )

        # Salary history
        salary_history = []
        for emp_id in range(1, 151):
            num_changes = random.randint(1, 5)
            current_salary = employees[emp_id - 1][8]
            for j in range(num_changes):
                effective_date = self.fake.date_between(start_date='-5y', end_date='today')
                salary = round(current_salary * random.uniform(0.7, 1.0), 2)
                current_salary = salary
                salary_history.append((
                    emp_id,
                    salary,
                    str(effective_date),
                    None,
                    random.choice(['Annual Review', 'Promotion', 'Market Adjustment', 'New Hire'])
                ))
        self._insert_many(conn, 'salary_history',
                         ['employee_id', 'salary', 'effective_date', 'end_date',
                          'change_reason'], salary_history)

        # Performance reviews
        reviews = []
        for emp_id in range(1, 151):
            num_reviews = random.randint(0, 4)
            for _ in range(num_reviews):
                reviewer_id = random.randint(1, 150)
                reviews.append((
                    emp_id,
                    reviewer_id,
                    str(self.fake.date_between(start_date='-3y', end_date='today')),
                    random.randint(1, 5),
                    random.randint(50, 100),
                    self.fake.text(max_nb_chars=100),
                    self.fake.text(max_nb_chars=100),
                    self.fake.text(max_nb_chars=200)
                ))
        self._insert_many(conn, 'performance_reviews',
                         ['employee_id', 'reviewer_id', 'review_date', 'rating',
                          'goals_met_pct', 'strengths', 'areas_for_improvement',
                          'comments'], reviews)

        # Projects
        projects = []
        for i in range(30):
            start_date = self.fake.date_between(start_date='-2y', end_date='today')
            end_date = start_date + timedelta(days=random.randint(30, 365))
            projects.append((
                f"Project {self.fake.word().title()} {self.fake.word().title()}",
                self.fake.text(max_nb_chars=200),
                random.randint(1, 10),
                str(start_date),
                str(end_date),
                round(random.uniform(50000, 2000000), 2),
                random.choice(['planning', 'in_progress', 'completed', 'on_hold']),
                random.choice(['low', 'medium', 'high', 'critical'])
            ))
        self._insert_many(conn, 'projects',
                         ['name', 'description', 'department_id', 'start_date',
                          'end_date', 'budget', 'status', 'priority'], projects)

        # Project assignments
        assignments = []
        for proj_id in range(1, 31):
            num_members = random.randint(3, 10)
            member_ids = random.sample(range(1, 151), num_members)
            for emp_id in member_ids:
                assignments.append((
                    proj_id,
                    emp_id,
                    random.choice(['Developer', 'Analyst', 'Designer', 'Lead', 'Manager']),
                    random.randint(10, 40),
                    str(self.fake.date_between(start_date='-1y', end_date='today')),
                    None
                ))
        self._insert_many(conn, 'project_assignments',
                         ['project_id', 'employee_id', 'role', 'hours_allocated',
                          'start_date', 'end_date'], assignments)

        # Training courses
        courses = [
            ('SQL Fundamentals', 'Introduction to SQL', 8, 'John Smith', 200, 0),
            ('Leadership Skills', 'Management training', 16, 'Jane Doe', 500, 0),
            ('Python Programming', 'Python basics', 24, 'Bob Wilson', 300, 0),
            ('Security Awareness', 'Cybersecurity training', 4, 'Security Team', 0, 1),
            ('Agile Methodology', 'Scrum and Agile', 12, 'Mike Brown', 400, 0),
            ('Communication Skills', 'Effective communication', 8, 'Lisa Chen', 250, 0),
            ('Data Analysis', 'Data analytics basics', 20, 'Sarah Johnson', 350, 0),
            ('Compliance Training', 'Company policies', 2, 'HR Team', 0, 1),
        ]
        self._insert_many(conn, 'training_courses',
                         ['name', 'description', 'duration_hours', 'instructor',
                          'cost', 'is_mandatory'], courses)

        # Training enrollments
        enrollments = []
        for _ in range(200):
            emp_id = random.randint(1, 150)
            course_id = random.randint(1, 8)
            enrollment_date = self.fake.date_between(start_date='-1y', end_date='today')
            status = random.choice(['enrolled', 'completed', 'in_progress', 'dropped'])
            enrollments.append((
                course_id,
                emp_id,
                str(enrollment_date),
                str(enrollment_date + timedelta(days=random.randint(7, 60))) if status == 'completed' else None,
                random.randint(60, 100) if status == 'completed' else None,
                status
            ))
        self._insert_many(conn, 'training_enrollments',
                         ['course_id', 'employee_id', 'enrollment_date',
                          'completion_date', 'score', 'status'], enrollments)

    def _generate_finance_data(self, conn):
        """Generate finance/banking data"""
        # Branches
        branches = []
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                  'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
        for i, city in enumerate(cities):
            branches.append((
                f"{city} Main Branch",
                self.fake.street_address(),
                city,
                self.fake.state_abbr(),
                self.fake.zipcode(),
                self.fake.phone_number()[:15],
                self.fake.name(),
                str(self.fake.date_between(start_date='-20y', end_date='-5y'))
            ))
        self._insert_many(conn, 'branches',
                         ['name', 'address', 'city', 'state', 'zip_code', 'phone',
                          'manager_name', 'opened_date'], branches)

        # Account types
        account_types = [
            ('Checking', 'Standard checking account', 0, 0.001, 5.00),
            ('Savings', 'Regular savings account', 100, 0.02, 0),
            ('Premium Checking', 'Premium checking with benefits', 5000, 0.005, 0),
            ('High-Yield Savings', 'High interest savings', 10000, 0.045, 0),
            ('Money Market', 'Money market account', 25000, 0.04, 0),
            ('Student Checking', 'No-fee student checking', 0, 0, 0),
            ('Business Checking', 'Business checking account', 500, 0.001, 15.00),
        ]
        self._insert_many(conn, 'account_types',
                         ['name', 'description', 'min_balance', 'interest_rate',
                          'monthly_fee'], account_types)

        # Customers (120 customers)
        customers = []
        for i in range(120):
            customers.append((
                self.fake.first_name(),
                self.fake.last_name(),
                f"customer{i+1}@{self.fake.free_email_domain()}",
                self.fake.phone_number()[:15],
                str(random.randint(1000, 9999)),
                str(self.fake.date_of_birth(minimum_age=18, maximum_age=80)),
                self.fake.street_address(),
                self.fake.city(),
                self.fake.state_abbr(),
                self.fake.zipcode(),
                random.randint(300, 850),
                1 if random.random() > 0.05 else 0
            ))
        self._insert_many(conn, 'customers',
                         ['first_name', 'last_name', 'email', 'phone', 'ssn_last_four',
                          'date_of_birth', 'address', 'city', 'state', 'zip_code',
                          'credit_score', 'is_active'], customers)

        # Accounts (200 accounts)
        accounts = []
        for i in range(200):
            customer_id = random.randint(1, 120)
            account_type_id = random.randint(1, 7)
            opened_date = self.fake.date_between(start_date='-10y', end_date='today')
            accounts.append((
                customer_id,
                account_type_id,
                f"ACC{100000000 + i}",
                round(random.uniform(0, 100000), 2),
                str(opened_date),
                None,
                random.randint(1, 10),
                'active'
            ))
        self._insert_many(conn, 'accounts',
                         ['customer_id', 'account_type_id', 'account_number',
                          'balance', 'opened_date', 'closed_date', 'branch_id',
                          'status'], accounts)

        # Transactions (1000 transactions)
        transactions = []
        transaction_types = ['deposit', 'withdrawal', 'transfer', 'payment', 'fee', 'interest']
        categories = ['groceries', 'utilities', 'entertainment', 'dining', 'shopping',
                     'transportation', 'healthcare', 'salary', 'refund', None]

        for _ in range(1000):
            account_id = random.randint(1, 200)
            trans_type = random.choice(transaction_types)
            amount = round(random.uniform(10, 5000), 2)
            if trans_type in ['withdrawal', 'payment', 'fee']:
                amount = -amount
            transactions.append((
                account_id,
                trans_type,
                amount,
                round(random.uniform(0, 50000), 2),
                self.fake.text(max_nb_chars=50),
                str(self.fake.date_time_between(start_date='-2y', end_date='now')),
                f"REF{random.randint(100000, 999999)}",
                random.choice(categories)
            ))
        self._insert_many(conn, 'transactions',
                         ['account_id', 'transaction_type', 'amount', 'balance_after',
                          'description', 'transaction_date', 'reference_number',
                          'category'], transactions)

        # Transfers
        transfers = []
        for _ in range(100):
            from_acc = random.randint(1, 200)
            to_acc = random.randint(1, 200)
            while to_acc == from_acc:
                to_acc = random.randint(1, 200)
            transfers.append((
                from_acc,
                to_acc,
                round(random.uniform(50, 2000), 2),
                str(self.fake.date_time_between(start_date='-1y', end_date='now')),
                'completed',
                self.fake.text(max_nb_chars=50) if random.random() > 0.7 else None
            ))
        self._insert_many(conn, 'transfers',
                         ['from_account_id', 'to_account_id', 'amount',
                          'transfer_date', 'status', 'notes'], transfers)

        # Loans
        loan_types = ['mortgage', 'auto', 'personal', 'student', 'business']
        loans = []
        for i in range(80):
            customer_id = random.randint(1, 120)
            loan_type = random.choice(loan_types)
            if loan_type == 'mortgage':
                principal = round(random.uniform(100000, 500000), 2)
                term = random.choice([180, 240, 360])
            elif loan_type == 'auto':
                principal = round(random.uniform(15000, 60000), 2)
                term = random.choice([36, 48, 60, 72])
            else:
                principal = round(random.uniform(5000, 50000), 2)
                term = random.choice([12, 24, 36, 48, 60])

            rate = round(random.uniform(0.03, 0.15), 4)
            monthly = round(principal * (rate/12) / (1 - (1 + rate/12)**(-term)), 2)
            start_date = self.fake.date_between(start_date='-5y', end_date='today')

            loans.append((
                customer_id,
                loan_type,
                principal,
                rate,
                term,
                monthly,
                str(start_date),
                str(start_date + timedelta(days=term*30)),
                random.choice(['active', 'active', 'active', 'paid_off', 'defaulted']),
                self.fake.text(max_nb_chars=50) if loan_type in ['mortgage', 'auto'] else None
            ))
        self._insert_many(conn, 'loans',
                         ['customer_id', 'loan_type', 'principal_amount',
                          'interest_rate', 'term_months', 'monthly_payment',
                          'start_date', 'end_date', 'status', 'collateral'], loans)

        # Loan payments
        payments = []
        for loan_id in range(1, 81):
            num_payments = random.randint(1, 24)
            remaining = loans[loan_id-1][2]
            for j in range(num_payments):
                payment_date = self.fake.date_between(start_date='-2y', end_date='today')
                payment_amount = loans[loan_id-1][5]
                principal_paid = round(payment_amount * random.uniform(0.3, 0.7), 2)
                interest_paid = round(payment_amount - principal_paid, 2)
                remaining = max(0, remaining - principal_paid)
                payments.append((
                    loan_id,
                    str(payment_date),
                    payment_amount,
                    principal_paid,
                    interest_paid,
                    round(remaining, 2),
                    'completed'
                ))
        self._insert_many(conn, 'loan_payments',
                         ['loan_id', 'payment_date', 'amount', 'principal_paid',
                          'interest_paid', 'remaining_balance', 'status'], payments)

        # Credit cards
        credit_cards = []
        for i in range(60):
            customer_id = random.randint(1, 120)
            credit_limit = round(random.choice([1000, 2500, 5000, 10000, 15000, 25000]), 2)
            credit_cards.append((
                customer_id,
                str(random.randint(1000, 9999)),
                credit_limit,
                round(random.uniform(0, credit_limit * 0.8), 2),
                round(random.uniform(0.15, 0.25), 4),
                str(self.fake.date_between(start_date='-5y', end_date='today')),
                str(self.fake.date_between(start_date='today', end_date='+5y')),
                random.choice(['active', 'active', 'active', 'suspended', 'closed'])
            ))
        self._insert_many(conn, 'credit_cards',
                         ['customer_id', 'card_number_last_four', 'credit_limit',
                          'current_balance', 'apr', 'issue_date', 'expiry_date',
                          'status'], credit_cards)

    def _generate_social_media_data(self, conn):
        """Generate social media data"""
        # Users (100 users)
        users = []
        for i in range(100):
            created = self.fake.date_time_between(start_date='-3y', end_date='-1d')
            users.append((
                f"user_{self.fake.user_name()}{i}",
                f"user{i+1}@{self.fake.free_email_domain()}",
                self.fake.sha256(),
                self.fake.name(),
                self.fake.text(max_nb_chars=150),
                f"https://example.com/avatars/{i+1}.jpg",
                self.fake.city(),
                self.fake.url() if random.random() > 0.7 else None,
                1 if random.random() > 0.9 else 0,
                1 if random.random() > 0.85 else 0,
                str(created),
                str(self.fake.date_time_between(start_date=created, end_date='now')),
                0,  # Will update later
                0   # Will update later
            ))
        self._insert_many(conn, 'users',
                         ['username', 'email', 'password_hash', 'display_name',
                          'bio', 'profile_picture_url', 'location', 'website',
                          'is_verified', 'is_private', 'created_at', 'last_login',
                          'follower_count', 'following_count'], users)

        # Posts (400 posts)
        posts = []
        for i in range(400):
            user_id = random.randint(1, 100)
            post_type = random.choices(
                ['text', 'image', 'video'],
                weights=[60, 30, 10]
            )[0]
            created = self.fake.date_time_between(start_date='-1y', end_date='now')
            posts.append((
                user_id,
                self.fake.text(max_nb_chars=280),
                f"https://example.com/images/{i+1}.jpg" if post_type == 'image' else None,
                f"https://example.com/videos/{i+1}.mp4" if post_type == 'video' else None,
                post_type,
                str(created),
                str(self.fake.date_time_between(start_date=created, end_date='now')) if random.random() > 0.8 else None,
                0, 0, 0,
                1 if random.random() > 0.95 else 0,
                random.choice(['public', 'public', 'public', 'followers_only', 'private'])
            ))
        self._insert_many(conn, 'posts',
                         ['user_id', 'content', 'image_url', 'video_url',
                          'post_type', 'created_at', 'updated_at', 'like_count',
                          'comment_count', 'share_count', 'is_pinned', 'visibility'], posts)

        # Comments (600 comments)
        comments = []
        for i in range(600):
            post_id = random.randint(1, 400)
            user_id = random.randint(1, 100)
            parent_id = None
            if random.random() > 0.8 and i > 50:
                parent_id = random.randint(1, i)
            comments.append((
                post_id,
                user_id,
                parent_id,
                self.fake.text(max_nb_chars=200),
                str(self.fake.date_time_between(start_date='-1y', end_date='now')),
                random.randint(0, 50),
                1 if random.random() > 0.9 else 0
            ))
        self._insert_many(conn, 'comments',
                         ['post_id', 'user_id', 'parent_comment_id', 'content',
                          'created_at', 'like_count', 'is_edited'], comments)

        # Likes (1500 likes)
        likes = []
        like_set = set()
        for _ in range(1500):
            user_id = random.randint(1, 100)
            if random.random() > 0.3:
                post_id = random.randint(1, 400)
                comment_id = None
                key = (user_id, post_id, None)
            else:
                post_id = None
                comment_id = random.randint(1, 600)
                key = (user_id, None, comment_id)

            if key not in like_set:
                like_set.add(key)
                likes.append((
                    user_id, post_id, comment_id,
                    str(self.fake.date_time_between(start_date='-1y', end_date='now'))
                ))
        self._insert_many(conn, 'likes',
                         ['user_id', 'post_id', 'comment_id', 'created_at'], likes)

        # Update like counts
        conn.execute("""
            UPDATE posts SET like_count = (
                SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id
            )
        """)
        conn.execute("""
            UPDATE posts SET comment_count = (
                SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id
            )
        """)

        # Follows (500 follows)
        follows = []
        follow_set = set()
        for _ in range(500):
            follower = random.randint(1, 100)
            following = random.randint(1, 100)
            if follower != following and (follower, following) not in follow_set:
                follow_set.add((follower, following))
                follows.append((
                    follower, following,
                    str(self.fake.date_time_between(start_date='-2y', end_date='now'))
                ))
        self._insert_many(conn, 'follows',
                         ['follower_id', 'following_id', 'created_at'], follows)

        # Update follower/following counts
        conn.execute("""
            UPDATE users SET follower_count = (
                SELECT COUNT(*) FROM follows WHERE follows.following_id = users.id
            )
        """)
        conn.execute("""
            UPDATE users SET following_count = (
                SELECT COUNT(*) FROM follows WHERE follows.follower_id = users.id
            )
        """)

        # Hashtags
        hashtag_names = ['programming', 'python', 'sql', 'coding', 'tech', 'ai',
                        'machinelearning', 'webdev', 'javascript', 'data',
                        'tutorial', 'tips', 'motivation', 'learning', 'career',
                        'startup', 'productivity', 'opensource', 'database', 'cloud']
        hashtags = [(tag, 0) for tag in hashtag_names]
        self._insert_many(conn, 'hashtags', ['tag', 'usage_count'], hashtags)

        # Post hashtags
        post_hashtags = []
        ph_set = set()
        for post_id in range(1, 401):
            num_tags = random.randint(0, 5)
            tags = random.sample(range(1, 21), num_tags)
            for tag_id in tags:
                if (post_id, tag_id) not in ph_set:
                    ph_set.add((post_id, tag_id))
                    post_hashtags.append((post_id, tag_id))
        self._insert_many(conn, 'post_hashtags',
                         ['post_id', 'hashtag_id'], post_hashtags)

        # Update hashtag counts
        conn.execute("""
            UPDATE hashtags SET usage_count = (
                SELECT COUNT(*) FROM post_hashtags WHERE post_hashtags.hashtag_id = hashtags.id
            )
        """)

        # Messages (300 messages)
        messages = []
        for _ in range(300):
            sender = random.randint(1, 100)
            receiver = random.randint(1, 100)
            while receiver == sender:
                receiver = random.randint(1, 100)
            sent = self.fake.date_time_between(start_date='-6m', end_date='now')
            messages.append((
                sender, receiver,
                self.fake.text(max_nb_chars=200),
                str(sent),
                str(self.fake.date_time_between(start_date=sent, end_date='now')) if random.random() > 0.3 else None,
                0
            ))
        self._insert_many(conn, 'messages',
                         ['sender_id', 'receiver_id', 'content', 'sent_at',
                          'read_at', 'is_deleted'], messages)

        # Notifications
        notification_types = ['like', 'comment', 'follow', 'mention', 'message']
        notifications = []
        for _ in range(400):
            notifications.append((
                random.randint(1, 100),
                random.choice(notification_types),
                self.fake.text(max_nb_chars=100),
                random.randint(1, 400),
                random.choice([0, 0, 1]),
                str(self.fake.date_time_between(start_date='-1m', end_date='now'))
            ))
        self._insert_many(conn, 'notifications',
                         ['user_id', 'type', 'content', 'reference_id', 'is_read',
                          'created_at'], notifications)

        # Blocks (50 blocks)
        blocks = []
        block_set = set()
        for _ in range(50):
            blocker = random.randint(1, 100)
            blocked = random.randint(1, 100)
            if blocker != blocked and (blocker, blocked) not in block_set:
                block_set.add((blocker, blocked))
                blocks.append((
                    blocker, blocked,
                    str(self.fake.date_time_between(start_date='-1y', end_date='now'))
                ))
        self._insert_many(conn, 'blocks',
                         ['blocker_id', 'blocked_id', 'created_at'], blocks)

    def _generate_healthcare_data(self, conn):
        """Generate healthcare data"""
        # Departments
        departments = [
            ('Cardiology', 'Heart and cardiovascular care', 3, '555-0101'),
            ('Neurology', 'Brain and nervous system', 4, '555-0102'),
            ('Orthopedics', 'Bones, joints, and muscles', 2, '555-0103'),
            ('Pediatrics', 'Child healthcare', 1, '555-0104'),
            ('Oncology', 'Cancer treatment', 5, '555-0105'),
            ('Emergency', 'Emergency services', 1, '555-0106'),
            ('Radiology', 'Imaging and diagnostics', 2, '555-0107'),
            ('Surgery', 'Surgical procedures', 4, '555-0108'),
            ('Dermatology', 'Skin conditions', 3, '555-0109'),
            ('Psychiatry', 'Mental health', 5, '555-0110'),
        ]
        self._insert_many(conn, 'departments',
                         ['name', 'description', 'floor', 'phone'], departments)

        # Doctors (50 doctors)
        specializations = {
            1: ['Cardiologist', 'Cardiac Surgeon'],
            2: ['Neurologist', 'Neurosurgeon'],
            3: ['Orthopedic Surgeon', 'Sports Medicine'],
            4: ['Pediatrician', 'Neonatologist'],
            5: ['Oncologist', 'Radiation Oncologist'],
            6: ['Emergency Physician', 'Trauma Surgeon'],
            7: ['Radiologist', 'Interventional Radiologist'],
            8: ['General Surgeon', 'Vascular Surgeon'],
            9: ['Dermatologist', 'Cosmetic Dermatologist'],
            10: ['Psychiatrist', 'Clinical Psychologist']
        }

        doctors = []
        for i in range(50):
            dept_id = random.randint(1, 10)
            doctors.append((
                self.fake.first_name(),
                self.fake.last_name(),
                f"dr.{self.fake.last_name().lower()}{i}@hospital.com",
                self.fake.phone_number()[:15],
                random.choice(specializations[dept_id]),
                dept_id,
                f"MD-{random.randint(100000, 999999)}",
                str(self.fake.date_between(start_date='-20y', end_date='-1y')),
                random.randint(1, 30),
                round(random.uniform(100, 500), 2),
                1 if random.random() > 0.1 else 0
            ))
        self._insert_many(conn, 'doctors',
                         ['first_name', 'last_name', 'email', 'phone',
                          'specialization', 'department_id', 'license_number',
                          'hire_date', 'years_experience', 'consultation_fee',
                          'is_active'], doctors)

        # Update department heads
        for dept_id in range(1, 11):
            doc_id = random.randint(1, 50)
            conn.execute(
                "UPDATE departments SET head_doctor_id = ? WHERE id = ?",
                (doc_id, dept_id)
            )

        # Patients (150 patients)
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        insurance_providers = ['BlueCross', 'Aetna', 'United', 'Cigna', 'Kaiser', 'Humana', None]

        patients = []
        for i in range(150):
            reg_date = self.fake.date_between(start_date='-5y', end_date='today')
            patients.append((
                self.fake.first_name(),
                self.fake.last_name(),
                f"patient{i+1}@{self.fake.free_email_domain()}",
                self.fake.phone_number()[:15],
                str(self.fake.date_of_birth(minimum_age=1, maximum_age=90)),
                random.choice(['Male', 'Female', 'Other']),
                random.choice(blood_types),
                self.fake.street_address(),
                self.fake.city(),
                self.fake.state_abbr(),
                self.fake.zipcode(),
                self.fake.name(),
                self.fake.phone_number()[:15],
                random.choice(insurance_providers),
                f"INS-{random.randint(100000, 999999)}" if random.random() > 0.2 else None,
                str(reg_date),
                1 if random.random() > 0.05 else 0
            ))
        self._insert_many(conn, 'patients',
                         ['first_name', 'last_name', 'email', 'phone',
                          'date_of_birth', 'gender', 'blood_type', 'address',
                          'city', 'state', 'zip_code', 'emergency_contact_name',
                          'emergency_contact_phone', 'insurance_provider',
                          'insurance_number', 'registered_date', 'is_active'], patients)

        # Appointments (400 appointments)
        appointment_types = ['consultation', 'follow-up', 'procedure', 'emergency', 'check-up']
        statuses = ['scheduled', 'completed', 'cancelled', 'no-show']

        appointments = []
        for i in range(400):
            apt_date = self.fake.date_between(start_date='-1y', end_date='+1m')
            appointments.append((
                random.randint(1, 150),
                random.randint(1, 50),
                str(apt_date),
                f"{random.randint(8, 17):02d}:{random.choice(['00', '30'])}:00",
                random.choice([15, 30, 45, 60]),
                random.choices(statuses, weights=[20, 60, 15, 5])[0],
                random.choice(appointment_types),
                self.fake.text(max_nb_chars=100) if random.random() > 0.5 else None
            ))
        self._insert_many(conn, 'appointments',
                         ['patient_id', 'doctor_id', 'appointment_date',
                          'appointment_time', 'duration_minutes', 'status',
                          'type', 'notes'], appointments)

        # Diagnoses (300 diagnoses)
        diagnosis_codes = {
            'I10': 'Essential Hypertension',
            'E11': 'Type 2 Diabetes',
            'J06': 'Upper Respiratory Infection',
            'M54': 'Back Pain',
            'F32': 'Major Depressive Episode',
            'K21': 'Gastroesophageal Reflux',
            'J45': 'Asthma',
            'I25': 'Chronic Ischemic Heart Disease',
            'G43': 'Migraine',
            'N39': 'Urinary Tract Infection',
            'L20': 'Atopic Dermatitis',
            'R05': 'Cough',
            'M79': 'Fibromyalgia',
            'E78': 'Hyperlipidemia',
            'K29': 'Gastritis'
        }
        severities = ['mild', 'moderate', 'severe', 'critical']

        diagnoses = []
        for i in range(300):
            code = random.choice(list(diagnosis_codes.keys()))
            diagnoses.append((
                random.randint(1, 150),
                random.randint(1, 50),
                random.randint(1, 400) if random.random() > 0.3 else None,
                code,
                diagnosis_codes[code],
                self.fake.text(max_nb_chars=200),
                random.choice(severities),
                str(self.fake.date_between(start_date='-2y', end_date='today')),
                1 if random.random() > 0.7 else 0
            ))
        self._insert_many(conn, 'diagnoses',
                         ['patient_id', 'doctor_id', 'appointment_id',
                          'diagnosis_code', 'diagnosis_name', 'description',
                          'severity', 'diagnosis_date', 'is_chronic'], diagnoses)

        # Medications (60 medications)
        medication_data = [
            ('Lisinopril', 'Lisinopril', 'Merck', 'tablet', '10mg', 15.99, 1, 'cardiovascular'),
            ('Metformin', 'Metformin HCl', 'Bristol-Myers', 'tablet', '500mg', 12.99, 1, 'diabetes'),
            ('Amlodipine', 'Amlodipine', 'Pfizer', 'tablet', '5mg', 18.99, 1, 'cardiovascular'),
            ('Omeprazole', 'Omeprazole', 'AstraZeneca', 'capsule', '20mg', 22.99, 1, 'gastrointestinal'),
            ('Atorvastatin', 'Atorvastatin', 'Pfizer', 'tablet', '40mg', 25.99, 1, 'cardiovascular'),
            ('Amoxicillin', 'Amoxicillin', 'GlaxoSmithKline', 'capsule', '500mg', 8.99, 1, 'antibiotic'),
            ('Ibuprofen', 'Ibuprofen', 'Johnson & Johnson', 'tablet', '400mg', 6.99, 0, 'pain'),
            ('Metoprolol', 'Metoprolol', 'AstraZeneca', 'tablet', '50mg', 14.99, 1, 'cardiovascular'),
            ('Albuterol', 'Albuterol Sulfate', 'Teva', 'inhaler', '90mcg', 45.99, 1, 'respiratory'),
            ('Sertraline', 'Sertraline HCl', 'Pfizer', 'tablet', '50mg', 19.99, 1, 'psychiatric'),
        ]
        # Add more generic medications
        for _ in range(50):
            medication_data.append((
                self.fake.word().title() + random.choice(['ol', 'in', 'ate', 'ide']),
                None,
                random.choice(['Pfizer', 'Merck', 'Novartis', 'Roche', 'Sanofi']),
                random.choice(['tablet', 'capsule', 'liquid', 'injection', 'cream']),
                f"{random.choice([5, 10, 20, 50, 100, 250, 500])}{random.choice(['mg', 'mcg', 'ml'])}",
                round(random.uniform(5, 200), 2),
                random.choice([0, 1]),
                random.choice(['pain', 'antibiotic', 'cardiovascular', 'psychiatric', 'gastrointestinal'])
            ))
        self._insert_many(conn, 'medications',
                         ['name', 'generic_name', 'manufacturer', 'dosage_form',
                          'strength', 'unit_price', 'requires_prescription',
                          'category'], medication_data)

        # Prescriptions (250 prescriptions)
        prescriptions = []
        for i in range(250):
            prescriptions.append((
                random.randint(1, 150),
                random.randint(1, 50),
                random.randint(1, 300) if random.random() > 0.3 else None,
                str(self.fake.date_between(start_date='-1y', end_date='today')),
                self.fake.text(max_nb_chars=100) if random.random() > 0.5 else None,
                random.choice(['active', 'active', 'completed', 'cancelled'])
            ))
        self._insert_many(conn, 'prescriptions',
                         ['patient_id', 'doctor_id', 'diagnosis_id',
                          'prescription_date', 'notes', 'status'], prescriptions)

        # Prescription items
        frequencies = ['Once daily', 'Twice daily', 'Three times daily', 'Every 6 hours', 'As needed']
        items = []
        for presc_id in range(1, 251):
            num_items = random.randint(1, 4)
            meds = random.sample(range(1, 61), num_items)
            for med_id in meds:
                items.append((
                    presc_id,
                    med_id,
                    f"{random.choice([1, 2])} {random.choice(['tablet', 'capsule', 'ml'])}",
                    random.choice(frequencies),
                    random.choice([7, 14, 30, 60, 90]),
                    random.randint(7, 90),
                    self.fake.text(max_nb_chars=50) if random.random() > 0.6 else None
                ))
        self._insert_many(conn, 'prescription_items',
                         ['prescription_id', 'medication_id', 'dosage',
                          'frequency', 'duration_days', 'quantity',
                          'instructions'], items)

        # Medical records
        records = []
        for _ in range(200):
            records.append((
                random.randint(1, 150),
                random.randint(1, 50),
                str(self.fake.date_between(start_date='-1y', end_date='today')),
                self.fake.text(max_nb_chars=100),
                f"BP: {random.randint(90, 140)}/{random.randint(60, 90)}, HR: {random.randint(60, 100)}, Temp: {round(random.uniform(97, 100), 1)}F",
                self.fake.text(max_nb_chars=300),
                self.fake.text(max_nb_chars=200),
                str(self.fake.date_between(start_date='today', end_date='+3m')) if random.random() > 0.4 else None
            ))
        self._insert_many(conn, 'medical_records',
                         ['patient_id', 'doctor_id', 'visit_date',
                          'chief_complaint', 'vital_signs', 'examination_notes',
                          'treatment_plan', 'follow_up_date'], records)

        # Lab tests
        test_names = ['Complete Blood Count', 'Basic Metabolic Panel', 'Lipid Panel',
                     'Liver Function Test', 'Thyroid Panel', 'Urinalysis',
                     'Hemoglobin A1C', 'Blood Glucose', 'COVID-19 PCR', 'Vitamin D']
        tests = []
        for _ in range(300):
            tests.append((
                random.randint(1, 150),
                random.randint(1, 50),
                random.choice(test_names),
                str(self.fake.date_between(start_date='-6m', end_date='today')),
                self.fake.text(max_nb_chars=100) if random.random() > 0.3 else None,
                self.fake.text(max_nb_chars=50),
                random.choice(['pending', 'completed', 'reviewed']),
                self.fake.text(max_nb_chars=100) if random.random() > 0.6 else None
            ))
        self._insert_many(conn, 'lab_tests',
                         ['patient_id', 'doctor_id', 'test_name', 'test_date',
                          'results', 'normal_range', 'status', 'notes'], tests)

    def _generate_education_data(self, conn):
        """Generate education data"""
        # Departments
        departments = [
            ('Computer Science', 'CS', 'Study of computation and information', 'Engineering Building'),
            ('Mathematics', 'MATH', 'Study of numbers, quantities, and shapes', 'Science Hall'),
            ('Physics', 'PHYS', 'Study of matter and energy', 'Science Hall'),
            ('Chemistry', 'CHEM', 'Study of substances and reactions', 'Science Hall'),
            ('Biology', 'BIO', 'Study of living organisms', 'Life Sciences Building'),
            ('English', 'ENG', 'Study of literature and writing', 'Humanities Building'),
            ('History', 'HIST', 'Study of past events', 'Humanities Building'),
            ('Psychology', 'PSYCH', 'Study of mind and behavior', 'Social Sciences Building'),
            ('Economics', 'ECON', 'Study of production and consumption', 'Business School'),
            ('Business', 'BUS', 'Study of commerce and management', 'Business School'),
        ]
        self._insert_many(conn, 'departments',
                         ['name', 'code', 'description', 'building'], departments)

        # Instructors (40 instructors)
        titles = ['Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer', 'Adjunct']
        instructors = []
        for i in range(40):
            dept_id = random.randint(1, 10)
            instructors.append((
                self.fake.first_name(),
                self.fake.last_name(),
                f"professor{i+1}@university.edu",
                self.fake.phone_number()[:15],
                dept_id,
                random.choice(titles),
                f"Building {chr(65 + dept_id % 5)}-{random.randint(100, 400)}",
                str(self.fake.date_between(start_date='-20y', end_date='-1y')),
                random.choice(['tenured', 'tenure-track', 'non-tenure', 'adjunct']),
                round(random.uniform(50000, 150000), 2),
                1 if random.random() > 0.05 else 0
            ))
        self._insert_many(conn, 'instructors',
                         ['first_name', 'last_name', 'email', 'phone',
                          'department_id', 'title', 'office_location',
                          'hire_date', 'tenure_status', 'salary', 'is_active'], instructors)

        # Update department heads
        for dept_id in range(1, 11):
            inst_id = random.randint(1, 40)
            conn.execute(
                "UPDATE departments SET head_instructor_id = ? WHERE id = ?",
                (inst_id, dept_id)
            )

        # Semesters
        semesters = [
            ('Fall 2023', 2023, '2023-08-28', '2023-12-15', '2023-07-15', '2023-08-25', 0),
            ('Spring 2024', 2024, '2024-01-15', '2024-05-10', '2023-11-01', '2024-01-12', 0),
            ('Summer 2024', 2024, '2024-05-20', '2024-08-10', '2024-04-01', '2024-05-17', 0),
            ('Fall 2024', 2024, '2024-08-26', '2024-12-13', '2024-07-15', '2024-08-23', 1),
            ('Spring 2025', 2025, '2025-01-13', '2025-05-09', '2024-11-01', '2025-01-10', 0),
        ]
        self._insert_many(conn, 'semesters',
                         ['name', 'year', 'start_date', 'end_date',
                          'registration_start', 'registration_end', 'is_current'], semesters)

        # Courses (60 courses)
        course_data = {
            1: [('Introduction to Programming', 'CS101', 3, '100'),
                ('Data Structures', 'CS201', 3, '200'),
                ('Algorithms', 'CS301', 3, '300'),
                ('Database Systems', 'CS340', 3, '300'),
                ('Operating Systems', 'CS350', 3, '300'),
                ('Machine Learning', 'CS450', 3, '400')],
            2: [('Calculus I', 'MATH101', 4, '100'),
                ('Calculus II', 'MATH102', 4, '100'),
                ('Linear Algebra', 'MATH201', 3, '200'),
                ('Statistics', 'MATH301', 3, '300'),
                ('Differential Equations', 'MATH302', 3, '300')],
            3: [('Physics I', 'PHYS101', 4, '100'),
                ('Physics II', 'PHYS102', 4, '100'),
                ('Modern Physics', 'PHYS301', 3, '300'),
                ('Quantum Mechanics', 'PHYS401', 3, '400')],
            4: [('General Chemistry', 'CHEM101', 4, '100'),
                ('Organic Chemistry', 'CHEM201', 4, '200'),
                ('Biochemistry', 'CHEM301', 3, '300')],
            5: [('Introduction to Biology', 'BIO101', 4, '100'),
                ('Cell Biology', 'BIO201', 3, '200'),
                ('Genetics', 'BIO301', 3, '300'),
                ('Molecular Biology', 'BIO401', 3, '400')],
            6: [('Composition I', 'ENG101', 3, '100'),
                ('Composition II', 'ENG102', 3, '100'),
                ('American Literature', 'ENG201', 3, '200'),
                ('Creative Writing', 'ENG301', 3, '300')],
            7: [('World History', 'HIST101', 3, '100'),
                ('US History', 'HIST102', 3, '100'),
                ('Ancient Civilizations', 'HIST201', 3, '200')],
            8: [('Introduction to Psychology', 'PSYCH101', 3, '100'),
                ('Developmental Psychology', 'PSYCH201', 3, '200'),
                ('Abnormal Psychology', 'PSYCH301', 3, '300'),
                ('Research Methods', 'PSYCH350', 3, '300')],
            9: [('Microeconomics', 'ECON101', 3, '100'),
                ('Macroeconomics', 'ECON102', 3, '100'),
                ('Econometrics', 'ECON301', 3, '300')],
            10: [('Business Fundamentals', 'BUS101', 3, '100'),
                 ('Marketing', 'BUS201', 3, '200'),
                 ('Finance', 'BUS301', 3, '300'),
                 ('Strategic Management', 'BUS401', 3, '400')]
        }

        courses = []
        for dept_id, dept_courses in course_data.items():
            for name, code, credits, level in dept_courses:
                courses.append((
                    code,
                    name,
                    self.fake.text(max_nb_chars=200),
                    dept_id,
                    credits,
                    level,
                    None,
                    random.randint(25, 40),
                    1
                ))
        self._insert_many(conn, 'courses',
                         ['code', 'name', 'description', 'department_id',
                          'credits', 'level', 'prerequisites', 'max_enrollment',
                          'is_active'], courses)

        # Course sections (100 sections)
        schedules = ['MWF 9:00-9:50', 'MWF 10:00-10:50', 'MWF 11:00-11:50',
                    'TTh 9:30-10:45', 'TTh 11:00-12:15', 'TTh 1:00-2:15',
                    'MW 2:00-3:15', 'MW 4:00-5:15']
        rooms = [f"Room {chr(65+i)}{j}" for i in range(5) for j in range(101, 120)]

        sections = []
        for i in range(100):
            course_id = random.randint(1, len(courses))
            sections.append((
                course_id,
                random.randint(1, 5),  # semester
                random.randint(1, 40),  # instructor
                f"{random.randint(1, 3):02d}",  # section number
                random.choice(rooms),
                random.choice(schedules),
                random.randint(25, 40),
                random.randint(15, 35)
            ))
        self._insert_many(conn, 'course_sections',
                         ['course_id', 'semester_id', 'instructor_id',
                          'section_number', 'room', 'schedule', 'max_students',
                          'current_enrollment'], sections)

        # Students (200 students)
        students = []
        for i in range(200):
            enrollment_date = self.fake.date_between(start_date='-4y', end_date='today')
            students.append((
                f"STU{100000 + i}",
                self.fake.first_name(),
                self.fake.last_name(),
                f"student{i+1}@university.edu",
                self.fake.phone_number()[:15],
                str(self.fake.date_of_birth(minimum_age=18, maximum_age=30)),
                self.fake.street_address(),
                self.fake.city(),
                self.fake.state_abbr(),
                self.fake.zipcode(),
                random.randint(1, 10),  # major
                random.randint(1, 10) if random.random() > 0.6 else None,  # minor
                str(enrollment_date),
                str(enrollment_date + timedelta(days=1460)),  # 4 years
                round(random.uniform(2.0, 4.0), 2),
                random.randint(0, 120),
                random.choice(['active', 'active', 'active', 'on_leave', 'graduated', 'withdrawn'])
            ))
        self._insert_many(conn, 'students',
                         ['student_id', 'first_name', 'last_name', 'email',
                          'phone', 'date_of_birth', 'address', 'city', 'state',
                          'zip_code', 'major_department_id', 'minor_department_id',
                          'enrollment_date', 'expected_graduation', 'gpa',
                          'credits_completed', 'status'], students)

        # Enrollments (500 enrollments)
        grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F', None]
        grade_points = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                       'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0.0}

        enrollments = []
        for _ in range(500):
            grade = random.choice(grades)
            enrollments.append((
                random.randint(1, 200),
                random.randint(1, 100),
                str(self.fake.date_between(start_date='-2y', end_date='today')),
                random.choice(['enrolled', 'completed', 'dropped', 'withdrawn']),
                grade,
                grade_points.get(grade),
                round(random.uniform(70, 100), 1) if random.random() > 0.2 else None
            ))
        self._insert_many(conn, 'enrollments',
                         ['student_id', 'section_id', 'enrollment_date',
                          'status', 'grade', 'grade_points',
                          'attendance_percentage'], enrollments)

        # Grades (detailed)
        assignment_types = ['homework', 'quiz', 'midterm', 'final', 'project', 'participation']
        detailed_grades = []
        for enroll_id in range(1, 501):
            num_assignments = random.randint(5, 15)
            for _ in range(num_assignments):
                max_pts = random.choice([10, 20, 50, 100])
                detailed_grades.append((
                    enroll_id,
                    f"{random.choice(assignment_types).title()} {random.randint(1, 5)}",
                    random.choice(assignment_types),
                    max_pts,
                    round(random.uniform(max_pts * 0.5, max_pts), 1),
                    round(random.uniform(0.05, 0.25), 2),
                    str(self.fake.date_time_between(start_date='-1y', end_date='now')),
                    str(self.fake.date_time_between(start_date='-1y', end_date='now')),
                    self.fake.text(max_nb_chars=100) if random.random() > 0.7 else None
                ))
        self._insert_many(conn, 'grades',
                         ['enrollment_id', 'assignment_name', 'assignment_type',
                          'max_points', 'points_earned', 'weight',
                          'submission_date', 'graded_date', 'feedback'], detailed_grades)

        # Assignments
        assignments = []
        for section_id in range(1, 101):
            for _ in range(random.randint(5, 10)):
                atype = random.choice(assignment_types)
                assignments.append((
                    section_id,
                    f"{atype.title()} {random.randint(1, 5)}",
                    self.fake.text(max_nb_chars=200),
                    atype,
                    random.choice([10, 20, 50, 100]),
                    round(random.uniform(0.05, 0.25), 2),
                    str(self.fake.date_time_between(start_date='-1y', end_date='+2m'))
                ))
        self._insert_many(conn, 'assignments',
                         ['section_id', 'name', 'description', 'type',
                          'max_points', 'weight', 'due_date'], assignments)

        # Attendance
        attendance_statuses = ['present', 'absent', 'late', 'excused']
        attendance = []
        for enroll_id in range(1, 501):
            num_classes = random.randint(10, 30)
            for _ in range(num_classes):
                attendance.append((
                    enroll_id,
                    str(self.fake.date_between(start_date='-6m', end_date='today')),
                    random.choices(attendance_statuses, weights=[85, 5, 7, 3])[0],
                    self.fake.text(max_nb_chars=50) if random.random() > 0.9 else None
                ))
        self._insert_many(conn, 'attendance',
                         ['enrollment_id', 'class_date', 'status', 'notes'], attendance)

        # Scholarships
        scholarships = [
            ('Merit Scholarship', 'For students with high academic achievement', 5000, 'GPA >= 3.5'),
            ('Need-Based Grant', 'Financial assistance for eligible students', 3000, 'FAFSA required'),
            ('STEM Excellence', 'For outstanding STEM students', 7500, 'STEM major, GPA >= 3.3'),
            ('Athletic Scholarship', 'For student athletes', 10000, 'Varsity athlete'),
            ('Dean\'s Scholarship', 'Top 5% of class', 15000, 'Top 5% GPA'),
            ('Community Service Award', 'For community involvement', 2500, '100+ volunteer hours'),
            ('Research Fellowship', 'For research students', 8000, 'Research participation'),
            ('International Student Aid', 'For international students', 6000, 'International status'),
        ]
        self._insert_many(conn, 'scholarships',
                         ['name', 'description', 'amount', 'requirements'], scholarships)

        # Student scholarships
        student_scholarships = []
        for _ in range(100):
            student_scholarships.append((
                random.randint(1, 200),
                random.randint(1, 8),
                str(self.fake.date_between(start_date='-2y', end_date='today')),
                round(random.uniform(1000, 15000), 2),
                random.randint(1, 5),
                random.choice(['active', 'active', 'completed', 'cancelled'])
            ))
        self._insert_many(conn, 'student_scholarships',
                         ['student_id', 'scholarship_id', 'awarded_date',
                          'amount', 'semester_id', 'status'], student_scholarships)


def initialize_exercise_database():
    """Initialize the exercise database with all scenarios"""
    generator = DataGenerator()
    generator.generate_all_scenarios()
    print("Exercise database initialized successfully!")


if __name__ == "__main__":
    initialize_exercise_database()
