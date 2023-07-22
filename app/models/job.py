class Job:
    def __init__(self, title, company, must_have, nice_have, link, applied_date=None, first_contact_date=None, last_contact_date=None, status='Crickets'):
        self.title = title
        self.company = company
        self.must_have = must_have
        self.nice_have = nice_have
        self.link = link
        self.applied_date = applied_date
        self.first_contact_date = first_contact_date
        self.last_contact_date = last_contact_date
        self.status = status

    def __repr__(self):
        return f"<Job(company='{self.company}', applied_date='{self.company}', status='{self.status}')>"

