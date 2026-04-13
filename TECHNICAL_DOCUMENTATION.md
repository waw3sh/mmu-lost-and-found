# MMU Lost & Found - Technical Documentation

## **SYSTEM ARCHITECTURE**

### **Technology Stack**
- **Backend:** Python 3.13 + Django 4.2
- **Database:** PostgreSQL (Render.com)
- **Frontend:** HTML5 + CSS3 + JavaScript (TailwindCSS)
- **SMS API:** Africa's Talking (Sandbox & Production)
- **Deployment:** Render.com
- **Version Control:** Git + GitHub

### **Project Structure**
```
mmu-lost-and-found/
|
|--- accounts/           # User authentication & admin
|--- items/             # Item management & QR codes
|--- claims/            # OTP claim system
|--- reports/           # Finder reporting
|--- notifications/     # SMS & notifications
|--- templates/         # HTML templates
|--- lostfound/        # Django settings
|--- static/           # CSS, JS, images
|--- media/            # User uploads
```

---

## **DATABASE DESIGN**

### **User Model (accounts/models.py)**
```python
class User(AbstractUser):
    ROLE_CHOICES = [('STUDENT', 'Student'), ('STAFF', 'Staff'), ('ADMIN', 'Admin')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    phone = models.CharField(max_length=20, blank=True, null=True)
    student_id = models.CharField(max_length=50, blank=True, null=True)
```

### **Item Model (items/models.py)**
```python
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='active')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    qr_code = models.ImageField(upload_to='qr_codes/')
```

### **Claim Model (claims/models.py)**
```python
class Claim(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    claimant = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=64, blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='PENDING')
    handoff_method = models.CharField(max_length=200, blank=True, null=True)
```

---

## **API INTEGRATION**

### **Africa's Talking SMS Service**
```python
def send_sms(phone_number, message):
    url = "https://api.sandbox.africastalking.com/version1/messaging"
    headers = {
        'apiKey': AT_API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': AT_USERNAME,
        'to': phone_number,
        'message': message
    }
    response = requests.post(url, headers=headers, data=data, verify=False)
    return response.status_code == 200
```

### **Enhanced SMS Features**
- **Item found notifications** with finder contact info
- **OTP verification codes** for claim security
- **Welcome messages** for new users
- **Recovery confirmations** for collected items

---

## **SECURITY IMPLEMENTATION**

### **Authentication & Authorization**
- **Role-based access control** (STUDENT, STAFF, ADMIN)
- **Django's built-in authentication** system
- **CSRF protection** enabled
- **Session management** secure

### **OTP Security**
- **6-digit random codes** (100000-999999)
- **15-minute expiration** window
- **Database validation** with unique constraints
- **One-time use** verification

### **Data Protection**
- **Password hashing** with Django's default
- **SQL injection prevention** via Django ORM
- **XSS protection** in templates
- **Phone number validation** and formatting

---

## **QR CODE SYSTEM**

### **QR Code Generation**
```python
def generate_qr_code(item):
    qr_url = f"https://mmu-lost-and-found.onrender.com/found/{item.uuid}/"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    
    item.qr_code.save(f'qr_{item.uuid}.png', ContentFile(buffer.getvalue()))
```

### **QR Code Features**
- **Unique URLs** for each item
- **Direct claim links** for finders
- **High-quality images** for printing
- **Mobile-friendly** scanning

---

## **ADMIN DASHBOARD**

### **Features**
- **System statistics** (users, items, claims)
- **User management** with role assignment
- **Item tracking** with status updates
- **Claim monitoring** with OTP verification
- **SMS testing** and debugging

### **Security**
- **Admin-only access** with role validation
- **Secure data display** without sensitive info
- **Error handling** with graceful fallbacks
- **Performance optimization** for large datasets

---

## **DEPLOYMENT ARCHITECTURE**

### **Render.com Configuration**
```yaml
services:
  - type: web
    name: mmu-lost-and-found
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn lostfound.wsgi:application
    envVars:
      - key: DATABASE_URL
        value: postgresql://user:pass@host:port/db
      - key: SECRET_KEY
        value: your-secret-key
      - key: AT_API_KEY
        value: your-africa-talking-key
```

### **Environment Variables**
- **DATABASE_URL** - PostgreSQL connection
- **SECRET_KEY** - Django security
- **AT_API_KEY** - Africa's Talking API
- **AT_USERNAME** - SMS service username
- **APP_URL** - Production site URL

---

## **PERFORMANCE OPTIMIZATION**

### **Database Optimization**
- **Indexing** on frequently queried fields
- **Query optimization** with select_related/prefetch_related
- **Connection pooling** via Django settings
- **Caching strategy** for static data

### **API Rate Limiting**
- **SMS throttling** to prevent abuse
- **Request validation** for form submissions
- **Error handling** with retry logic
- **Fallback mechanisms** for network issues

---

## **TESTING STRATEGY**

### **Unit Testing**
- **Model validation** tests
- **View functionality** tests
- **SMS service** tests
- **OTP generation** tests

### **Integration Testing**
- **User registration** flow
- **Item claiming** process
- **SMS delivery** verification
- **Admin dashboard** functionality

### **End-to-End Testing**
- **Complete user journey** tests
- **Mobile responsiveness** tests
- **Browser compatibility** tests
- **Performance benchmarking**

---

## **FUTURE ENHANCEMENTS**

### **Planned Features**
- **Mobile application** (React Native)
- **Push notifications** (Firebase)
- **Advanced analytics** (Google Analytics)
- **Multi-campus support**
- **API documentation** (Swagger)

### **Technical Improvements**
- **Microservices architecture**
- **Redis caching** layer
- **Elasticsearch** for search
- **Docker containerization**
- **CI/CD pipeline** automation

---

## **MAINTENANCE & SUPPORT**

### **Monitoring**
- **Application performance** monitoring
- **Error tracking** (Sentry)
- **Database performance** metrics
- **SMS delivery** statistics

### **Backup Strategy**
- **Database backups** (daily)
- **Media file backups** (weekly)
- **Configuration backups** (version control)
- **Disaster recovery** plan

---

**DOCUMENTATION VERSION:** 1.0  
**LAST UPDATED:** April 13, 2026  
**MAINTAINED BY:** MMU Lost & Found Development Team
