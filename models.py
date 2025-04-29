from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum,func
from datetime import datetime,timezone
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()
bcrypt=Bcrypt()

#common model for both profiles
class User(db.Model,UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    # user_type = db.Column(Enum('client', 'professional', name='user_type_enum'), nullable=False)
    # is_admin = db.Column(db.Boolean, default=False, nullable=False) 
   
    # Relationships
    professional_profile = db.relationship('ProfessionalProfile', uselist=False, back_populates='user', cascade="all, delete-orphan")
    client_profile = db.relationship('ClientProfile', uselist=False, back_populates='user', single_parent=True, cascade="all, delete-orphan", passive_deletes=True)
    
   
    # Define user types as choices
    CLIENT = 'client'
    PROFESSIONAL = 'professional'
    

    USER_TYPE_CHOICES = [
        (CLIENT, 'Client'),
        (PROFESSIONAL, 'Professional')
        
    ]

     # Set password (hashed)
    def set_password(self, password):
        self.password = generate_password_hash(password)

     # Check password
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

# ClientProfile model
class ClientProfile(User):
    __tablename__ = 'client_profile'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    profile_picture = db.Column(db.String(200), nullable=True, default='default.jpg')
    address = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())
    gender = db.Column(db.String(10), nullable=True)
    
    user = db.relationship('User', back_populates='client_profile',lazy=True,uselist=False)
    reviews_made = db.relationship('Review', back_populates='client_profile')
    
    __mapper_args__ = {
        'polymorphic_identity': 'client',  # Matches the 'client' value in user_type
    }
    def __repr__(self):
        return f'<ClientProfile {self.user.username}>'
    
# Category model
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(120), nullable=True)

    def professional_count(self):
        return len(self.professionals)

# ProfessionalProfile model
class ProfessionalProfile(User):
    __tablename__ = 'professional_profile'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    profile_picture = db.Column(db.String(200), nullable=True, default='default.jpg')
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)  # Total number of reviews received
    profile_completed = db.Column(db.Boolean, default=False, nullable=False)
    availability_status =db.Column(Enum("available", "unavailable", name="availability_status_enum"), default="available", nullable=False)
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship with Category
    category = db.relationship('Category', backref=db.backref('category', lazy='joined'))
    user = db.relationship('User', back_populates='professional_profile', lazy='joined')
    reviews_received = db.relationship('Review', back_populates="professional_profile")
    
    __mapper_args__ = {
        'polymorphic_identity': 'professional'  # Matches the 'professional' value in user_type
    }

    def __repr__(self):
        return f'<ProfessionalProfile {self.user.username}>'

   # Method to calculate the average rating from reviews (dynamic calculation)
   
    @property
    def average_rating(self):
        total_rating = db.session.query(func.sum(Review.rating)).filter(Review.professional_id == self.user_id).scalar() or 0
        total_reviews = db.session.query(func.count(Review.id)).filter(Review.professional_id == self.user_id).scalar() or 0
        
        return total_rating / total_reviews if total_reviews > 0 else 0.0


class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client_profile.user_id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional_profile.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False,index=True)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    message = db.Column(db.Text, nullable=True,default="No message provided")

    # Foreign Key Relationships
    client = db.relationship('ClientProfile', foreign_keys=[client_id], backref='bookings_made', lazy=True)
    professional = db.relationship('ProfessionalProfile', foreign_keys=[professional_id], backref='bookings_received', lazy=True)
    category = db.relationship('Category', backref='bookings')

    def __repr__(self):
        return f'<Booking {self.id} from {self.client_id} to {self.professional_id}>'


class Review(db.Model):
     
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client_profile.user_id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional_profile.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating could be an integer, e.g., 1-5
    review_text = db.Column(db.Text, nullable=False)  # Feedback message from the client
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    client_profile = db.relationship('ClientProfile', back_populates="reviews_made")
    professional_profile = db.relationship('ProfessionalProfile',  back_populates="reviews_received")
   
    def __repr__(self):
        return f"<Review {self.id} by Client {self.client_id} for Professional {self.professional_id}>"


class AdminProfile(User):
    __tablename__ = 'admin_profile'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __repr__(self):
        return f'<AdminProfile {self.user.username}>'
