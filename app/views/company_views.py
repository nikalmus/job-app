# app/views/company_views.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app


company_bp = Blueprint('company', __name__, url_prefix='/companies', template_folder='templates/companies')

@company_bp.route('/')
def list_companies():
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Fetch all companies from the database
    cursor.execute("SELECT * FROM company")
    companies = cursor.fetchall()

    cursor.close()

    return render_template('companies/companies_list.html', companies=companies)

@company_bp.route('/create', methods=['GET', 'POST'])
def create_company():
    if request.method == 'POST':
        # Get form data from the request
        name = request.form['name']

        # Validate and insert the new company into the database
        conn = current_app.config['DB_CONN']
        cursor = conn.cursor()

        # Assuming "name" is required and must not be empty
        if name:
            cursor.execute("INSERT INTO company (name) VALUES (%s)", (name,))
            conn.commit()

        cursor.close()

        return redirect(url_for('company.list_companies'))

    return render_template('companies/create_company.html')

@company_bp.route('/update/<int:company_id>', methods=['GET', 'POST'])
def update_company(company_id):
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Fetch the company from the database based on company_id
    cursor.execute("SELECT * FROM company WHERE id = %s", (company_id,))
    company = cursor.fetchone()

    if request.method == 'POST':
        # Get form data from the request
        name = request.form['name']

        # Validate and update the company in the database
        if name:
            cursor.execute("UPDATE company SET name = %s WHERE id = %s", (name, company_id))
            conn.commit()

        cursor.close()

        return redirect(url_for('company.list_companies'))

    return render_template('update_company.html', company=company)

@company_bp.route('/delete/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Delete the company from the database based on company_id
    cursor.execute("DELETE FROM company WHERE id = %s", (company_id,))
    conn.commit()

    cursor.close()

    return redirect(url_for('company.list_companies'))
