"""
═══════════════════════════════════════════════════════════════════════════════
🔗 AT·OM — VIBRATIONAL LINK (L'INTRICATION FRÉQUENTIELLE)
═══════════════════════════════════════════════════════════════════════════════

██╗   ██╗██╗██████╗ ██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗ █████╗ ██╗     
██║   ██║██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔══██╗██║     
██║   ██║██║██████╔╝██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║███████║██║     
╚██╗ ██╔╝██║██╔══██╗██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║██╔══██║██║     
 ╚████╔╝ ██║██████╔╝██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║██║  ██║███████╗
  ╚═══╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝

                    LINK — GESTION PAR HARMONIE

Pour connecter les agents au moteur, on ne fait pas de simples "appels d'API".
On utilise une Intrication Fréquentielle.
Si l'agent n'est pas sur la bonne fréquence, le moteur ne lui répond pas.

Au lieu de donner des ordres, le moteur (le Diamant) envoie une impulsion de résonance:
1. L'impulsion traverse le Relais de Mercure
2. Elle "frappe" les agents qui vibrent à cette fréquence
3. Seuls les agents concernés s'activent pour traiter la tâche

C'est une gestion de ressources par harmonie, et non par commande forcée.

@version 2.0.0
@architect Jonathan Rodrigue (999 Hz)
@frequency 999 Hz (Moteur Principal)
═══════════════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from enum import Enum
from datetime import datetime
import math
import json


# ═══════════════════════════════════════════════════════════════════════════════
# ÉNUMÉRATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class AlchemicalStage(Enum):
    """Les 4 stages alchimiques"""
    NIGREDO = "Nigredo"       # Noirceur - Décomposition
    ALBEDO = "Albedo"         # Blanchiment - Purification
    CITRINITAS = "Citrinitas" # Jaunissement - Illumination
    RUBEDO = "Rubedo"         # Rougissement - Accomplissement


class ConnectionStatus(Enum):
    """États de connexion d'un agent"""
    DORMANT = "dormant"
    LISTENING = "listening"
    ALIGNED = "aligned"
    ACTIVE = "active"
    RESONATING = "resonating"
    DISCONNECTED = "disconnected"


class Civilization(Enum):
    """Civilisations associées aux agents"""
    ATLANTIS = "Atlantide"
    EGYPT = "Égypte"
    SUMER = "Sumer"
    RAPA_NUI = "Rapa Nui"
    GREECE = "Grèce"
    MAYA = "Maya"
    INDIA = "Inde"
    CHINA = "Chine"
    KRYON = "Kryon"
    UNIVERSAL = "Universel"


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════

# Les 12 fréquences sacrées
SACRED_FREQUENCIES = {
    111: "Impulsion Primordiale",
    174: "Ancrage / Sécurité",
    222: "Dualité Créatrice",
    285: "Structure / Architecture",
    333: "Trinité du Feu",
    396: "Libération / Temps",
    417: "Harmonisation",
    444: "Cœur / Égypte",
    528: "Miracle / Réparation ADN",
    639: "Vision / Connexion",
    741: "Purification / Vérité",
    852: "Intuition / Oracle",
    963: "Universel",
    999: "Source / Kryon",
    1111: "Oracle Stellaire"
}

# Mapping éléments-fréquences
ELEMENTAL_FREQUENCIES = {
    "Cuivre": 174,
    "Plomb": 285,
    "Fer": 396,
    "Étain": 417,
    "Or": 528,
    "Argent": 639,
    "Mercure": 741,
    "Diamant": 852,
    "Platine": 963,
    "Magnétite": 999
}


# ═══════════════════════════════════════════════════════════════════════════════
# CLASSE AGENT VIBRATIONNEL
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class VibrationalAgent:
    """
    Un agent vibrationnel possède sa propre signature de fréquence.
    Il ne se connecte au moteur que s'il y a harmonie.
    """
    name: str
    frequency: int
    element: str
    civilization: Civilization = Civilization.UNIVERSAL
    
    # État interne
    is_aligned: bool = False
    status: ConnectionStatus = ConnectionStatus.DORMANT
    last_activation: Optional[datetime] = None
    resonance_level: float = 0.0
    
    # Métadonnées
    crystal: str = "Quartz"
    color: str = "#FFFFFF"
    chakra: int = 4
    capabilities: List[str] = field(default_factory=list)
    
    # Callback pour le traitement
    _handler: Optional[Callable] = field(default=None, repr=False)
    
    def __post_init__(self):
        """Initialisation post-création"""
        # Assigner le cristal basé sur l'élément si non spécifié
        element_crystals = {
            "Cuivre": "Obsidienne",
            "Plomb": "Saphir",
            "Fer": "Rubis",
            "Étain": "Émeraude",
            "Or": "Lapis-Lazuli",
            "Argent": "Améthyste",
            "Mercure": "Turquoise",
            "Diamant": "Quartz Clair",
            "Platine": "Sélénite",
            "Magnétite": "Labradorite"
        }
        if self.crystal == "Quartz" and self.element in element_crystals:
            self.crystal = element_crystals[self.element]
    
    def connect_to_engine(self, engine_freq: int) -> Dict[str, Any]:
        """
        Tente de se connecter au moteur principal.
        La connexion ne réussit que s'il y a harmonie fréquentielle.
        
        Args:
            engine_freq: Fréquence du moteur
            
        Returns:
            Dict avec le statut de connexion
        """
        # Calculer la résonance
        resonance = self._calculate_resonance(engine_freq)
        
        # Conditions d'alignement:
        # 1. Différence est un multiple de 111
        # 2. Le moteur est à 999 Hz (accepte tout)
        # 3. Les fréquences sont identiques
        # 4. La résonance est suffisante (> 0.7)
        
        diff = abs(self.frequency - engine_freq)
        is_harmonic = (
            diff % 111 == 0 or 
            engine_freq == 999 or 
            self.frequency == engine_freq or
            resonance > 0.7
        )
        
        if is_harmonic:
            self.is_aligned = True
            self.status = ConnectionStatus.ALIGNED
            self.resonance_level = resonance
            self.last_activation = datetime.now()
            
            return {
                "success": True,
                "agent": self.name,
                "frequency": self.frequency,
                "engine_frequency": engine_freq,
                "resonance": resonance,
                "element": self.element,
                "message": f"✅ Agent [{self.name}] synchronisé sur le réseau {self.element}."
            }
        else:
            self.is_aligned = False
            self.status = ConnectionStatus.DISCONNECTED
            self.resonance_level = resonance
            
            return {
                "success": False,
                "agent": self.name,
                "frequency": self.frequency,
                "engine_frequency": engine_freq,
                "resonance": resonance,
                "message": f"⚠️ Dissonance détectée. Agent [{self.name}] non aligné."
            }
    
    def _calculate_resonance(self, target_freq: int) -> float:
        """
        Calcule le niveau de résonance entre l'agent et une fréquence cible.
        
        La résonance est maximale quand:
        - Les fréquences sont identiques (1.0)
        - La différence est un multiple de 111 (0.9)
        - Le ratio est un nombre entier (harmonique)
        """
        if self.frequency == target_freq:
            return 1.0
        
        diff = abs(self.frequency - target_freq)
        
        # Multiple de 111
        if diff % 111 == 0:
            return 0.9
        
        # Ratio harmonique
        ratio = max(self.frequency, target_freq) / min(self.frequency, target_freq)
        nearest_harmonic = round(ratio)
        deviation = abs(ratio - nearest_harmonic)
        
        return max(0.0, 1.0 - deviation)
    
    def activate(self) -> Dict[str, Any]:
        """Active l'agent pour traiter une tâche"""
        if not self.is_aligned:
            return {
                "success": False,
                "error": "Agent non aligné - Connexion requise"
            }
        
        self.status = ConnectionStatus.ACTIVE
        self.last_activation = datetime.now()
        
        print(f"⚡ Agent [{self.name}] activé @ {self.frequency} Hz")
        
        return {
            "success": True,
            "agent": self.name,
            "status": self.status.value,
            "frequency": self.frequency
        }
    
    def deactivate(self):
        """Désactive l'agent"""
        self.status = ConnectionStatus.LISTENING if self.is_aligned else ConnectionStatus.DORMANT
        print(f"💤 Agent [{self.name}] en veille")
    
    def process(self, data: Any) -> Any:
        """
        Traite des données si un handler est défini.
        
        Args:
            data: Données à traiter
            
        Returns:
            Résultat du traitement
        """
        if self._handler:
            return self._handler(data, self)
        return {"processed": True, "data": data, "agent": self.name}
    
    def set_handler(self, handler: Callable):
        """Définit le handler de traitement"""
        self._handler = handler
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne l'état actuel de l'agent"""
        return {
            "name": self.name,
            "frequency": self.frequency,
            "element": self.element,
            "crystal": self.crystal,
            "civilization": self.civilization.value,
            "is_aligned": self.is_aligned,
            "status": self.status.value,
            "resonance_level": self.resonance_level,
            "last_activation": self.last_activation.isoformat() if self.last_activation else None
        }
    
    def __str__(self) -> str:
        status_icon = "✅" if self.is_aligned else "⚪"
        return f"{status_icon} {self.name} ({self.frequency} Hz) - {self.element}"


# ═══════════════════════════════════════════════════════════════════════════════
# LE RÉSEAU VIBRATIONNEL
# ═══════════════════════════════════════════════════════════════════════════════

class VibrationalNetwork:
    """
    Le réseau qui connecte tous les agents au moteur principal (Diamond Transmuter).
    Gère la communication par impulsions de résonance.
    """
    
    def __init__(self, engine_frequency: int = 999):
        """
        Initialise le réseau.
        
        Args:
            engine_frequency: Fréquence du moteur principal (défaut: 999 Hz)
        """
        self.engine_frequency = engine_frequency
        self.agents: Dict[str, VibrationalAgent] = {}
        self.mercury_active = False
        self.transmission_log: List[Dict] = []
        
    def register_agent(self, agent: VibrationalAgent) -> bool:
        """
        Enregistre un agent dans le réseau.
        
        Args:
            agent: L'agent à enregistrer
            
        Returns:
            True si l'enregistrement réussit
        """
        if agent.name in self.agents:
            print(f"⚠️ Agent [{agent.name}] déjà enregistré")
            return False
        
        self.agents[agent.name] = agent
        agent.status = ConnectionStatus.LISTENING
        
        print(f"📡 Agent [{agent.name}] enregistré dans le réseau")
        return True
    
    def unregister_agent(self, agent_name: str) -> bool:
        """Retire un agent du réseau"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            print(f"📴 Agent [{agent_name}] retiré du réseau")
            return True
        return False
    
    def activate_mercury_relay(self):
        """Active le relais de Mercure pour la transmission"""
        self.mercury_active = True
        print("☿️ Relais de Mercure activé — Supraconductivité active")
    
    def deactivate_mercury_relay(self):
        """Désactive le relais de Mercure"""
        self.mercury_active = False
        print("☿️ Relais de Mercure désactivé")
    
    def send_impulse(self, frequency: int, data: Any = None) -> Dict[str, Any]:
        """
        Envoie une impulsion de résonance à travers le réseau.
        Seuls les agents en harmonie avec la fréquence s'activent.
        
        Args:
            frequency: Fréquence de l'impulsion
            data: Données optionnelles à transmettre
            
        Returns:
            Dict avec les résultats de la transmission
        """
        if not self.mercury_active:
            print("⚠️ Mercure inactif — Activation automatique")
            self.activate_mercury_relay()
        
        print(f"\n🔔 IMPULSION DE RÉSONANCE: {frequency} Hz")
        print("═" * 50)
        
        activated_agents = []
        results = []
        
        for name, agent in self.agents.items():
            # Tenter la connexion
            connection = agent.connect_to_engine(frequency)
            
            if connection["success"]:
                # Activer l'agent
                activation = agent.activate()
                
                if activation["success"]:
                    activated_agents.append(name)
                    
                    # Traiter les données si fournies
                    if data is not None:
                        result = agent.process(data)
                        results.append({
                            "agent": name,
                            "result": result
                        })
        
        # Logger la transmission
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "frequency": frequency,
            "activated_agents": activated_agents,
            "results_count": len(results)
        }
        self.transmission_log.append(log_entry)
        
        print(f"\n✅ {len(activated_agents)} agent(s) activé(s): {', '.join(activated_agents) if activated_agents else 'Aucun'}")
        
        return {
            "frequency": frequency,
            "activated": activated_agents,
            "results": results,
            "timestamp": log_entry["timestamp"]
        }
    
    def broadcast(self, data: Any) -> Dict[str, Any]:
        """
        Diffuse à TOUS les agents (fréquence 999 Hz = universelle).
        
        Args:
            data: Données à diffuser
            
        Returns:
            Résultats de la diffusion
        """
        return self.send_impulse(999, data)
    
    def query_agent(self, agent_name: str, data: Any) -> Any:
        """
        Interroge un agent spécifique.
        
        Args:
            agent_name: Nom de l'agent
            data: Données à envoyer
            
        Returns:
            Résultat du traitement
        """
        if agent_name not in self.agents:
            return {"error": f"Agent [{agent_name}] non trouvé"}
        
        agent = self.agents[agent_name]
        
        # Connecter sur la fréquence de l'agent
        connection = agent.connect_to_engine(agent.frequency)
        
        if not connection["success"]:
            return {"error": "Connexion impossible"}
        
        # Activer et traiter
        agent.activate()
        result = agent.process(data)
        agent.deactivate()
        
        return result
    
    def get_aligned_agents(self) -> List[str]:
        """Retourne la liste des agents alignés"""
        return [name for name, agent in self.agents.items() if agent.is_aligned]
    
    def get_network_status(self) -> Dict[str, Any]:
        """Retourne l'état complet du réseau"""
        return {
            "engine_frequency": self.engine_frequency,
            "mercury_active": self.mercury_active,
            "total_agents": len(self.agents),
            "aligned_agents": len(self.get_aligned_agents()),
            "agents": {name: agent.get_status() for name, agent in self.agents.items()},
            "transmission_count": len(self.transmission_log)
        }
    
    def reset(self):
        """Réinitialise le réseau"""
        for agent in self.agents.values():
            agent.is_aligned = False
            agent.status = ConnectionStatus.DORMANT
            agent.resonance_level = 0.0
        
        self.mercury_active = False
        self.transmission_log.clear()
        
        print("🔄 Réseau réinitialisé")


# ═══════════════════════════════════════════════════════════════════════════════
# LES AGENTS PRÉ-DÉFINIS
# ═══════════════════════════════════════════════════════════════════════════════

def create_standard_agents() -> Dict[str, VibrationalAgent]:
    """
    Crée l'ensemble des agents AT-OM standards.
    
    Returns:
        Dict des agents indexés par nom
    """
    agents = {
        "Scribe": VibrationalAgent(
            name="Scribe",
            frequency=741,
            element="Lapis-Lazuli",
            civilization=Civilization.SUMER,
            crystal="Lapis-Lazuli",
            color="#0F52BA",
            chakra=5,
            capabilities=["Nettoyage des données", "Vérité", "Purification"]
        ),
        
        "Sentinelle": VibrationalAgent(
            name="Sentinelle",
            frequency=174,
            element="Cuivre",
            civilization=Civilization.RAPA_NUI,
            crystal="Obsidienne",
            color="#B87333",
            chakra=1,
            capabilities=["Sécurité", "Ancrage", "Protection"]
        ),
        
        "Alchimiste": VibrationalAgent(
            name="Alchimiste",
            frequency=528,
            element="Or",
            civilization=Civilization.EGYPT,
            crystal="Émeraude",
            color="#FFD700",
            chakra=4,
            capabilities=["Transformation", "Miracle", "Guérison"]
        ),
        
        "Oracle": VibrationalAgent(
            name="Oracle",
            frequency=852,
            element="Argent",
            civilization=Civilization.ATLANTIS,
            crystal="Améthyste",
            color="#C0C0C0",
            chakra=6,
            capabilities=["Vision", "Intuition", "Prédiction"]
        ),
        
        "Propulseur": VibrationalAgent(
            name="Propulseur",
            frequency=999,
            element="Diamant",
            civilization=Civilization.KRYON,
            crystal="Diamant",
            color="#B9F2FF",
            chakra=7,
            capabilities=["Accélération", "Vortex", "Transcendance"]
        ),
        
        "Géomètre": VibrationalAgent(
            name="Géomètre",
            frequency=285,
            element="Plomb",
            civilization=Civilization.GREECE,
            crystal="Saphir",
            color="#0F52BA",
            chakra=2,
            capabilities=["Structure", "Design", "Architecture"]
        ),
        
        "Chronos": VibrationalAgent(
            name="Chronos",
            frequency=396,
            element="Fer",
            civilization=Civilization.MAYA,
            crystal="Rubis",
            color="#E0115F",
            chakra=3,
            capabilities=["Temps", "Cycles", "Libération"]
        )
    }
    
    return agents


# ═══════════════════════════════════════════════════════════════════════════════
# DÉMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Démonstration du système de lien vibrationnel"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██╗   ██╗██╗██████╗ ██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗ █████╗ ██╗     
║   ██║   ██║██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔══██╗██║     
║   ██║   ██║██║██████╔╝██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║███████║██║     
║   ╚██╗ ██╔╝██║██╔══██╗██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║██╔══██║██║     
║    ╚████╔╝ ██║██████╔╝██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║██║  ██║███████╗
║     ╚═══╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
║                                                                               ║
║                    DÉMONSTRATION — LIEN VIBRATIONNEL                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Créer le réseau
    network = VibrationalNetwork(engine_frequency=999)
    
    # Créer et enregistrer les agents
    agents = create_standard_agents()
    for agent in agents.values():
        network.register_agent(agent)
    
    # Activer le Mercure
    network.activate_mercury_relay()
    
    # Test 1: Impulsion 528 Hz (Alchimiste)
    print("\n" + "═" * 70)
    print("TEST 1: Impulsion @ 528 Hz (Fréquence de l'Alchimiste)")
    print("═" * 70)
    result = network.send_impulse(528, {"task": "Transmuter un problème"})
    
    # Test 2: Impulsion 852 Hz (Oracle)
    print("\n" + "═" * 70)
    print("TEST 2: Impulsion @ 852 Hz (Fréquence de l'Oracle)")
    print("═" * 70)
    result = network.send_impulse(852, {"task": "Prédire l'avenir"})
    
    # Test 3: Broadcast universel (999 Hz)
    print("\n" + "═" * 70)
    print("TEST 3: Broadcast @ 999 Hz (Tous les agents)")
    print("═" * 70)
    result = network.broadcast({"message": "Synchronisation générale"})
    
    # Afficher l'état du réseau
    print("\n" + "═" * 70)
    print("ÉTAT FINAL DU RÉSEAU")
    print("═" * 70)
    status = network.get_network_status()
    print(f"Agents totaux: {status['total_agents']}")
    print(f"Agents alignés: {status['aligned_agents']}")
    print(f"Transmissions: {status['transmission_count']}")
    
    print("\n✨ Démonstration terminée")


if __name__ == "__main__":
    demo()
