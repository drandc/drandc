"""
Schema Generator for SQL Practice Generator
Creates database schemas for different data scenarios
"""
from typing import Dict, List


class SchemaGenerator:
    """Generates database schemas for different practice scenarios"""

    @staticmethod
    def get_ecommerce_schema() -> str:
        """E-commerce database schema"""
        return """
        -- Customers table
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            country TEXT DEFAULT 'USA',
            zip_code TEXT,
            join_date DATE NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            loyalty_points INTEGER DEFAULT 0
        );

        -- Categories table
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            parent_category_id INTEGER,
            FOREIGN KEY (parent_category_id) REFERENCES categories(id)
        );

        -- Products table
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            cost DECIMAL(10, 2),
            sku TEXT UNIQUE,
            weight DECIMAL(8, 2),
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );

        -- Inventory table
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL UNIQUE,
            quantity INTEGER NOT NULL DEFAULT 0,
            warehouse_location TEXT,
            last_restocked DATE,
            reorder_level INTEGER DEFAULT 10,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        -- Orders table
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TIMESTAMP NOT NULL,
            status TEXT DEFAULT 'pending',
            shipping_address TEXT,
            shipping_city TEXT,
            shipping_state TEXT,
            shipping_zip TEXT,
            shipping_cost DECIMAL(8, 2) DEFAULT 0,
            tax_amount DECIMAL(8, 2) DEFAULT 0,
            total_amount DECIMAL(10, 2),
            payment_method TEXT,
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        -- Order items table
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            discount_percent DECIMAL(5, 2) DEFAULT 0,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        -- Reviews table
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
            title TEXT,
            comment TEXT,
            review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            helpful_votes INTEGER DEFAULT 0,
            verified_purchase BOOLEAN DEFAULT 0,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        -- Coupons table
        CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            discount_type TEXT NOT NULL,
            discount_value DECIMAL(10, 2) NOT NULL,
            min_order_amount DECIMAL(10, 2) DEFAULT 0,
            max_uses INTEGER,
            uses_count INTEGER DEFAULT 0,
            start_date DATE,
            end_date DATE,
            is_active BOOLEAN DEFAULT 1
        );
        """

    @staticmethod
    def get_hr_schema() -> str:
        """HR/Corporate database schema"""
        return """
        -- Departments table
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            budget DECIMAL(15, 2),
            location TEXT,
            manager_id INTEGER
        );

        -- Employees table
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            hire_date DATE NOT NULL,
            job_title TEXT NOT NULL,
            department_id INTEGER,
            manager_id INTEGER,
            salary DECIMAL(12, 2) NOT NULL,
            commission_pct DECIMAL(4, 2),
            is_active BOOLEAN DEFAULT 1,
            birth_date DATE,
            address TEXT,
            city TEXT,
            state TEXT,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            FOREIGN KEY (manager_id) REFERENCES employees(id)
        );

        -- Update departments with manager foreign key
        -- (handled in data generator due to circular reference)

        -- Salaries history table
        CREATE TABLE IF NOT EXISTS salary_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            salary DECIMAL(12, 2) NOT NULL,
            effective_date DATE NOT NULL,
            end_date DATE,
            change_reason TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );

        -- Performance reviews table
        CREATE TABLE IF NOT EXISTS performance_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            reviewer_id INTEGER NOT NULL,
            review_date DATE NOT NULL,
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
            goals_met_pct INTEGER,
            strengths TEXT,
            areas_for_improvement TEXT,
            comments TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            FOREIGN KEY (reviewer_id) REFERENCES employees(id)
        );

        -- Projects table
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            department_id INTEGER,
            start_date DATE,
            end_date DATE,
            budget DECIMAL(15, 2),
            status TEXT DEFAULT 'planning',
            priority TEXT DEFAULT 'medium',
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );

        -- Project assignments table
        CREATE TABLE IF NOT EXISTS project_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            role TEXT,
            hours_allocated INTEGER,
            start_date DATE,
            end_date DATE,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );

        -- Time off requests table
        CREATE TABLE IF NOT EXISTS time_off_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            request_type TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            status TEXT DEFAULT 'pending',
            approved_by INTEGER,
            request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            FOREIGN KEY (approved_by) REFERENCES employees(id)
        );

        -- Training courses table
        CREATE TABLE IF NOT EXISTS training_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            duration_hours INTEGER,
            instructor TEXT,
            cost DECIMAL(10, 2),
            is_mandatory BOOLEAN DEFAULT 0
        );

        -- Training enrollments table
        CREATE TABLE IF NOT EXISTS training_enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            enrollment_date DATE,
            completion_date DATE,
            score INTEGER,
            status TEXT DEFAULT 'enrolled',
            FOREIGN KEY (course_id) REFERENCES training_courses(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );
        """

    @staticmethod
    def get_finance_schema() -> str:
        """Finance/Banking database schema"""
        return """
        -- Branches table
        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            phone TEXT,
            manager_name TEXT,
            opened_date DATE
        );

        -- Customers table
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            ssn_last_four TEXT,
            date_of_birth DATE,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            credit_score INTEGER,
            is_active BOOLEAN DEFAULT 1
        );

        -- Account types table
        CREATE TABLE IF NOT EXISTS account_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            min_balance DECIMAL(12, 2) DEFAULT 0,
            interest_rate DECIMAL(6, 4),
            monthly_fee DECIMAL(8, 2) DEFAULT 0
        );

        -- Accounts table
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            account_type_id INTEGER NOT NULL,
            account_number TEXT UNIQUE NOT NULL,
            balance DECIMAL(15, 2) DEFAULT 0,
            opened_date DATE NOT NULL,
            closed_date DATE,
            branch_id INTEGER,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (account_type_id) REFERENCES account_types(id),
            FOREIGN KEY (branch_id) REFERENCES branches(id)
        );

        -- Transactions table
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount DECIMAL(12, 2) NOT NULL,
            balance_after DECIMAL(15, 2),
            description TEXT,
            transaction_date TIMESTAMP NOT NULL,
            reference_number TEXT,
            category TEXT,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        );

        -- Transfers table
        CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_account_id INTEGER NOT NULL,
            to_account_id INTEGER NOT NULL,
            amount DECIMAL(12, 2) NOT NULL,
            transfer_date TIMESTAMP NOT NULL,
            status TEXT DEFAULT 'completed',
            notes TEXT,
            FOREIGN KEY (from_account_id) REFERENCES accounts(id),
            FOREIGN KEY (to_account_id) REFERENCES accounts(id)
        );

        -- Loans table
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            loan_type TEXT NOT NULL,
            principal_amount DECIMAL(15, 2) NOT NULL,
            interest_rate DECIMAL(6, 4) NOT NULL,
            term_months INTEGER NOT NULL,
            monthly_payment DECIMAL(12, 2),
            start_date DATE NOT NULL,
            end_date DATE,
            status TEXT DEFAULT 'active',
            collateral TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        -- Loan payments table
        CREATE TABLE IF NOT EXISTS loan_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loan_id INTEGER NOT NULL,
            payment_date DATE NOT NULL,
            amount DECIMAL(12, 2) NOT NULL,
            principal_paid DECIMAL(12, 2),
            interest_paid DECIMAL(12, 2),
            remaining_balance DECIMAL(15, 2),
            status TEXT DEFAULT 'completed',
            FOREIGN KEY (loan_id) REFERENCES loans(id)
        );

        -- Credit cards table
        CREATE TABLE IF NOT EXISTS credit_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            card_number_last_four TEXT,
            credit_limit DECIMAL(12, 2),
            current_balance DECIMAL(12, 2) DEFAULT 0,
            apr DECIMAL(6, 4),
            issue_date DATE,
            expiry_date DATE,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
        """

    @staticmethod
    def get_social_media_schema() -> str:
        """Social Media database schema"""
        return """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            display_name TEXT,
            bio TEXT,
            profile_picture_url TEXT,
            location TEXT,
            website TEXT,
            is_verified BOOLEAN DEFAULT 0,
            is_private BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            follower_count INTEGER DEFAULT 0,
            following_count INTEGER DEFAULT 0
        );

        -- Posts table
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT,
            image_url TEXT,
            video_url TEXT,
            post_type TEXT DEFAULT 'text',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            like_count INTEGER DEFAULT 0,
            comment_count INTEGER DEFAULT 0,
            share_count INTEGER DEFAULT 0,
            is_pinned BOOLEAN DEFAULT 0,
            visibility TEXT DEFAULT 'public',
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        -- Comments table
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            parent_comment_id INTEGER,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            like_count INTEGER DEFAULT 0,
            is_edited BOOLEAN DEFAULT 0,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (parent_comment_id) REFERENCES comments(id)
        );

        -- Likes table
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            post_id INTEGER,
            comment_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (comment_id) REFERENCES comments(id)
        );

        -- Follows table
        CREATE TABLE IF NOT EXISTS follows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            follower_id INTEGER NOT NULL,
            following_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (follower_id) REFERENCES users(id),
            FOREIGN KEY (following_id) REFERENCES users(id),
            UNIQUE(follower_id, following_id)
        );

        -- Hashtags table
        CREATE TABLE IF NOT EXISTS hashtags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT UNIQUE NOT NULL,
            usage_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Post hashtags junction table
        CREATE TABLE IF NOT EXISTS post_hashtags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            hashtag_id INTEGER NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (hashtag_id) REFERENCES hashtags(id),
            UNIQUE(post_id, hashtag_id)
        );

        -- Messages table
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            read_at TIMESTAMP,
            is_deleted BOOLEAN DEFAULT 0,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        );

        -- Notifications table
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            content TEXT,
            reference_id INTEGER,
            is_read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        -- Blocks table
        CREATE TABLE IF NOT EXISTS blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blocker_id INTEGER NOT NULL,
            blocked_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (blocker_id) REFERENCES users(id),
            FOREIGN KEY (blocked_id) REFERENCES users(id),
            UNIQUE(blocker_id, blocked_id)
        );
        """

    @staticmethod
    def get_healthcare_schema() -> str:
        """Healthcare database schema"""
        return """
        -- Departments table
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            floor INTEGER,
            phone TEXT,
            head_doctor_id INTEGER
        );

        -- Doctors table
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            specialization TEXT NOT NULL,
            department_id INTEGER,
            license_number TEXT UNIQUE,
            hire_date DATE,
            years_experience INTEGER,
            consultation_fee DECIMAL(10, 2),
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );

        -- Patients table
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            date_of_birth DATE NOT NULL,
            gender TEXT,
            blood_type TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            emergency_contact_name TEXT,
            emergency_contact_phone TEXT,
            insurance_provider TEXT,
            insurance_number TEXT,
            registered_date DATE NOT NULL,
            is_active BOOLEAN DEFAULT 1
        );

        -- Appointments table
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            duration_minutes INTEGER DEFAULT 30,
            status TEXT DEFAULT 'scheduled',
            type TEXT DEFAULT 'consultation',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        );

        -- Diagnoses table
        CREATE TABLE IF NOT EXISTS diagnoses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_id INTEGER,
            diagnosis_code TEXT,
            diagnosis_name TEXT NOT NULL,
            description TEXT,
            severity TEXT,
            diagnosis_date DATE NOT NULL,
            is_chronic BOOLEAN DEFAULT 0,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id),
            FOREIGN KEY (appointment_id) REFERENCES appointments(id)
        );

        -- Medications table
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            generic_name TEXT,
            manufacturer TEXT,
            dosage_form TEXT,
            strength TEXT,
            unit_price DECIMAL(10, 2),
            requires_prescription BOOLEAN DEFAULT 1,
            category TEXT
        );

        -- Prescriptions table
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            diagnosis_id INTEGER,
            prescription_date DATE NOT NULL,
            notes TEXT,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id),
            FOREIGN KEY (diagnosis_id) REFERENCES diagnoses(id)
        );

        -- Prescription items table
        CREATE TABLE IF NOT EXISTS prescription_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prescription_id INTEGER NOT NULL,
            medication_id INTEGER NOT NULL,
            dosage TEXT NOT NULL,
            frequency TEXT NOT NULL,
            duration_days INTEGER,
            quantity INTEGER,
            instructions TEXT,
            FOREIGN KEY (prescription_id) REFERENCES prescriptions(id),
            FOREIGN KEY (medication_id) REFERENCES medications(id)
        );

        -- Medical records table
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            visit_date DATE NOT NULL,
            chief_complaint TEXT,
            vital_signs TEXT,
            examination_notes TEXT,
            treatment_plan TEXT,
            follow_up_date DATE,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        );

        -- Lab tests table
        CREATE TABLE IF NOT EXISTS lab_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            test_name TEXT NOT NULL,
            test_date DATE NOT NULL,
            results TEXT,
            normal_range TEXT,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        );
        """

    @staticmethod
    def get_education_schema() -> str:
        """Education database schema"""
        return """
        -- Departments table
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            code TEXT UNIQUE,
            description TEXT,
            building TEXT,
            phone TEXT,
            head_instructor_id INTEGER
        );

        -- Instructors table
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            department_id INTEGER,
            title TEXT,
            office_location TEXT,
            hire_date DATE,
            tenure_status TEXT,
            salary DECIMAL(12, 2),
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );

        -- Semesters table
        CREATE TABLE IF NOT EXISTS semesters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            registration_start DATE,
            registration_end DATE,
            is_current BOOLEAN DEFAULT 0
        );

        -- Courses table
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            department_id INTEGER,
            credits INTEGER NOT NULL,
            level TEXT,
            prerequisites TEXT,
            max_enrollment INTEGER DEFAULT 30,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );

        -- Course sections table
        CREATE TABLE IF NOT EXISTS course_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            semester_id INTEGER NOT NULL,
            instructor_id INTEGER NOT NULL,
            section_number TEXT NOT NULL,
            room TEXT,
            schedule TEXT,
            max_students INTEGER DEFAULT 30,
            current_enrollment INTEGER DEFAULT 0,
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (semester_id) REFERENCES semesters(id),
            FOREIGN KEY (instructor_id) REFERENCES instructors(id)
        );

        -- Students table
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            date_of_birth DATE,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            major_department_id INTEGER,
            minor_department_id INTEGER,
            enrollment_date DATE NOT NULL,
            expected_graduation DATE,
            gpa DECIMAL(3, 2),
            credits_completed INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (major_department_id) REFERENCES departments(id),
            FOREIGN KEY (minor_department_id) REFERENCES departments(id)
        );

        -- Enrollments table
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            section_id INTEGER NOT NULL,
            enrollment_date DATE NOT NULL,
            status TEXT DEFAULT 'enrolled',
            grade TEXT,
            grade_points DECIMAL(3, 2),
            attendance_percentage DECIMAL(5, 2),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (section_id) REFERENCES course_sections(id)
        );

        -- Grades table (detailed grade breakdown)
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_id INTEGER NOT NULL,
            assignment_name TEXT NOT NULL,
            assignment_type TEXT,
            max_points DECIMAL(8, 2),
            points_earned DECIMAL(8, 2),
            weight DECIMAL(5, 2),
            submission_date TIMESTAMP,
            graded_date TIMESTAMP,
            feedback TEXT,
            FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
        );

        -- Assignments table
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            type TEXT,
            max_points DECIMAL(8, 2),
            weight DECIMAL(5, 2),
            due_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (section_id) REFERENCES course_sections(id)
        );

        -- Attendance table
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_id INTEGER NOT NULL,
            class_date DATE NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
        );

        -- Scholarships table
        CREATE TABLE IF NOT EXISTS scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            amount DECIMAL(12, 2),
            requirements TEXT,
            deadline DATE
        );

        -- Student scholarships table
        CREATE TABLE IF NOT EXISTS student_scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            scholarship_id INTEGER NOT NULL,
            awarded_date DATE,
            amount DECIMAL(12, 2),
            semester_id INTEGER,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (scholarship_id) REFERENCES scholarships(id),
            FOREIGN KEY (semester_id) REFERENCES semesters(id)
        );
        """

    @classmethod
    def get_schema(cls, scenario: str) -> str:
        """Get the schema for a specific scenario"""
        schemas = {
            'ecommerce': cls.get_ecommerce_schema,
            'hr': cls.get_hr_schema,
            'finance': cls.get_finance_schema,
            'social_media': cls.get_social_media_schema,
            'healthcare': cls.get_healthcare_schema,
            'education': cls.get_education_schema
        }
        if scenario not in schemas:
            raise ValueError(f"Unknown scenario: {scenario}")
        return schemas[scenario]()

    @classmethod
    def get_all_schemas(cls) -> Dict[str, str]:
        """Get all available schemas"""
        return {
            'ecommerce': cls.get_ecommerce_schema(),
            'hr': cls.get_hr_schema(),
            'finance': cls.get_finance_schema(),
            'social_media': cls.get_social_media_schema(),
            'healthcare': cls.get_healthcare_schema(),
            'education': cls.get_education_schema()
        }

    @classmethod
    def get_scenario_tables(cls, scenario: str) -> List[str]:
        """Get the list of tables for a specific scenario"""
        table_lists = {
            'ecommerce': ['customers', 'categories', 'products', 'inventory',
                         'orders', 'order_items', 'reviews', 'coupons'],
            'hr': ['departments', 'employees', 'salary_history', 'performance_reviews',
                  'projects', 'project_assignments', 'time_off_requests',
                  'training_courses', 'training_enrollments'],
            'finance': ['branches', 'customers', 'account_types', 'accounts',
                       'transactions', 'transfers', 'loans', 'loan_payments', 'credit_cards'],
            'social_media': ['users', 'posts', 'comments', 'likes', 'follows',
                            'hashtags', 'post_hashtags', 'messages', 'notifications', 'blocks'],
            'healthcare': ['departments', 'doctors', 'patients', 'appointments',
                          'diagnoses', 'medications', 'prescriptions', 'prescription_items',
                          'medical_records', 'lab_tests'],
            'education': ['departments', 'instructors', 'semesters', 'courses',
                         'course_sections', 'students', 'enrollments', 'grades',
                         'assignments', 'attendance', 'scholarships', 'student_scholarships']
        }
        return table_lists.get(scenario, [])
