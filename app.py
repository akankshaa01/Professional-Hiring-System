from flask import Flask, render_template,redirect, url_for, flash, request,current_app,abort
from config import Config 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import RegistrationForm, LoginForm ,ProfessionalProfileForm ,ClientProfileForm,UpdateBookingForm
from forms import BookingForm, AdminEditUserForm,DeleteUserForm,CreateCategoryForm
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect,validate_csrf, ValidationError, CSRFError, generate_csrf
from werkzeug.exceptions import BadRequest
from models import User,Category, ClientProfile, ProfessionalProfile,Booking
from models import db
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField
from email_validator import validate_email, EmailNotValidError
from db import session
from models import Category
from flask_login import current_user
import os
import secrets
from PIL import Image
from sqlalchemy import desc

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from Config class
print("SECRET_KEY:", app.config['SECRET_KEY']) 
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page when unauthorized

csrf = CSRFProtect(app)  # Enable CSRF protection

# Creating tables in the database
with app.app_context():
    # from models import User, ClientProfile, ProfessionalProfile, Category
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    
    return User.query.get(int(user_id))


@app.route('/')
def home():
    categories = db.session.query(Category).limit(3).all()
    print(categories)
    return render_template ('home.html',categories=categories)

@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    form = UpdateBookingForm()
    total_users = User.query.count()
    total_bookings = Booking.query.count()
    total_categories = Category.query.count()
    categories = Category.query.all()
    users = User.query.order_by(desc(User.id)).all()
    bookings = Booking.query.order_by(desc(Booking.created_at)).all()
    
    if form.validate_on_submit():
        booking = Booking.query.get_or_404(form.booking_id.data)
        booking.status = form.status.data
        db.session.commit()
        flash(f"Booking #{booking.id} status updated to {form.status.data}!", "success")
        print(bookings) 
        return redirect(url_for('admin_dashboard'))  # To prevent form resubmission
   
    return render_template(
        'admin_dashboard.html',
        total_users=total_users,
        total_bookings=total_bookings,
        total_categories=total_categories,
        categories=categories,
        users=users,
        form=form,
        bookings=bookings  
    )


@app.route('/admin/manage_users')
# @admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin_manage_users.html', users=users)

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
# @admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminEditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.user_type = form.user_type.data
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit_user.html', form=form, user=user)

@app.route('/admin/create_user', methods=['GET', 'POST'])
def admin_create_user():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Create user logic
        username = form.username.data
        email = form.email.data
        password = form.password.data
        name = form.name.data
        user_type = form.user_type.data

        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return render_template('admin_create_user.html', form=form)

        # Create the new user
        new_user = User(username=username, email=email, name=name, user_type=user_type)
        new_user.set_password(password)  # Hash the password

        # Add to the database
        db.session.add(new_user)
        db.session.commit()
        flash(f'{user_type.capitalize()} user created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_create_user.html', form=form)

    
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
# @admin_required
def delete_user(user_id):
    form = DeleteUserForm()
    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():
        # Explicitly delete relationships to avoid circular dependency
        if user.professional_profile:
            user.professional_profile.user = None  # Break the relationship manually
            db.session.delete(user.professional_profile)

        if user.client_profile:
            user.client_profile.user = None  # Break the relationship manually
            db.session.delete(user.client_profile)


        db.session.delete(user)
        # Delete the user from the database
        # db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_dashboard.html')


@app.route('/admin/create_category', methods=['GET', 'POST'])
@login_required  # Ensure only authenticated users can access
def admin_create_category():
    form = CreateCategoryForm()
    if form.validate_on_submit():
        # Extract data from the form
        name = form.name.data
        description = form.description.data
        image = form.image.data

        # Check if category already exists
        if Category.query.filter_by(name=name).first():
            flash("Category already exists!", "danger")
            return redirect(url_for('admin_create_category'))

        # Create and save the category
        new_category = Category(name=name, description=description, image=image)
        db.session.add(new_category)
        db.session.commit()

        flash("Category created successfully!", "success")
        return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard or categories page
    
    return render_template('admin_create_category.html', form=form)

@app.route('/user_dashboard', methods=['GET'])
@login_required
def user_dashboard():
    user_profile = None

    if current_user.user_type == 'professional':
        user_profile = ProfessionalProfile.query.filter_by(user_id=current_user.id).first()
    elif current_user.user_type == 'client':
        user_profile = ClientProfile.query.filter_by(user_id=current_user.id).first()

    if not user_profile:
        flash("Profile not found. Please contact support.", "danger")
        return redirect(url_for('home'))  # Redirect to a safe fallback page

    return render_template('user_dashboard.html', user_profile=user_profile, user_type=current_user.user_type)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        try:
            if form.user_type.data == 'professional':
                user = ProfessionalProfile(
                    username=form.username.data,
                    email=form.email.data,
                    name=form.name.data,
                    user_type=form.user_type.data
                )
            elif form.user_type.data == 'client':
                user = ClientProfile(
                    username=form.username.data,
                    email=form.email.data,
                    name=form.name.data,
                    user_type=form.user_type.data
                )
            elif form.user_type.data == 'admin':
                user = User(
                    username=form.username.data,
                    email=form.email.data,
                    name=form.name.data,
                    user_type=form.user_type.data
                )
            else:
                raise ValueError("Invalid user type!")

            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            flash('Account created successfully!', 'success')
            login_user(user)
            return redirect(url_for('home'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)


@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(f"User found: {user.username}, type: {user.user_type}")  
        if user and user.check_password(form.password.data):
            print("Password is correct")
            login_user(user)
            flash('Login successful!', 'success')
            # Redirect based on user type
            if user.user_type == 'client':
                return redirect(url_for('user_dashboard'))
            elif user.user_type == 'professional':
                return redirect(url_for('user_dashboard'))
            elif user.user_type == 'admin':
                return redirect(url_for('admin_dashboard')) 
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/professional_list', methods=['GET','POST'])
def professional_list():
    category_id = request.args.get('category_id', type=int)  # Get category filter from query params
    query = ProfessionalProfile.query
        
    if category_id:  # Apply filter if category_id is provided
        query = query.filter_by(category_id=category_id)

    professionals = query.all()  # Fetch filtered professionals
    categories = db.session.query(Category).all()  # Fetch categories for filter options
    
    return render_template('professional_list.html', professionals=professionals, categories=categories)

@app.route('/professional/<int:professional_id>', methods=['GET'])
def professional_profile(professional_id):
    professional = ProfessionalProfile.query.get_or_404(professional_id)
    return render_template('professional_profile_view.html', professional=professional)


@app.route('/request_booking/<int:professional_id>/')
def request_booking():
    return render_template('bookings.html')


@app.route('/categories')
def categories():
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)


@app.route('/create_booking/<int:professional_id>/<int:category_id>', methods=['GET','POST'])
@login_required
def create_booking(professional_id, category_id):
  
   # Fetch the professional and category from the database
    professional = ProfessionalProfile.query.filter_by(user_id=professional_id).first()
    category = Category.query.get(category_id)

     # Handle the case where professional or category does not exist
    if not professional:
        flash('The professional does not exist.', 'danger')
        return redirect(url_for('professional_list'))
    if not category:
        flash('The category does not exist.', 'danger')
        return redirect(url_for('professional_list'))
    
    # Initialize the form with pre-filled values
    form = BookingForm()
    form.professional_id.data = professional.user_id
    form.category_id.data = category.id
    form.client_id.data = current_user.id  # Pre-fill client ID

    if form.validate_on_submit():
        # Create a new booking object based on form data
        new_booking = Booking(
            client_id=form.client_id.data, 
            professional_id=form.professional_id.data,
            category_id=form.category_id.data,
            scheduled_time=form.scheduled_time.data,
            message=form.message.data
        )

        # Save to the database
        db.session.add(new_booking)
        db.session.commit()
        flash('Booking created successfully!', 'success')
        return redirect(url_for('user_dashboard'))  

    return render_template('create_booking.html', form=form, professional=professional, category=category)


@app.route('/my_booking', methods=['GET', 'POST'])
@login_required
def bookings():
    form = UpdateBookingForm()

    # Check if the form is submitted and is valid
    if form.validate_on_submit():
        booking_id = form.booking_id.data
        print(f"Booking ID: {booking_id}")
        status = form.status.data

        print(f"Booking ID: {booking_id}, Status: {status}")
        # Fetch the booking based on the booking_id
        booking = db.session.get(Booking, booking_id)
        if booking and current_user.id == booking.professional_id:
            print(f"Found booking: {booking}")
           
            booking.status = status
            db.session.commit()
            flash("Booking status updated successfully.", "success")
            return redirect(url_for('bookings'))  # Redirect after form submission

        else:
            flash("Booking not found or unauthorized action.", "danger")
    
    # Fetch bookings based on the user type
    if current_user.user_type == 'client':
        # Get bookings for the client
        bookings = Booking.query.filter_by(client_id=current_user.id).order_by(desc(Booking.created_at)).all()
        user_type = 'client'  # Pass user type to the template
    elif current_user.user_type == 'professional':
        # Get bookings for the professional
        bookings = Booking.query.filter_by(professional_id=current_user.id).order_by(desc(Booking.created_at)).all()
        user_type = 'professional'  # Pass user type to the template
    else:
        bookings = []  # Default empty list if user type is unexpected
        user_type = 'unknown'  # For unexpected user types, just in case

    # Render the bookings template, passing both bookings and user_type
    return render_template('bookings.html', bookings=bookings, form=form, user_type=user_type)

    
@app.route('/update_booking_status/<int:booking_id>', methods=['POST'])
def update_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if current_user.account_type == 'professional':
        booking.status = request.form['status']
        db.session.commit()
        flash('Booking status updated!')
    return render_template('professional_dashboard.html')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Get the current user
    user = current_user

    # Check if user is a client
    if user.user_type == 'client':
        profile = ClientProfile.query.filter_by(user_id=user.id).first()  # Get the client profile
        form = ClientProfileForm(obj=profile)

        # Pre-populate basic fields with the user's data
        form.name.data = user.name
        form.email.data = user.email
        form.username.data = user.username

        # Save the form data if valid
        if form.validate_on_submit():
            print("Form data:", form.data)
            print("Username on form submit:", form.username.data)
            user.name = form.name.data
            user.email = form.email.data
            user.username = form.username.data
           
            
            # Save the client's additional fields (phone_number, address)
            if profile:
                profile.phone_number = form.phone_number.data
                profile.address = form.address.data
                profile.gender = form.gender.data
                profile.date_of_birth = form.date_of_birth.data
                if form.profile_picture.data:
                        picture_file = save_picture(form.profile_picture.data)
                        profile.profile_picture = picture_file
            else:
                new_profile = ClientProfile(user_id=user.id, 
                    phone_number=form.phone_number.data,
                    address=form.address.data,
                    gender=form.gender.data,
                    date_of_birth=form.date_of_birth.data
                    )
                db.session.add(new_profile)

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('edit_profile'))

    # Check if user is a professional
    elif user.user_type == 'professional':
        profile = ProfessionalProfile.query.filter_by(user_id=user.id).first()  # Get the professional profile
        form = ProfessionalProfileForm(obj=profile)

        # Pre-populate basic fields with the user's data
        form.name.data = user.name
        form.email.data = user.email
        form.username.data = user.username

        form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
        # Handle form submission
        if form.validate_on_submit():
            print("Form data:", form.data)

            # Check if username is in the form data
            print("Username on form submit:", form.username.data)

            user.name = form.name.data           
            user.email = form.email.data
            user.username = form.username.data

            # Save the professional's additional fields (bio, experience)
            if profile:
                profile.bio = form.bio.data
                profile.experience = form.experience.data
                profile.availability_status = form.availability_status.data
                profile.category_id = form.category_id.data
                profile.gender = form.gender.data
                profile.date_of_birth = form.date_of_birth.data
                profile.address = form.address.data
                profile.phone_number = form.phone_number.data
                
                if form.profile_picture.data:
                        picture_file = save_picture(form.profile_picture.data)
                        profile.profile_picture = picture_file
            else:
                new_profile = ProfessionalProfile(user_id=user.id, 
                   
                    bio=form.bio.data,
                    experience=form.experience.data,
                    availability_status=form.availability_status.data,
                    category_id=form.category_id.data,
                    gender=form.gender.data,
                    date_of_birth=form.date_of_birth.data,
                    profile_picture=save_picture(form.profile_picture.data) if form.profile_picture.data else None
                    )
                db.session.add(new_profile)

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('edit_profile'))

    return render_template('edit_profile.html', form=form)

def save_picture(form_picture):
    # Generate a random filename to avoid conflicts
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    # Define the path where the picture will be saved
    picture_path = os.path.join(current_app.root_path, 'static/media/profile_pics', picture_fn)

    # Resize the image before saving to save space
    output_size = (300, 300)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn

if __name__ == '__main__':
    app.run(debug=True)
   
