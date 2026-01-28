# SQL Practice Generator

A comprehensive SQL practice application that generates unlimited, intelligently-structured exercises with automatic answer validation and skill-tree progression. Master SQL through daily practice!

## Features

- **13-Level Skill Tree**: Progressive learning from basic SELECT to advanced CTEs and window functions
- **6 Data Scenarios**: E-commerce, HR, Finance, Social Media, Healthcare, and Education databases
- **50+ Exercise Templates**: Varied problems across all skill levels and difficulties
- **Intelligent Validation**: Automatic answer checking with helpful feedback and hints
- **Progress Tracking**: Track your stats, streaks, and achievements
- **SQL Playground**: Free-form practice with all available data
- **Gamification**: Achievements, mastery badges, and daily challenges

## Requirements

- Python 3.8 or higher
- Windows 10/11, macOS, or Linux
- Web browser (Chrome, Firefox, Edge, Safari)

## Quick Start (Windows)

1. **Download or clone the repository**

2. **Open Command Prompt or PowerShell** in the `sql_practice_app` folder

3. **Run the setup script**:
   ```
   python setup.py
   ```

4. **Start the application**:
   ```
   python app.py
   ```

5. **Open your browser** and go to: http://127.0.0.1:5000

## Manual Installation

1. **Install Python dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Initialize the database** (optional, happens automatically on first run):
   ```
   python -c "from database.data_generator import initialize_exercise_database; initialize_exercise_database()"
   ```

3. **Run the application**:
   ```
   python app.py
   ```

## Skill Levels

| Level | Topic | Description |
|-------|-------|-------------|
| 1 | Foundation | SELECT, WHERE, basic operators, LIMIT/OFFSET |
| 2 | Sorting & Uniqueness | ORDER BY, DISTINCT, string/math functions |
| 3 | Aggregation Basics | GROUP BY, HAVING, COUNT, SUM, AVG, MIN, MAX |
| 4 | Basic Joins | INNER JOIN, table aliases, join conditions |
| 5 | Advanced Joins | LEFT/RIGHT/FULL JOINs, self-joins, CROSS JOIN |
| 6 | Subqueries | Subqueries in WHERE, FROM, SELECT, EXISTS |
| 7 | Conditional Logic | CASE, COALESCE, NULLIF, IIF |
| 8 | Window Functions | ROW_NUMBER, RANK, LAG, LEAD, SUM OVER |
| 9 | CTEs | WITH clause, multiple CTEs, chaining |
| 10 | Advanced CTEs | Recursive CTEs, complex multi-level CTEs |
| 11 | Optimization | EXPLAIN, index usage, performance analysis |
| 12 | Data Manipulation | INSERT, UPDATE, DELETE, UPSERT |
| 13 | Advanced Topics | Transactions, views, temp tables, datetime |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+Enter | Run query |
| Ctrl+H | Get hint |
| Ctrl+N | Next exercise |
| Ctrl+S | Show solution |
| Escape | Close modals |

## Project Structure

```
sql_practice_app/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── setup.py               # Setup script
├── requirements.txt       # Python dependencies
├── database/
│   ├── db_manager.py      # Database connection & operations
│   ├── schema_generator.py # Database schemas for all scenarios
│   └── data_generator.py  # Realistic data generation
├── exercises/
│   ├── exercise_loader.py # Load exercise templates
│   ├── generator.py       # Generate exercise instances
│   └── templates/         # JSON exercise templates
├── validation/
│   ├── validator.py       # Query validation engine
│   ├── comparator.py      # Result comparison logic
│   └── security.py        # SQL injection prevention
├── progress/
│   ├── tracker.py         # Progress tracking
│   └── achievements.py    # Gamification system
├── static/
│   ├── css/style.css      # Application styles
│   └── js/app.js          # Frontend JavaScript
├── templates/
│   ├── base.html          # Base template
│   ├── dashboard.html     # Home page
│   ├── skills.html        # Skill tree & session config
│   ├── exercise.html      # Exercise practice
│   ├── playground.html    # Free-form SQL practice
│   ├── stats.html         # Statistics & achievements
│   └── settings.html      # User settings
└── data/                  # SQLite databases (created on setup)
```

## Adding Custom Exercises

1. Create a JSON file in `exercises/templates/`
2. Follow this format:
   ```json
   {
     "id": "custom_001",
     "level": 3,
     "difficulty": "medium",
     "skills": ["GROUP_BY", "COUNT"],
     "scenario": "ecommerce",
     "problem": "Your problem description here",
     "tables": ["customers", "orders"],
     "solution": "SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id",
     "hints": [
       "Hint 1",
       "Hint 2",
       "Hint 3"
     ]
   }
   ```

## Troubleshooting

### "Module not found" error
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Make sure you're running from the `sql_practice_app` directory

### Database errors
- Delete the `data/` folder and restart the app to reinitialize

### Port already in use
- Change the port in `app.py` (last line): `app.run(port=5001)`

### Query timeout
- The default timeout is 10 seconds. Very complex queries may need optimization.

## Data Scenarios

### E-commerce
Tables: customers, categories, products, inventory, orders, order_items, reviews, coupons

### HR/Corporate
Tables: departments, employees, salary_history, performance_reviews, projects, project_assignments, training_courses, training_enrollments

### Finance/Banking
Tables: branches, customers, account_types, accounts, transactions, transfers, loans, loan_payments, credit_cards

### Social Media
Tables: users, posts, comments, likes, follows, hashtags, post_hashtags, messages, notifications, blocks

### Healthcare
Tables: departments, doctors, patients, appointments, diagnoses, medications, prescriptions, prescription_items, medical_records, lab_tests

### Education
Tables: departments, instructors, semesters, courses, course_sections, students, enrollments, grades, assignments, attendance, scholarships

## Tips for Learning

1. **Start with Level 1** - Master the basics before moving on
2. **Read error messages** - They often tell you exactly what's wrong
3. **Use hints wisely** - Try to solve without hints first
4. **Practice regularly** - Daily practice is more effective than marathon sessions
5. **Experiment in Playground** - Use the playground to explore data and test ideas
6. **Review mistakes** - Learn from incorrect answers

## License

This project is provided for educational purposes.

## Support

For issues or questions, please open an issue on GitHub.
