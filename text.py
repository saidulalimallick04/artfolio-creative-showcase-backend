
def generate_users(count=100):
    users = []
    domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com", "creative.io"]
    
    indian_names = [
        "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
        "Shaurya", "Atharva", "Neel", "Aryan", "Dhruv", "Kabir", "Rohan", "Rahul", "Vikram", "Sanjay",
        "Diya", "Saanvi", "Anya", "Aadhya", "Pari", "Ananya", "Myra", "Riya", "Meera", "Ira",
        "Ishita", "Kavya", "Anika", "Saanvi", "Aditi", "Priya", "Neha", "Sneha", "Pooja", "Anjali",
        "Raj", "Amit", "Suresh", "Ramesh", "Sunil", "Anil", "Deepak", "Vijay", "Manoj", "Ajay"
    ]
    
    prefixes = [
        "Creative", "Artistic", "ColorOf", "Explorer", "DesignBy", "Hello", "TheReal", "Capture", 
        "Mystic", "Vivid", "Urban", "Digital", "Sketch", "Paint", "Draw", "Master", "Pro"
    ]
    
    for i in range(1, count + 1):
        name = random.choice(indian_names)
        
        # Randomly choose a username pattern
        pattern = random.choice(["prefix", "suffix", "both"])
        
        if pattern == "prefix":
            username = f"{random.choice(prefixes)}{name}"
        elif pattern == "suffix":
            suffix = str(random.randint(1, 999))
            username = f"{name}{suffix}"
        else:
            username = f"{random.choice(prefixes)}{name}{random.randint(1, 99)}"
            
        # Ensure email matches username strictly as requested
        domain = random.choice(domains)
        email = f"{username.lower()}@{domain}"
        
        # Generate a random password
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$", k=12))
        
        user = {
            "username": username,
            "email": email,
            "password": password
        }
        users.append(user)
        
    return users

def generate_artworks():
    artworks = [
        {
            "title": "Abstract Harmony",
            "description": "A vibrant explosion of colors representing the chaos and beauty of modern life. Created with acrylics on canvas.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19"
        },
        {
            "title": "Urban Solitude",
            "description": "A high-contrast black and white photograph capturing the quiet moments in a bustling city metropolis.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Digital Dreams",
            "description": "A futuristic cyberpunk landscape rendered in 3D, exploring the intersection of humanity and technology.",
            "image_url": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b"
        },
        {
            "title": "Classic Portrait",
            "description": "An oil painting style digital portrait focusing on emotion and light, reminiscent of the Renaissance era.",
            "image_url": "https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb"
        },
        {
            "title": "Nature's Whisper",
            "description": "A serene landscape of a misty forest at dawn, capturing the peaceful silence of the natural world.",
            "image_url": "https://images.unsplash.com/photo-1547891654-e66ed7ebb968"
        }
    ]
    return artworks