# Example R&D Proposal — VALID ✅

USER TYPE: Academic Researcher

CONTEXT: Professor has completed peer-reviewed research paper accepted in Nature journal. Wants to announce publication to professional network.

HUMAN ACTION: User clicks "Publish to Social" button in Scholar sphere, reviews preview of social post, confirms publication.

NEED: Share validated research results with professional community without manual reposting.

WHAT MUST NEVER BE AUTOMATED: Decision to publish (user must click), timing of publication, content of social post (user reviews first).

FAILURE RISK: Auto-publishing research could share preliminary/unvalidated work, violate journal embargos, or publish during inappropriate times.

SPHERES: Scholar, Social & Media

CONNECTION TYPE: Projection

HUMAN VALIDATION: Explicit per-action approval. User must click "Publish" button after reviewing generated social post preview. Action logged with timestamp and user_id in scholar_social_projections table.

UNDO/REVERSIBILITY: User can delete social post via "Remove Projection" button. Original Scholar content remains unchanged. Deletion logged in audit trail with undo_patch containing original post data.

REDUNDANCY CHECK: Verified against existing Scholar→Social features. No current projection mechanism exists. Checked social.py, scholar.py, and cross_sphere_requests table—no duplication.
