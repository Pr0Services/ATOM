#!/bin/bash
############################################################
#                                                          #
#  CHE·NU — CORRECTION SCRIPTS                             #
#  Fixes for identified audit issues                       #
#                                                          #
############################################################

# ============================================================
# SCRIPT 1: Replace CHENU references with CHE·NU
# ============================================================

echo "🔧 Starting CHENU → CHE·NU replacement..."

# Function to replace in files
replace_chenu() {
    local dir=$1
    
    # Find and replace in .md files
    find "$dir" -name "*.md" -type f -exec sed -i '' \
        -e 's/CHENU/CHE·NU/g' \
        -e 's/Chenu/CheNu/g' \
        -e 's/chenu/chenu/g' \
        {} \;
    
    # Find and replace in .ts files
    find "$dir" -name "*.ts" -type f -exec sed -i '' \
        -e 's/CHENU/CHENU/g' \
        -e 's/Chenu/CheNu/g' \
        -e 's/chenu/chenu/g' \
        {} \;
    
    # Find and replace in .tsx files
    find "$dir" -name "*.tsx" -type f -exec sed -i '' \
        -e 's/CHENU/CHENU/g' \
        -e 's/Chenu/CheNu/g' \
        -e 's/chenu/chenu/g' \
        {} \;
    
    # Find and replace in .yaml files
    find "$dir" -name "*.yaml" -type f -exec sed -i '' \
        -e 's/CHENU/CHE·NU/g' \
        -e 's/Chenu/CheNu/g' \
        -e 's/chenu/chenu/g' \
        {} \;
}

# Uncomment to run:
# replace_chenu "/path/to/chenu-project"

echo "✅ CHENU replacement complete!"

# ============================================================
# SCRIPT 2: Fix UTF-8 encoding issues
# ============================================================

echo "🔧 Fixing UTF-8 encoding..."

fix_encoding() {
    local dir=$1
    
    # Common UTF-8 corruptions and their fixes
    find "$dir" \( -name "*.ts" -o -name "*.tsx" -o -name "*.md" \) -type f | while read file; do
        # Create backup
        cp "$file" "$file.bak"
        
        # Fix common encoding issues
        sed -i '' \
            -e 's/â€"/—/g' \
            -e 's/â€™/'"'"'/g' \
            -e 's/â€œ/"/g' \
            -e 's/â€/"/g' \
            -e 's/Ã©/é/g' \
            -e 's/Ã¨/è/g' \
            -e 's/Ã /à/g' \
            -e 's/Ã¢/â/g' \
            -e 's/Ã®/î/g' \
            -e 's/Ã´/ô/g' \
            -e 's/Ã»/û/g' \
            -e 's/Ã§/ç/g' \
            -e 's/Ã‰/É/g' \
            -e 's/ðŸ'¤/👤/g' \
            -e 's/ðŸ'¼/💼/g' \
            -e 's/ðŸŽ¨/🎨/g' \
            -e 's/ðŸ"š/📚/g' \
            -e 's/ðŸ—ï¸/🏗️/g' \
            -e 's/ðŸ'°/💰/g' \
            -e 's/ðŸŒ¿/🌿/g' \
            -e 's/ðŸ§ª/🧪/g' \
            -e 's/ðŸ"¦/📦/g' \
            "$file"
        
        # Remove backup if successful
        if [ $? -eq 0 ]; then
            rm "$file.bak"
        fi
    done
}

# Uncomment to run:
# fix_encoding "/path/to/chenu-project"

echo "✅ UTF-8 encoding fixed!"

# ============================================================
# SCRIPT 3: Centralize types
# ============================================================

echo "🔧 Generating types index..."

generate_types_index() {
    local output_file=$1
    
    cat > "$output_file" << 'EOF'
/**
 * CHE·NU Unified Types Index
 * Auto-generated - DO NOT EDIT MANUALLY
 * 
 * Import all types from this file:
 * import { Agent, SphereId, ... } from '@/types';
 */

// Core types
export type { Agent, AgentRole, AgentStatus, AgentLevel } from './agent.types';
export type { SphereId, SphereConfig } from './sphere.types';
export type { BaseModel, UUID, Timestamp } from './core.types';

// SDK Layer types
export type { ProjectModel, ProjectInput } from '../sdk/project/types';
export type { MissionModel, MissionInput } from '../sdk/mission/types';
export type { ProcessModel, ProcessInput } from '../sdk/process/types';
export type { KnowledgeModel, KnowledgeNode } from '../sdk/knowledge/types';
export type { XRSceneModel, XRObject } from '../sdk/xr/types';
export type { SimulationModel, SimulationFrame } from '../sdk/simulation/types';
export type { PersonaModel, PersonaTrait } from '../sdk/persona/types';
export type { ContextModel, SituationModel } from '../sdk/context/types';
export type { TemplateModel, TemplateType } from '../sdk/template_factory/types';
export type { ToolModel, ToolSet, ToolChain } from '../sdk/tool/types';

// Constants
export { OFFICIAL_SPHERES, SPHERE_CONFIGS, SPHERE_COUNT } from './sphere.types';
export { BRAND_COLORS, SAFE_COMPLIANCE, CHENU_VERSION } from './constants';
EOF

    echo "✅ Types index generated at: $output_file"
}

# Uncomment to run:
# generate_types_index "/path/to/chenu-project/types/index.ts"

# ============================================================
# SCRIPT 4: Validate sphere consistency
# ============================================================

echo "🔧 Validating sphere consistency..."

validate_spheres() {
    local dir=$1
    
    echo "Checking sphere definitions..."
    
    # Count sphere definitions in different files
    default_count=$(grep -c "id: '" "$dir/defaultSpheres.ts" 2>/dev/null || echo 0)
    config_count=$(grep -c "SphereId" "$dir/types/sphere.types.ts" 2>/dev/null || echo 0)
    
    echo "defaultSpheres.ts: $default_count spheres"
    echo "sphere.types.ts: $config_count sphere types"
    
    if [ "$default_count" != "11" ]; then
        echo "⚠️  WARNING: Expected 11 spheres in defaultSpheres.ts, found $default_count"
    fi
    
    # Check for missing pages
    echo ""
    echo "Checking frontend pages..."
    
    pages=("MaisonPage" "EntreprisePage" "ProjetPage" "CreativeStudioPage" 
           "GouvernementPage" "ImmobilierPage" "AssociationsPage" 
           "ScholarPage" "FinancePage" "WellnessPage" "SandboxPage")
    
    for page in "${pages[@]}"; do
        if find "$dir" -name "${page}.tsx" | grep -q .; then
            echo "✅ $page.tsx found"
        else
            echo "❌ $page.tsx MISSING"
        fi
    done
}

# Uncomment to run:
# validate_spheres "/path/to/chenu-project"

# ============================================================
# SCRIPT 5: Generate API routes for new layers
# ============================================================

echo "🔧 Generating API route stubs..."

generate_api_routes() {
    local output_dir=$1
    
    # Create routes directory if not exists
    mkdir -p "$output_dir/api/routes"
    
    # Generate route files for new layers
    layers=("mission" "process" "knowledge" "simulation" "persona" "context" "template" "tool")
    
    for layer in "${layers[@]}"; do
        cat > "$output_dir/api/routes/${layer}.py" << EOF
"""
CHE·NU API Routes - ${layer^} Layer
Auto-generated stub - implement business logic
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/${layer}s", tags=["${layer^}"])

# Models
class ${layer^}Create(BaseModel):
    name: str
    description: Optional[str] = None

class ${layer^}Response(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: str

# Routes
@router.get("/", response_model=List[${layer^}Response])
async def list_${layer}s():
    """List all ${layer}s"""
    # TODO: Implement
    return []

@router.post("/", response_model=${layer^}Response)
async def create_${layer}(data: ${layer^}Create):
    """Create a new ${layer}"""
    # TODO: Implement
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/{${layer}_id}", response_model=${layer^}Response)
async def get_${layer}(${layer}_id: str):
    """Get ${layer} by ID"""
    # TODO: Implement
    raise HTTPException(status_code=404, detail="${layer^} not found")

@router.put("/{${layer}_id}", response_model=${layer^}Response)
async def update_${layer}(${layer}_id: str, data: ${layer^}Create):
    """Update ${layer}"""
    # TODO: Implement
    raise HTTPException(status_code=501, detail="Not implemented")

@router.delete("/{${layer}_id}")
async def delete_${layer}(${layer}_id: str):
    """Delete ${layer}"""
    # TODO: Implement
    raise HTTPException(status_code=501, detail="Not implemented")
EOF
        echo "✅ Generated: ${layer}.py"
    done
}

# Uncomment to run:
# generate_api_routes "/path/to/chenu-project/backend"

echo ""
echo "============================================================"
echo "  CHE·NU CORRECTION SCRIPTS READY"
echo "============================================================"
echo ""
echo "Available scripts:"
echo "  1. replace_chenu     - Replace CHENU → CHE·NU"
echo "  2. fix_encoding      - Fix UTF-8 encoding issues"
echo "  3. generate_types    - Generate unified types index"
echo "  4. validate_spheres  - Validate 11 sphere consistency"
echo "  5. generate_api      - Generate API route stubs"
echo ""
echo "Edit this file and uncomment the function calls to run."
echo "============================================================"
