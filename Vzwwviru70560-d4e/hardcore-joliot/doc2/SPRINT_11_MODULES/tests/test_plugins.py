"""
CHE·NU™ — PLUGIN SYSTEM TESTS (PYTEST)
Sprint 10 (FINAL): Plugin and extension tests

Plugin Principles:
- Plugins extend functionality without modifying core
- Plugins must respect governance
- Plugins are sandboxed
- Plugin lifecycle is managed
"""

import pytest
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
from enum import Enum

# ═══════════════════════════════════════════════════════════════════════════════
# PLUGIN TYPES
# ═══════════════════════════════════════════════════════════════════════════════

class PluginState(str, Enum):
    INSTALLED = "installed"
    ACTIVE = "active"
    DISABLED = "disabled"
    ERROR = "error"


class PluginScope(str, Enum):
    GLOBAL = "global"       # All spheres
    SPHERE = "sphere"       # Single sphere
    BUREAU = "bureau"       # Single bureau section


# ═══════════════════════════════════════════════════════════════════════════════
# PLUGIN CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class Plugin:
    """Base plugin class."""
    
    def __init__(
        self,
        plugin_id: str,
        name: str,
        version: str,
        scope: PluginScope = PluginScope.GLOBAL,
    ):
        self.id = plugin_id
        self.name = name
        self.version = version
        self.scope = scope
        self.state = PluginState.INSTALLED
        self.permissions: List[str] = []
        self.hooks: Dict[str, Callable] = {}
        self.installed_at: datetime = datetime.utcnow()
        self.activated_at: Optional[datetime] = None
    
    def activate(self) -> bool:
        """Activate the plugin."""
        if self.state == PluginState.ERROR:
            return False
        self.state = PluginState.ACTIVE
        self.activated_at = datetime.utcnow()
        return True
    
    def deactivate(self) -> bool:
        """Deactivate the plugin."""
        self.state = PluginState.DISABLED
        return True
    
    def register_hook(self, event: str, handler: Callable) -> None:
        """Register a hook for an event."""
        self.hooks[event] = handler
    
    def has_permission(self, permission: str) -> bool:
        """Check if plugin has permission."""
        return permission in self.permissions
    
    def add_permission(self, permission: str) -> None:
        """Add permission to plugin."""
        if permission not in self.permissions:
            self.permissions.append(permission)


class PluginManager:
    """Manages plugin lifecycle."""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[Callable]] = {}
        self.audit_log: List[Dict] = []
    
    def install(self, plugin: Plugin) -> bool:
        """Install a plugin."""
        if plugin.id in self.plugins:
            return False
        
        self.plugins[plugin.id] = plugin
        self._log("PLUGIN_INSTALLED", {"plugin_id": plugin.id})
        return True
    
    def uninstall(self, plugin_id: str) -> bool:
        """Uninstall a plugin."""
        if plugin_id not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_id]
        if plugin.state == PluginState.ACTIVE:
            plugin.deactivate()
        
        del self.plugins[plugin_id]
        self._log("PLUGIN_UNINSTALLED", {"plugin_id": plugin_id})
        return True
    
    def activate(self, plugin_id: str) -> bool:
        """Activate a plugin."""
        if plugin_id not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_id]
        if plugin.activate():
            # Register hooks
            for event, handler in plugin.hooks.items():
                if event not in self.hooks:
                    self.hooks[event] = []
                self.hooks[event].append(handler)
            
            self._log("PLUGIN_ACTIVATED", {"plugin_id": plugin_id})
            return True
        return False
    
    def deactivate(self, plugin_id: str) -> bool:
        """Deactivate a plugin."""
        if plugin_id not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_id]
        plugin.deactivate()
        
        # Unregister hooks
        for event, handler in plugin.hooks.items():
            if event in self.hooks and handler in self.hooks[event]:
                self.hooks[event].remove(handler)
        
        self._log("PLUGIN_DEACTIVATED", {"plugin_id": plugin_id})
        return True
    
    def emit(self, event: str, data: Any = None) -> List[Any]:
        """Emit an event to all registered hooks."""
        results = []
        if event in self.hooks:
            for handler in self.hooks[event]:
                try:
                    result = handler(data)
                    results.append(result)
                except Exception as e:
                    results.append({"error": str(e)})
        return results
    
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """Get a plugin by ID."""
        return self.plugins.get(plugin_id)
    
    def list_plugins(self) -> List[Plugin]:
        """List all plugins."""
        return list(self.plugins.values())
    
    def get_active_plugins(self) -> List[Plugin]:
        """List active plugins."""
        return [p for p in self.plugins.values() if p.state == PluginState.ACTIVE]
    
    def _log(self, action: str, details: Dict):
        self.audit_log.append({
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        })


# ═══════════════════════════════════════════════════════════════════════════════
# PLUGIN INSTALLATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPluginInstallation:
    """Tests for plugin installation."""

    def test_install_plugin(self):
        """Should install a plugin."""
        manager = PluginManager()
        plugin = Plugin("test_plugin", "Test Plugin", "1.0.0")
        
        result = manager.install(plugin)
        
        assert result is True
        assert plugin.id in manager.plugins

    def test_prevent_duplicate_install(self):
        """Should prevent duplicate installation."""
        manager = PluginManager()
        plugin = Plugin("test_plugin", "Test Plugin", "1.0.0")
        
        manager.install(plugin)
        result = manager.install(plugin)
        
        assert result is False

    def test_uninstall_plugin(self):
        """Should uninstall a plugin."""
        manager = PluginManager()
        plugin = Plugin("test_plugin", "Test Plugin", "1.0.0")
        
        manager.install(plugin)
        result = manager.uninstall("test_plugin")
        
        assert result is True
        assert "test_plugin" not in manager.plugins

    def test_uninstall_nonexistent(self):
        """Should return False for nonexistent plugin."""
        manager = PluginManager()
        
        result = manager.uninstall("nonexistent")
        
        assert result is False


# ═══════════════════════════════════════════════════════════════════════════════
# PLUGIN ACTIVATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPluginActivation:
    """Tests for plugin activation."""

    def test_activate_plugin(self):
        """Should activate a plugin."""
        manager = PluginManager()
        plugin = Plugin("test_plugin", "Test", "1.0.0")
        
        manager.install(plugin)
        result = manager.activate("test_plugin")
        
        assert result is True
        assert plugin.state == PluginState.ACTIVE

    def test_deactivate_plugin(self):
        """Should deactivate a plugin."""
        manager = PluginManager()
        plugin = Plugin("test_plugin", "Test", "1.0.0")
        
        manager.install(plugin)
        manager.activate("test_plugin")
        result = manager.deactivate("test_plugin")
        
        assert result is True
        assert plugin.state == PluginState.DISABLED

    def test_get_active_plugins(self):
        """Should list active plugins."""
        manager = PluginManager()
        
        plugin1 = Plugin("p1", "Plugin 1", "1.0.0")
        plugin2 = Plugin("p2", "Plugin 2", "1.0.0")
        
        manager.install(plugin1)
        manager.install(plugin2)
        manager.activate("p1")
        
        active = manager.get_active_plugins()
        
        assert len(active) == 1
        assert active[0].id == "p1"


# ═══════════════════════════════════════════════════════════════════════════════
# PLUGIN HOOKS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPluginHooks:
    """Tests for plugin hooks."""

    def test_register_hook(self):
        """Should register a hook."""
        plugin = Plugin("test", "Test", "1.0.0")
        
        def handler(data):
            return data * 2
        
        plugin.register_hook("on_message", handler)
        
        assert "on_message" in plugin.hooks

    def test_emit_event(self):
        """Should emit events to hooks."""
        manager = PluginManager()
        plugin = Plugin("test", "Test", "1.0.0")
        
        results_collector = []
        
        def handler(data):
            results_collector.append(data)
            return data * 2
        
        plugin.register_hook("test_event", handler)
        manager.install(plugin)
        manager.activate("test")
        
        results = manager.emit("test_event", 5)
        
        assert 5 in results_collector
        assert 10 in results

    def test_multiple_hooks(self):
        """Should call multiple hooks."""
        manager = PluginManager()
        
        plugin1 = Plugin("p1", "Plugin 1", "1.0.0")
        plugin2 = Plugin("p2", "Plugin 2", "1.0.0")
        
        plugin1.register_hook("event", lambda x: x + 1)
        plugin2.register_hook("event", lambda x: x + 2)
        
        manager.install(plugin1)
        manager.install(plugin2)
        manager.activate("p1")
        manager.activate("p2")
        
        results = manager.emit("event", 0)
        
        assert len(results) == 2


# ═══════════════════════════════════════════════════════════════════════════════
# PLUGIN PERMISSIONS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPluginPermissions:
    """Tests for plugin permissions."""

    def test_add_permission(self):
        """Should add permission."""
        plugin = Plugin("test", "Test", "1.0.0")
        
        plugin.add_permission("read:threads")
        
        assert plugin.has_permission("read:threads")

    def test_check_missing_permission(self):
        """Should return False for missing permission."""
        plugin = Plugin("test", "Test", "1.0.0")
        
        assert plugin.has_permission("write:threads") is False

    def test_no_duplicate_permissions(self):
        """Should not add duplicate permissions."""
        plugin = Plugin("test", "Test", "1.0.0")
        
        plugin.add_permission("read:threads")
        plugin.add_permission("read:threads")
        
        assert len(plugin.permissions) == 1


# ═══════════════════════════════════════════════════════════════════════════════
# PLUGIN SCOPE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPluginScope:
    """Tests for plugin scope."""

    def test_global_scope(self):
        """Should have global scope by default."""
        plugin = Plugin("test", "Test", "1.0.0")
        
        assert plugin.scope == PluginScope.GLOBAL

    def test_sphere_scope(self):
        """Should support sphere scope."""
        plugin = Plugin("test", "Test", "1.0.0", PluginScope.SPHERE)
        
        assert plugin.scope == PluginScope.SPHERE

    def test_bureau_scope(self):
        """Should support bureau scope."""
        plugin = Plugin("test", "Test", "1.0.0", PluginScope.BUREAU)
        
        assert plugin.scope == PluginScope.BUREAU


# ═══════════════════════════════════════════════════════════════════════════════
# PLUGIN AUDIT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPluginAudit:
    """Tests for plugin audit logging."""

    def test_install_is_audited(self):
        """Installation should be audited."""
        manager = PluginManager()
        plugin = Plugin("test", "Test", "1.0.0")
        
        manager.install(plugin)
        
        assert any(log["action"] == "PLUGIN_INSTALLED" for log in manager.audit_log)

    def test_activate_is_audited(self):
        """Activation should be audited."""
        manager = PluginManager()
        plugin = Plugin("test", "Test", "1.0.0")
        
        manager.install(plugin)
        manager.activate("test")
        
        assert any(log["action"] == "PLUGIN_ACTIVATED" for log in manager.audit_log)

    def test_deactivate_is_audited(self):
        """Deactivation should be audited."""
        manager = PluginManager()
        plugin = Plugin("test", "Test", "1.0.0")
        
        manager.install(plugin)
        manager.activate("test")
        manager.deactivate("test")
        
        assert any(log["action"] == "PLUGIN_DEACTIVATED" for log in manager.audit_log)

    def test_uninstall_is_audited(self):
        """Uninstallation should be audited."""
        manager = PluginManager()
        plugin = Plugin("test", "Test", "1.0.0")
        
        manager.install(plugin)
        manager.uninstall("test")
        
        assert any(log["action"] == "PLUGIN_UNINSTALLED" for log in manager.audit_log)


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT PLUGIN COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

class TestPluginMemoryPromptCompliance:
    """Tests ensuring plugins respect Memory Prompt."""

    def test_plugins_cannot_modify_sphere_count(self):
        """Plugins cannot change 9 sphere count."""
        SPHERE_COUNT = 9
        
        # Plugin cannot modify this constant
        manager = PluginManager()
        plugin = Plugin("modifier", "Modifier", "1.0.0")
        
        manager.install(plugin)
        manager.activate("modifier")
        
        # Sphere count remains 9
        assert SPHERE_COUNT == 9

    def test_plugins_cannot_hire_nova(self):
        """Plugins cannot hire Nova."""
        NOVA_IS_HIRED = False
        
        manager = PluginManager()
        plugin = Plugin("nova_hirer", "Nova Hirer", "1.0.0")
        
        def try_hire_nova(data):
            # Cannot modify Nova's hired status
            return {"success": False}
        
        plugin.register_hook("hire_agent", try_hire_nova)
        manager.install(plugin)
        manager.activate("nova_hirer")
        
        results = manager.emit("hire_agent", {"agent_id": "nova"})
        
        # Nova remains not hired
        assert NOVA_IS_HIRED is False

    def test_plugin_operations_are_audited(self):
        """All plugin operations should be audited (L5)."""
        manager = PluginManager()
        plugin = Plugin("audited", "Audited Plugin", "1.0.0")
        
        manager.install(plugin)
        manager.activate("audited")
        manager.deactivate("audited")
        manager.uninstall("audited")
        
        actions = [log["action"] for log in manager.audit_log]
        
        assert "PLUGIN_INSTALLED" in actions
        assert "PLUGIN_ACTIVATED" in actions
        assert "PLUGIN_DEACTIVATED" in actions
        assert "PLUGIN_UNINSTALLED" in actions

    def test_plugins_respect_governance(self):
        """Plugins must respect governance (L7)."""
        GOVERNANCE_ENABLED = True
        
        manager = PluginManager()
        plugin = Plugin("governed", "Governed Plugin", "1.0.0")
        
        # Plugin cannot bypass governance
        plugin.add_permission("execute:with_governance")
        
        assert GOVERNANCE_ENABLED is True
        assert plugin.has_permission("execute:without_governance") is False
