import xmlrpc.client
from decouple import config


def get_odoo_connection():
    ODOO_URL = config('ODOO_URL', default='http://172.10.12.208:3334/')
    ODOO_DB = config('ODOO_DB', default='otech_testing')
    ODOO_USERNAME = config('ODOO_USERNAME', default='admin')
    ODOO_PASSWORD = config('ODOO_PASSWORD', default='admin')

    try:
        common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        version = common.version()
        print(f"Odoo Version: {version}")
        if not version:
            raise Exception("Failed to connect to Odoo server.")
        uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
        print(f"Authenticated with UID: {uid}")
        if not uid:
            raise Exception("Odoo authentication failed. Check database, username, or password.")
        models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
        return models, ODOO_DB, uid, ODOO_PASSWORD
    except ConnectionRefusedError:
        raise Exception(f"Connection refused to {ODOO_URL}. Ensure Odoo server is running on port 3334.")
    except Exception as e:
        raise Exception(f"Error connecting to Odoo: {str(e)}")


def fetch_odoo_jobs(search=None, offset=0, limit=12):
    try:
        models, db, uid, password = get_odoo_connection()
        domain = [('is_published', '=', True), ('website_published', '=', True)]
        if search:
            domain.append(('name', 'ilike', search))
        print(f"Fetching jobs with domain: {domain}")
        job_ids = models.execute_kw(db, uid, password, 'hr.job', 'search', [domain], {
            'offset': offset,
            'limit': limit
        })
        print(f"Found job IDs: {job_ids}")

        jobs = []
        for job_id in job_ids:
            try:
                # Include additional fields: description, career_level, cgpa_requirement
                job = models.execute_kw(db, uid, password, 'hr.job', 'read', 
                    [[job_id], ['id', 'name', 'description', 'career_level', 'cgpa_requirement']])[0]
                print(f"Fetched job ID {job_id}: {job}")
                jobs.append({
                    'id': job['id'],
                    'name': job['name'],
                    'job_description': job.get('description', '') or '',  # Use description or empty string
                    'career_level': job.get('career_level', 'Not Specified') or 'Not Specified',
                    'cgpa_requirement': job.get('cgpa_requirement', 0.0) or 0.0,
                    'date_to': '',
                    'company_id': False,
                    'address_id': False,
                    'department_id': False,
                    'recruitment_request_id': False
                })
            except Exception as e:
                print(f"Skipping job ID {job_id}: {str(e)}")
                continue

        print(f"Processed jobs: {jobs}")
        return jobs
    except Exception as e:
        print(f"Error fetching jobs from Odoo: {str(e)}")
        return []


def create_odoo_application(vals):
    try:
        models, db, uid, password = get_odoo_connection()
        attachment = None
        if 'cv_data' in vals:
            attachment = {
                'name': vals['cv_filename'],
                'datas': vals['cv_data'],
                'res_model': 'hr.applicant',
                'res_id': 0,
                'public': True
            }
            attachment_id = models.execute_kw(db, uid, password, 'ir.attachment', 'create', [attachment])
            vals['attachment_ids'] = [(4, attachment_id)]
            del vals['cv_data'], vals['cv_filename']
        initial_stage = models.execute_kw(db, uid, password, 'hr.recruitment.stage', 'search',
                                         [[('name', '=', 'Initial Qualification')]], {'limit': 1})
        if initial_stage:
            vals['stage_id'] = initial_stage[0]

        applicant_id = models.execute_kw(db, uid, password, 'hr.applicant', 'create', [vals])
        print(f"Created applicant ID: {applicant_id}")
        return applicant_id
    except Exception as e:
        print(f"Error creating application in Odoo: {str(e)}")
        raise