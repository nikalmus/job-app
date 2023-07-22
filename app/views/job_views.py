# app/views/job_views.py

from flask import Blueprint, render_template, request, redirect, url_for, current_app


job_bp = Blueprint('job', __name__, url_prefix='/jobs', template_folder='templates/jobs')


@job_bp.route('/')
def list_jobs():
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Fetch all jobs from the database
    cursor.execute("SELECT * FROM job")
    jobs = cursor.fetchall()

    cursor.close()

    return render_template('jobs/jobs_list.html', jobs=jobs)

@job_bp.route('/create', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        # Get form data from the request
        title = request.form['title']
        company_id = request.form['company_id']
        must_have = request.form.getlist('must_have')
        nice_have = request.form.getlist('nice_have')
        link = request.form['link']

        # Validate and insert the new job into the database
        conn = current_app.config['DB_CONN']
        cursor = conn.cursor()

        # Assuming "title" and "company_id" are required and must not be empty
        if title and company_id:
            cursor.execute(
                "INSERT INTO job (title, company_id, must_have, nice_have, link) VALUES (%s, %s, %s, %s, %s)",
                (title, company_id, must_have, nice_have, link)
            )
            conn.commit()

        cursor.close()

        return redirect(url_for('job.list_jobs'))

    return render_template('jobs/create_job.html')

@job_bp.route('/update/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Fetch the job from the database based on job_id
    cursor.execute("SELECT * FROM job WHERE id = %s", (job_id,))
    job = cursor.fetchone()

    if request.method == 'POST':
        # Get form data from the request
        title = request.form['title']
        company_id = request.form['company_id']
        must_have = request.form.getlist('must_have')
        nice_have = request.form.getlist('nice_have')
        link = request.form['link']

        # Validate and update the job in the database
        if title and company_id:
            cursor.execute(
                "UPDATE job SET title = %s, company_id = %s, must_have = %s, nice_have = %s, link = %s WHERE id = %s",
                (title, company_id, must_have, nice_have, link, job_id)
            )
            conn.commit()

        cursor.close()

        return redirect(url_for('job.list_jobs'))

    return render_template('jobs/update_job.html', job=job)

@job_bp.route('/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    conn = current_app.config['DB_CONN']
    cursor = conn.cursor()

    # Delete the job from the database based on job_id
    cursor.execute("DELETE FROM job WHERE id = %s", (job_id,))
    conn.commit()

    cursor.close()

    return redirect(url_for('job.list_jobs'))
