import asyncio
import random
import string
import sys
import os
from typing import List

# Add parent directory to path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from models.user import User
from models.artwork import Artwork
from core.security import get_password_hash

# --- Generation Logic from text.py ---

def generate_users(count=100) -> List[dict]:
    users = []
    domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com", "creative.io"]
    
    indian_names = list(set([
        "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
        "Shaurya", "Atharva", "Neel", "Aryan", "Dhruv", "Kabir", "Rohan", "Rahul", "Vikram", "Sanjay",
        "Diya", "Saanvi", "Anya", "Aadhya", "Pari", "Ananya", "Myra", "Riya", "Meera", "Ira",
        "Ishita", "Kavya", "Anika", "Aditi", "Priya", "Neha", "Sneha", "Pooja", "Anjali",
        "Raj", "Amit", "Suresh", "Ramesh", "Sunil", "Anil", "Deepak", "Vijay", "Manoj", "Ajay"
    ]))
    
    prefixes = [
        "Creative", "Artistic", "ColorOf", "Explorer", "DesignBy", "Hello", "TheReal", "Capture", 
        "Mystic", "Vivid", "Urban", "Digital", "Sketch", "Paint", "Draw", "Master", "Pro"
    ]
    
    seen_usernames = set()
    while len(users) < count:
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
            
        if username in seen_usernames:
            continue
            
        seen_usernames.add(username)
            
        # Ensure email matches username strictly as requested
        domain = random.choice(domains)
        email = f"{username.lower()}@{domain}"
        
        # Generator random password
        password = "password123"
        
        user = {
            "username": username,
            "email": email,
            "password": password
        }
        users.append(user)
        
    return users

def generate_artworks(count=500):
    templates = [
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
        },
        {
            "title": "Geometric Fusion",
            "description": "Bold geometric shapes intersect in a minimalist composition exploring balance and spatial relationships.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Ocean's Embrace",
            "description": "A sweeping seascape capturing the raw power and tranquility of ocean waves meeting the shore.",
            "image_url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0"
        },
        {
            "title": "Neon Nights",
            "description": "A contemporary street art piece featuring vibrant neon colors and urban graffiti aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Ethereal Bloom",
            "description": "Delicate watercolor florals floating in soft pastel hues, evoking a dreamlike spring garden.",
            "image_url": "https://images.unsplash.com/photo-1490750967868-88aa4486c946"
        },
        {
            "title": "Industrial Symphony",
            "description": "A photographic exploration of abandoned factories, showcasing the beauty in decay and rust.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Celestial Dance",
            "description": "A cosmic artwork depicting swirling galaxies and nebulae in deep purples and blues.",
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a"
        },
        {
            "title": "Vintage Memories",
            "description": "A nostalgic collage combining old photographs, stamps, and ephemera from the early 20th century.",
            "image_url": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b"
        },
        {
            "title": "Minimalist Zen",
            "description": "A simple composition of stones and sand arranged in meditative patterns, inspired by Japanese gardens.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Surreal Escape",
            "description": "A dreamlike digital manipulation blending reality and fantasy with floating islands and impossible architecture.",
            "image_url": "https://images.unsplash.com/photo-1518640467707-6811f4a6ab73"
        },
        {
            "title": "Textured Layers",
            "description": "An abstract mixed media piece featuring thick impasto techniques and layered materials creating depth.",
            "image_url": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5"
        },
        {
            "title": "Cultural Tapestry",
            "description": "A vibrant textile artwork incorporating traditional patterns and motifs from various global cultures.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Motion Blur",
            "description": "A dynamic photograph capturing movement and energy through intentional blur and long exposure.",
            "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa"
        },
        {
            "title": "Botanical Study",
            "description": "A detailed scientific illustration of rare plant specimens rendered in precise ink and watercolor.",
            "image_url": "https://images.unsplash.com/photo-1466781783364-36c955e42a7f"
        },
        {
            "title": "Chromatic Waves",
            "description": "Flowing gradients of color transitioning smoothly across the canvas like liquid light.",
            "image_url": "https://images.unsplash.com/photo-1507908708918-778587c9e563"
        },
        {
            "title": "Arctic Silence",
            "description": "A stark winter landscape painted in cool whites and blues, conveying isolation and purity.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Jazz Improvisation",
            "description": "An energetic abstract expressionist piece capturing the rhythm and spontaneity of jazz music.",
            "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4"
        },
        {
            "title": "Desert Mirage",
            "description": "A sun-baked landscape of sand dunes and heat waves, exploring themes of survival and beauty.",
            "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35"
        },
        {
            "title": "Pop Art Revival",
            "description": "A bold composition using halftone dots and bright colors in homage to 1960s pop art movement.",
            "image_url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062"
        },
        {
            "title": "Reflection Pool",
            "description": "A serene photograph of still water creating perfect mirror reflections of surrounding trees.",
            "image_url": "https://images.unsplash.com/photo-1433086966358-54859d0ed716"
        },
        {
            "title": "Steampunk Machinery",
            "description": "An intricate illustration of Victorian-era inspired mechanical contraptions with gears and brass.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Monochrome Emotion",
            "description": "A powerful black and white portrait study focusing on raw human emotion and vulnerability.",
            "image_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330"
        },
        {
            "title": "Fractal Universe",
            "description": "A computer-generated artwork exploring infinite patterns and mathematical beauty in nature.",
            "image_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564"
        },
        {
            "title": "Autumn Palette",
            "description": "A warm landscape painting celebrating the golden and crimson hues of fall foliage.",
            "image_url": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97"
        },
        {
            "title": "Street Performance",
            "description": "A candid documentary photograph capturing the energy and passion of urban street performers.",
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"
        },
        {
            "title": "Marble Dreams",
            "description": "An elegant abstract piece mimicking the flowing patterns and colors of natural marble stone.",
            "image_url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85"
        },
        {
            "title": "Skyline Silhouette",
            "description": "A dramatic sunset photograph with city buildings creating stark silhouettes against vibrant sky.",
            "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000"
        },
        {
            "title": "Origami Dreams",
            "description": "A photographic series showcasing the delicate art of Japanese paper folding in creative compositions.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Grunge Texture",
            "description": "A layered mixed media artwork incorporating distressed surfaces, stains, and weathered materials.",
            "image_url": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3"
        },
        {
            "title": "Liquid Gold",
            "description": "An abstract pour painting technique creating organic forms with metallic gold and deep blacks.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Mountain Majesty",
            "description": "A grand landscape painting of snow-capped peaks rising dramatically above forested valleys.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Digital Glitch",
            "description": "A contemporary artwork exploring technology errors and digital artifacts as aesthetic elements.",
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f"
        },
        {
            "title": "Impressionist Garden",
            "description": "A soft-focus painting of flowers and light inspired by Monet's garden at Giverny.",
            "image_url": "https://images.unsplash.com/photo-1490750967868-88aa4486c946"
        },
        {
            "title": "Concrete Jungle",
            "description": "An urban photography series documenting the raw architectural forms of modern cities.",
            "image_url": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b"
        },
        {
            "title": "Watercolor Sky",
            "description": "A delicate painting capturing the ethereal quality of clouds at sunset using transparent layers.",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        },
        {
            "title": "Tribal Patterns",
            "description": "A geometric artwork inspired by indigenous art forms featuring bold lines and symbolic shapes.",
            "image_url": "https://images.unsplash.com/photo-1482800304058-6e50b7b78103"
        },
        {
            "title": "Candlelight Vigil",
            "description": "A dramatic chiaroscuro painting using strong contrasts between light and shadow.",
            "image_url": "https://images.unsplash.com/photo-1516450137517-162bfbeb8dba"
        },
        {
            "title": "Mosaic Vision",
            "description": "A colorful artwork composed of thousands of tiny tiles creating a larger unified image.",
            "image_url": "https://images.unsplash.com/photo-1482784160316-6eb046863ece"
        },
        {
            "title": "Foggy Harbor",
            "description": "A mysterious photograph of boats emerging from morning mist in a quiet coastal harbor.",
            "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
        },
        {
            "title": "Kaleidoscope Mind",
            "description": "A symmetrical mandala design bursting with intricate patterns and vibrant rainbow colors.",
            "image_url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0"
        },
        {
            "title": "Rustic Charm",
            "description": "A still life painting of weathered farm tools and aged wood celebrating rural simplicity.",
            "image_url": "https://images.unsplash.com/photo-1500964757637-c85e8a162699"
        },
        {
            "title": "Neon Samurai",
            "description": "A cyberpunk illustration blending traditional Japanese warrior aesthetics with futuristic elements.",
            "image_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853"
        },
        {
            "title": "Cave Paintings",
            "description": "A primitive art inspired work using earth pigments to recreate ancient storytelling methods.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Crystal Formations",
            "description": "A macro photograph revealing the geometric perfection and colors within natural mineral crystals.",
            "image_url": "https://images.unsplash.com/photo-1518331647614-7a1f04cd34cf"
        },
        {
            "title": "Expressionist Fury",
            "description": "A bold painting with aggressive brushstrokes conveying intense emotional energy and movement.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Pastel Morning",
            "description": "A gentle landscape rendered in soft pinks, lavenders, and pale blues evoking peaceful dawn.",
            "image_url": "https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9"
        },
        {
            "title": "Metal Sculpture",
            "description": "A contemporary three-dimensional artwork crafted from welded steel and industrial materials.",
            "image_url": "https://images.unsplash.com/photo-1544967082-d9d25d867d66"
        },
        {
            "title": "Vintage Cinema",
            "description": "A nostalgic illustration capturing the golden age of Hollywood with art deco styling.",
            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728"
        },
        {
            "title": "Coral Reef",
            "description": "An underwater photography series showcasing the vibrant biodiversity of tropical marine ecosystems.",
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19"
        },
        {
            "title": "Ink Wash",
            "description": "A traditional East Asian brush painting using varying tones of black ink on rice paper.",
            "image_url": "https://images.unsplash.com/photo-1523554888454-84137e72c3ce"
        },
        {
            "title": "Stained Glass",
            "description": "A digital artwork emulating the luminous quality and religious symbolism of cathedral windows.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Prairie Winds",
            "description": "An expansive landscape painting of endless grasslands under dramatic cloud formations.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Graffiti Soul",
            "description": "A vibrant street art mural featuring bold letters, characters, and social commentary.",
            "image_url": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Holographic Future",
            "description": "A futuristic digital artwork exploring iridescent surfaces and augmented reality aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Pottery Wheel",
            "description": "A photographic study of ceramic artistry capturing hands shaping clay on a spinning wheel.",
            "image_url": "https://images.unsplash.com/photo-1493106819501-66d381c466f1"
        },
        {
            "title": "Starry Expanse",
            "description": "A night sky photograph revealing the Milky Way galaxy stretching across the darkness.",
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a"
        },
        {
            "title": "Paper Collage",
            "description": "A mixed media composition combining torn magazines, newspapers, and textured papers.",
            "image_url": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b"
        },
        {
            "title": "Tropical Paradise",
            "description": "A vibrant painting of lush jungle foliage and exotic birds in saturated greens and reds.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Art Nouveau",
            "description": "An elegant illustration featuring flowing organic lines and decorative floral motifs.",
            "image_url": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5"
        },
        {
            "title": "Storm Brewing",
            "description": "A dramatic seascape capturing dark clouds and turbulent waves before a tempest.",
            "image_url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0"
        },
        {
            "title": "Minimalist Lines",
            "description": "A simple geometric composition using only black lines on white exploring negative space.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Carnival Colors",
            "description": "A festive artwork bursting with the energy and vibrant hues of celebration and joy.",
            "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30"
        },
        {
            "title": "Ancient Ruins",
            "description": "A detailed architectural drawing of classical columns and weathered stone structures.",
            "image_url": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd"
        },
        {
            "title": "Quantum Field",
            "description": "An abstract scientific visualization representing subatomic particles and energy waves.",
            "image_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564"
        },
        {
            "title": "Gothic Architecture",
            "description": "A dramatic photograph of towering cathedral spires and intricate stone carvings.",
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"
        },
        {
            "title": "Silk Road",
            "description": "A textile artwork incorporating traditional weaving techniques and ancient trade route patterns.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Brushstroke Energy",
            "description": "An action painting showcasing dynamic gestural marks and spontaneous artistic expression.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Winter Frost",
            "description": "A delicate macro photograph of ice crystals forming intricate patterns on glass.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Urban Decay",
            "description": "A photographic exploration of abandoned buildings and the beauty of deterioration.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Waterfall Mist",
            "description": "A long-exposure photograph creating silky smooth water flows in a forest setting.",
            "image_url": "https://images.unsplash.com/photo-1433086966358-54859d0ed716"
        },
        {
            "title": "Pop Portrait",
            "description": "A contemporary portrait using bold flat colors and simplified forms in pop art style.",
            "image_url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062"
        },
        {
            "title": "Desert Bloom",
            "description": "A painting celebrating the rare and beautiful wildflowers that emerge after desert rains.",
            "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35"
        },
        {
            "title": "Neon Typography",
            "description": "A graphic design piece featuring illuminated letters and urban signage aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Renaissance Light",
            "description": "A classical portrait study using sfumato technique and careful attention to anatomy.",
            "image_url": "https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb"
        },
        {
            "title": "Abstract Motion",
            "description": "A kinetic artwork suggesting movement through curved lines and flowing forms.",
            "image_url": "https://images.unsplash.com/photo-1507908708918-778587c9e563"
        },
        {
            "title": "Bamboo Forest",
            "description": "A serene Asian-inspired painting of tall bamboo stalks creating natural vertical rhythms.",
            "image_url": "https://images.unsplash.com/photo-1547891654-e66ed7ebb968"
        },
        {
            "title": "Industrial Age",
            "description": "A steampunk aesthetic piece celebrating the mechanical innovations of Victorian era.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Color Field",
            "description": "A large-scale abstract painting featuring expansive areas of solid color exploration.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19"
        },
        {
            "title": "Mountain Reflection",
            "description": "A pristine landscape photograph with perfect mirror symmetry in alpine lake water.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Digital Mosaic",
            "description": "A pixel art composition creating recognizable images from tiny colored squares.",
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f"
        },
        {
            "title": "Autumn Path",
            "description": "A romantic landscape of a tree-lined path covered in golden fallen leaves.",
            "image_url": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97"
        },
        {
            "title": "Street Musician",
            "description": "A candid portrait capturing the soul and passion of performers sharing art publicly.",
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"
        },
        {
            "title": "Marble Luxury",
            "description": "An abstract design mimicking the elegant veining patterns found in premium marble.",
            "image_url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85"
        },
        {
            "title": "City Lights",
            "description": "A night photography series of urban landscapes illuminated by artificial light sources.",
            "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000"
        },
        {
            "title": "Paper Sculpture",
            "description": "Three-dimensional artwork created through cutting, folding, and layering paper materials.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Textured Paint",
            "description": "A heavily layered canvas with thick impasto creating tactile three-dimensional surfaces.",
            "image_url": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3"
        },
        {
            "title": "Golden Hour",
            "description": "A landscape bathed in the warm glow of sunset light creating long dramatic shadows.",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        },
        {
            "title": "Sacred Geometry",
            "description": "A mandala artwork exploring mathematical perfection and spiritual symbolism.",
            "image_url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0"
        },
        {
            "title": "Vintage Keys",
            "description": "A nostalgic still life photograph of antique skeleton keys arranged artistically.",
            "image_url": "https://images.unsplash.com/photo-1500964757637-c85e8a162699"
        },
        {
            "title": "Neon Dreams",
            "description": "A cyberpunk inspired artwork featuring glowing signs and rain-slicked streets.",
            "image_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853"
        },
        {
            "title": "Cave Art",
            "description": "Primitive style paintings using natural pigments depicting hunting scenes and animals.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Gem Macro",
            "description": "Extreme close-up photography revealing the internal structure and beauty of precious stones.",
            "image_url": "https://images.unsplash.com/photo-1518331647614-7a1f04cd34cf"
        },
        {
            "title": "Wild Brushwork",
            "description": "An expressionist piece with aggressive paint application conveying raw emotional power.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Dawn Colors",
            "description": "A tranquil landscape painted in the soft pastel palette of early morning light.",
            "image_url": "https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9"
        },
        {
            "title": "Steel Art",
            "description": "A modern sculpture crafted from industrial metal materials with geometric forms.",
            "image_url": "https://images.unsplash.com/photo-1544967082-d9d25d867d66"
        },
        {
            "title": "Old Hollywood",
            "description": "A glamorous illustration celebrating classic film stars and art deco design.",
            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728"
        },
        {
            "title": "Ocean Life",
            "description": "Vibrant underwater photography showcasing colorful fish and coral formations.",
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19"
        },
        {
            "title": "Sumi-e Style",
            "description": "Traditional Japanese ink painting featuring minimal brushstrokes and zen aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1523554888454-84137e72c3ce"
        },
        {
            "title": "Glass Art",
            "description": "A colorful composition inspired by medieval stained glass windows and light transmission.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Open Plains",
            "description": "A sweeping prairie landscape with endless horizons under vast sky.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Wall Art",
            "description": "A large-scale street mural featuring bold graphics and social messages.",
            "image_url": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Future Vision",
            "description": "A holographic artwork exploring technological advancement and digital aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Clay Hands",
            "description": "An intimate photograph of an artist working with wet clay on pottery wheel.",
            "image_url": "https://images.unsplash.com/photo-1493106819501-66d381c466f1"
        },
        {
            "title": "Night Sky",
            "description": "A stunning astrophotography image revealing countless stars and galactic structures.",
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a"
        },
        {
            "title": "Mixed Papers",
            "description": "A textural collage combining various paper types, colors, and printed materials.",
            "image_url": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b"
        },
        {
            "title": "Jungle Vibes",
            "description": "A tropical painting featuring dense foliage, exotic flowers, and wildlife in rich colors.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Flowing Forms",
            "description": "An Art Nouveau inspired piece with sinuous lines and botanical decorative elements.",
            "image_url": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5"
        },
        {
            "title": "Tempest Sea",
            "description": "A powerful seascape showing waves crashing against rocks during a violent storm.",
            "image_url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0"
        },
        {
            "title": "Clean Lines",
            "description": "A minimalist artwork using simple geometric forms and negative space principles.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Festival Joy",
            "description": "A vibrant celebration of cultural festivities captured in brilliant colors and movement.",
            "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30"
        },
        {
            "title": "Classical Columns",
            "description": "An architectural study of Greco-Roman temple remains with detailed stone textures.",
            "image_url": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd"
        },
        {
            "title": "Particle Theory",
            "description": "A scientific art visualization representing quantum mechanics and wave-particle duality.",
            "image_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564"
        },
        {
            "title": "Cathedral Height",
            "description": "A dramatic upward view of Gothic church architecture with vaulted ceilings.",
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"
        },
        {
            "title": "Woven Stories",
            "description": "A textile art piece incorporating traditional techniques and cultural narrative patterns.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Dynamic Marks",
            "description": "An energetic abstract with gestural brushstrokes capturing spontaneous creative motion.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Ice Patterns",
            "description": "A delicate macro study of frost crystals creating natural geometric designs.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Forgotten Places",
            "description": "Documentary photography exploring the aesthetic qualities of abandoned architecture.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Flowing Water",
            "description": "A serene long-exposure capture of cascading waterfalls with silky smooth motion.",
            "image_url": "https://images.unsplash.com/photo-1433086966358-54859d0ed716"
        },
        {
            "title": "Bold Portrait",
            "description": "A contemporary face painting using simplified shapes and vibrant pop colors.",
            "image_url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062"
        },
        {
            "title": "Wildflower Spring",
            "description": "A celebration of desert wildflowers blooming after rare rainfall events.",
            "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35"
        },
        {
            "title": "Light Letters",
            "description": "A graphic design featuring glowing neon typography in urban nighttime settings.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Master Study",
            "description": "A classical portrait demonstrating Renaissance techniques of light and shadow.",
            "image_url": "https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb"
        },
        {
            "title": "Kinetic Flow",
            "description": "An abstract suggesting movement through dynamic curves and color transitions.",
            "image_url": "https://images.unsplash.com/photo-1507908708918-778587c9e563"
        },
        {
            "title": "Zen Garden",
            "description": "A peaceful painting of bamboo groves creating vertical rhythms and natural patterns.",
            "image_url": "https://images.unsplash.com/photo-1547891654-e66ed7ebb968"
        },
        {
            "title": "Mechanical Dreams",
            "description": "A steampunk artwork celebrating Victorian-era industrial design and gears.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Pure Color",
            "description": "A large abstract canvas exploring relationships between expansive color fields.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19"
        },
        {
            "title": "Alpine Mirror",
            "description": "A pristine mountain landscape perfectly reflected in still lake waters.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Pixel Perfect",
            "description": "A digital mosaic artwork creating images from small geometric colored units.",
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f"
        },
        {
            "title": "Golden Path",
            "description": "A romantic autumn scene with tree-lined walkway covered in fallen leaves.",
            "image_url": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97"
        },
        {
            "title": "Street Soul",
            "description": "A documentary portrait of urban musicians sharing their passion with passersby.",
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"
        },
        {
            "title": "Stone Veins",
            "description": "An elegant abstract design inspired by natural marble veining patterns.",
            "image_url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85"
        },
        {
            "title": "Urban Glow",
            "description": "Night photography capturing cities illuminated by streetlights and building windows.",
            "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000"
        },
        {
            "title": "Folded Art",
            "description": "Three-dimensional paper sculptures created through intricate cutting and folding.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Thick Paint",
            "description": "A textured canvas with heavy impasto technique creating sculptural surfaces.",
            "image_url": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3"
        },
        {
            "title": "Sunset Glow",
            "description": "A landscape illuminated by warm golden hour light creating magical atmosphere.",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        },
        {
            "title": "Divine Patterns",
            "description": "A mandala exploring sacred geometry and mathematical spiritual symbolism.",
            "image_url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0"
        },
        {
            "title": "Antique Collection",
            "description": "A nostalgic still life arrangement of vintage keys and aged metal objects.",
            "image_url": "https://images.unsplash.com/photo-1500964757637-c85e8a162699"
        },
        {
            "title": "Electric City",
            "description": "A cyberpunk scene featuring neon-lit streets and futuristic urban atmosphere.",
            "image_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853"
        },
        {
            "title": "Prehistoric Art",
            "description": "Ancient style paintings using earth pigments showing early human artistic expression.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Crystal Close",
            "description": "Macro photography revealing intricate internal structures of natural gemstones.",
            "image_url": "https://images.unsplash.com/photo-1518331647614-7a1f04cd34cf"
        },
        {
            "title": "Raw Expression",
            "description": "An expressionist work with bold brushwork conveying intense emotional content.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Soft Morning",
            "description": "A peaceful landscape rendered in gentle pastel tones of dawn light.",
            "image_url": "https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9"
        },
        {
            "title": "Metal Forms",
            "description": "A contemporary sculpture using welded steel in abstract geometric compositions.",
            "image_url": "https://images.unsplash.com/photo-1544967082-d9d25d867d66"
        },
        {
            "title": "Silver Screen",
            "description": "A glamorous art deco illustration celebrating Hollywood's golden age stars.",
            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728"
        },
        {
            "title": "Reef Beauty",
            "description": "Underwater photography showcasing vibrant coral and tropical marine biodiversity.",
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19"
        },
        {
            "title": "Ink Meditation",
            "description": "A zen-inspired Japanese brush painting using minimalist black ink techniques.",
            "image_url": "https://images.unsplash.com/photo-1523554888454-84137e72c3ce"
        },
        {
            "title": "Light Through Glass",
            "description": "A colorful artwork inspired by cathedral stained glass and transmitted light.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Wide Horizons",
            "description": "An expansive prairie landscape featuring endless grasslands meeting sky.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Public Canvas",
            "description": "A large outdoor mural featuring bold street art graphics and messages.",
            "image_url": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Tech Tomorrow",
            "description": "A futuristic holographic piece exploring themes of digital advancement.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Shaping Clay",
            "description": "An intimate view of ceramic artistry with hands molding wet clay.",
            "image_url": "https://images.unsplash.com/photo-1493106819501-66d381c466f1"
        },
        {
            "title": "Starfield",
            "description": "A breathtaking astrophotography capturing the vastness of the night sky.",
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a"
        },
        {
            "title": "Paper Layers",
            "description": "A textural collage using varied paper materials in mixed media composition.",
            "image_url": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b"
        },
        {
            "title": "Rainforest Canopy",
            "description": "A lush painting of tropical vegetation with layered greens and exotic life.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Elegant Curves",
            "description": "An Art Nouveau design featuring organic flowing lines and floral motifs.",
            "image_url": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5"
        },
        {
            "title": "Ocean Fury",
            "description": "A dramatic seascape depicting powerful waves during a coastal storm.",
            "image_url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0"
        },
        {
            "title": "Simple Geometry",
            "description": "A minimalist composition exploring basic shapes and spatial relationships.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Celebration",
            "description": "A festive artwork bursting with the colors and energy of cultural celebration.",
            "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30"
        },
        {
            "title": "Ancient Temple",
            "description": "A detailed architectural rendering of classical Greek or Roman ruins.",
            "image_url": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd"
        },
        {
            "title": "Quantum Art",
            "description": "A scientific visualization representing subatomic particle behavior and energy.",
            "image_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564"
        },
        {
            "title": "Soaring Spires",
            "description": "An upward photograph of Gothic cathedral architecture reaching skyward.",
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"
        },
        {
            "title": "Cultural Threads",
            "description": "A textile artwork weaving together traditional patterns from multiple cultures.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Spontaneous Paint",
            "description": "An action painting featuring gestural marks and energetic brushwork.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Frost Art",
            "description": "A macro photograph of intricate ice crystal formations on surfaces.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Lost Architecture",
            "description": "A photographic series documenting the aesthetic of abandoned structures.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Silky Cascade",
            "description": "A long-exposure waterfall photograph with smooth flowing water effects.",
            "image_url": "https://images.unsplash.com/photo-1433086966358-54859d0ed716"
        },
        {
            "title": "Pop Face",
            "description": "A contemporary portrait using flat colors and pop art simplification.",
            "image_url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062"
        },
        {
            "title": "Desert Flowers",
            "description": "A vibrant painting of rare wildflowers blooming in arid landscapes.",
            "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35"
        },
        {
            "title": "Glowing Signs",
            "description": "A graphic design featuring illuminated urban typography and neon aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Old Master",
            "description": "A classical portrait demonstrating traditional oil painting techniques.",
            "image_url": "https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb"
        },
        {
            "title": "Fluid Motion",
            "description": "An abstract work suggesting movement through flowing forms and colors.",
            "image_url": "https://images.unsplash.com/photo-1507908708918-778587c9e563"
        },
        {
            "title": "Bamboo Grove",
            "description": "A serene Asian landscape featuring tall bamboo creating vertical patterns.",
            "image_url": "https://images.unsplash.com/photo-1547891654-e66ed7ebb968"
        },
        {
            "title": "Victorian Tech",
            "description": "A steampunk illustration celebrating mechanical innovation and brass gears.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Color Blocks",
            "description": "A large-scale abstract featuring bold expanses of saturated color.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19"
        },
        {
            "title": "Lake Mirror",
            "description": "A mountain landscape with perfect symmetrical reflection in calm water.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Digital Grid",
            "description": "A pixel art composition using small squares to create larger imagery.",
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f"
        },
        {
            "title": "Fall Colors",
            "description": "An autumn landscape with trees displaying golden and red foliage.",
            "image_url": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97"
        },
        {
            "title": "Urban Musicians",
            "description": "A candid documentary series of street performers sharing their art.",
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"
        },
        {
            "title": "Marble Effect",
            "description": "An abstract design mimicking luxurious marble stone veining.",
            "image_url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85"
        },
        {
            "title": "Night Metropolis",
            "description": "A cityscape photograph showcasing urban illumination after dark.",
            "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000"
        },
        {
            "title": "Paper Engineering",
            "description": "Complex three-dimensional structures created from precisely cut paper.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Impasto Texture",
            "description": "A heavily textured painting with thick applications of oil paint.",
            "image_url": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3"
        },
        {
            "title": "Magic Hour",
            "description": "A landscape bathed in the warm golden light of sunset.",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        },
        {
            "title": "Sacred Circle",
            "description": "A mandala design exploring geometric perfection and spiritual meaning.",
            "image_url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0"
        },
        {
            "title": "Vintage Hardware",
            "description": "A still life photograph of antique keys and aged metal objects.",
            "image_url": "https://images.unsplash.com/photo-1500964757637-c85e8a162699"
        },
        {
            "title": "Neon Rain",
            "description": "A cyberpunk scene with glowing signs reflected in wet streets.",
            "image_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853"
        },
        {
            "title": "Cave Dwellers",
            "description": "Primitive art using natural pigments depicting early human life.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Gem Interior",
            "description": "Extreme macro revealing the crystalline structure inside precious stones.",
            "image_url": "https://images.unsplash.com/photo-1518331647614-7a1f04cd34cf"
        },
        {
            "title": "Emotional Strokes",
            "description": "An expressionist painting with powerful brushwork and raw emotion.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Pastel Dawn",
            "description": "A tranquil landscape in soft morning colors and gentle light.",
            "image_url": "https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9"
        },
        {
            "title": "Welded Sculpture",
            "description": "A modern steel sculpture with industrial materials and geometric design.",
            "image_url": "https://images.unsplash.com/photo-1544967082-d9d25d867d66"
        },
        {
            "title": "Deco Glamour",
            "description": "An art deco illustration celebrating 1920s style and elegance.",
            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728"
        },
        {
            "title": "Coral Gardens",
            "description": "Underwater photography of colorful reef ecosystems and marine life.",
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19"
        },
        {
            "title": "Zen Brushwork",
            "description": "A minimalist Japanese ink painting embodying simplicity and meditation.",
            "image_url": "https://images.unsplash.com/photo-1523554888454-84137e72c3ce"
        },
        {
            "title": "Cathedral Glass",
            "description": "A colorful composition inspired by medieval stained glass artistry.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Endless Prairie",
            "description": "A vast landscape of grasslands stretching to distant horizons.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Street Canvas",
            "description": "A large-scale outdoor mural with bold graphics and urban messages.",
            "image_url": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Holographic Art",
            "description": "A futuristic piece exploring iridescent surfaces and digital aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Potter's Touch",
            "description": "An intimate photograph of hands shaping clay on a spinning wheel.",
            "image_url": "https://images.unsplash.com/photo-1493106819501-66d381c466f1"
        },
        {
            "title": "Galaxy View",
            "description": "An astrophotography image revealing the Milky Way across the sky.",
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a"
        },
        {
            "title": "Collage Mix",
            "description": "A mixed media artwork combining various papers and printed materials.",
            "image_url": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b"
        },
        {
            "title": "Tropical Lush",
            "description": "A vibrant jungle painting with dense foliage and exotic colors.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Art Nouveau Lines",
            "description": "A decorative design featuring organic curves and botanical elements.",
            "image_url": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5"
        },
        {
            "title": "Crashing Waves",
            "description": "A dynamic seascape showing the power of ocean waves hitting shore.",
            "image_url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0"
        },
        {
            "title": "Negative Space",
            "description": "A minimalist work exploring the balance of form and emptiness.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Fiesta Colors",
            "description": "A jubilant artwork capturing the spirit of festival and celebration.",
            "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30"
        },
        {
            "title": "Roman Columns",
            "description": "An architectural study of ancient classical temple structures.",
            "image_url": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd"
        },
        {
            "title": "Subatomic World",
            "description": "A visualization of quantum physics and particle interactions.",
            "image_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564"
        },
        {
            "title": "Gothic Towers",
            "description": "A photograph capturing towering cathedral spires and intricate stonework.",
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"
        },
        {
            "title": "Woven Heritage",
            "description": "A textile piece incorporating traditional weaving and cultural patterns.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Gesture Paint",
            "description": "An action painting with bold spontaneous marks and energy.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Winter Crystals",
            "description": "A macro study of frost forming geometric patterns on glass.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Abandoned Beauty",
            "description": "A photographic exploration of decay and forgotten architecture.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Smooth Falls",
            "description": "A long-exposure photograph of waterfall creating silky water effect.",
            "image_url": "https://images.unsplash.com/photo-1433086966358-54859d0ed716"
        },
        {
            "title": "Pop Color Face",
            "description": "A contemporary portrait in simplified pop art style with bold hues.",
            "image_url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062"
        },
        {
            "title": "Arid Bloom",
            "description": "A painting of wildflowers transforming desert landscape after rain.",
            "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35"
        },
        {
            "title": "Neon Letters",
            "description": "A graphic design with glowing urban typography and night aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Renaissance Portrait",
            "description": "A classical portrait study using traditional painting techniques.",
            "image_url": "https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb"
        },
        {
            "title": "Abstract Flow",
            "description": "A kinetic artwork suggesting movement through curves and gradients.",
            "image_url": "https://images.unsplash.com/photo-1507908708918-778587c9e563"
        },
        {
            "title": "Forest Zen",
            "description": "A peaceful bamboo grove painting with natural vertical rhythms.",
            "image_url": "https://images.unsplash.com/photo-1547891654-e66ed7ebb968"
        },
        {
            "title": "Brass Gears",
            "description": "A steampunk piece celebrating Victorian mechanical design.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Saturated Fields",
            "description": "A bold abstract with large areas of intense saturated color.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19"
        },
        {
            "title": "Peak Reflection",
            "description": "A mountain scene with perfect mirror image in alpine lake.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "8-Bit Art",
            "description": "A nostalgic pixel artwork creating images from colored squares.",
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f"
        },
        {
            "title": "Autumn Walk",
            "description": "A tree-lined path covered in colorful fallen autumn leaves.",
            "image_url": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97"
        },
        {
            "title": "Busker Life",
            "description": "A documentary portrait of street performers and their passion.",
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"
        },
        {
            "title": "Stone Luxury",
            "description": "An abstract inspired by premium marble veining and patterns.",
            "image_url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85"
        },
        {
            "title": "After Dark",
            "description": "A night cityscape with buildings lit by artificial illumination.",
            "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000"
        },
        {
            "title": "Kirigami",
            "description": "A Japanese paper cutting art creating intricate three-dimensional forms.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Palette Knife",
            "description": "A heavily textured painting created with thick paint application.",
            "image_url": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3"
        },
        {
            "title": "Evening Light",
            "description": "A landscape glowing in warm sunset illumination and long shadows.",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        },
        {
            "title": "Cosmic Mandala",
            "description": "A spiritual geometric design exploring universal patterns.",
            "image_url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0"
        },
        {
            "title": "Rusty Keys",
            "description": "A nostalgic photograph of antique keys with aged patina.",
            "image_url": "https://images.unsplash.com/photo-1500964757637-c85e8a162699"
        },
        {
            "title": "Blade Runner",
            "description": "A cyberpunk artwork with neon signs and rain-soaked streets.",
            "image_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853"
        },
        {
            "title": "Stone Age",
            "description": "Primitive artwork using earth pigments on rough surfaces.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Jewel Heart",
            "description": "A macro photograph revealing gemstone internal crystalline beauty.",
            "image_url": "https://images.unsplash.com/photo-1518331647614-7a1f04cd34cf"
        },
        {
            "title": "Paint Fury",
            "description": "An expressionist piece with aggressive brushwork and emotion.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "First Light",
            "description": "A serene landscape in the soft pastel colors of dawn.",
            "image_url": "https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9"
        },
        {
            "title": "Iron Works",
            "description": "A contemporary metal sculpture with geometric industrial design.",
            "image_url": "https://images.unsplash.com/photo-1544967082-d9d25d867d66"
        },
        {
            "title": "Jazz Age",
            "description": "An art deco illustration celebrating the roaring twenties style.",
            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728"
        },
        {
            "title": "Tropical Reef",
            "description": "Vibrant underwater photography of coral ecosystems and fish.",
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19"
        },
        {
            "title": "Black Ink",
            "description": "A zen Japanese brush painting with minimalist aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1523554888454-84137e72c3ce"
        },
        {
            "title": "Sacred Windows",
            "description": "A colorful piece inspired by religious stained glass artistry.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Big Sky Country",
            "description": "An expansive prairie with endless horizons under vast sky.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Urban Message",
            "description": "A large street mural with bold graphics and social themes.",
            "image_url": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Future Tech",
            "description": "A holographic artwork exploring advanced digital aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Ceramic Art",
            "description": "An intimate view of pottery creation on a spinning wheel.",
            "image_url": "https://images.unsplash.com/photo-1493106819501-66d381c466f1"
        },
        {
            "title": "Deep Space",
            "description": "An astrophotography capturing countless stars and cosmic beauty.",
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a"
        },
        {
            "title": "Paper Art",
            "description": "A mixed media collage using diverse paper textures and colors.",
            "image_url": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b"
        },
        {
            "title": "Jungle Life",
            "description": "A lush tropical painting with dense vegetation and wildlife.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Nouveau Style",
            "description": "A decorative artwork with organic flowing lines and florals.",
            "image_url": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5"
        },
        {
            "title": "Wild Sea",
            "description": "A powerful ocean scene with waves crashing dramatically.",
            "image_url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0"
        },
        {
            "title": "Less Is More",
            "description": "A minimalist composition exploring simplicity and balance.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Festive Spirit",
            "description": "A vibrant celebration artwork bursting with color and joy.",
            "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30"
        },
        {
            "title": "Parthenon",
            "description": "An architectural study of ancient Greek temple columns.",
            "image_url": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd"
        },
        {
            "title": "Particle Dance",
            "description": "A scientific art piece representing quantum mechanics visually.",
            "image_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564"
        },
        {
            "title": "Medieval Heights",
            "description": "A photograph of Gothic cathedral spires reaching upward.",
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"
        },
        {
            "title": "Fabric Stories",
            "description": "A textile artwork weaving cultural narratives and patterns.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Action Marks",
            "description": "An energetic painting with spontaneous gestural brushstrokes.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Ice Windows",
            "description": "A macro photograph of frost patterns creating natural designs.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Ruins",
            "description": "A documentary photograph of abandoned architecture and decay.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Misty Falls",
            "description": "A long-exposure waterfall with smooth ethereal water flow.",
            "image_url": "https://images.unsplash.com/photo-1433086966358-54859d0ed716"
        },
        {
            "title": "Warhol Style",
            "description": "A pop art portrait using simplified forms and bright colors.",
            "image_url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062"
        },
        {
            "title": "Desert Life",
            "description": "A painting celebrating wildflowers blooming in arid landscapes.",
            "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35"
        },
        {
            "title": "City Signs",
            "description": "A graphic design featuring illuminated urban neon typography.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Baroque Light",
            "description": "A classical portrait with dramatic light and shadow contrast.",
            "image_url": "https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb"
        },
        {
            "title": "Wave Motion",
            "description": "An abstract suggesting fluid movement through organic forms.",
            "image_url": "https://images.unsplash.com/photo-1507908708918-778587c9e563"
        },
        {
            "title": "Asian Serenity",
            "description": "A peaceful bamboo landscape with natural vertical patterns.",
            "image_url": "https://images.unsplash.com/photo-1547891654-e66ed7ebb968"
        },
        {
            "title": "Clockwork",
            "description": "A steampunk illustration of Victorian mechanical contraptions.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Bold Colors",
            "description": "A large abstract featuring expansive saturated color areas.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19"
        },
        {
            "title": "Perfect Mirror",
            "description": "A mountain landscape reflected symmetrically in still water.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Retro Pixels",
            "description": "A pixel art piece creating imagery from small colored blocks.",
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f"
        },
        {
            "title": "Leaf Path",
            "description": "An autumn scene with pathway covered in golden leaves.",
            "image_url": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97"
        },
        {
            "title": "Street Artists",
            "description": "A documentary series capturing urban performers and their art.",
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"
        },
        {
            "title": "Carrara Dreams",
            "description": "An abstract design inspired by Italian marble patterns.",
            "image_url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85"
        },
        {
            "title": "Skyline Night",
            "description": "A city photograph showcasing nighttime urban illumination.",
            "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000"
        },
        {
            "title": "Cut Paper",
            "description": "Three-dimensional artwork created through precise paper cutting.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Heavy Texture",
            "description": "A thickly painted canvas with sculptural impasto technique.",
            "image_url": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3"
        },
        {
            "title": "Dusk Light",
            "description": "A landscape illuminated by the warm glow of setting sun.",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        },
        {
            "title": "Symmetry",
            "description": "A mandala exploring perfect geometric balance and spirituality.",
            "image_url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0"
        },
        {
            "title": "Old Metal",
            "description": "A still life of vintage keys with weathered patina.",
            "image_url": "https://images.unsplash.com/photo-1500964757637-c85e8a162699"
        },
        {
            "title": "Cyber Streets",
            "description": "A cyberpunk scene with neon reflections on wet pavement.",
            "image_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853"
        },
        {
            "title": "Ancient Art",
            "description": "Primitive paintings using natural earth pigments and simple forms.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Crystal Macro",
            "description": "Extreme close-up revealing internal gemstone crystal structures.",
            "image_url": "https://images.unsplash.com/photo-1518331647614-7a1f04cd34cf"
        },
        {
            "title": "Raw Emotion",
            "description": "An expressionist work with powerful brushstrokes and feeling.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Morning Soft",
            "description": "A peaceful landscape in gentle dawn pastel hues.",
            "image_url": "https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9"
        },
        {
            "title": "Steel Forms",
            "description": "A modern sculpture using welded metal in abstract shapes.",
            "image_url": "https://images.unsplash.com/photo-1544967082-d9d25d867d66"
        },
        {
            "title": "Gatsby Era",
            "description": "An art deco design celebrating 1920s glamour and style.",
            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728"
        },
        {
            "title": "Under Sea",
            "description": "Underwater photography of vibrant coral reefs and marine biodiversity.",
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19"
        },
        {
            "title": "Zen Ink",
            "description": "A minimalist Japanese brush painting with meditative quality.",
            "image_url": "https://images.unsplash.com/photo-1523554888454-84137e72c3ce"
        },
        {
            "title": "Colored Glass",
            "description": "An artwork inspired by stained glass windows and light.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Grasslands",
            "description": "A vast prairie landscape with endless rolling plains.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Mural Art",
            "description": "A large outdoor wall painting with bold street art graphics.",
            "image_url": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Holo Future",
            "description": "A futuristic piece with holographic and iridescent effects.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Wheel Work",
            "description": "A photograph of hands shaping clay on a potter's wheel.",
            "image_url": "https://images.unsplash.com/photo-1493106819501-66d381c466f1"
        },
        {
            "title": "Cosmic View",
            "description": "An astrophotography image of the starry Milky Way galaxy.",
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a"
        },
        {
            "title": "Paper Mix",
            "description": "A collage artwork using various papers and printed ephemera.",
            "image_url": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b"
        },
        {
            "title": "Dense Jungle",
            "description": "A tropical painting with layered foliage and exotic plants.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Organic Lines",
            "description": "An Art Nouveau piece with flowing botanical decorative motifs.",
            "image_url": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5"
        },
        {
            "title": "Storm Sea",
            "description": "A dramatic seascape with powerful waves during tempest.",
            "image_url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0"
        },
        {
            "title": "Pure Form",
            "description": "A minimalist artwork exploring essential geometric shapes.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Color Party",
            "description": "A festive artwork with vibrant colors celebrating joy.",
            "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30"
        },
        {
            "title": "Temple Ruins",
            "description": "An architectural drawing of ancient classical structures.",
            "image_url": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd"
        },
        {
            "title": "Quantum Visual",
            "description": "A scientific visualization of subatomic particle behavior.",
            "image_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564"
        },
        {
            "title": "Stone Spires",
            "description": "A photograph of Gothic cathedral towers and architecture.",
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"
        },
        {
            "title": "Cultural Weave",
            "description": "A textile artwork combining traditional patterns and techniques.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Free Expression",
            "description": "An action painting with spontaneous energetic brushwork.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Frozen Art",
            "description": "A macro study of ice crystals forming natural patterns.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Left Behind",
            "description": "A photographic exploration of abandoned buildings and spaces.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Water Silk",
            "description": "A long-exposure waterfall creating smooth flowing effects.",
            "image_url": "https://images.unsplash.com/photo-1433086966358-54859d0ed716"
        },
        {
            "title": "Pop Icon",
            "description": "A contemporary portrait in bold pop art style.",
            "image_url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062"
        },
        {
            "title": "Blooming Desert",
            "description": "A painting of rare wildflowers in arid environment.",
            "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35"
        },
        {
            "title": "Bright Signs",
            "description": "A graphic design with glowing urban neon lettering.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Rembrandt Light",
            "description": "A classical portrait using dramatic chiaroscuro technique.",
            "image_url": "https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb"
        },
        {
            "title": "Liquid Forms",
            "description": "An abstract with flowing organic shapes suggesting movement.",
            "image_url": "https://images.unsplash.com/photo-1507908708918-778587c9e563"
        },
        {
            "title": "Bamboo Peace",
            "description": "A serene Asian landscape with tall bamboo stalks.",
            "image_url": "https://images.unsplash.com/photo-1547891654-e66ed7ebb968"
        },
        {
            "title": "Victorian Machine",
            "description": "A steampunk piece with intricate gears and brass mechanisms.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Color Power",
            "description": "A large abstract with bold expansive color fields.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19"
        },
        {
            "title": "Water Mirror",
            "description": "A mountain landscape with perfect reflection symmetry.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Game Graphics",
            "description": "A pixel art composition using retro video game aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f"
        },
        {
            "title": "Fall Carpet",
            "description": "An autumn path covered with colorful fallen foliage.",
            "image_url": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97"
        },
        {
            "title": "Performance Art",
            "description": "A candid documentary of street performers sharing passion.",
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"
        },
        {
            "title": "Elegant Stone",
            "description": "An abstract design mimicking luxurious marble veining.",
            "image_url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85"
        },
        {
            "title": "City Glow",
            "description": "A nighttime cityscape with brilliant artificial lighting.",
            "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000"
        },
        {
            "title": "Paper Sculpture",
            "description": "Three-dimensional forms created from cut and folded paper.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Sculptural Paint",
            "description": "A heavily textured painting with thick tactile surfaces.",
            "image_url": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3"
        },
        {
            "title": "Golden Light",
            "description": "A landscape bathed in warm sunset golden hour glow.",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        },
        {
            "title": "Perfect Balance",
            "description": "A mandala design exploring geometric harmony and spirituality.",
            "image_url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0"
        },
        {
            "title": "Aged Keys",
            "description": "A nostalgic photograph of antique skeleton keys.",
            "image_url": "https://images.unsplash.com/photo-1500964757637-c85e8a162699"
        },
        {
            "title": "Neon Future",
            "description": "A cyberpunk artwork with glowing signs and futuristic mood.",
            "image_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853"
        },
        {
            "title": "Cave Paintings",
            "description": "Primitive art using natural pigments on rough stone surfaces.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Gem Beauty",
            "description": "A macro revealing the internal crystalline structure of gems.",
            "image_url": "https://images.unsplash.com/photo-1518331647614-7a1f04cd34cf"
        },
        {
            "title": "Expressive Energy",
            "description": "An expressionist painting with aggressive emotional brushwork.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Gentle Dawn",
            "description": "A tranquil landscape in soft early morning pastel light.",
            "image_url": "https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9"
        },
        {
            "title": "Metal Sculpture",
            "description": "A contemporary artwork using industrial steel materials.",
            "image_url": "https://images.unsplash.com/photo-1544967082-d9d25d867d66"
        },
        {
            "title": "Deco Design",
            "description": "An elegant illustration celebrating art deco aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728"
        },
        {
            "title": "Marine World",
            "description": "Underwater photography showcasing colorful reef ecosystems.",
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19"
        },
        {
            "title": "Brush Meditation",
            "description": "A Japanese ink painting with zen minimalist philosophy.",
            "image_url": "https://images.unsplash.com/photo-1523554888454-84137e72c3ce"
        },
        {
            "title": "Glass Light",
            "description": "A colorful artwork inspired by stained glass windows.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Open Range",
            "description": "A vast prairie with endless grasslands under big sky.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Street Mural",
            "description": "A large outdoor wall painting with vibrant street art.",
            "image_url": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Digital Hologram",
            "description": "A futuristic artwork with holographic iridescent effects.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Clay Creation",
            "description": "An intimate photograph of pottery being shaped by hand.",
            "image_url": "https://images.unsplash.com/photo-1493106819501-66d381c466f1"
        },
        {
            "title": "Starry Night",
            "description": "An astrophotography revealing the Milky Way across darkness.",
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a"
        },
        {
            "title": "Collage Work",
            "description": "A mixed media piece combining papers and printed materials.",
            "image_url": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b"
        },
        {
            "title": "Wild Tropics",
            "description": "A lush jungle painting with dense exotic vegetation.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Floral Curves",
            "description": "An Art Nouveau design with sinuous botanical lines.",
            "image_url": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5"
        },
        {
            "title": "Raging Waters",
            "description": "A powerful seascape with waves crashing violently.",
            "image_url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0"
        },
        {
            "title": "Essential Forms",
            "description": "A minimalist piece exploring basic geometric principles.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Joyful Colors",
            "description": "A celebratory artwork bursting with festive vibrant hues.",
            "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30"
        },
        {
            "title": "Greek Ruins",
            "description": "An architectural study of ancient classical temple remains.",
            "image_url": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd"
        },
        {
            "title": "Subatomic Art",
            "description": "A visualization of quantum particle physics and energy.",
            "image_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564"
        },
        {
            "title": "Cathedral Spire",
            "description": "A dramatic photograph of Gothic church architecture.",
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"
        },
        {
            "title": "Woven Art",
            "description": "A textile piece incorporating traditional cultural weaving.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Gesture Art",
            "description": "An action painting with bold spontaneous brushwork.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Ice Beauty",
            "description": "A macro photograph of frost creating geometric patterns.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Decay Art",
            "description": "A photographic exploration of abandoned architectural beauty.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Smooth Water",
            "description": "A long-exposure waterfall with silky flowing effect.",
            "image_url": "https://images.unsplash.com/photo-1433086966358-54859d0ed716"
        },
        {
            "title": "Pop Art Face",
            "description": "A contemporary portrait in simplified pop art colors.",
            "image_url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062"
        },
        {
            "title": "Desert Spring",
            "description": "A painting of wildflowers blooming in dry landscape.",
            "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35"
        },
        {
            "title": "Urban Neon",
            "description": "A graphic design with illuminated city typography.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Classic Portrait",
            "description": "A traditional portrait using old master painting techniques.",
            "image_url": "https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb"
        },
        {
            "title": "Flow State",
            "description": "An abstract suggesting movement through curved forms.",
            "image_url": "https://images.unsplash.com/photo-1507908708918-778587c9e563"
        },
        {
            "title": "Tranquil Bamboo",
            "description": "A peaceful bamboo grove with vertical natural rhythms.",
            "image_url": "https://images.unsplash.com/photo-1547891654-e66ed7ebb968"
        },
        {
            "title": "Gear Work",
            "description": "A steampunk artwork with Victorian mechanical elements.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Vibrant Fields",
            "description": "A large abstract with expansive areas of bold color.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19"
        },
        {
            "title": "Reflection Art",
            "description": "A mountain scene perfectly mirrored in lake water.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Pixel Art",
            "description": "A digital mosaic creating images from colored squares.",
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f"
        },
        {
            "title": "Autumn Scene",
            "description": "A romantic pathway covered in golden fallen leaves.",
            "image_url": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97"
        },
        {
            "title": "Street Show",
            "description": "A documentary of urban performers and their passion.",
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"
        },
        {
            "title": "Marble Art",
            "description": "An abstract inspired by natural marble stone patterns.",
            "image_url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85"
        },
        {
            "title": "Night City",
            "description": "A cityscape illuminated by nighttime artificial lights.",
            "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000"
        },
        {
            "title": "Paper Form",
            "description": "Three-dimensional art created from cut folded paper.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Textured Canvas",
            "description": "A thickly painted work with heavy impasto technique.",
            "image_url": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3"
        },
        {
            "title": "Warm Glow",
            "description": "A landscape bathed in golden hour sunset light.",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        },
        {
            "title": "Sacred Art",
            "description": "A mandala exploring geometric patterns and spirituality.",
            "image_url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0"
        },
        {
            "title": "Antique Keys",
            "description": "A nostalgic still life of vintage metal keys.",
            "image_url": "https://images.unsplash.com/photo-1500964757637-c85e8a162699"
        },
        {
            "title": "Cyber Noir",
            "description": "A cyberpunk scene with neon and rain-soaked streets.",
            "image_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853"
        },
        {
            "title": "Primitive Work",
            "description": "Ancient style art using natural earth pigments.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Crystal Art",
            "description": "A macro photograph revealing gemstone internal beauty.",
            "image_url": "https://images.unsplash.com/photo-1518331647614-7a1f04cd34cf"
        },
        {
            "title": "Bold Strokes",
            "description": "An expressionist painting with powerful emotional energy.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Pastel Light",
            "description": "A serene landscape in gentle dawn pastel colors.",
            "image_url": "https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9"
        },
        {
            "title": "Steel Art",
            "description": "A modern sculpture using welded industrial metal.",
            "image_url": "https://images.unsplash.com/photo-1544967082-d9d25d867d66"
        },
        {
            "title": "Art Deco",
            "description": "An elegant design celebrating 1920s art deco style.",
            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728"
        },
        {
            "title": "Reef Life",
            "description": "Underwater photography of vibrant coral and marine life.",
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19"
        },
        {
            "title": "Ink Art",
            "description": "A Japanese brush painting with zen minimalist approach.",
            "image_url": "https://images.unsplash.com/photo-1523554888454-84137e72c3ce"
        },
        {
            "title": "Stained Art",
            "description": "A colorful piece inspired by cathedral stained glass.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Plains Vista",
            "description": "An expansive prairie landscape with endless horizons.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Wall Art",
            "description": "A large street mural with bold graphics and color.",
            "image_url": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Future Art",
            "description": "A futuristic holographic piece with digital aesthetics.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Pottery Art",
            "description": "An intimate view of ceramic creation on wheel.",
            "image_url": "https://images.unsplash.com/photo-1493106819501-66d381c466f1"
        },
        {
            "title": "Stellar Art",
            "description": "An astrophotography capturing the vastness of stars.",
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a"
        },
        {
            "title": "Mixed Media",
            "description": "A collage using varied papers and printed materials.",
            "image_url": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b"
        },
        {
            "title": "Tropical Art",
            "description": "A lush painting with dense jungle foliage.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Nouveau Art",
            "description": "An Art Nouveau design with flowing organic lines.",
            "image_url": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5"
        },
        {
            "title": "Ocean Storm",
            "description": "A dramatic seascape with crashing powerful waves.",
            "image_url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0"
        },
        {
            "title": "Minimal Art",
            "description": "A minimalist composition exploring simple forms.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Festival Art",
            "description": "A vibrant celebration piece bursting with color.",
            "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30"
        },
        {
            "title": "Ancient Columns",
            "description": "An architectural study of classical temple ruins.",
            "image_url": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd"
        },
        {
            "title": "Quantum Art",
            "description": "A scientific visualization of particle physics.",
            "image_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564"
        },
        {
            "title": "Gothic Art",
            "description": "A photograph of cathedral spires and stonework.",
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"
        },
        {
            "title": "Textile Art",
            "description": "A woven piece with traditional cultural patterns.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Action Art",
            "description": "An energetic painting with spontaneous brushwork.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Frost Art",
            "description": "A macro study of ice crystal natural patterns.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Ruins Art",
            "description": "A photographic series of abandoned architecture.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Water Art",
            "description": "A long-exposure waterfall with smooth flow.",
            "image_url": "https://images.unsplash.com/photo-1433086966358-54859d0ed716"
        },
        {
            "title": "Pop Portrait",
            "description": "A contemporary portrait in pop art style.",
            "image_url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062"
        },
        {
            "title": "Bloom Art",
            "description": "A painting of wildflowers in desert landscape.",
            "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35"
        },
        {
            "title": "Neon Art",
            "description": "A graphic design with glowing urban typography.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Portrait Study",
            "description": "A classical portrait using traditional techniques.",
            "image_url": "https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb"
        },
        {
            "title": "Motion Art",
            "description": "An abstract suggesting movement through forms.",
            "image_url": "https://images.unsplash.com/photo-1507908708918-778587c9e563"
        },
        {
            "title": "Bamboo Art",
            "description": "A peaceful Asian landscape with bamboo groves.",
            "image_url": "https://images.unsplash.com/photo-1547891654-e66ed7ebb968"
        },
        {
            "title": "Steampunk Art",
            "description": "A Victorian-inspired piece with mechanical gears.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Color Art",
            "description": "A large abstract with bold color field areas.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19"
        },
        {
            "title": "Mirror Art",
            "description": "A mountain landscape with perfect water reflection.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Digital Art",
            "description": "A pixel mosaic creating larger imagery.",
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f"
        },
        {
            "title": "Fall Art",
            "description": "An autumn scene with golden leaf-covered path.",
            "image_url": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97"
        },
        {
            "title": "Performance",
            "description": "A documentary of street performers sharing art.",
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"
        },
        {
            "title": "Stone Art",
            "description": "An abstract design inspired by marble patterns.",
            "image_url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85"
        },
        {
            "title": "Urban Night",
            "description": "A cityscape photograph with nighttime lights.",
            "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000"
        },
        {
            "title": "Paper Art",
            "description": "Three-dimensional sculpture from cut paper.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Texture Art",
            "description": "A painting with heavy impasto textured surface.",
            "image_url": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3"
        },
        {
            "title": "Sunset Art",
            "description": "A landscape in warm golden hour light.",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        },
        {
            "title": "Mandala Art",
            "description": "A geometric design exploring spiritual patterns.",
            "image_url": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0"
        },
        {
            "title": "Vintage Art",
            "description": "A still life photograph of antique keys.",
            "image_url": "https://images.unsplash.com/photo-1500964757637-c85e8a162699"
        },
        {
            "title": "Cyberpunk Art",
            "description": "A futuristic scene with neon and rain.",
            "image_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853"
        },
        {
            "title": "Ancient Art",
            "description": "Primitive painting using natural earth pigments.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Gem Art",
            "description": "A macro revealing gemstone crystalline structures.",
            "image_url": "https://images.unsplash.com/photo-1518331647614-7a1f04cd34cf"
        },
        {
            "title": "Expression Art",
            "description": "An expressionist work with powerful brushstrokes.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Dawn Art",
            "description": "A tranquil landscape in soft pastel dawn hues.",
            "image_url": "https://images.unsplash.com/photo-1502481851512-e9e2529bfbf9"
        },
        {
            "title": "Sculpture Art",
            "description": "A modern steel sculpture with geometric forms.",
            "image_url": "https://images.unsplash.com/photo-1544967082-d9d25d867d66"
        },
        {
            "title": "Deco Art",
            "description": "An elegant art deco style illustration.",
            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728"
        },
        {
            "title": "Marine Art",
            "description": "Underwater photography of coral reef ecosystems.",
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19"
        },
        {
            "title": "Zen Art",
            "description": "A Japanese ink painting with minimalist zen.",
            "image_url": "https://images.unsplash.com/photo-1523554888454-84137e72c3ce"
        },
        {
            "title": "Glass Art",
            "description": "A colorful piece inspired by stained glass.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Prairie Art",
            "description": "A vast grassland landscape with open horizons.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Mural",
            "description": "A large outdoor wall painting with street art.",
            "image_url": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Holographic",
            "description": "A futuristic piece with holographic effects.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Ceramic",
            "description": "A photograph of hands shaping pottery clay.",
            "image_url": "https://images.unsplash.com/photo-1493106819501-66d381c466f1"
        },
        {
            "title": "Cosmos",
            "description": "An astrophotography of the starry Milky Way.",
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a"
        },
        {
            "title": "Collage",
            "description": "A mixed media artwork combining various papers.",
            "image_url": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b"
        },
        {
            "title": "Jungle",
            "description": "A tropical painting with lush dense foliage.",
            "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"
        },
        {
            "title": "Flowing Lines",
            "description": "An Art Nouveau design with organic curves.",
            "image_url": "https://images.unsplash.com/photo-1536924940846-227afb31e2a5"
        },
        {
            "title": "Seascape",
            "description": "A dramatic ocean view with powerful waves.",
            "image_url": "https://images.unsplash.com/photo-1505142468610-359e7d316be0"
        },
        {
            "title": "Simplicity",
            "description": "A minimalist work exploring essential forms.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Celebration",
            "description": "A festive artwork with vibrant joyful colors.",
            "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30"
        },
        {
            "title": "Ruins",
            "description": "An architectural study of ancient structures.",
            "image_url": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd"
        },
        {
            "title": "Particles",
            "description": "A visualization of quantum physics concepts.",
            "image_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564"
        },
        {
            "title": "Cathedral",
            "description": "A photograph of Gothic cathedral architecture.",
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"
        },
        {
            "title": "Weaving",
            "description": "A textile artwork with cultural patterns.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Gesture",
            "description": "An action painting with spontaneous marks.",
            "image_url": "https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8"
        },
        {
            "title": "Ice Crystal",
            "description": "A macro of frost forming natural patterns.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Abandoned",
            "description": "A photograph exploring architectural decay.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Cascade",
            "description": "A long-exposure waterfall with silky water.",
            "image_url": "https://images.unsplash.com/photo-1433086966358-54859d0ed716"
        },
        {
            "title": "Pop Style",
            "description": "A contemporary portrait in pop art colors.",
            "image_url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062"
        },
        {
            "title": "Wildflowers",
            "description": "A painting of desert blooms after rainfall.",
            "image_url": "https://images.unsplash.com/photo-1509316785289-025f5b846b35"
        },
        {
            "title": "Typography",
            "description": "A graphic design with glowing neon letters.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Masterpiece",
            "description": "A classical portrait using old master style.",
            "image_url": "https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb"
        },
        {
            "title": "Movement",
            "description": "An abstract with dynamic flowing curved shapes.",
            "image_url": "https://images.unsplash.com/photo-1507908708918-778587c9e563"
        },
        {
            "title": "Tranquility",
            "description": "A peaceful bamboo grove landscape painting.",
            "image_url": "https://images.unsplash.com/photo-1547891654-e66ed7ebb968"
        },
        {
            "title": "Machinery",
            "description": "A steampunk piece with Victorian gears and brass.",
            "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23"
        },
        {
            "title": "Ethereal Layers",
            "description": "A translucent mixed media piece exploring depth through overlapping transparent materials and soft colors.",
            "image_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5"
        },
        {
            "title": "Bronze Age",
            "description": "A sculptural study in bronze capturing human form with classical proportions and modern interpretation.",
            "image_url": "https://images.unsplash.com/photo-1577083552431-6e5fd01988ec"
        },
        {
            "title": "Ink Blossoms",
            "description": "A delicate sumi-e painting of cherry blossoms rendered with traditional Japanese brush techniques.",
            "image_url": "https://images.unsplash.com/photo-1524721696987-b9527df9e512"
        },
        {
            "title": "Urban Canvas",
            "description": "A large-scale street art installation transforming city walls into vibrant public galleries.",
            "image_url": "https://images.unsplash.com/photo-1561214115-f2f134cc4912"
        },
        {
            "title": "Spectrum Shift",
            "description": "A gradient painting exploring subtle color transitions across the full visible spectrum.",
            "image_url": "https://images.unsplash.com/photo-1551732998-9d5d9781d7ca"
        },
        {
            "title": "Memory Fragments",
            "description": "A photomontage combining vintage family photographs with contemporary digital manipulation techniques.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Volcanic Passion",
            "description": "An explosive abstract in fiery reds and oranges capturing the raw power of molten lava.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Minimalist Chapel",
            "description": "A photograph of modern religious architecture emphasizing light, space, and spiritual contemplation.",
            "image_url": "https://images.unsplash.com/photo-1478860409698-8707f313ee8b"
        },
        {
            "title": "Textile Traditions",
            "description": "A handwoven tapestry incorporating indigenous patterns passed down through generations.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Moonlit Serenity",
            "description": "A nocturnal landscape painting bathed in silvery moonlight with mysterious shadows.",
            "image_url": "https://images.unsplash.com/photo-1532274402911-5a369e4c4bb5"
        },
        {
            "title": "Shattered Perspectives",
            "description": "A cubist-inspired composition fragmenting reality into geometric planes and multiple viewpoints.",
            "image_url": "https://images.unsplash.com/photo-1541961017774-22349e4a1262"
        },
        {
            "title": "Golden Ratio",
            "description": "A mathematical art piece exploring the Fibonacci sequence and divine proportion in visual form.",
            "image_url": "https://images.unsplash.com/photo-1557672172-298e090bd0f1"
        },
        {
            "title": "Weathered Dignity",
            "description": "A portrait photography series capturing the character and wisdom etched in elderly faces.",
            "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"
        },
        {
            "title": "Neon Genesis",
            "description": "A futuristic digital artwork depicting the birth of artificial consciousness in electric colors.",
            "image_url": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853"
        },
        {
            "title": "Botanical Anatomy",
            "description": "A scientific illustration series dissecting plant structures with precise detail and artistic beauty.",
            "image_url": "https://images.unsplash.com/photo-1466781783364-36c955e42a7f"
        },
        {
            "title": "Rhythmic Patterns",
            "description": "A textile design featuring repeating motifs inspired by African tribal art and music.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Impressionist Rain",
            "description": "A soft-focus painting capturing the atmosphere and mood of a rainy Parisian afternoon.",
            "image_url": "https://images.unsplash.com/photo-1428908728789-d2de25dbd4e2"
        },
        {
            "title": "Industrial Elegance",
            "description": "A photography series finding beauty in factories, machinery, and manufacturing processes.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"
        },
        {
            "title": "Charcoal Depths",
            "description": "A dramatic portrait study using compressed charcoal to create intense contrast and emotion.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        },
        {
            "title": "Aurora Borealis",
            "description": "A photograph capturing the dancing lights of the northern aurora in brilliant greens and purples.",
            "image_url": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7"
        },
        {
            "title": "Fluid Dynamics",
            "description": "An abstract pour painting exploring the natural flow patterns of liquid acrylics.",
            "image_url": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Metropolitan Pulse",
            "description": "A time-lapse photography series capturing the frenetic energy of rush hour traffic.",
            "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000"
        },
        {
            "title": "Stone Garden",
            "description": "A meditative photograph of Japanese rock garden arrangements emphasizing zen simplicity.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Graffiti Poetry",
            "description": "A street art piece combining spray paint techniques with calligraphic letterforms and verses.",
            "image_url": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "title": "Crystalline Structure",
            "description": "A macro photography study revealing the geometric perfection of snowflake formations.",
            "image_url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5"
        },
        {
            "title": "Sunset Symphony",
            "description": "A panoramic landscape painting celebrating the orchestral colors of dusk over mountains.",
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        },
        {
            "title": "Digital Weave",
            "description": "A generative art piece creating intricate patterns through algorithmic computation and code.",
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f"
        },
        {
            "title": "Cafe Culture",
            "description": "A documentary photography series capturing the intimate moments and characters of coffee shops.",
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f"
        },
        {
            "title": "Mosaic Heritage",
            "description": "A traditional mosaic artwork using colored tiles to create Byzantine-inspired religious imagery.",
            "image_url": "https://images.unsplash.com/photo-1482800304058-6e50b7b78103"
        },
        {
            "title": "Smoke and Mirrors",
            "description": "An experimental photography series using smoke, light, and reflection to create surreal effects.",
            "image_url": "https://images.unsplash.com/photo-1518640467707-6811f4a6ab73"
        },
        {
            "title": "Vintage Glamour",
            "description": "A fashion illustration series celebrating the elegance and sophistication of 1950s haute couture.",
            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728"
        },
        {
            "title": "Abstract Emotion",
            "description": "A large-scale expressionist painting channeling pure feeling through color, form, and gesture.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19"
        },
        {
            "title": "Whispers of Dawn",
            "description": "A misty morning landscape where fog softly blankets rolling hills in peaceful pastel tones.",
            "image_url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        },
        {
            "title": "Urban Geometry",
            "description": "An architectural photography series exploring the stark angles and lines of contemporary skyscrapers.",
            "image_url": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b"
        },
        {
            "title": "Ancestral Masks",
            "description": "A collection of traditional ceremonial masks carved from wood, representing cultural spirits and deities.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64"
        },
        {
            "title": "Liquid Light",
            "description": "A mesmerizing fluid art piece where metallic paints create shimmering organic patterns and flows.",
            "image_url": "https://images.unsplash.com/photo-1557682250-33bd709cbe85"
        },
        {
            "title": "Silent Witness",
            "description": "A powerful black and white documentary photograph capturing a pivotal moment in social history.",
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"
        }
    ]
    
    artworks = []
    for i in range(count):
        template = random.choice(templates)
        # Create unique variations
        artworks.append({
            "title": f"{template['title']} #{i+1}",
            "description": template['description'],
            "image_url": template['image_url']
        })
    return artworks

def split_number_randomly(total, count):
    """
    Splits 'total' into 'count' random integers that sum up to 'total'.
    Each number is at least 1 (assuming we want everyone to have at least one artwork? 
    or maybe 0 is allowed. The user said 'Some user may have 20 some user may have ... 60'
    so let's aim for a decent spread. Simple implementation: Generate random points and take differences.)
    """
    if count <= 0: return []
    
    # Generate count-1 random cut points
    points = sorted([random.randint(0, total) for _ in range(count - 1)])
    # Add 0 and total to the list of points
    points = [0] + points + [total]
    
    # Calculate differences to get the parts
    parts = [points[i+1] - points[i] for i in range(count)]
    
    # The simple cut method might result in 0s. Let's ensure a slightly more balanced spread if needed,
    # but strictly random cuts is statistically sound for "random distribution".
    # User said "Some user may have 20... 60", which implies high variance is okay.
    return parts

async def populate_db():
    print("Connecting to database...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client[settings.DB_NAME], document_models=[User, Artwork])
    
    print("Generating 100 User Profiles...")
    user_data_list = generate_users(100)
    
    users_to_insert = []
    for u_data in user_data_list:
        users_to_insert.append(User(
            username=u_data["username"],
            email=u_data["email"],
            hashed_password=get_password_hash(u_data["password"]),
            is_active=True
        ))
    
    # Insert Users
    print("Inserting Users into Database...")
    inserted_users = []
    # Beanie doesn't return the inserted objects with IDs in insert_many easily in all versions, 
    # but let's try insert_many or loop if safer. Loop is slower but safer for ID retrieval if driver specific.
    # Actually User.insert_many returns InsertManyResult, but doesn't update instances in-place in older beanie versions.
    # We'll use a loop to be safe and get IDs.
    for user in users_to_insert:
        created_user = await user.create()
        inserted_users.append(created_user)
        
    print(f"Successfully inserted {len(inserted_users)} users.")
    
    print("Generating 500 Artworks...")
    artwork_data_list = generate_artworks(500)
    random.shuffle(artwork_data_list) # Shuffle to mix types
    
    print("Distributing artworks among users...")
    # Get random counts for each user summing to 500
    counts = split_number_randomly(500, 100)
    
    # Verify sum
    assert sum(counts) == 500
    
    artworks_to_insert = []
    artwork_idx = 0
    
    for i, user in enumerate(inserted_users):
        count = counts[i]
        # Assign 'count' artworks to this user
        for _ in range(count):
            if artwork_idx < len(artwork_data_list):
                art_data = artwork_data_list[artwork_idx]
                artworks_to_insert.append(Artwork(
                    title=art_data["title"],
                    description=art_data["description"],
                    image_url=art_data["image_url"],
                    owner=user  # Beanie Link
                ))
                artwork_idx += 1
    
    print(f"Inserting {len(artworks_to_insert)} Artworks into Database...")
    # Chunking insert to be safe
    chunk_size = 100
    for i in range(0, len(artworks_to_insert), chunk_size):
        chunk = artworks_to_insert[i:i + chunk_size]
        await Artwork.insert_many(chunk)
        print(f"Inserted chunk {i//chunk_size + 1}...")

    print("✅ Database Population Complete!")
    print(f"Total Users: {len(inserted_users)}")
    print(f"Total Artworks: {len(artworks_to_insert)}")

if __name__ == "__main__":
    asyncio.run(populate_db())
