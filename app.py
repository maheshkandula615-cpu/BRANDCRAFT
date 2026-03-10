from flask import Flask, request, jsonify, send_from_directory
import os
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# API Key configuration
API_KEY = os.environ.get('BRANDCRAFT_API_KEY', 'your-secret-api-key-here')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if not api_key or api_key != API_KEY:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

@app.route('/generate-logo')
@require_api_key
def generate_logo():
    keyword = request.args.get('keyword', 'Brand').strip() or 'Brand'

    style_variants = [
        {'name': 'Minimalist Tech', 'id': 'minimal'},
        {'name': 'Geometric Blue', 'id': 'geometric'},
        {'name': 'Futuristic Glow', 'id': 'futuristic'}
    ]

    logos = []
    for variant in style_variants:
        svg = build_logo_svg(keyword, variant['id'])
        logos.append({
            'style': variant['name'],
            'svg': svg
        })

    return jsonify({'logos': logos})


def build_logo_svg(keyword, style):
    # deterministic color palette based on keyword + style
    import hashlib
    hash_obj = hashlib.md5((keyword + style).encode())
    hash_int = int(hash_obj.hexdigest(), 16)

    if style == 'minimal':
        color1 = '#0D47A1'
        color2 = '#1976D2'
        color3 = '#64B5F6'
        accent_color = '#42A5F5'
        background_shapes = f'<rect width="300" height="150" fill="{color1}" rx="20" opacity="0.15"/>'
        decorative_elements = ''
        icon = '<g><rect x="90" y="45" width="30" height="60" fill="white" opacity="0.9" rx="4"/><rect x="150" y="45" width="30" height="60" fill="white" opacity="0.9" rx="4"/><rect x="210" y="45" width="30" height="60" fill="white" opacity="0.9" rx="4"/></g>'
        font_style = f'<text x="150" y="120" font-family="Segoe UI, sans-serif" font-size="26" font-weight="700" fill="white" text-anchor="middle">{keyword}</text>'

    elif style == 'geometric':
        color1 = '#1E3A8A'
        color2 = '#2563EB'
        color3 = '#93C5FD'
        accent_color = '#60A5FA'
        background_shapes = get_background_shapes(keyword.lower(), color1, color2, color3, accent_color)
        decorative_elements = get_decorative_elements(keyword.lower(), accent_color)
        icon = get_icon_for_keyword(keyword.lower())
        font_style = f'<text x="150" y="120" font-family="Poppins, sans-serif" font-size="28" font-weight="800" fill="url(#textGrad)" text-anchor="middle">{keyword}</text>'

    else:  # futuristic
        color1 = '#0B69A3'
        color2 = '#1973D8'
        color3 = '#1FB5FF'
        accent_color = '#7BB7FF'
        background_shapes = f'<polygon points="20,130 70,20 160,40 260,20 280,125" fill="{color2}" opacity="0.25"/><line x1="30" y1="110" x2="270" y2="40" stroke="{accent_color}" stroke-width="2" opacity="0.5"/>'
        decorative_elements = '<circle cx="45" cy="45" r="8" fill="white" opacity="0.4"/><circle cx="250" cy="110" r="6" fill="white" opacity="0.35"/>'
        icon = '<g><path d="M75 55 L115 55 L120 85 L80 85 Z" fill="white" opacity="0.9"/><path d="M90 40 L90 100" stroke="white" stroke-width="3" opacity="0.8"/></g>'
        font_style = f'<text x="150" y="120" font-family="Orbitron, sans-serif" font-size="26" font-weight="700" fill="url(#textGrad)" text-anchor="middle">{keyword}</text>'

    pattern = get_pattern_for_keyword(keyword.lower())

    svg = f'''<svg width="300" height="150" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 150">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color1};stop-opacity:0.9" />
      <stop offset="50%" style="stop-color:{color2};stop-opacity:0.85" />
      <stop offset="100%" style="stop-color:{color3};stop-opacity:0.9" />
    </linearGradient>
    <radialGradient id="radialGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:white;stop-opacity:0.2" />
      <stop offset="100%" style="stop-color:{color1};stop-opacity:0" />
    </radialGradient>
    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ffffff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#dbeafe;stop-opacity:0.95" />
    </linearGradient>
    {pattern}
  </defs>
  <rect width="300" height="150" fill="url(#grad1)" rx="20"/>
  {background_shapes}
  {decorative_elements}
  <rect width="300" height="150" fill="url(#radialGlow)" rx="20" opacity="0.5"/>
  <g>{icon}</g>
  {font_style}
</svg>'''

    return svg

def get_background_shapes(keyword, color1, color2, color3, accent_color):
    """Return dynamic background shapes based on industry"""
    shapes = {
        'tech': f'''<defs><linearGradient id="backGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color1}" />
      <stop offset="100%" style="stop-color:{color2}" />
    </linearGradient></defs>
    <polygon points="150,10 280,50 260,130 40,130 20,50" fill="url(#backGrad)" opacity="0.9"/>
    <rect x="0" y="0" width="300" height="150" fill="url(#grad1)" rx="0" opacity="0.3"/>''',
        
        'coffee': f'''<circle cx="150" cy="75" r="75" fill="url(#grad1)" opacity="0.85"/>
    <circle cx="150" cy="75" r="70" fill="{color1}" opacity="0.1"/>''',
        
        'food': f'''<polygon points="47,10 253,10 300,70 253,130 47,130 0,70" fill="url(#grad1)"/>
    <polygon points="50,15 250,15 295,65 250,125 50,125 5,65" fill="{color2}" opacity="0.15" stroke="{accent_color}" stroke-width="1"/>''',
        
        'fitness': f'''<rect x="5" y="5" width="290" height="140" fill="url(#grad1)" rx="35"/>
    <rect x="10" y="10" width="280" height="130" fill="none" stroke="{color3}" stroke-width="2" rx="30" opacity="0.3"/>''',
        
        'music': f'''<path d="M 40 30 Q 150 10 260 30 L 280 120 Q 150 140 20 120 Z" fill="url(#grad1)"/>
    <ellipse cx="150" cy="75" rx="90" ry="50" fill="{color2}" opacity="0.1"/>''',
        
        'travel': f'''<polygon points="150,15 280,60 270,130 30,130 20,60" fill="url(#grad1)"/>
    <polygon points="150,25 265,65 255,125 45,125 35,65" fill="none" stroke="white" stroke-width="1.5" opacity="0.3"/>''',
        
        'fashion': f'''<path d="M 75 10 L 225 10 Q 280 10 280 50 L 270 140 L 30 140 L 20 50 Q 20 10 75 10" fill="url(#grad1)"/>
    <ellipse cx="150" cy="65" rx="60" ry="45" fill="{color3}" opacity="0.15"/>''',
        
        'crypto': f'''<polygon points="150,10 260,50 290,135 150,150 10,135 40,50" fill="url(#grad1)"/>
    <polygon points="150,20 250,55 275,130 150,142 25,130 50,55" fill="none" stroke="{accent_color}" stroke-width="1" opacity="0.4"/>''',
    }
    
    for key, shape in shapes.items():
        if key in keyword:
            return shape
    
    # Default rounded rectangle
    return f'''<rect width="300" height="150" fill="url(#grad1)" rx="20"/>
    <rect x="3" y="3" width="294" height="144" fill="none" stroke="white" stroke-width="1" rx="18" opacity="0.2"/>'''

def get_decorative_elements(keyword, accent_color):
    """Return decorative geometric elements"""
    elements = {
        'tech': f'''<g opacity="0.15">
      <circle cx="30" cy="30" r="8" fill="white"/>
      <circle cx="270" cy="120" r="6" fill="white"/>
      <rect x="20" y="100" width="15" height="15" fill="{accent_color}"/>
      <polygon points="260,20 268,28 260,36" fill="white"/>
    </g>''',
        
        'coffee': f'''<g opacity="0.12">
      <circle cx="25" cy="25" r="7" fill="white"/>
      <circle cx="275" cy="130" r="5" fill="white"/>
      <polygon points="280,40 290,50 280,60" fill="{accent_color}"/>
    </g>''',
        
        'food': f'''<g opacity="0.15">
      <polygon points="30,20 40,30 30,40" fill="white"/>
      <polygon points="270,110 280,120 270,130" fill="white"/>
      <circle cx="50" cy="120" r="6" fill="{accent_color}"/>
    </g>''',
        
        'fitness': f'''<g opacity="0.14">
      <line x1="20" y1="30" x2="40" y2="30" stroke="white" stroke-width="2"/>
      <line x1="30" y1="20" x2="30" y2="40" stroke="white" stroke-width="2"/>
      <circle cx="270" cy="120" r="7" fill="{accent_color}"/>
    </g>''',
        
        'music': f'''<g opacity="0.12">
      <path d="M 30 40 Q 35 30 40 40" stroke="white" stroke-width="1.5" fill="none"/>
      <path d="M 260 100 Q 265 90 270 100" stroke="white" stroke-width="1.5" fill="none"/>
      <circle cx="275" cy="40" r="5" fill="{accent_color}"/>
    </g>''',
        
        'travel': f'''<g opacity="0.15">
      <polygon points="30,20 35,35 25,35" fill="white"/>
      <polygon points="270,110 275,125 265,125" fill="white"/>
      <circle cx="50" cy="100" r="6" fill="{accent_color}"/>
    </g>''',
    }
    
    for key, elem in elements.items():
        if key in keyword:
            return elem
    
    return f'''<g opacity="0.12">
      <circle cx="25" cy="25" r="5" fill="white"/>
      <circle cx="275" cy="125" r="4" fill="white"/>
      <rect x="15" y="110" width="12" height="12" fill="{accent_color}"/>
    </g>'''

def get_pattern_for_keyword(keyword):
    """Return decorative SVG pattern based on industry"""
    patterns = {
        'tech': '''<pattern id="patternFill" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="20" y2="20" stroke="white" stroke-width="1"/>
      <line x1="20" y1="0" x2="0" y2="20" stroke="white" stroke-width="1"/>
    </pattern>''',
        'coffee': '''<pattern id="patternFill" x="0" y="0" width="30" height="30" patternUnits="userSpaceOnUse">
      <circle cx="15" cy="15" r="3" fill="white"/>
    </pattern>''',
        'food': '''<pattern id="patternFill" x="0" y="0" width="25" height="25" patternUnits="userSpaceOnUse">
      <polygon points="12,5 20,12 12,20 5,12" fill="white"/>
    </pattern>''',
        'fitness': '''<pattern id="patternFill" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <line x1="0" y1="10" x2="20" y2="10" stroke="white" stroke-width="1"/>
      <line x1="10" y1="0" x2="10" y2="20" stroke="white" stroke-width="1"/>
    </pattern>''',
        'music': '''<pattern id="patternFill" x="0" y="0" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M15 5 Q20 10 15 15 Q10 10 15 5" fill="white"/>
    </pattern>''',
        'travel': '''<pattern id="patternFill" x="0" y="0" width="25" height="25" patternUnits="userSpaceOnUse">
      <polygon points="12,5 18,15 6,15" fill="white"/>
    </pattern>''',
    }
    
    for key, pattern in patterns.items():
        if key in keyword:
            return pattern
    
    # Default dotted pattern
    return '''<pattern id="patternFill" x="0" y="0" width="15" height="15" patternUnits="userSpaceOnUse">
      <circle cx="7.5" cy="7.5" r="2" fill="white"/>
    </pattern>'''

def get_font_style_for_keyword(keyword, color1, color2):
    """Return styled text based on industry theme"""
    brand_name = keyword.split()[0].upper() if keyword else "BRAND"
    
    # Different styles for different industries
    if 'tech' in keyword or 'ai' in keyword or 'crypto' in keyword:
        # Tech: Modern, bold, geometric
        return f'''<text x="150" y="92" font-family="'Courier New', monospace" font-size="32" font-weight="900" fill="url(#textGrad)" text-anchor="middle" filter="url(#shadow)" letter-spacing="2">{brand_name}</text>'''
    
    elif 'coffee' in keyword or 'cafe' in keyword or 'tea' in keyword:
        # Coffee/Cafe: Elegant, slightly italic
        return f'''<text x="150" y="92" font-family="'Georgia', serif" font-size="30" font-weight="700" fill="url(#textGrad)" text-anchor="middle" filter="url(#shadow)" font-style="italic">{brand_name}</text>'''
    
    elif 'food' in keyword or 'restaurant' in keyword or 'pizza' in keyword:
        # Food: Fun, playful, rounded
        return f'''<text x="150" y="92" font-family="'Comic Sans MS', cursive" font-size="28" font-weight="900" fill="url(#textGrad)" text-anchor="middle" filter="url(#shadow)">{brand_name}</text>'''
    
    elif 'fashion' in keyword or 'beauty' in keyword:
        # Fashion: Stylish, thin, elegant
        return f'''<text x="150" y="92" font-family="'Trebuchet MS', sans-serif" font-size="32" font-weight="300" fill="url(#textGrad)" text-anchor="middle" filter="url(#shadow)" letter-spacing="3">{brand_name}</text>'''
    
    elif 'fitness' in keyword or 'gym' in keyword or 'health' in keyword:
        # Fitness: Bold, strong, energetic
        return f'''<text x="150" y="92" font-family="'Impact', sans-serif" font-size="36" font-weight="900" fill="url(#textGrad)" text-anchor="middle" filter="url(#shadow)">{brand_name}</text>'''
    
    elif 'music' in keyword or 'audio' in keyword:
        # Music: Creative, flowing
        return f'''<text x="150" y="92" font-family="'Verdana', sans-serif" font-size="30" font-weight="700" fill="url(#textGrad)" text-anchor="middle" filter="url(#shadow)" letter-spacing="1">{brand_name}</text>'''
    
    elif 'travel' in keyword or 'adventure' in keyword:
        # Travel: Bold, adventurous
        return f'''<text x="150" y="92" font-family="'Arial Black', sans-serif" font-size="34" font-weight="900" fill="url(#textGrad)" text-anchor="middle" filter="url(#shadow)">{brand_name}</text>'''
    
    else:
        # Default: Modern, clean, professional
        return f'''<text x="150" y="92" font-family="'Segoe UI', sans-serif" font-size="32" font-weight="700" fill="url(#textGrad)" text-anchor="middle" filter="url(#shadow)" letter-spacing="1">{brand_name}</text>'''

def get_icon_for_keyword(keyword):
    """Return SVG icon based on keyword"""
    icons = {
        'tech': '<g><rect x="60" y="50" width="30" height="35" fill="white" opacity="0.9" rx="3"/><rect x="63" y="53" width="24" height="18" fill="#2575fc"/><circle cx="75" cy="87" r="2" fill="white" opacity="0.9"/></g>',
        'coffee': '<g><path d="M65 50 Q65 45 70 45 L75 45 Q80 45 80 50 L80 75 Q80 80 75 80 L70 80 Q65 80 65 75 Z" fill="white" opacity="0.9" stroke="#2575fc" stroke-width="1.5"/><path d="M80 55 Q85 55 87 58 Q85 65 80 65" fill="none" stroke="white" opacity="0.9" stroke-width="1.5"/></g>',
        'food': '<g><path d="M60 75 L90 75 L85 50 Q80 45 75 45 Q70 45 65 50 Z" fill="white" opacity="0.9"/><circle cx="72" cy="65" r="2" fill="#2575fc"/><circle cx="78" cy="60" r="2" fill="#2575fc"/><circle cx="85" cy="68" r="2" fill="#2575fc"/></g>',
        'fitness': '<g><rect x="65" y="60" width="20" height="3" fill="white" opacity="0.9"/><circle cx="60" cy="62" r="4" fill="white" opacity="0.9"/><circle cx="90" cy="62" r="4" fill="white" opacity="0.9"/><path d="M75 45 L75 80" stroke="white" stroke-width="2" opacity="0.9"/></g>',
        'crypto': '<g><circle cx="75" cy="62" r="15" fill="white" opacity="0.8" stroke="#2575fc" stroke-width="1.5"/><text x="75" y="68" font-size="16" font-weight="bold" fill="#2575fc" text-anchor="middle">₿</text></g>',
        'fashion': '<g><path d="M65 48 L70 55 L80 55 L85 48 L83 55 L82 80 L68 80 L67 55 Z" fill="white" opacity="0.9"/><circle cx="75" cy="50" r="3" fill="white" opacity="0.9"/></g>',
        'health': '<g><path d="M75 50 L75 80 M60 65 L90 65" stroke="white" stroke-width="3" opacity="0.9" stroke-linecap="round"/></g>',
        'travel': '<g><path d="M60 70 L90 70 L85 55 L65 55 Z" fill="white" opacity="0.8"/><polygon points="75,50 72,55 78,55" fill="white" opacity="0.9"/></g>',
        'music': '<g><ellipse cx="65" cy="70" rx="3" ry="5" fill="white" opacity="0.9"/><path d="M68 65 Q75 55 82 65 L82 75 Q75 82 68 75" fill="white" opacity="0.8"/></g>',
        'ai': '<g><circle cx="70" cy="60" r="4" fill="white" opacity="0.9"/><circle cx="80" cy="60" r="4" fill="white" opacity="0.9"/><circle cx="75" cy="72" r="4" fill="white" opacity="0.9"/><line x1="70" y1="64" x2="75" y2="68" stroke="white" stroke-width="1.5" opacity="0.9"/><line x1="80" y1="64" x2="75" y2="68" stroke="white" stroke-width="1.5" opacity="0.9"/></g>',
    }
    
    # Match keyword to icon
    for key, icon in icons.items():
        if key in keyword:
            return icon
    
    # Default generic icon (lightbulb for ideas/innovation)
    return '<g><circle cx="75" cy="60" r="10" fill="white" opacity="0.8"/><path d="M75 50 L75 48" stroke="white" stroke-width="1.5" opacity="0.9"/><path d="M70 72 L80 72 L79 75 L71 75" fill="white" opacity="0.8"/></g>'

@app.route('/generate-marketing')
@require_api_key
def generate_marketing():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({'error': 'Keyword required'}), 400
    
    # Mock marketing ideas
    ideas = [
        f"Create social media campaigns highlighting {keyword}'s unique features",
        f"Partner with influencers in the {keyword} niche",
        f"Launch targeted email marketing to potential {keyword} customers",
        f"Develop content marketing around {keyword} success stories",
        f"Run paid ads focusing on {keyword} benefits"
    ]
    return jsonify({'ideas': ideas})


@app.route('/generate-names')
@require_api_key
def generate_names():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({'error': 'Keyword required'}), 400
    
    names = [
        f"{keyword}Hub",
        f"{keyword}Pro",
        f"{keyword}AI",
        f"{keyword}Tech",
        f"{keyword}Solutions"
    ]
    # create short, inspirational taglines for each name
    taglines = [
        f"empower your {keyword}",
        f"{keyword} meets innovation",
        f"future of {keyword}",
        f"{keyword} success partner",
        f"transform {keyword} ideas"
    ]
    
    # Add useful information for each brand
    personalities = [
        "Community-driven, accessible, reliable",
        "Premium, professional, cutting-edge",
        "Intelligent, futuristic, data-focused",
        "Innovative, agile, forward-thinking",
        "Comprehensive, scalable, enterprise-grade"
    ]
    
    target_audiences = [
        "Small businesses, startups, individuals",
        "Mid-market companies, professionals",
        "Tech enthusiasts, early adopters",
        "Growth-focused teams, innovators",
        "Enterprise clients, large organizations"
    ]
    
    positioning = [
        "Community platform, hub for collaboration",
        "Premium service, professional choice",
        "AI-powered intelligence, smart solutions",
        "Technology-first approach, modern tools",
        "All-in-one solutions, scalable platform"
    ]
    
    social_handles = [
        f"@{keyword}hub, #{keyword}hub",
        f"@{keyword}pro, #{keyword}pro",
        f"@{keyword}ai, #{keyword}ai",
        f"@{keyword}tech, #{keyword}tech",
        f"@{keyword}solutions, #{keyword}solutions"
    ]
    
    domain_suggestions = [
        f"{keyword}hub.com, thehub{keyword}.com",
        f"{keyword}pro.io, pro{keyword}.io",
        f"{keyword}ai.tech, {keyword}intelligence.io",
        f"{keyword}tech.io, {keyword}platform.io",
        f"{keyword}solutions.io, smart{keyword}.io"
    ]
    
    paired = []
    for i, (name, tagline) in enumerate(zip(names, taglines)):
        paired.append({
            'name': name,
            'tagline': tagline,
            'personality': personalities[i],
            'audience': target_audiences[i],
            'positioning': positioning[i],
            'social_handles': social_handles[i],
            'domains': domain_suggestions[i]
        })
    
    return jsonify({'brands': paired})


if __name__ == '__main__':
    # bind to all network interfaces so the server is reachable externally
    app.run(debug=True, port=3000, host='0.0.0.0')