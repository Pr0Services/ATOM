# CHE·NU API DOCUMENTATION

**Complete API Reference**

---

## 📚 AVAILABLE DOCUMENTATION

1. **[API Specs v29](./CHENU_API_SPECS_v29.md)** — Complete API specifications
2. **[Swagger/OpenAPI](./swagger.json)** — Interactive API documentation
3. **[Master Reference](./CHENU_MASTER_REFERENCE_v5_FINAL__1_.md)** — System architecture
4. **[System Manual](./CHENU_SYSTEM_MANUAL.md)** — Complete system manual
5. **[Agent Prompts](./CHENU_AGENT_PROMPTS_v29.md)** — 226 agent definitions
6. **[Mermaid Diagrams](./CHENU_MERMAID_DIAGRAMS_v29.md)** — Visual architecture

---

## 🚀 QUICK START

See [../api/README.md](../api/README.md) for complete setup instructions.

---

## 📖 CHAPTERS

Detailed documentation for each engine:

- [Backstage Intelligence](./chapters/BACKSTAGE_INTELLIGENCE_CHAPTER.md)
- [DataSpace Engine](./chapters/DATASPACE_ENGINE_CHAPTER.md)
- [Immobilier Domain](./chapters/IMMOBILIER_DOMAIN_CHAPTER.md)
- [Layout Engine](./chapters/LAYOUT_ENGINE_CHAPTER.md)
- [Meeting System](./chapters/MEETING_SYSTEM_CHAPTER.md)
- [Memory Governance](./chapters/MEMORY_GOVERNANCE_CHAPTER.md)
- [OCW (Collaborative Whiteboard)](./chapters/OCW_CHAPTER.md)
- [OneClick Engine](./chapters/ONECLICK_ENGINE_CHAPTER.md)
- [Workspace Engine](./chapters/WORKSPACE_ENGINE_CHAPTER.md)

---

## 🔐 AUTHENTICATION

All endpoints (except `/auth/register` and `/auth/login`) require JWT authentication:

```http
Authorization: Bearer <token>
X-Identity-ID: <identity_uuid>
```

---

## 📊 API STATISTICS

- **Total Endpoints:** 107+
- **Total Tables:** 57
- **Total Agents:** 226
- **Middleware:** Governed Execution Pipeline (10 steps)
- **Governance:** Tree Laws (8 rules)

---

**For detailed endpoint documentation, see [CHENU_API_SPECS_v29.md](./CHENU_API_SPECS_v29.md)**
