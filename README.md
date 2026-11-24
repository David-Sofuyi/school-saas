# Nigerian School Management SaaS (EduNaija)

A comprehensive, multi-tenant school management web application and progressive web app (PWA) engineered specifically for Nigerian primary and secondary schools.

---

## 🚀 Key Highlights & PRD Compliance

1. **Multi-Tenancy & Data Isolation**
   - Unique tenant identity per registered school.
   - Database queries strictly scoped via `TenantModel` and `TenantQuerySetMixin`.
   - Parent access restricted strictly to linked children within the school tenant.

2. **Compulsory 40/60 Assessment & Grading System**
   - Compulsory split: **40 marks Continuous Assessment (CA)** + **60 marks Examination** (100 total).
   - Fully customizable CA breakdown components (Class tests, Assignments, Projects) summing to 40.
   - Result approval workflow: Teacher Entry &rarr; Principal Review & Approval &rarr; Published & Locked.
   - Automated terminal report card generation.

3. **Termly Fee Management & Bursar Verification (₦)**
   - Termly fee schedules by class level and section.
   - Individual student fee adjustments: Scholarships, special discounts, waivers, and extra charges.
   - Parents upload bank transfer/teller evidence (`PaymentEvidence`).
   - Bursar checks uploaded proof against bank statements before payment approval and receipt generation.

4. **Attendance Management with Africa/Lagos Scheduling**
   - Daily student attendance by class arm.
   - Automatic 8:30 AM WAT roll call reminder to teachers on school days (excluding holidays & closures).
   - 9:00 AM WAT student absence alert to class teacher, proprietor, and platform superuser.
   - Teacher self check-in/out with immutable timestamps and principal verification dashboard.

5. **Academic Calendar & Document Uploads**
   - Central Nigerian public holiday management maintained centrally by superuser.
   - School-specific breaks: Mid-term, term vacations, Christmas, Easter, Long vacation.
   - Official academic calendar document uploads (PDF, DOCX, XLSX, JPG, PNG) with full version history and no silent overwrites.

6. **Interactive Landing Page & Role-Specific Portals**
   - Brand-new marketing landing page showcasing features, pricing tiers, and direct portal access.
   - Tailored dashboards for:
     - **Superuser**: Platform-wide school registry and subscription monitoring.
     - **Proprietor & Admin**: Complete school governance, settings, fee billing, and analytics.
     - **Principal**: Result approvals, academic supervision, teacher attendance verification.
     - **Teacher**: Roll-call, CA score entry, timetable schedules.
     - **Bursar**: Bank accounts, payment verification, student receipts, fee reports.
     - **Parent**: Children performance tracking, fee invoices, teller upload, receipts.
     - **Student**: Terminal results, timetable, academic calendar, notices.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11+ / Django 5.x / Django REST Framework
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: Django Templates, Bootstrap 5.3, Bootstrap Icons, JavaScript
- **Background Tasks**: Celery & Redis (Timezone: `Africa/Lagos`)
- **Package & Environment Manager**: `uv` / `pip`

---

## 💻 Quickstart & Setup

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/David-Sofuyi/school-saas.git
cd school-saas
uv venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
uv pip install -r requirements/base.txt
```

### 3. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

Open **`http://127.0.0.1:8000/`** in your browser to view the **Landing Page**.

---

## 🔑 Default Credentials (Development)

- **Superuser**: `admin@edunaija.com`
- **Password**: `adminpassword123`
- **Sample School**: Grace High School, Ikeja, Lagos
