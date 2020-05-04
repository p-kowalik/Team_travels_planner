# Team_travels_planner
http://pawelkowalik.pythonanywhere.com/index/
(login required to dig into options. Let me know if any interest so I will provide you with access for testing.)

Web application supporting work of travel
coordinator who's in charge of company business travels. Company sends
monthly a hundreds of employees to destinations around the world.
Main goal was to provide a tool to anticipate the upcoming travels and
follow up booking and reservations requires to travel.
It is a calendar events / data base driven app with access control for
various groups of users. It sends automatic, requests to employees for
obtaining their approvals and comments, financial and operational
summaries to supervisors.
Technologies: Python, Django, Postgres, Bootstrap, HTML, CSS, Cron

Steps after installation:
 - create .env (see .env_example attched for reference)
 - create django superuser to be able to login with its credentials
 - populate db with some data using command: populate_blank_DB
 - configure email sender parameters in settings.py - you may need to allow access
  to less secure apps in your email account (at least if you use google)
 - if you wish to receive notifications modify user email (by default it will be faker generated address)
- employees are not assigned to users accounts by default - you can do it by creating user account and assigning
  to particular employee id (see Manage employees section). Users created here are limited access users (make sure
  they have no staff, no superusers permissions). After logging in they will be redirected to employees section, to their accounts.