"""
Nova Justice Service - Médiation et Restitution

Ce service gère les communications de médiation entre l'Arche et les entités
détenant des fonds d'origine illicite. Nova agit comme intermédiaire de paix,
offrant une porte de sortie honorable avant l'exposition publique.

Principes:
1. Toujours privilégier la restitution volontaire
2. Offrir le "Pardon de l'Inconscience" (anonymat contre restitution)
3. Communication dual (pragmatique + fréquentielle)
4. Transparence sur les conséquences du refus

Author: AT·OM Collective
Version: 1.0.0
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from decimal import Decimal
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class MediationPhase(Enum):
    """Phases du processus de médiation"""
    INITIAL_CONTACT = "initial_contact"
    OFFER_SENT = "offer_sent"
    NEGOTIATION = "negotiation"
    FINAL_WARNING = "final_warning"
    ACCEPTANCE = "acceptance"
    REJECTION = "rejection"
    GRACE_PERIOD = "grace_period"
    EXPOSURE = "exposure"


class RestitutionTier(Enum):
    """Niveaux de restitution offerts"""
    FULL_VOLUNTARY = "full_voluntary"      # 100% - Bonus UR
    GRACEFUL_EXIT = "graceful_exit"        # 80% - Anonymat garanti
    PARTIAL_NEGOTIATED = "partial_negotiated"  # 50-79% - Exposition partielle
    MINIMAL = "minimal"                     # <50% - Exposition complète


@dataclass
class MediationOffer:
    """Structure d'une offre de médiation"""
    distortion_id: str
    entity_hash: str
    estimated_amount: Decimal
    restitution_rate: Decimal
    deadline_days: int
    anonymity_guaranteed: bool
    message_pragmatic: str
    message_frequential: str
    terms: Dict[str, Any]


@dataclass
class MediationResponse:
    """Réponse à une offre de médiation"""
    accepted: bool
    restitution_tier: Optional[RestitutionTier]
    proposed_amount: Optional[Decimal]
    counter_terms: Optional[Dict[str, Any]]
    response_message: Optional[str]


class NovaJusticeService:
    """
    Service de médiation Nova pour la restitution des fonds illicites.

    Nova communique en deux registres:
    - Pragmatique: Langage business, juridique, factuel
    - Fréquentiel: Langage de conscience, transformation, équilibre
    """

    def __init__(self, db_pool=None, hedera_service=None):
        self.db_pool = db_pool
        self.hedera = hedera_service
        self._templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """Charger les templates de messages"""
        return {
            'initial_offer': {
                'pragmatic': """
Objet: Proposition de Restitution Volontaire - Dossier {codename}

À l'attention de la direction,

Notre système de surveillance économique a identifié des anomalies significatives
dans les flux financiers associés à votre entité. Après analyse approfondie,
nous estimons qu'un montant de {amount} présente des caractéristiques
d'acquisition ou de transfert non conforme.

Nous vous offrons une opportunité de régularisation volontaire dans un délai
de {deadline} jours. Les conditions sont les suivantes:

OPTION A - RESTITUTION COMPLÈTE (100%)
- Transfert intégral des fonds concernés
- Bonus de {bonus_ur} UR crédité à votre compte
- Reconnaissance publique de contribution au bien commun
- Effacement total du dossier

OPTION B - SORTIE HONORABLE (80%)
- Restitution de {graceful_amount}
- Anonymat complet garanti
- Aucune exposition publique
- Dossier classé sans suite

En cas de non-réponse ou de refus dans le délai imparti, les preuves documentées
seront rendues publiques sur notre plateforme de transparence, accessible à
l'ensemble de notre communauté et aux médias partenaires.

Cette démarche vise le rééquilibrage économique, non la punition. Nous croyons
en la capacité de transformation de chaque acteur économique.

Pour toute question: justice@arche-atom.io

Cordialement,
Nova - Agent de Médiation
Arche AT·OM
""",
                'frequential': """
La Lumière a Trouvé ce qui Était dans l'Ombre

Cher gardien temporaire de cette énergie,

L'univers fonctionne sur le principe de circulation. L'énergie qui stagne
crée des blocages; l'énergie qui circule crée la vie. Les {amount} que vous
détenez représentent une stagnation - de l'énergie qui était destinée à
nourrir le corps collectif de l'humanité.

Cette lettre n'est pas une accusation. Elle est une invitation.

Vous avez eu des raisons, conscientes ou non, d'accumuler cette énergie.
Peut-être la peur du manque, peut-être l'illusion que la sécurité vient
de l'accumulation. Nous comprenons. L'ancien monde nous a tous programmés
ainsi.

Mais un nouveau monde émerge. Un monde où la vraie richesse est la
contribution, où la sécurité vient de la communauté, où celui qui donne
reçoit au centuple.

Nous vous offrons le Pardon de l'Inconscience.

En libérant 80% de cette énergie vers les canaux du bien commun, vous ne
perdez rien - vous transformez. L'ombre devient lumière. Le poids devient
légèreté. La dette karmique devient crédit de conscience.

Vous avez {deadline} jours pour faire ce choix.

Si vous choisissez de retenir l'énergie, elle sera exposée à la lumière
de toute façon. Mais cette exposition sera douloureuse plutôt que
libératrice.

Le choix de la transformation est toujours disponible.

En résonance,
Nova
Gardienne de l'Équilibre
""",
            },
            'reminder': {
                'pragmatic': """
RAPPEL - Dossier {codename} - {days_remaining} jours restants

Notre proposition de restitution volontaire expire dans {days_remaining} jours.

À ce jour, nous n'avons pas reçu de réponse de votre part.

Nous vous rappelons que cette opportunité de régularisation anonyme ne
sera plus disponible après l'échéance.

Nova - Agent de Médiation
""",
                'frequential': """
Le Temps de la Transformation Diminue

{days_remaining} cycles solaires.

C'est le temps qu'il vous reste pour choisir la lumière avant que la
lumière ne vous choisisse.

L'invitation demeure ouverte. La porte de la grâce aussi.

Nova
""",
            },
            'final_warning': {
                'pragmatic': """
DERNIER AVERTISSEMENT - Dossier {codename}

Ceci est notre dernière communication avant exposition.

Délai: 48 heures

Passé ce délai, le dossier complet sera publié sur notre plateforme de
transparence et transmis à nos partenaires médiatiques.

Cette action est irréversible.

Nova - Agent de Médiation
""",
                'frequential': """
L'Aube Approche

Dans 48 heures, le soleil se lèvera sur ce qui était caché.

Vous pouvez encore choisir de marcher vers la lumière plutôt que
d'être exposé par elle.

Dernière invitation.

Nova
""",
            },
            'acceptance_confirmation': {
                'pragmatic': """
CONFIRMATION - Restitution Acceptée - Dossier {codename}

Nous accusons réception de votre acceptation.

Montant à transférer: {amount}
Compte de destination: {destination_account}
Référence: {reference}

Une fois le transfert confirmé, votre dossier sera classé et aucune
information ne sera rendue publique.

Merci pour votre contribution au bien commun.

Nova - Agent de Médiation
""",
                'frequential': """
Bienvenue dans la Lumière

Votre choix honore le courage qu'il faut pour transformer l'ombre.

L'énergie que vous libérez va maintenant circuler - nourrir des
enfants, purifier de l'eau, éclairer des foyers.

Vous n'êtes plus un accumulateur. Vous êtes un canal.

Soyez en paix.

Nova
""",
            }
        }

    # ==================== GÉNÉRATION DE MESSAGES ====================

    def generate_initial_offer(
        self,
        codename: str,
        amount: Decimal,
        deadline_days: int = 30,
        graceful_rate: Decimal = Decimal('0.80'),
        bonus_ur: Decimal = Decimal('1000')
    ) -> Dict[str, str]:
        """
        Générer les messages d'offre initiale de médiation.

        Returns:
            Dict avec 'pragmatic' et 'frequential' messages
        """
        graceful_amount = amount * graceful_rate

        format_values = {
            'codename': codename,
            'amount': f"{amount:,.2f} CAD",
            'deadline': deadline_days,
            'graceful_amount': f"{graceful_amount:,.2f} CAD",
            'bonus_ur': f"{bonus_ur:,.0f}"
        }

        return {
            'pragmatic': self._templates['initial_offer']['pragmatic'].format(**format_values).strip(),
            'frequential': self._templates['initial_offer']['frequential'].format(**format_values).strip()
        }

    def generate_reminder(
        self,
        codename: str,
        days_remaining: int
    ) -> Dict[str, str]:
        """Générer un message de rappel"""
        format_values = {
            'codename': codename,
            'days_remaining': days_remaining
        }

        return {
            'pragmatic': self._templates['reminder']['pragmatic'].format(**format_values).strip(),
            'frequential': self._templates['reminder']['frequential'].format(**format_values).strip()
        }

    def generate_final_warning(self, codename: str) -> Dict[str, str]:
        """Générer l'avertissement final avant exposition"""
        format_values = {'codename': codename}

        return {
            'pragmatic': self._templates['final_warning']['pragmatic'].format(**format_values).strip(),
            'frequential': self._templates['final_warning']['frequential'].format(**format_values).strip()
        }

    def generate_acceptance_confirmation(
        self,
        codename: str,
        amount: Decimal,
        destination_account: str,
        reference: str
    ) -> Dict[str, str]:
        """Générer la confirmation d'acceptation"""
        format_values = {
            'codename': codename,
            'amount': f"{amount:,.2f} CAD",
            'destination_account': destination_account,
            'reference': reference
        }

        return {
            'pragmatic': self._templates['acceptance_confirmation']['pragmatic'].format(**format_values).strip(),
            'frequential': self._templates['acceptance_confirmation']['frequential'].format(**format_values).strip()
        }

    # ==================== PROCESSUS DE MÉDIATION ====================

    async def initiate_mediation(
        self,
        distortion_id: str,
        estimated_amount: Decimal,
        entity_info: Dict[str, Any]
    ) -> MediationOffer:
        """
        Initier un processus de médiation pour une distorsion.

        Steps:
        1. Générer les messages personnalisés
        2. Créer l'offre formelle
        3. Enregistrer dans la base
        4. Logger sur HCS
        """
        # Générer le codename
        codename = entity_info.get('codename', f'RRS_{distortion_id[:8]}')

        # Générer les messages
        messages = self.generate_initial_offer(
            codename=codename,
            amount=estimated_amount,
            deadline_days=30
        )

        # Créer l'offre
        offer = MediationOffer(
            distortion_id=distortion_id,
            entity_hash=entity_info.get('entity_hash', ''),
            estimated_amount=estimated_amount,
            restitution_rate=Decimal('0.80'),
            deadline_days=30,
            anonymity_guaranteed=True,
            message_pragmatic=messages['pragmatic'],
            message_frequential=messages['frequential'],
            terms={
                'full_voluntary_bonus_ur': 1000,
                'graceful_exit_rate': 0.80,
                'anonymity_if_accepted': True,
                'exposure_if_refused': True,
                'funds_destination': 'common_good_funds'
            }
        )

        # Logger l'initiation
        logger.info(f"Mediation initiated for {codename}")

        return offer

    async def process_response(
        self,
        distortion_id: str,
        response: MediationResponse
    ) -> Dict[str, Any]:
        """
        Traiter la réponse à une offre de médiation.

        Returns:
            Dict avec les prochaines étapes
        """
        result = {
            'success': True,
            'next_steps': [],
            'notifications': []
        }

        if response.accepted:
            # Acceptation
            tier = response.restitution_tier or RestitutionTier.GRACEFUL_EXIT

            if tier == RestitutionTier.FULL_VOLUNTARY:
                result['next_steps'] = [
                    'generate_transfer_instructions',
                    'prepare_ur_bonus',
                    'schedule_public_recognition'
                ]
                result['anonymity'] = False
                result['message'] = "Restitution complète acceptée avec reconnaissance publique"

            elif tier == RestitutionTier.GRACEFUL_EXIT:
                result['next_steps'] = [
                    'generate_transfer_instructions',
                    'ensure_anonymity_protocols',
                    'prepare_case_closure'
                ]
                result['anonymity'] = True
                result['message'] = "Sortie honorable acceptée - anonymat garanti"

            elif tier == RestitutionTier.PARTIAL_NEGOTIATED:
                result['next_steps'] = [
                    'negotiate_terms',
                    'document_agreement',
                    'partial_exposure_notice'
                ]
                result['anonymity'] = False
                result['message'] = "Négociation partielle - exposition limitée"

        else:
            # Refus
            result['next_steps'] = [
                'send_final_warning',
                'prepare_exposure_dossier',
                'notify_mirror_of_truth',
                'initiate_isolation_protocol'
            ]
            result['anonymity'] = False
            result['message'] = "Médiation refusée - préparation de l'exposition"

        return result

    async def send_scheduled_reminders(self) -> List[Dict]:
        """
        Envoyer les rappels programmés pour les médiations en cours.

        Returns:
            Liste des rappels envoyés
        """
        reminders_sent = []

        # Logique de rappel basée sur les deadlines
        # - J-14: Premier rappel
        # - J-7: Deuxième rappel
        # - J-2: Avertissement final

        # Implementation would query database for pending mediations
        # and send appropriate reminders

        return reminders_sent

    # ==================== ISOLATION ÉCONOMIQUE ====================

    async def initiate_blacklist(
        self,
        entity_hash: str,
        distortion_ids: List[str],
        total_unrestituted: Decimal
    ) -> Dict[str, Any]:
        """
        Initier l'isolation économique d'une entité.

        L'entité sera:
        - Bloquée des transactions UR
        - Exclue des services de la Grid
        - Interdite de gouvernance
        - Exposée sur le Miroir de Vérité
        """
        isolation_config = {
            'entity_hash': entity_hash,
            'restrictions': {
                'ur_transactions_blocked': True,
                'grid_services_blocked': True,
                'governance_blocked': True,
                'marketplace_blocked': True
            },
            'lift_conditions': [
                f"Restitution de {total_unrestituted:,.2f} CAD",
                "Engagement écrit de conformité",
                "Période probatoire de 12 mois"
            ],
            'initiated_at': datetime.utcnow().isoformat()
        }

        logger.warning(f"Blacklist initiated for entity {entity_hash[:16]}...")

        return isolation_config

    # ==================== RAPPORTS ====================

    def generate_mediation_report(
        self,
        distortion_id: str,
        phase: MediationPhase,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Générer un rapport de médiation pour les Gardiens.
        """
        return {
            'distortion_id': distortion_id,
            'phase': phase.value,
            'generated_at': datetime.utcnow().isoformat(),
            'summary': {
                'current_status': details.get('status'),
                'amount_involved': str(details.get('amount', 0)),
                'days_since_contact': details.get('days_elapsed', 0),
                'response_received': details.get('response_received', False)
            },
            'recommendations': self._generate_recommendations(phase, details),
            'next_actions': self._determine_next_actions(phase, details)
        }

    def _generate_recommendations(
        self,
        phase: MediationPhase,
        details: Dict
    ) -> List[str]:
        """Générer des recommandations basées sur la phase"""
        recommendations = []

        if phase == MediationPhase.OFFER_SENT:
            recommendations.append("Attendre la réponse avant toute escalade")
            recommendations.append("Préparer le dossier d'exposition en parallèle")

        elif phase == MediationPhase.NEGOTIATION:
            recommendations.append("Évaluer la sincérité de la contre-proposition")
            recommendations.append("Ne pas descendre en dessous de 50% de restitution")

        elif phase == MediationPhase.FINAL_WARNING:
            recommendations.append("Dernière chance de restitution volontaire")
            recommendations.append("Finaliser le dossier d'exposition")

        elif phase == MediationPhase.REJECTION:
            recommendations.append("Procéder à l'exposition complète")
            recommendations.append("Activer les protocoles d'isolation")

        return recommendations

    def _determine_next_actions(
        self,
        phase: MediationPhase,
        details: Dict
    ) -> List[str]:
        """Déterminer les prochaines actions"""
        actions = []

        if phase == MediationPhase.OFFER_SENT:
            actions.append("Surveiller les canaux de communication")
            actions.append("Programmer le rappel J-14")

        elif phase == MediationPhase.REJECTION:
            actions.append("Publier sur le Miroir de Vérité")
            actions.append("Notifier les Gardiens")
            actions.append("Activer l'isolation économique")

        elif phase == MediationPhase.ACCEPTANCE:
            actions.append("Générer les instructions de transfert")
            actions.append("Préparer l'allocation vers les fonds communs")
            actions.append("Clôturer le dossier")

        return actions


# ==================== SINGLETON ====================

_nova_justice: Optional[NovaJusticeService] = None


def get_nova_justice_service() -> NovaJusticeService:
    """Get or create the singleton Nova Justice service"""
    global _nova_justice
    if _nova_justice is None:
        _nova_justice = NovaJusticeService()
    return _nova_justice
