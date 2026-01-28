/**
 * SQL Practice Generator - Main JavaScript
 */

// Global state
const App = {
    currentExercise: null,
    sessionStatus: null,
    editor: null,

    // Initialize the application
    init() {
        this.setupKeyboardShortcuts();
        this.loadTheme();
    },

    // Setup global keyboard shortcuts
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Escape to close modals
            if (e.key === 'Escape') {
                this.closeAllModals();
            }
        });
    },

    // Close all modal windows
    closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    },

    // Load and apply saved theme
    loadTheme() {
        const theme = localStorage.getItem('theme') || 'light';
        document.body.className = theme;
    },

    // Save theme preference
    setTheme(theme) {
        localStorage.setItem('theme', theme);
        document.body.className = theme;
    },

    // Show notification
    notify(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },

    // Format SQL query
    formatSQL(query) {
        // Simple SQL formatting
        let formatted = query.replace(/\s+/g, ' ').trim();

        const keywords = [
            'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'GROUP BY', 'HAVING',
            'ORDER BY', 'LIMIT', 'OFFSET', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN',
            'INNER JOIN', 'OUTER JOIN', 'FULL JOIN', 'CROSS JOIN', 'ON',
            'UNION', 'UNION ALL', 'INSERT INTO', 'VALUES', 'UPDATE', 'SET',
            'DELETE FROM', 'CREATE', 'DROP', 'ALTER', 'WITH'
        ];

        keywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
            formatted = formatted.replace(regex, `\n${keyword}`);
        });

        // Remove leading newline
        formatted = formatted.replace(/^\n/, '');

        return formatted;
    },

    // API helper
    async api(endpoint, method = 'GET', data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`/api/${endpoint}`, options);
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return { success: false, error: error.message };
        }
    },

    // Start a practice session
    async startSession(levels, difficulties, scenarios, count) {
        const result = await this.api('start-session', 'POST', {
            levels,
            difficulties,
            scenarios,
            count
        });

        if (result.success) {
            window.location.href = '/exercise';
        } else {
            this.notify(result.error || 'Failed to start session', 'error');
        }
    },

    // Submit answer
    async submitAnswer(query, exerciseId, hintsUsed, attempts) {
        const result = await this.api('validate', 'POST', {
            query,
            exercise_id: exerciseId,
            hints_used: hintsUsed,
            attempts
        });

        return result;
    },

    // Get hint
    async getHint(level) {
        const result = await this.api('hint', 'POST', { hint_level: level });
        return result;
    },

    // Get solution
    async getSolution() {
        const result = await this.api('solution', 'GET');
        return result;
    },

    // Move to next exercise
    async nextExercise(skip = false) {
        const result = await this.api('next-exercise', 'POST', { skip });
        return result;
    },

    // Execute playground query
    async executePlayground(query) {
        const result = await this.api('execute-playground', 'POST', { query });
        return result;
    },

    // Get stats
    async getStats() {
        const result = await this.api('stats', 'GET');
        return result;
    },

    // Export progress
    async exportProgress() {
        const result = await this.api('export-progress', 'GET');
        if (result) {
            const blob = new Blob([JSON.stringify(result, null, 2)], {
                type: 'application/json'
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'sql_progress_export.json';
            a.click();
            URL.revokeObjectURL(url);
        }
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

// Utility functions for global access
function formatQuery(editor) {
    if (editor) {
        const formatted = App.formatSQL(editor.getValue());
        editor.setValue(formatted);
    }
}

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Table data display helper
function renderTable(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container || !data || data.length === 0) {
        if (container) {
            container.innerHTML = '<p class="no-results">No data to display</p>';
        }
        return;
    }

    const columns = Object.keys(data[0]);
    let html = '<table class="result-table"><thead><tr>';

    columns.forEach(col => {
        html += `<th>${col}</th>`;
    });

    html += '</tr></thead><tbody>';

    data.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            const value = row[col];
            html += `<td>${value !== null && value !== undefined ? value : 'NULL'}</td>`;
        });
        html += '</tr>';
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

// Debounce helper
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export App for use in other scripts
window.App = App;
