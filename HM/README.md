# 🏥 MediCare Hospital Management System

A full-featured Hospital Management System built with **Django**, **Jinja2**, **Bootstrap 5**, **jQuery**, **PostgreSQL** — deployable to **Railway** or **Render**.

---

## 📁 Project Structure

```
hospital_management/
├── hospital_management/        # Django project config
│   ├── settings.py             # Main settings (env-based)
│   ├── urls.py                 # Root URL config
│   ├── wsgi.py                 # WSGI entry point
│   ├── celery.py               # Celery config
│   └── jinja2.py               # Jinja2 environment
│
├── apps/                       # All Django apps
│   ├── accounts/               # Auth, users, roles
│   ├── patients/               # Patient records, vitals, medical history
│   ├── doctors/                # Doctors, departments, schedules
│   ├── appointments/           # Booking, scheduling, status
│   ├── billing/                # Invoices, payments
│   ├── pharmacy/               # Medicines, prescriptions
│   ├── lab/                    # Lab tests, orders, results
│   └── dashboard/              # Dashboard, analytics, API
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Master layout with sidebar
│   ├── accounts/
│   ├── patients/
│   ├── doctors/
│   ├── appointments/
│   ├── billing/
│   ├── pharmacy/
│   ├── lab/
│   └── dashboard/
│
├── static/
│   ├── css/main.css            # Custom CSS (variables, components)
│   ├── js/main.js              # jQuery + vanilla JS
│   └── images/
│
├── Procfile                    # Railway/Render process definitions
├── railway.toml                # Railway config
├── nixpacks.toml               # Build config
├── runtime.txt                 # Python version
├── requirements.txt            # All dependencies
└── .env.example                # Environment variables template
```

---

## 🧩 Modules

| Module | Features |
|---|---|
| **Patients** | Registration, profiles, medical records, vitals, history |
| **Doctors** | Profiles, departments, specializations, schedules |
| **Appointments** | Booking, calendar, status tracking, reminders |
| **Billing** | Invoices, payments, reports, PDF generation |
| **Pharmacy** | Medicine inventory, prescriptions, low-stock alerts |
| **Laboratory** | Test catalog, orders, results management |
| **Dashboard** | Analytics, charts, real-time stats |
| **Accounts** | Multi-role auth (Admin, Doctor, Nurse, Receptionist, etc.) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2 |
| Templates | Jinja2 |
| Frontend | HTML5, CSS3, Bootstrap 5, jQuery 3.7 |
| Charts | Chart.js 4 |
| Database | PostgreSQL (SQLite for dev) |
| Task Queue | Celery + Redis |
| Email | SendGrid |
| File Storage | Local / Cloudinary / S3 |
| Deployment | Railway / Render |

---

## ⚡ Local Setup

### 1. Clone and create virtual environment
```bash
git clone https://github.com/yourname/hospital-management.git
cd hospital_management
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your values
```

### 4. Run migrations and create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### 5. Start development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🚀 Railway Deployment (Step-by-Step)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - MediCare HMS"
git remote add origin https://github.com/yourname/hospital-management.git
git push -u origin main
```

### Step 2: Create Railway Project
1. Go to https://railway.app
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Choose your repository

### Step 3: Add PostgreSQL Database
1. In your Railway project, click **+ New**
2. Select **Database → PostgreSQL**
3. Railway auto-sets `DATABASE_URL` in your environment

### Step 4: Add Redis (for Celery)
1. Click **+ New** → **Database → Redis**
2. Railway auto-sets `REDIS_URL`

### Step 5: Set Environment Variables
In Railway → Your Service → Variables, add:

```
SECRET_KEY=your-super-secret-key-50-chars-minimum
DEBUG=False
ALLOWED_HOSTS=yourapp.railway.app
DATABASE_URL=(auto-set by Railway)
REDIS_URL=(auto-set by Railway)
HOSPITAL_NAME=Your Hospital Name
```

### Step 6: Deploy
Railway auto-deploys on every push to main. Your app will be live at:
`https://yourapp.railway.app`

### Step 7: Run migrations on Railway
In Railway terminal or CLI:
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

---

## 🌐 Render Deployment

### 1. Create Web Service
- Connect GitHub repo
- Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start Command: `gunicorn hospital_management.wsgi:application`

### 2. Add PostgreSQL
- Create a new PostgreSQL instance in Render
- Copy `DATABASE_URL` to environment variables

### 3. Environment Variables (same as Railway above)

---

## 👥 User Roles

| Role | Access |
|---|---|
| **Admin** | Full access to everything |
| **Doctor** | Patients, appointments, medical records |
| **Nurse** | Patient vitals, basic records |
| **Receptionist** | Appointments, patient registration |
| **Pharmacist** | Pharmacy, prescriptions |
| **Lab Technician** | Lab orders and results |
| **Accountant** | Billing and invoices |

---

## 🔑 Default Admin Access
After running `createsuperuser`:
- URL: `/admin/`
- Set role to `admin` in User model

---

## 📊 API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/stats/` | Real-time dashboard stats (JSON) |

---

## 🔧 Extending the Project

### Add SMS notifications
```bash
pip install twilio
```
Add Twilio credentials to `.env` and create a notification service.

### Add Stripe payments
```bash
pip install stripe
```
Integrate in billing app views.

### Add AI features
```bash
pip install openai
```
Use in lab results analysis or patient symptom checker.

### Enable file uploads to Cloudinary
```bash
pip install cloudinary django-cloudinary-storage
```
Add `CLOUDINARY_URL` to `.env`.

---

## 🗄️ Database Schema (Key Models)

```
User ──────────────────── Doctor ──── Department
  │                          │           │
  │                          │           │
Patient ─── MedicalRecord    │        DoctorSchedule
  │              │           │
  │              └───── Appointment ─── Invoice ─── InvoiceItem
  │                          │
  ├── VitalSign              │
  ├── LabOrder ─── LabResult │
  └── Prescription ─── PrescriptionItem
            │
          Medicine ─── MedicineCategory
```

---

## 📦 Key Dependencies

```
Django==4.2.7              # Web framework
psycopg2-binary==2.9.9     # PostgreSQL adapter
gunicorn==21.2.0           # WSGI server
whitenoise==6.6.0          # Static file serving
celery==5.3.4              # Async task queue
redis==5.0.1               # Cache & message broker
reportlab==4.0.7           # PDF generation
dj-database-url==2.1.0     # Database URL parsing
python-decouple==3.8       # Environment variables
```

---

## 🐛 Troubleshooting

**Static files not loading on production?**
```bash
python manage.py collectstatic --noinput
# Make sure STATIC_ROOT is set and whitenoise is in MIDDLEWARE
```

**Database migrations failing?**
```bash
python manage.py showmigrations
python manage.py migrate --run-syncdb
```

**Celery not working?**
```bash
# Make sure Redis is running
redis-cli ping  # Should return PONG
celery -A hospital_management worker --loglevel=debug
```
