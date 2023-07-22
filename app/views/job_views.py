# app/views/job_views.py

from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, current_app


job_bp = Blueprint('job', __name__, url_prefix='/jobs', template_folder='templates/jobs')

# def dict_from_row(row, cursor):
#     """Converts a database query result row to a dictionary."""
#     return {description[0]: value for description, value in zip(cursor.description, row)}

def dict_from_row(row, cursor):
    d = {}
    for idx, col in enumerate(cursor.description):
        if isinstance(row[idx], (date, datetime)):
            d[col.name] = row[idx].isoformat()
        elif isinstance(row[idx], list):
            d[col.name] = row[idx]
        else:
            d[col.name] = row[idx]
    return d


@job_bp.route('/')
def list_jobs():
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Fetch all jobs from the database
    query = '''SELECT job.id, job.title, company.id AS company_id, company.name AS company_name,
                job.applied_date, job.first_contact_date, job.last_contact_date, job.status
                FROM job JOIN company ON job.company_id = company.id'''
    

    cursor.execute(query)
    jobs_data = cursor.fetchall()

    cursor.close()

    # Convert the query results to dictionaries
    jobs = []
    for row in jobs_data:
        job_dict = dict_from_row(row, cursor)
        company_dict = {
            'id': job_dict['company_id'],
            'name': job_dict['company_name']
        }
        del job_dict['company_id']
        del job_dict['company_name']
        job_dict['company'] = company_dict
        jobs.append(job_dict)

    return render_template('jobs/jobs_list.html', jobs=jobs)


@job_bp.route('/<int:job_id>')
def job_detail(job_id):
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Get the job data from the database using job_id
    query = '''SELECT job.id, job.title, company.id AS company_id, company.name AS company_name,
                job.must_have, job.nice_have, job.link, job.applied_date, job.first_contact_date,
                job.last_contact_date, job.status
                FROM job JOIN company ON job.company_id = company.id
                WHERE job.id = %s'''
    cursor.execute(query, (job_id,))
    job_data = cursor.fetchone()

    if job_data:
        # Convert the query result to a dictionary
        job_dict = dict_from_row(job_data, cursor)

        company_dict = {
            'id': job_dict['company_id'],
            'name': job_dict['company_name']
        }
        del job_dict['company_id']
        del job_dict['company_name']
        job_dict['company'] = company_dict
        job = job_dict

        # Convert the "Must Have" and "Nice Have" fields to lists
        job['must_have'] = job['must_have'] or []
        job['nice_have'] = job['nice_have'] or []

        cursor.close()

        print(f"Must Have: {job['must_have']}")
        print(f"Nice Have: {job['nice_have']}")

        return render_template('jobs/job_detail.html', job=job)
    else:
        cursor.close()
        return "Job not found", 404

@job_bp.route('/create', methods=['GET', 'POST'])
def create_job():
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Fetch all companies from the database
    cursor.execute("SELECT id, name FROM company")
    companies = cursor.fetchall()

    # Convert the query results to dictionaries
    companies = [dict_from_row(row, cursor) for row in companies]

    if request.method == 'POST':
        # Get form data from the request
        title = request.form['title']
        company_id = request.form['company']
        must_have = request.form.getlist('must_have')  # Get list of must_have values
        nice_have = request.form.getlist('nice_have')  # Get list of nice_have values
        link = request.form['link']

        print("----------------------request.form:")
        print(request.form)
        print("----------------------")

        # Validate and insert the new job into the database
        if title and company_id:
            cursor.execute("INSERT INTO job (title, company_id, must_have, nice_have, link) VALUES (%s, %s, %s, %s, %s)",
                           (title, company_id, must_have, nice_have, link))
            conn.commit()

        cursor.close()

        return redirect(url_for('job.list_jobs'))

    return render_template('jobs/create_job.html', companies=companies)

@job_bp.route('/update/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Fetch all companies from the database
    cursor.execute("SELECT id, name FROM company")
    companies = cursor.fetchall()

    # Convert the query results to dictionaries
    companies = [dict_from_row(row, cursor) for row in companies]

    # Get the job data from the database using job_id
    query = '''SELECT job.id, job.title, company.id AS company_id, company.name AS company_name,
                job.must_have, job.nice_have, job.link, job.applied_date, job.first_contact_date,
                job.last_contact_date, job.status
                FROM job JOIN company ON job.company_id = company.id
                WHERE job.id = %s'''
    cursor.execute(query, (job_id,))
    job_data = cursor.fetchone()

    # Convert the query result to a dictionary
    job_dict = dict_from_row(job_data, cursor)

    company_dict = {
        'id': job_dict['company_id'],
        'name': job_dict['company_name']
    }
    del job_dict['company_id']
    del job_dict['company_name']
    job_dict['company'] = company_dict
    job = job_dict

    if request.method == 'POST':
        # Get form data from the request
        title = request.form['title']
        company_id = request.form['company']  # Changed 'company_id' to 'company'
        must_have = [request.form[f'must_have_{i}'] for i in range(1, 4) if request.form[f'must_have_{i}']]
        nice_have = [request.form[f'nice_have_{i}'] for i in range(1, 4) if request.form[f'nice_have_{i}']]
        link = request.form['link']
        applied_date = request.form['applied_date']
        first_contact_date = request.form['first_contact_date']
        last_contact_date = request.form['last_contact_date']
        status = request.form['status']

        print(f"Form Data: title={title}, company_id={company_id}, must_have={must_have}, nice_have={nice_have}, link={link}")

        # Validate and update the job in the database
        if title and company_id:
            first_contact_date = first_contact_date or None
            last_contact_date = last_contact_date or None

            cursor.execute(
                "UPDATE job SET title = %s, company_id = %s, must_have = %s, nice_have = %s, link = %s, applied_date = %s, first_contact_date = %s, last_contact_date = %s, status = %s WHERE id = %s",
                (title, company_id, must_have, nice_have, link, applied_date, first_contact_date, last_contact_date, status, job_id)
            )
            conn.commit()

        cursor.close()

        print(f"Job Company ID: {job['company']['id']}")  # Access company_id via nested dictionary
        return redirect(url_for('job.list_jobs'))

    return render_template('jobs/update_job.html', job=job, companies=companies)





@job_bp.route('/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Delete the job from the database based on job_id
    cursor.execute("DELETE FROM job WHERE id = %s", (job_id,))
    conn.commit()

    cursor.close()

    return redirect(url_for('job.list_jobs'))
