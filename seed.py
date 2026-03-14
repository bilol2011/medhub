from app import create_app, db
from app.models import User, Doctor, Post

app = create_app()

def seed():
    with app.app_context():
        # Clear existing
        db.drop_all()
        db.create_all()

        # Create Doctors
        doctors_data = [
            ('cardio_dr', 'cardio@medhub.com', 'Kardiologiya', 12, 150.0),
            ('dentist_dr', 'dentist@medhub.com', 'Stomatologiya', 8, 80.0),
            ('skin_dr', 'skin@medhub.com', 'Dermatologiya', 5, 120.0),
            ('brain_dr', 'neuro@medhub.com', 'Nevrologiya', 15, 200.0)
        ]

        for username, email, specialty, exp, fee in doctors_data:
            u = User(username=username, email=email, role='doctor')
            u.set_password('password123')
            db.session.add(u)
            db.session.flush()
            
            d = Doctor(user_id=u.id, specialty=specialty, experience=exp, consultation_fee=fee, rating=4.8)
            db.session.add(d)

        # Create an admin user
        admin = User(username='admin', email='admin@medhub.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        # Create a regular user
        u = User(username='patient_demo', email='patient@example.com', role='patient')
        u.set_password('password123')
        db.session.add(u)


        # Create some posts
        posts_data = [
            ('Sog‘lom yurak uchun 5 ta maslahat', 'Yurak salomatligi uzoq umr ko‘rish garovidir. Har kuni jismoniy mashqlar bajaring va ko‘proq ko‘katlar iste’mol qiling.'),
            ('Nima uchun tish gigiyenasi muhim?', 'Kuniga ikki marta tish yuvish nafaqat tishlaringiz, balki umumiy salomatligingiz uchun ham muhimdir.')
        ]

        for title, content in posts_data:
            p = Post(title=title, content=content, author_id=1) # Link to first doctor
            db.session.add(p)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
