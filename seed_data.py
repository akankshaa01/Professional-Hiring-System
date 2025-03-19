from db import session
from models import Category,ProfessionalProfile,User,ClientProfile
from datetime import date
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

"""
new_categories=[

    Category(name="Engineering",description="Ensure your project’s technical strength and structural integrity.",image="media/project_images/engineers_1.jpg"),

    Category(name="Architecture",description="Design blueprints and layouts for structurally sound and beautiful homes.",image="media/project_images/architecture_1.jpg"),

    Category(name="Construction",description="Manage all stages of building your home from the ground up.",image="media/project_images/construction_1.jpg"),

    Category(name="Interior Design",description="Create stylish and functional interiors tailored to your taste.",image="media/project_images/interior_design_1.jpg"),

    Category(name="Real Estate Services",description="Find the perfect location and property for your construction project.",image="media/project_images/real_estate_1.jpg"),

    Category(name="Plumbing",description="Install reliable water systems for kitchens, bathrooms, and more.",image="media/project_images/plumbing_1.jpg"),

    Category(name="Electrical",description="Professional installation and maintenance of electrical systems.",image="media/project_images/electrical_1.webp"),

    Category(name="HVAC services",description="Set up efficient heating, ventilation, and air conditioning systems.",image="media/project_images/HVAC_service_1.jpg"),

    Category(name="Landscaping",description="Enhance outdoor spaces with beautiful garden and landscape designs.",image="media/project_images/Landscaping_1.jpg"),

    Category(name="Painting",description="Add color and protection with professional interior and exterior painting.",image="media/project_images/ painting_1.jpg"),

    Category(name="Flooring",description="Install durable and stylish flooring to complete your interior",image="media/project_images/flooring_1.jpg"),

    Category(name="Roofing",description="Protect your home with sturdy and weather-resistant roofing.",image="media/project_images/roofing.jpg"),

    Category(name="Legal Services",description="Handle legal permits, contracts, and compliance for safe building.",image="media/project_images/legal_services_1.jpg"),

    Category(name="Finance",description="Get financial assistance and budgeting for your project needs",image="media/project_images/finance_service_1.jpg")

]

for category in new_categories:
    if not session.query(Category).filter_by(name=category.name).first():
        session.add(category)

"""


# Professional data
new_professionals = [
    {
        "username": "raj_sharma",
        "email": "raj.sharma@example.com",
        "password": "securepassword",  # Will be hashed
        "name": "Raj Sharma",
        "user_type": "professional",
        "profile_picture": "media/profile_pics/profile_pic_11.jpg",
        "date_of_birth": date(1990, 3, 20),
        "gender": "Male",
        "phone_number": "9876543210",
        "address": "45 MG Road, Bengaluru, Karnataka",
        "category_id": 1,  # Engineering
        "bio": "I am a civil engineer with 9 years of experience specializing in residential construction projects. I focus on the structural integrity and safety of homes, including foundation design, drainage systems, and site planning. I work closely with contractors and homeowners to ensure that every project meets the required safety standards and is completed on schedule, making homes safe and durable.",
        "experience": 9,
        "profile_completed": True,
        "availability_status": "available",
    },
    
    #  {
    #    "username": "Hardik95K",
    #     "email": "hardik95K@gmail.com",
    #     "password": "demopassword",  # This will be hashed before saving
    #     "name": "Hardik Kumar",
    #     "user_type": "professional",
    #     "profile_picture": "media/profile_pics/profile_pic_2.jpg",
    #     "date_of_birth": date(1994, 12, 15),
    #     "gender": "Male",
    #     "phone_number": "9485762528",
    #     "address": "130/2422 Park Street, Kolkata, West Bengal",
    #     "category_id": 3,  #construction
    #     "bio": "I am a civil engineer with 10 years of experience in residential construction projects. I manage the construction of homes from the ground up, ensuring that each project is completed on time and within budget. My focus is on quality craftsmanship, adherence to safety regulations, and delivering homes that stand the test of time.",
    #     "experience": 10,
    #     "profile_completed": True,
    #     "availability_status": "available",
    # },
    # {
    #     "username": "amar_patel",
    #     "email": "amar.patel@example.com",
    #     "password": "demopassword",  
    #     "name": "Amar Patel",
    #     "user_type": "professional",
    #     "profile_picture": "media/profile_pics/profile_pic_7.jpg",
    #     "date_of_birth": date(1988, 5, 10),
    #     "gender": "Male",
    #     "phone_number": "9012345678",
    #     "address": "78 Station Road, Ahmedabad, Gujarat",
    #     "category_id": 5,  # real estate
    #     "bio": "I specialize in real estate services for residential properties. With 12 years of experience in helping clients buy, sell, and rent homes, I provide guidance on market trends, pricing, and neighborhood selections. My goal is to simplify the home-buying and selling process, ensuring a smooth and hassle-free experience for my clients",
    #     "experience": 12,
    #     "profile_completed": True,
    #     "availability_status": "available",
    # },
    
    # {
    #     "username": "nikita_singh",
    #     "email": "NikitaSingh88@gmail.com",
    #     "password": "demopassword",  # Will be hashed
    #     "name": "Nikita Singh",
    #     "user_type": "professional",
    #     "profile_picture": "media/profile_pics/profile_pic_5.jpg",
    #     "date_of_birth": date(1989, 11, 7),
    #     "gender": "Female",
    #     "phone_number": "9063145896",
    #     "address": "12 South Avenue, Chennai, Tamil Nadu",
    #     "category_id": 2,  # architecture
    #     "bio": "I am an architect with 5 years of experience specializing in home renovation and design. I assist homeowners in creating functional and aesthetic living spaces, offering solutions for space optimization, interior layout, and personalized design. Whether it’s a small apartment or a large house, I help bring my clients' visions to life with practical and stylish designs.",
    #     "experience": 5,
    #     "profile_completed": True,
    #     "availability_status": "available",
    # },
    # {
    #  "username": "naira_pathak",
    #     "email": "nairapathak88@gmail.com",
    #     "password": "demopassword",  # Will be hashed
    #     "name": "Naira Pathak",
    #     "user_type": "professional",
    #     "profile_picture": "media/profile_pics/profile_pic_4.jpg",
    #     "date_of_birth": date(1996, 3, 25),
    #     "gender": "Female",
    #     "phone_number": "6325564878",
    #     "address": "78 Lalbagh Road, Lucknow, UP",
    #     "category_id": 13,  # legal
    #     "bio": "I am a legal advisor with 7 years of experience specializing in property law, particularly in matters related to home ownership, rental agreements, and real estate transactions. I help clients with legal issues regarding property disputes, title verification, and drafting contracts to ensure they are legally protected in their home-related matters.",
    #     "experience": 7,
    #     "profile_completed": True,
    #     "availability_status": "available",
    # },

    # {
    #     "username": "ravi_nair",
    #     "email": "ravi.nair@example.com",
    #     "password": "demopassword",  # Will be hashed
    #     "name": "Ravi Nair",
    #     "user_type": "professional",
    #     "profile_picture": "media/profile_pics/profile_pic_6.jpg",
    #     "date_of_birth": date(1985, 12, 1),
    #     "gender": "Male",
    #     "phone_number": "9119876543",
    #     "address": "67 Marine Drive, Mumbai, Maharashtra",
    #     "category_id": 14,  #finance
    #     "bio": "I am a certified financial advisor with 6 years of experience in helping homeowners with budgeting and financing for home improvements and purchases. My expertise includes securing home loans, advising on mortgage options, and assisting clients in managing their finances to make informed decisions about their homes.",
    #     "experience": 6,
    #     "profile_completed": True,
    #     "availability_status": "available",
    # },
    # {
    #     "username": "arun_prakash",
    #     "email": "arun.prakash@example.com",
    #     "password": "securepassword",  # Will be hashed
    #     "name": "Arun Prakash",
    #     "user_type": "professional",
    #     "profile_picture": "media/profile_pics/profile_pic_3.jpg",
    #     "date_of_birth": date(1987, 2, 18),
    #     "gender": "Male",
    #     "phone_number": "9012123456",
    #     "address": "33 Nehru Nagar, Hyderabad, Telangana",
    #     "category_id": 1,  # engineer
    #     "bio": "I am a mechanical engineer with over 8 years of experience in home appliance repairs and installations. My expertise includes fixing air conditioning units, refrigerators, and other major home appliances. I aim to provide prompt, reliable, and high-quality service to homeowners, ensuring their appliances run efficiently and safely.",
    #     "experience": 8,
    #     "profile_completed": True,
    #     "availability_status": "available",
    # },
    # {
    #     "username": "deepa_verma",
    #     "email": "deepa.verma@example.com",
    #     "password": "securepassword",  # Will be hashed
    #     "name": "Deepa Verma",
    #     "user_type": "professional",
    #     "profile_picture": "media/profile_pics/profile_pic_8.jpg",
    #     "date_of_birth": date(1992, 7, 15),
    #     "gender": "Female",
    #     "phone_number": "9871123456",
    #     "address": "14 Lodhi Colony, Delhi",
    #     "category_id": 4, #interior 
    #     "bio": "With 5 years of experience as an interior designer, I specialize in creating personalized living spaces that reflect the personality and style of homeowners. I work with clients to design modern, functional spaces, paying close attention to lighting, furniture layout, and color palettes. My aim is to ensure that every home feels like a warm, welcoming haven, blending beauty and comfort effortlessly.",
    #     "experience": 5,
    #     "profile_completed": True,
    #     "availability_status": "available",
    # },
    
    # {
    #     "username": "suraj_kumar",
    #     "email": "suraj.kumar@example.com",
    #     "password": "demopassword",  # Will be hashed
    #     "name": "Suraj Kumar",
    #     "user_type": "professional",
    #     "profile_picture": "media/profile_pics/profile_pic_10.webp",
    #     "date_of_birth": date(1994, 8, 22),
    #     "gender": "Male",
    #     "phone_number": "9123432121",
    #     "address": "40 Nehru Road, Agra, UP",
    #     "category_id": 8,  # Plumbing
    #     "bio": "I am an experienced plumber with 6 years of service specializing in residential plumbing. Whether it’s fixing leaks, installing water heaters, or conducting routine maintenance, I provide fast, reliable, and affordable plumbing services for homes. My goal is to ensure your plumbing systems are working efficiently and prevent future issues.",
    #     "experience": 6,
    #     "profile_completed": True,
    #     "availability_status": "available",
    # },

    # {
    #     "username": "arav_sen",
    #     "email": "Arav.sen@example.com",
    #     "password": "demopassword",  # Will be hashed
    #     "name": "Arun Sen",
    #     "user_type": "professional",
    #     "profile_picture": "media/profile_pics/profile_pic_9.jpg",
    #     "date_of_birth": date(1993, 4, 25),
    #     "gender": "Male",
    #     "phone_number": "9123456789",
    #     "address": "91 Park Street, Bhopal, MP",
    #     "category_id": 4,  # Interior Design
    #     "bio": "I am a passionate interior designer with 4 years of experience in transforming residential spaces. My focus is on enhancing the functionality and aesthetic of homes, whether through small renovations or full-scale redesigns. I believe in creating designs that are not only visually stunning but also practical, ensuring that each space is optimized for both comfort and usability.",
    #     "experience": 4,
    #     "profile_completed": True,
    #     "availability_status": "available",
    # },
]

# Add professionals only if they don't already exist
try:
    for professional in new_professionals:
        print("Processing Professional Data:", professional)

        # Validate required fields
        missing_fields = [key for key in ["username", "email", "password", "name"] if not professional.get(key)]
        if missing_fields:
            print(f"Skipping due to missing fields: {missing_fields}")
            continue

        # Check if the user already exists
        existing_user = session.query(User).filter_by(username=professional["username"]).first()
        if existing_user:
            print(f"User {professional['username']} already exists. Skipping...")
            continue

        # Create the User
        user = User(
            username=professional["username"],
            email=professional["email"],
            password=generate_password_hash(professional["password"]),
            name=professional["name"],
            user_type="professional"
        )
        session.add(user)
        session.flush()  # Ensure the user ID is generated

        # Create the ProfessionalProfile
        profile = ProfessionalProfile(
            user_id=user.id,
            profile_picture=professional.get("profile_picture", "default.jpg"),
            date_of_birth=professional.get("date_of_birth"),
            gender=professional.get("gender"),
            phone_number=professional.get("phone_number"),
            address=professional.get("address"),
            category_id=professional.get("category_id"),
            bio=professional.get("bio"),
            experience=professional.get("experience"),
            profile_completed=professional.get("profile_completed", False),
            availability_status=professional.get("availability_status", "available"),
        )
        session.add(profile)

    session.commit()
    print("Data inserted successfully!")
except Exception as e:
    session.rollback()
    print("Error inserting data:", str(e))
finally:
    session.close()