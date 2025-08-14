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
        if not job_ids:
            print("No jobs found. Check if hr.job records exist and match the domain filter.")

        jobs_data = models.execute_kw(db, uid, password, 'hr.job', 'read', 
            [job_ids, ['id', 'name', 'description', 'career_level', 'cgpa_requirement', 'deadline', 'company_id']])
        
        jobs = []
        for job in jobs_data:
            try:
                job_entry = {
                    'id': job['id'],
                    'name': job['name'],
                    'job_title': job['name'],
                    'job_description': job.get('description', '') or '',
                    'career_level': job.get('career_level', 'Not Specified') or 'Not Specified',
                    'cgpa_requirement': job.get('cgpa_requirement', 0.0) or 0.0,
                    'date_to': job.get('deadline', '') or '',
                    'company_id': job.get('company_id', False),
                    'address_id': False,
                    'department_id': False,
                    'recruitment_request_id': False
                }
                jobs.append(job_entry)
                print(f"Processed job ID {job['id']}: {job['name']}, Deadline: {job.get('deadline', '')}, Company ID: {job.get('company_id')}")
            except Exception as e:
                print(f"Skipping job ID {job.get('id', 'unknown')}: {str(e)}")
                continue

        print(f"Processed jobs: {jobs}")
        return jobs
    except Exception as e:
        print(f"Error fetching jobs from Odoo: {str(e)}")
        return []

def create_odoo_application(vals):
    try:
        models, db, uid, password = get_odoo_connection()
        
        # Check hr.candidate fields for debugging
        candidate_fields = models.execute_kw(db, uid, password, 'ir.model.fields', 'search_read',
                                            [[('model', '=', 'hr.candidate')]], {'fields': ['name', 'ttype', 'required']})
        print(f"hr.candidate fields: {candidate_fields}")
        required_fields = [f['name'] for f in candidate_fields if f['required']]
        print(f"Required hr.candidate fields: {required_fields}")

        # Create res.partner record
        partner_data = {
            'name': vals['partner_name'],
            'email': vals.get('email_from', ''),
            'phone': vals.get('partner_phone', ''),
            'company_id': vals.get('company_id', False),
        }
        partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [partner_data])
        print(f"Created partner ID: {partner_id}")
        vals['partner_id'] = partner_id

        # Create hr.candidate record
        candidate_data = {
            'partner_name': vals['partner_name'],  # Use partner_name instead of name
            'email_from': vals.get('email_from', ''),
            'partner_phone': vals.get('partner_phone', ''),
            'company_id': vals.get('company_id', False),
            'partner_id': partner_id,
        }
        # Include required fields if missing
        for field in required_fields:
            if field not in candidate_data:
                if field in ['partner_name', 'email_from', 'partner_phone', 'company_id', 'partner_id']:
                    continue  # Already set
                candidate_data[field] = False  # Default for unknown fields
        print(f"Creating hr.candidate with data: {candidate_data}")
        candidate_id = models.execute_kw(db, uid, password, 'hr.candidate', 'create', [candidate_data])
        print(f"Created candidate ID: {candidate_id}")
        vals['candidate_id'] = candidate_id

        # Handle CV attachment
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
        
        # Set initial stage
        initial_stage = models.execute_kw(db, uid, password, 'hr.recruitment.stage', 'search',
                                         [[('name', '=', 'Initial Qualification')]], {'limit': 1})
        if initial_stage:
            vals['stage_id'] = initial_stage[0]
        else:
            print("Warning: Initial Qualification stage not found. Application will be created without stage.")

        # Remove invalid fields
        if 'company_id' in vals and not vals['company_id']:
            print(f"Removing invalid company_id from vals: {vals['company_id']}")
            del vals['company_id']
        if 'department_id' in vals:
            del vals['department_id']

        print(f"Creating hr.applicant with vals: {vals}")
        applicant_id = models.execute_kw(db, uid, password, 'hr.applicant', 'create', [vals])
        print(f"Created applicant ID: {applicant_id}")
        return applicant_id
    except xmlrpc.client.Fault as e:
        print(f"Odoo XML-RPC Fault: Code: {e.faultCode}, String: {e.faultString}")
        raise Exception(f"Odoo error: {e.faultString}")
    except Exception as e:
        print(f"Error creating application in Odoo: {str(e)}")
        raise