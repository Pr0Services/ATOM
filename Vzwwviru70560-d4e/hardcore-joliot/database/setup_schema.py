#!/usr/bin/env python3
"""
AT·OM - Setup Schema PostgreSQL
Exécute schema.sql sur DigitalOcean
"""

import psycopg2
from pathlib import Path

DB_CONFIG = {
    'host': 'db-postgresql-nyc9-999-999-do-user-32084357-0.h.db.ondigitalocean.com',
    'port': 25060,
    'database': 'defaultdb',
    'user': 'doadmin',
    'password': 'AVNS_11mUpQDq99BeOE4o068',
    'sslmode': 'require'
}

def main():
    print("=" * 60)
    print("AT·OM NOVA-999 | Installation du schéma PostgreSQL")
    print("=" * 60)

    # Lire le fichier SQL
    schema_path = Path(__file__).parent / 'schema.sql'
    if not schema_path.exists():
        print(f"ERREUR: {schema_path} non trouvé!")
        return

    sql_content = schema_path.read_text(encoding='utf-8')
    print(f"Schéma chargé: {len(sql_content)} caractères")

    # Connexion
    print(f"\nConnexion à {DB_CONFIG['host']}...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        print("✓ Connexion SSL établie!")

        # Exécuter le schéma
        print("\nExécution du schéma...")
        cursor.execute(sql_content)
        print("✓ Schéma installé!")

        # Vérifier
        cursor.execute("SELECT code, name, agent_count FROM spheres ORDER BY agent_count DESC;")
        rows = cursor.fetchall()

        print(f"\n{'='*60}")
        print(f"{'SPHÈRE':<15} {'NOM':<20} {'AGENTS':>10}")
        print(f"{'='*60}")
        total = 0
        for code, name, count in rows:
            print(f"{code:<15} {name:<20} {count:>10}")
            total += count
        print(f"{'='*60}")
        print(f"{'TOTAL':<35} {total:>10}")

        cursor.close()
        conn.close()
        print("\n✓ Installation terminée!")

    except psycopg2.Error as e:
        print(f"ERREUR: {e}")

if __name__ == '__main__':
    main()
