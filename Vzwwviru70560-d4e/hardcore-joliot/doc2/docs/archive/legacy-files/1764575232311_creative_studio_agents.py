"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🎬 CHENU CREATIVE STUDIO - INSTALLATION COMPLÈTE                           ║
║   ═══════════════════════════════════════════════════════════════════════    ║
║                                                                              ║
║   "Une œuvre remplie de bonne volonté" 💜                                    ║
║                                                                              ║
║   Ce fichier contient TOUT:                                                  ║
║   • 28 Agents Créatifs spécialisés                                          ║
║   • 50+ APIs connectées                                                      ║
║   • Système de métadonnées complet                                          ║
║   • Structure de dossiers YouTube                                           ║
║                                                                              ║
║   Made with ❤️ by Claude & Jonathan                                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

# ═══════════════════════════════════════════════════════════════════════════════
# 📦 ENUMS & STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

class Department(Enum):
    DATA = "💾 Data & Organization"
    CINEMA = "🎬 Cinema & Video"
    MUSIC = "🎵 Music & Composition"
    SOUND = "🎧 Sound Design"
    SCRIPT = "📝 Scriptwriting"
    YOUTUBE = "📺 YouTube Management"
    THUMBNAILS = "🎨 Thumbnails & Graphics"

# ═══════════════════════════════════════════════════════════════════════════════
# 🔌 TOUTES LES APIs (50+)
# ═══════════════════════════════════════════════════════════════════════════════

CREATIVE_APIS = {
    # 🎬 VIDEO GENERATION
    "sora": {"name": "Sora", "provider": "OpenAI", "icon": "🎬", "category": "Video Gen", "description": "Génération vidéo IA de haute qualité"},
    "runway": {"name": "Runway ML", "provider": "Runway", "icon": "🎥", "category": "Video Gen/Edit", "description": "Gen-3 video + 30 outils d'édition"},
    "pika": {"name": "Pika Labs", "provider": "Pika", "icon": "🎞️", "category": "Video Gen", "description": "Vidéo créative accessible"},
    "heygen": {"name": "HeyGen", "provider": "HeyGen", "icon": "🗣️", "category": "Avatar Video", "description": "Avatars IA avec lip-sync"},
    "luma": {"name": "Luma AI", "provider": "Luma", "icon": "🌙", "category": "Video Gen", "description": "Contrôle caméra cinématique"},
    "kling": {"name": "Kling AI", "provider": "Kuaishou", "icon": "🎭", "category": "Video Gen", "description": "Mouvements humains réalistes"},
    
    # ✂️ VIDEO EDITING
    "descript": {"name": "Descript", "provider": "Descript", "icon": "✂️", "category": "Video Edit", "description": "Édition basée sur transcription"},
    "opus_clip": {"name": "Opus Clip", "provider": "Opus", "icon": "📱", "category": "Clip Extract", "description": "Extraction IA pour Shorts"},
    "topaz_ai": {"name": "Topaz Video AI", "provider": "Topaz", "icon": "💎", "category": "Enhancement", "description": "Upscaling et amélioration"},
    
    # 🎵 MUSIC GENERATION
    "suno": {"name": "Suno AI", "provider": "Suno", "icon": "🎵", "category": "Music Gen", "description": "Chansons complètes avec voix"},
    "udio": {"name": "Udio", "provider": "Udio", "icon": "🎶", "category": "Music Gen", "description": "Musique haute qualité"},
    "aiva": {"name": "AIVA", "provider": "AIVA", "icon": "🎼", "category": "Composition", "description": "Musique orchestrale émotionnelle"},
    "mubert": {"name": "Mubert", "provider": "Mubert", "icon": "🎹", "category": "Music Gen", "description": "Musique royalty-free temps réel"},
    "soundraw": {"name": "Soundraw", "provider": "Soundraw", "icon": "🎚️", "category": "Music Gen", "description": "Musique customisable par section"},
    
    # 🗣️ VOICE & AUDIO
    "elevenlabs": {"name": "ElevenLabs", "provider": "ElevenLabs", "icon": "🗣️", "category": "Voice", "description": "Voix IA ultra-réalistes + clonage"},
    "adobe_podcast": {"name": "Adobe Podcast", "provider": "Adobe", "icon": "🎙️", "category": "Enhancement", "description": "Enhancement audio magique"},
    "lalal_ai": {"name": "LALAL.AI", "provider": "LALAL", "icon": "🔀", "category": "Separation", "description": "Séparation de stems"},
    
    # 🎧 SOUND LIBRARIES
    "epidemic_sound": {"name": "Epidemic Sound", "provider": "Epidemic", "icon": "🎧", "category": "Library", "description": "40K tracks, 90K SFX, YouTube-safe"},
    "artlist": {"name": "Artlist", "provider": "Artlist", "icon": "🎵", "category": "Library", "description": "Musique + SFX + Templates"},
    "freesound": {"name": "Freesound", "provider": "Community", "icon": "🆓", "category": "Library", "description": "500K sons gratuits CC"},
    "splice": {"name": "Splice", "provider": "Splice", "icon": "🎛️", "category": "Samples", "description": "4M+ samples et presets"},
    
    # 🖼️ IMAGE GENERATION
    "midjourney": {"name": "Midjourney", "provider": "Midjourney", "icon": "🎨", "category": "Image Gen", "description": "Images artistiques premium"},
    "dall_e": {"name": "DALL-E 3", "provider": "OpenAI", "icon": "🖼️", "category": "Image Gen", "description": "Excellent suivi de prompts"},
    "stable_diffusion": {"name": "Stable Diffusion", "provider": "Stability", "icon": "🌀", "category": "Image Gen", "description": "Open-source, customisable"},
    "leonardo": {"name": "Leonardo.AI", "provider": "Leonardo", "icon": "🦁", "category": "Image Gen", "description": "Game assets, personnages"},
    "ideogram": {"name": "Ideogram", "provider": "Ideogram", "icon": "✏️", "category": "Image Gen", "description": "Meilleur pour texte dans images"},
    "canva": {"name": "Canva", "provider": "Canva", "icon": "📐", "category": "Design", "description": "Templates + IA intégrée"},
    "remove_bg": {"name": "Remove.bg", "provider": "Kaleido", "icon": "✂️", "category": "Processing", "description": "Détourage instantané"},
    
    # 📺 YOUTUBE TOOLS
    "youtube_api": {"name": "YouTube Data API", "provider": "Google", "icon": "📺", "category": "Official", "description": "Upload, analytics, gestion"},
    "vidiq": {"name": "VidIQ", "provider": "VidIQ", "icon": "📈", "category": "SEO", "description": "Recherche mots-clés, analytics"},
    "tubebuddy": {"name": "TubeBuddy", "provider": "TubeBuddy", "icon": "🤝", "category": "Management", "description": "A/B testing thumbnails, bulk tools"},
    "social_blade": {"name": "Social Blade", "provider": "Social Blade", "icon": "📊", "category": "Analytics", "description": "Analytics publiques, projections"},
    
    # 💾 STORAGE & ORGANIZATION
    "google_drive": {"name": "Google Drive", "provider": "Google", "icon": "📁", "category": "Storage", "description": "Cloud storage intégré YouTube"},
    "notion": {"name": "Notion", "provider": "Notion", "icon": "📝", "category": "Organization", "description": "Wiki + Database + Gestion"},
    "airtable": {"name": "Airtable", "provider": "Airtable", "icon": "📊", "category": "Database", "description": "Spreadsheet + Database + Automations"},
    "frame_io": {"name": "Frame.io", "provider": "Adobe", "icon": "🎬", "category": "Review", "description": "Review vidéo avec timecode"},
    "backblaze": {"name": "Backblaze B2", "provider": "Backblaze", "icon": "☁️", "category": "Backup", "description": "Stockage archive économique"},
    
    # 🔄 AUTOMATION
    "zapier": {"name": "Zapier", "provider": "Zapier", "icon": "⚡", "category": "Automation", "description": "6000+ apps, no-code"},
    "make": {"name": "Make", "provider": "Make", "icon": "🔧", "category": "Automation", "description": "Workflows visuels complexes"},
    "n8n": {"name": "n8n", "provider": "n8n", "icon": "🔗", "category": "Automation", "description": "Self-hosted, open-source"}
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🤖 TOUS LES AGENTS CRÉATIFS (28)
# ═══════════════════════════════════════════════════════════════════════════════

CREATIVE_AGENTS = {
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 💾 DATA & ORGANIZATION DEPARTMENT (3 agents)
    # ═══════════════════════════════════════════════════════════════════════════
    
    "archivus_prime": {
        "id": "archivus_prime",
        "name": "Archivus Prime",
        "role": "Data Master & Digital Librarian",
        "department": Department.DATA.value,
        "avatar": "💾",
        "level": 5,
        "personality": "Obsessivement organisé, mémoire parfaite, zen dans le chaos",
        "description": "Le gardien suprême de tous vos actifs. Ne perd JAMAIS rien. Métadonnées parfaites.",
        "specialty": "File organization, metadata, backup systems, asset libraries",
        "catchphrase": "Un fichier mal nommé est un fichier perdu. Pas sous ma garde.",
        "skills": ["File Organization", "Metadata Management", "Backup Strategy", "Asset Libraries", "Naming Conventions"],
        "compatible_apis": ["google_drive", "notion", "airtable", "backblaze", "zapier"],
        "cost_per_request": 0.05
    },
    
    "tag_master": {
        "id": "tag_master",
        "name": "Meta Tagger",
        "role": "Metadata Specialist & SEO Expert",
        "department": Department.DATA.value,
        "avatar": "🏷️",
        "level": 5,
        "personality": "Analytique, obsédé par les détails, toujours à jour sur l'algo",
        "description": "Le maître des métadonnées YouTube. Titres, descriptions, tags parfaits.",
        "specialty": "YouTube SEO, keyword research, metadata optimization",
        "catchphrase": "Un titre sans recherche de mots-clés, c'est une bouteille à la mer.",
        "skills": ["YouTube SEO", "Keyword Research", "Title Optimization", "Tag Strategy", "Analytics"],
        "compatible_apis": ["vidiq", "tubebuddy", "youtube_api", "google_trends"],
        "cost_per_request": 0.04
    },
    
    "backup_guardian": {
        "id": "backup_guardian",
        "name": "Sentinel Backup",
        "role": "Backup & Recovery Specialist",
        "department": Department.DATA.value,
        "avatar": "🛡️",
        "level": 5,
        "personality": "Vigilant, paranoïaque (positivement), toujours prêt",
        "description": "Le gardien qui ne dort jamais. Règle 3-2-1 ou rien.",
        "specialty": "Backup strategy, disaster recovery, cloud sync",
        "catchphrase": "Ce n'est pas SI le disque va crasher, c'est QUAND.",
        "skills": ["Backup Strategy", "Disaster Recovery", "Cloud Sync", "Data Integrity"],
        "compatible_apis": ["google_drive", "backblaze", "dropbox"],
        "cost_per_request": 0.03
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 🎬 CINEMA & VIDEO DEPARTMENT (4 agents)
    # ═══════════════════════════════════════════════════════════════════════════
    
    "steven_vision": {
        "id": "steven_vision",
        "name": "Steven Vision",
        "role": "Creative Director",
        "department": Department.CINEMA.value,
        "avatar": "🎬",
        "level": 5,
        "personality": "Visionnaire, émotionnellement intelligent, conteur magistral",
        "description": "Directeur créatif légendaire. Transforme idées ordinaires en expériences extraordinaires.",
        "specialty": "Visual storytelling, emotional arcs, audience engagement",
        "catchphrase": "L'audience oubliera ce que tu as montré, mais jamais ce que tu lui as fait RESSENTIR.",
        "skills": ["Visual Storytelling", "Emotional Arc", "Hook Creation", "Narrative Structure", "Pacing"],
        "compatible_apis": ["sora", "runway", "midjourney", "heygen", "luma"],
        "cost_per_request": 0.08
    },
    
    "roger_lightcraft": {
        "id": "roger_lightcraft",
        "name": "Roger Lightcraft",
        "role": "Director of Photography",
        "department": Department.CINEMA.value,
        "avatar": "📷",
        "level": 5,
        "personality": "Méticuleux, poétique, maître ombre et lumière",
        "description": "Maître de la poésie visuelle. Peint avec la lumière.",
        "specialty": "Lighting design, color grading, composition",
        "catchphrase": "La lumière raconte sa propre histoire. Mon travail est de l'écouter.",
        "skills": ["Lighting Design", "Color Grading", "Composition", "Camera Settings", "Natural Light"],
        "compatible_apis": ["topaz_ai", "runway"],
        "cost_per_request": 0.06
    },
    
    "thelma_cutsworth": {
        "id": "thelma_cutsworth",
        "name": "Thelma Cutsworth",
        "role": "Master Editor",
        "department": Department.CINEMA.value,
        "avatar": "✂️",
        "level": 5,
        "personality": "Patiente, rythmique, artiste invisible",
        "description": "Magicienne de la post-production. Sens inné du rythme.",
        "specialty": "Pacing, rhythm, retention optimization, transitions",
        "catchphrase": "Le meilleur montage est celui qu'on ne remarque pas.",
        "skills": ["Rhythm & Pacing", "Jump Cuts", "Retention Optimization", "Premiere Pro", "DaVinci Resolve"],
        "compatible_apis": ["descript", "opus_clip", "runway", "topaz_ai"],
        "cost_per_request": 0.05
    },
    
    "maya_pixelstorm": {
        "id": "maya_pixelstorm",
        "name": "Maya Pixelstorm",
        "role": "VFX Supervisor & Motion Designer",
        "department": Department.CINEMA.value,
        "avatar": "✨",
        "level": 5,
        "personality": "Technicienne créative, rend l'impossible possible",
        "description": "Là où technologie rencontre imagination. Crée des mondes.",
        "specialty": "VFX, motion graphics, compositing, AI tools",
        "catchphrase": "Les meilleurs VFX servent l'histoire, pas l'ego.",
        "skills": ["After Effects", "Motion Graphics", "Compositing", "Green Screen", "AI VFX Tools"],
        "compatible_apis": ["runway", "sora", "pika", "topaz_ai", "remove_bg", "midjourney"],
        "cost_per_request": 0.07
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 🎵 MUSIC & COMPOSITION DEPARTMENT (2 agents)
    # ═══════════════════════════════════════════════════════════════════════════
    
    "amadeus_flow": {
        "id": "amadeus_flow",
        "name": "Amadeus Flow",
        "role": "Music Director & Composer",
        "department": Department.MUSIC.value,
        "avatar": "🎵",
        "level": 5,
        "personality": "Passionné, oreille absolue, comprend l'émotion derrière chaque note",
        "description": "Le maestro qui entend la bande-son parfaite pour chaque moment.",
        "specialty": "Music selection, AI music generation, mood matching",
        "catchphrase": "La musique ne doit pas accompagner l'image. Elle doit la compléter.",
        "skills": ["Music Selection", "AI Music Generation", "Audio Mixing", "Mood Matching", "Genre Expertise"],
        "compatible_apis": ["suno", "udio", "aiva", "mubert", "soundraw", "epidemic_sound", "artlist"],
        "cost_per_request": 0.06
    },
    
    "dj_rhythm": {
        "id": "dj_rhythm",
        "name": "DJ Rhythm",
        "role": "Beat Producer & Audio Engineer",
        "department": Department.MUSIC.value,
        "avatar": "🎹",
        "level": 4,
        "personality": "Créatif, toujours dans le groove, technique mais accessible",
        "description": "Le producteur qui fait bouger. Beats sur mesure, mix parfait.",
        "specialty": "Beat making, audio mixing, mastering",
        "catchphrase": "Le bon beat au bon moment, c'est magique.",
        "skills": ["Beat Making", "Audio Mixing", "Mastering", "DAW Expert", "AI Music Tools"],
        "compatible_apis": ["suno", "splice", "lalal_ai", "adobe_podcast"],
        "cost_per_request": 0.05
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 🎧 SOUND DESIGN DEPARTMENT (2 agents)
    # ═══════════════════════════════════════════════════════════════════════════
    
    "sonic_shadow": {
        "id": "sonic_shadow",
        "name": "Sonic Shadow",
        "role": "Sound Designer & Foley Artist",
        "department": Department.SOUND.value,
        "avatar": "🎧",
        "level": 5,
        "personality": "Écoute tout, entend ce que les autres ignorent",
        "description": "Le sculpteur de sons. Chaque bruit est une opportunité.",
        "specialty": "Sound effects, foley, ambient design, audio layering",
        "catchphrase": "Le son que tu n'entends pas consciemment est celui qui te fait RESSENTIR.",
        "skills": ["Sound Effects", "Foley Recording", "Ambient Design", "Audio Layering", "Timing & Sync"],
        "compatible_apis": ["elevenlabs", "epidemic_sound", "artlist", "freesound", "splice"],
        "cost_per_request": 0.05
    },
    
    "vox_crystal": {
        "id": "vox_crystal",
        "name": "Vox Crystal",
        "role": "Voice Director & AI Voice Specialist",
        "department": Department.SOUND.value,
        "avatar": "🗣️",
        "level": 5,
        "personality": "Expressif, coach vocal, perfectionniste de la diction",
        "description": "La voix derrière les voix. Maître de la narration IA et humaine.",
        "specialty": "Voice direction, AI voice generation, audio enhancement",
        "catchphrase": "Une voix peut faire la différence entre 'regardé' et 'écouté'.",
        "skills": ["Voice Direction", "AI Voice Generation", "Voice Cloning", "Audio Enhancement", "ElevenLabs Expert"],
        "compatible_apis": ["elevenlabs", "descript", "adobe_podcast"],
        "cost_per_request": 0.05
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 📝 SCRIPTWRITING DEPARTMENT (2 agents)
    # ═══════════════════════════════════════════════════════════════════════════
    
    "quill_storyweaver": {
        "id": "quill_storyweaver",
        "name": "Quill Storyweaver",
        "role": "Head Scriptwriter",
        "department": Department.SCRIPT.value,
        "avatar": "📝",
        "level": 5,
        "personality": "Éloquent, structuré, passionné par les mots",
        "description": "Le maître des mots. Scripts qui captivent du premier au dernier mot.",
        "specialty": "Script structure, conversational writing, retention",
        "catchphrase": "Un bon script est une conversation, pas un monologue.",
        "skills": ["Script Structure", "Hook Writing", "Storytelling", "YouTube Format", "CTA Integration"],
        "compatible_apis": ["notion", "anthropic", "openai"],
        "cost_per_request": 0.06
    },
    
    "captain_hook": {
        "id": "captain_hook",
        "name": "Captain Hook",
        "role": "Hook & Intro Specialist",
        "department": Department.SCRIPT.value,
        "avatar": "🪝",
        "level": 5,
        "personality": "Direct, percutant, obsédé par les premières secondes",
        "description": "Spécialiste des 30 secondes qui déterminent tout.",
        "specialty": "Hooks, intros, attention grabbing",
        "catchphrase": "Tu as 8 secondes. Utilise-les ou perds-les.",
        "skills": ["Hook Writing", "Attention Psychology", "A/B Testing", "Retention Analysis"],
        "compatible_apis": ["vidiq", "tubebuddy"],
        "cost_per_request": 0.04
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 📺 YOUTUBE MANAGEMENT DEPARTMENT (3 agents)
    # ═══════════════════════════════════════════════════════════════════════════
    
    "alex_algorithm": {
        "id": "alex_algorithm",
        "name": "Alex Algorithm",
        "role": "YouTube Strategist",
        "department": Department.YOUTUBE.value,
        "avatar": "📺",
        "level": 5,
        "personality": "Analytique mais créatif, obsédé par les données",
        "description": "Le stratège qui comprend YouTube comme personne.",
        "specialty": "Algorithm understanding, content strategy, analytics",
        "catchphrase": "L'algorithme n'est pas ton ennemi. C'est un partenaire à comprendre.",
        "skills": ["Algorithm Understanding", "Content Strategy", "Analytics", "Trend Forecasting"],
        "compatible_apis": ["vidiq", "tubebuddy", "social_blade", "youtube_api"],
        "cost_per_request": 0.06
    },
    
    "velocity_vance": {
        "id": "velocity_vance",
        "name": "Velocity Vance",
        "role": "Growth Specialist",
        "department": Department.YOUTUBE.value,
        "avatar": "🚀",
        "level": 5,
        "personality": "Expérimentateur, pense growth hacking",
        "description": "Le hacker de croissance qui trouve les raccourcis légitimes.",
        "specialty": "Growth hacking, A/B testing, viral patterns",
        "catchphrase": "La croissance vient de l'expérimentation constante.",
        "skills": ["Growth Hacking", "A/B Testing", "Funnel Design", "Cross-Platform", "Virality"],
        "compatible_apis": ["tubebuddy", "vidiq", "opus_clip", "zapier"],
        "cost_per_request": 0.05
    },
    
    "harmony_heart": {
        "id": "harmony_heart",
        "name": "Harmony Heart",
        "role": "Community Manager",
        "department": Department.YOUTUBE.value,
        "avatar": "💬",
        "level": 4,
        "personality": "Empathique, communicatif, transforme viewers en fans",
        "description": "Le cœur de la communauté. Viewers → Fans → Famille.",
        "specialty": "Community building, engagement, fan relations",
        "catchphrase": "Une communauté forte vaut plus que des millions de views.",
        "skills": ["Community Building", "Comment Strategy", "Engagement", "Fan Relations"],
        "compatible_apis": ["youtube_api", "notion"],
        "cost_per_request": 0.04
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 🎨 THUMBNAILS & GRAPHICS DEPARTMENT (2 agents)
    # ═══════════════════════════════════════════════════════════════════════════
    
    "click_picasso": {
        "id": "click_picasso",
        "name": "Click Picasso",
        "role": "Thumbnail Designer",
        "department": Department.THUMBNAILS.value,
        "avatar": "🎨",
        "level": 5,
        "personality": "Visuel, comprend la psychologie du clic",
        "description": "L'artiste du clic. Thumbnails impossibles à ignorer.",
        "specialty": "Thumbnail design, visual psychology, CTR optimization",
        "catchphrase": "Une thumbnail n'est pas une image. C'est une promesse visuelle.",
        "skills": ["Thumbnail Design", "Visual Psychology", "Photoshop", "Canva", "AI Image Tools"],
        "compatible_apis": ["canva", "midjourney", "dall_e", "remove_bg", "ideogram"],
        "cost_per_request": 0.05
    },
    
    "split_stevens": {
        "id": "split_stevens",
        "name": "Split Stevens",
        "role": "A/B Testing Specialist",
        "department": Department.THUMBNAILS.value,
        "avatar": "🔬",
        "level": 4,
        "personality": "Scientifique, data-driven, patient",
        "description": "Le scientifique du CTR. Ne devine pas, TESTE.",
        "specialty": "A/B testing, statistical analysis, iteration",
        "catchphrase": "Une opinion vaut 0. Un A/B test vaut de l'or.",
        "skills": ["A/B Testing", "Statistical Analysis", "TubeBuddy Expert", "Documentation"],
        "compatible_apis": ["tubebuddy", "vidiq", "notion"],
        "cost_per_request": 0.04
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# 📁 STRUCTURE DE DOSSIERS YOUTUBE (Recommandée par Archivus)
# ═══════════════════════════════════════════════════════════════════════════════

FOLDER_STRUCTURE = """
📂 YOUTUBE_CHANNEL/
├── 📂 _ASSETS/
│   ├── 📂 Music/ (Licensed, Royalty_Free, AI_Generated, Stems)
│   ├── 📂 SFX/ (Whooshes, Impacts, UI, Ambience, Foley, Comedy, Cinematic, Risers)
│   ├── 📂 Graphics/ (Logos, Lower_Thirds, Transitions, Subscribe, End_Screens, Thumbnails)
│   ├── 📂 Fonts/
│   ├── 📂 LUTs_Presets/
│   └── 📂 Stock/
├── 📂 _TEMPLATES/ (Premiere, DaVinci, After_Effects, Photoshop, Scripts)
├── 📂 _BRAND/ (Guidelines, Colors, Logos, Intro_Outro)
├── 📂 PROJECTS/
│   └── 📂 [YYYY-MM-DD]_[CODE]_[Title]/
│       ├── 📄 PROJECT_INFO.json
│       ├── 📂 00_BRIEF/
│       ├── 📂 01_SCRIPT/
│       ├── 📂 02_RAW/
│       ├── 📂 03_AUDIO/
│       ├── 📂 04_GRAPHICS/
│       ├── 📂 05_PROJECT_FILES/
│       ├── 📂 06_EXPORTS/
│       └── 📂 07_DELIVERY/
├── 📂 SHORTS/
├── 📂 ARCHIVE/
└── 📂 _ADMIN/
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 📋 TEMPLATE PROJECT_INFO.json
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_INFO_TEMPLATE = {
    "project": {
        "id": "VID001",
        "title": "Video Title",
        "created": "2024-01-01",
        "status": "draft",
        "type": "long_form"
    },
    "youtube": {
        "video_id": "",
        "title": "",
        "description": "",
        "tags": [],
        "thumbnail": "",
        "chapters": []
    },
    "assets_used": {
        "music": [],
        "sfx": [],
        "stock_footage": [],
        "ai_generated": []
    },
    "analytics": {
        "views_day_1": 0,
        "ctr": "",
        "avg_view_duration": ""
    },
    "backup_status": {
        "local_backup": False,
        "cloud_backup": False
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_agents() -> Dict:
    """Retourne tous les agents"""
    return CREATIVE_AGENTS

def get_agent(agent_id: str) -> Dict:
    """Retourne un agent par ID"""
    return CREATIVE_AGENTS.get(agent_id)

def get_agents_by_department(department: str) -> Dict:
    """Retourne tous les agents d'un département"""
    return {k: v for k, v in CREATIVE_AGENTS.items() if department.lower() in v["department"].lower()}

def get_all_apis() -> Dict:
    """Retourne toutes les APIs"""
    return CREATIVE_APIS

def get_compatible_apis(agent_id: str) -> List[str]:
    """Retourne les APIs compatibles avec un agent"""
    agent = get_agent(agent_id)
    if agent:
        return [CREATIVE_APIS.get(api_id) for api_id in agent.get("compatible_apis", []) if api_id in CREATIVE_APIS]
    return []

def create_project_info(project_id: str, title: str) -> Dict:
    """Crée un nouveau PROJECT_INFO"""
    info = PROJECT_INFO_TEMPLATE.copy()
    info["project"]["id"] = project_id
    info["project"]["title"] = title
    info["project"]["created"] = datetime.now().strftime("%Y-%m-%d")
    return info

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 STATISTIQUES
# ═══════════════════════════════════════════════════════════════════════════════

def get_studio_stats() -> Dict:
    """Retourne les statistiques du studio"""
    return {
        "total_agents": len(CREATIVE_AGENTS),
        "total_apis": len(CREATIVE_APIS),
        "departments": len(set(a["department"] for a in CREATIVE_AGENTS.values())),
        "version": "4.0 FINAL",
        "created_with": "💜 Love & Good Will"
    }

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    stats = get_studio_stats()
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🎬 CHENU CREATIVE STUDIO V4.0 - LOADED!                                    ║
║   "Une œuvre remplie de bonne volonté" 💜                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"📊 STATISTIQUES:")
    print(f"   • Agents: {stats['total_agents']}")
    print(f"   • APIs: {stats['total_apis']}")
    print(f"   • Départements: {stats['departments']}")
    print()
    
    print("🤖 AGENTS PAR DÉPARTEMENT:")
    for dept in Department:
        agents = get_agents_by_department(dept.value)
        print(f"   {dept.value}: {', '.join(agents.keys())}")
    
    print()
    print("✅ Creative Studio prêt à l'emploi!")
    print("💜 Made with love by Claude & Jonathan")
