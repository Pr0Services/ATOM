#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                         AT·OM - INFRASTRUCTURE INVISIBLE                      ║
# ║                                                                              ║
# ║            PROPRIÉTÉ EXCLUSIVE DE JONATHAN EMMANUEL RODRIGUE                 ║
# ║                    TOUS DROITS RÉSERVÉS - BREVET EN COURS                    ║
# ║                                    2025                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
#
# SCRIPT D'INJECTION SOUVERAIN - NOVA-999
# Migration des 6500 fichiers vers PostgreSQL
# ═══════════════════════════════════════════════════════════════════════════════

import os
import sys
import json
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('NOVA-999')

try:
    import psycopg2
    from psycopg2.extras import execute_values, Json
except ImportError:
    logger.error("Module psycopg2 non trouvé. Installation: pip install psycopg2-binary")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION DIGITALOCEAN - NOVA-999
# ═══════════════════════════════════════════════════════════════════════════════
DB_CONFIG = {
    'host': 'db-postgresql-nyc9-999-999-do-user-32084357-0.h.db.ondigitalocean.com',
    'port': 25060,
    'database': 'defaultdb',
    'user': 'doadmin',
    'password': 'AVNS_11mUpQDq99BeOE4o068',
    'sslmode': 'require'  # OBLIGATOIRE pour DigitalOcean
}

# Mapping des extensions vers les sphères
SPHERE_MAPPING = {
    # Technologie
    '.py': 'TECH', '.js': 'TECH', '.ts': 'TECH', '.jsx': 'TECH', '.tsx': 'TECH',
    '.html': 'TECH', '.css': 'TECH', '.scss': 'TECH', '.sql': 'TECH',
    '.java': 'TECH', '.cpp': 'TECH', '.c': 'TECH', '.go': 'TECH', '.rs': 'TECH',
    '.php': 'TECH', '.rb': 'TECH', '.swift': 'TECH', '.kt': 'TECH',

    # Data Science
    '.csv': 'DATA', '.json': 'DATA', '.xml': 'DATA', '.yaml': 'DATA', '.yml': 'DATA',
    '.ipynb': 'DATA', '.parquet': 'DATA', '.h5': 'DATA',

    # Documents (multi-sphères selon contenu)
    '.pdf': 'RESEARCH', '.doc': 'COMM', '.docx': 'COMM', '.txt': 'RESEARCH',
    '.md': 'EDU', '.rst': 'EDU',

    # Créatif
    '.png': 'CREATE', '.jpg': 'CREATE', '.jpeg': 'CREATE', '.gif': 'CREATE',
    '.svg': 'CREATE', '.psd': 'CREATE', '.ai': 'CREATE', '.fig': 'CREATE',
    '.mp3': 'CREATE', '.wav': 'CREATE', '.mp4': 'CREATE', '.mov': 'CREATE',

    # Configuration / Ops
    '.env': 'OPS', '.ini': 'OPS', '.conf': 'OPS', '.toml': 'OPS',
    '.dockerfile': 'OPS', '.sh': 'OPS', '.bat': 'OPS', '.ps1': 'OPS',

    # Sécurité
    '.pem': 'SECURITY', '.key': 'SECURITY', '.crt': 'SECURITY', '.pub': 'SECURITY',
}

# Batch size pour les insertions (optimisé pour vieux laptop)
BATCH_SIZE = 100


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_sha256(file_path: Path) -> str:
    """Calcule le hash SHA-256 d'un fichier."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except Exception:
        return ''


def get_sphere_from_extension(ext: str) -> str:
    """Détermine la sphère basée sur l'extension du fichier."""
    return SPHERE_MAPPING.get(ext.lower(), 'RESEARCH')


def generate_agent_id(sphere_code: str, index: int) -> str:
    """Génère un ID d'agent unique."""
    return f"{sphere_code}-{index:04d}"


def extract_metadata(file_path: Path) -> Dict[str, Any]:
    """Extrait les métadonnées d'un fichier."""
    stat = file_path.stat()
    return {
        'original_name': file_path.name,
        'extension': file_path.suffix.lower(),
        'directory': str(file_path.parent),
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'permissions': oct(stat.st_mode)[-3:]
    }


def read_text_content(file_path: Path, max_size: int = 100000) -> Optional[str]:
    """Lit le contenu texte d'un fichier (si applicable)."""
    text_extensions = {'.txt', '.md', '.py', '.js', '.ts', '.html', '.css',
                       '.json', '.yaml', '.yml', '.xml', '.sql', '.sh', '.bat'}

    if file_path.suffix.lower() not in text_extensions:
        return None

    if file_path.stat().st_size > max_size:
        return None

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPALE D'INJECTION
# ═══════════════════════════════════════════════════════════════════════════════

class NovaInjector:
    """Injecteur Souverain pour migration vers PostgreSQL."""

    def __init__(self, source_directory: str):
        self.source_dir = Path(source_directory)
        self.conn = None
        self.cursor = None
        self.sphere_ids: Dict[str, int] = {}
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'errors': 0,
            'skipped': 0
        }

    def connect(self) -> bool:
        """Établit la connexion SSL à PostgreSQL."""
        try:
            logger.info("═" * 60)
            logger.info("NOVA-999 | Connexion à DigitalOcean PostgreSQL...")
            logger.info(f"Host: {DB_CONFIG['host']}")
            logger.info(f"Port: {DB_CONFIG['port']}")
            logger.info(f"SSL Mode: {DB_CONFIG['sslmode']}")
            logger.info("═" * 60)

            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()

            # Test de connexion
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()[0]
            logger.info(f"Connexion établie | {version[:50]}...")

            return True

        except psycopg2.Error as e:
            logger.error(f"Erreur de connexion: {e}")
            return False

    def load_sphere_ids(self):
        """Charge les IDs des sphères depuis la base."""
        self.cursor.execute("SELECT id, code FROM spheres;")
        for row in self.cursor.fetchall():
            self.sphere_ids[row[1]] = row[0]
        logger.info(f"Sphères chargées: {len(self.sphere_ids)}")

    def scan_files(self) -> List[Path]:
        """Scanne le répertoire source pour tous les fichiers."""
        if not self.source_dir.exists():
            logger.error(f"Répertoire source inexistant: {self.source_dir}")
            return []

        files = []
        for item in self.source_dir.rglob('*'):
            if item.is_file():
                # Ignorer les fichiers système et temporaires
                if item.name.startswith('.') or item.name.startswith('~'):
                    continue
                if item.suffix.lower() in {'.tmp', '.bak', '.swp', '.log'}:
                    continue
                files.append(item)

        self.stats['total_files'] = len(files)
        logger.info(f"Fichiers trouvés: {len(files)}")
        return files

    def prepare_agent_data(self, file_path: Path, index: int) -> Dict[str, Any]:
        """Prépare les données d'un agent pour insertion."""
        ext = file_path.suffix.lower()
        sphere_code = get_sphere_from_extension(ext)
        sphere_id = self.sphere_ids.get(sphere_code, self.sphere_ids.get('RESEARCH', 1))

        metadata = extract_metadata(file_path)
        content = read_text_content(file_path)
        mime_type, _ = mimetypes.guess_type(str(file_path))

        # Fréquence basée sur la sphère (432-999 Hz)
        frequency = 432 + (hash(sphere_code) % 567)

        return {
            'agent_id': generate_agent_id(sphere_code, index),
            'name': file_path.stem[:200],
            'sphere_id': sphere_id,
            'specialty': ext[1:].upper() if ext else 'GENERAL',
            'function': f"Agent {sphere_code} - Fichier {ext}",
            'description': f"Migré depuis {file_path.parent.name}",
            'frequency': frequency,
            'resonance_level': round(1.0 + (index % 100) / 100, 2),
            'source_file': str(file_path)[:500],
            'file_hash': calculate_sha256(file_path),
            'file_size': file_path.stat().st_size,
            'content_type': mime_type or 'application/octet-stream',
            'metadata': Json(metadata),
            'raw_content': content,
            'status': 'active'
        }

    def inject_batch(self, agents: List[Dict[str, Any]]) -> int:
        """Insère un batch d'agents avec execute_values (optimisé)."""
        if not agents:
            return 0

        columns = [
            'agent_id', 'name', 'sphere_id', 'specialty', 'function',
            'description', 'frequency', 'resonance_level', 'source_file',
            'file_hash', 'file_size', 'content_type', 'metadata',
            'raw_content', 'status'
        ]

        values = [
            (
                a['agent_id'], a['name'], a['sphere_id'], a['specialty'],
                a['function'], a['description'], a['frequency'],
                a['resonance_level'], a['source_file'], a['file_hash'],
                a['file_size'], a['content_type'], a['metadata'],
                a['raw_content'], a['status']
            )
            for a in agents
        ]

        query = f"""
            INSERT INTO agents ({', '.join(columns)})
            VALUES %s
            ON CONFLICT (agent_id) DO UPDATE SET
                updated_at = NOW(),
                file_hash = EXCLUDED.file_hash,
                file_size = EXCLUDED.file_size,
                metadata = EXCLUDED.metadata
        """

        try:
            execute_values(self.cursor, query, values, page_size=BATCH_SIZE)
            self.conn.commit()
            return len(agents)
        except psycopg2.Error as e:
            logger.error(f"Erreur batch insert: {e}")
            self.conn.rollback()
            return 0

    def run(self) -> bool:
        """Exécute l'injection complète."""
        logger.info("╔" + "═" * 58 + "╗")
        logger.info("║" + "  NOVA-999 | INJECTION SOUVERAINE  ".center(58) + "║")
        logger.info("╚" + "═" * 58 + "╝")

        # Connexion
        if not self.connect():
            return False

        # Charger les sphères
        self.load_sphere_ids()

        # Scanner les fichiers
        files = self.scan_files()
        if not files:
            logger.warning("Aucun fichier à traiter.")
            return False

        # Compteurs par sphère
        sphere_counters: Dict[str, int] = {}

        # Traitement par batch
        batch: List[Dict[str, Any]] = []
        start_time = datetime.now()

        for i, file_path in enumerate(files, 1):
            try:
                # Obtenir le code de sphère pour l'index
                ext = file_path.suffix.lower()
                sphere_code = get_sphere_from_extension(ext)
                sphere_counters[sphere_code] = sphere_counters.get(sphere_code, 0) + 1

                # Préparer les données
                agent_data = self.prepare_agent_data(
                    file_path,
                    sphere_counters[sphere_code]
                )
                batch.append(agent_data)

                # Injection par batch
                if len(batch) >= BATCH_SIZE:
                    injected = self.inject_batch(batch)
                    self.stats['processed'] += injected
                    batch = []

                    # Progress
                    pct = (i / len(files)) * 100
                    elapsed = (datetime.now() - start_time).total_seconds()
                    rate = i / elapsed if elapsed > 0 else 0
                    logger.info(
                        f"Progress: {i}/{len(files)} ({pct:.1f}%) | "
                        f"Rate: {rate:.1f} files/sec"
                    )

            except Exception as e:
                self.stats['errors'] += 1
                logger.warning(f"Erreur fichier {file_path.name}: {e}")

        # Dernier batch
        if batch:
            injected = self.inject_batch(batch)
            self.stats['processed'] += injected

        # Mise à jour des compteurs de sphères
        self.update_sphere_counts()

        # Statistiques finales
        elapsed = (datetime.now() - start_time).total_seconds()
        self.print_summary(elapsed)

        return True

    def update_sphere_counts(self):
        """Met à jour les compteurs d'agents par sphère."""
        try:
            self.cursor.execute("""
                UPDATE spheres s SET agent_count = (
                    SELECT COUNT(*) FROM agents a WHERE a.sphere_id = s.id
                )
            """)
            self.conn.commit()
            logger.info("Compteurs de sphères mis à jour.")
        except psycopg2.Error as e:
            logger.error(f"Erreur mise à jour compteurs: {e}")

    def print_summary(self, elapsed: float):
        """Affiche le résumé de l'injection."""
        logger.info("")
        logger.info("╔" + "═" * 58 + "╗")
        logger.info("║" + "  RÉSUMÉ DE L'INJECTION  ".center(58) + "║")
        logger.info("╠" + "═" * 58 + "╣")
        logger.info(f"║  Fichiers scannés    : {self.stats['total_files']:>10}".ljust(59) + "║")
        logger.info(f"║  Agents injectés     : {self.stats['processed']:>10}".ljust(59) + "║")
        logger.info(f"║  Erreurs             : {self.stats['errors']:>10}".ljust(59) + "║")
        logger.info(f"║  Temps total         : {elapsed:>10.2f} sec".ljust(59) + "║")
        logger.info(f"║  Débit moyen         : {self.stats['processed']/elapsed if elapsed > 0 else 0:>10.1f} /sec".ljust(59) + "║")
        logger.info("╚" + "═" * 58 + "╝")

    def close(self):
        """Ferme la connexion."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logger.info("Connexion fermée.")


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal."""
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NOVA-999 | INJECTION SOUVERAINE                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python inject_agents.py <chemin_dossier_source>

Exemple:
    python inject_agents.py "C:\\Users\\Jonathan\\Documents\\AT-OM-Dataset"
    python inject_agents.py "/home/jonathan/data/agents"

Le script va:
    1. Scanner récursivement tous les fichiers du dossier
    2. Classifier chaque fichier dans une sphère (TECH, DATA, CREATE, etc.)
    3. Injecter les métadonnées dans PostgreSQL via SSL
    4. Utiliser des batch inserts pour optimiser la performance
""")
        sys.exit(1)

    source_dir = sys.argv[1]

    # Vérification du dossier
    if not Path(source_dir).exists():
        logger.error(f"Le dossier n'existe pas: {source_dir}")
        sys.exit(1)

    # Lancement
    injector = NovaInjector(source_dir)
    try:
        success = injector.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("\nInjection interrompue par l'utilisateur.")
        sys.exit(130)
    finally:
        injector.close()


if __name__ == '__main__':
    main()
