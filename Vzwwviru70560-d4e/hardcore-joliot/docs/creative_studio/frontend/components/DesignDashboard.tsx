// Creative Studio - Design & Brand Management
// React + TypeScript Component

import React, { useState, useEffect } from 'react';
import { Palette, Upload, Check, X, Search, Filter } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useCreativeStudio } from '@/hooks/useCreativeStudio';

interface BrandKit {
  id: string;
  name: string;
  primary_colors: string[];
  secondary_colors: string[];
  heading_font: string;
  body_font: string;
  logo_primary_url: string;
}

interface DesignAsset {
  id: string;
  name: string;
  type: string;
  file_url: string;
  thumbnail_url: string;
  colors_detected: string[];
  ai_tags: string[];
  created_at: Date;
}

export const DesignDashboard: React.FC = () => {
  const { user } = useAuth();
  const { brandKits, assets, checkCompliance, searchAssets } = useCreativeStudio();
  
  const [activeBrandKit, setActiveBrandKit] = useState<BrandKit | null>(null);
  const [assetList, setAssetList] = useState<DesignAsset[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedAsset, setSelectedAsset] = useState<string | null>(null);
  const [complianceResult, setComplianceResult] = useState<any>(null);

  useEffect(() => {
    loadBrandKit();
    loadAssets();
  }, []);

  const loadBrandKit = async () => {
    const kits = await brandKits.list();
    if (kits.length > 0) {
      setActiveBrandKit(kits[0]);
    }
  };

  const loadAssets = async () => {
    const data = await assets.list();
    setAssetList(data);
  };

  const handleAssetUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const result = await assets.upload(formData);
      setAssetList([result.asset, ...assetList]);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  const handleComplianceCheck = async (assetId: string) => {
    if (!activeBrandKit) return;
    
    const result = await checkCompliance({
      asset_id: assetId,
      checks: ['colors', 'fonts', 'logo_usage', 'spacing']
    });
    
    setComplianceResult(result);
  };

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    if (query) {
      const results = await searchAssets({ query });
      setAssetList(results.assets);
    } else {
      loadAssets();
    }
  };

  return (
    <div className="design-dashboard p-6">
      {/* Header */}
      <div className="header mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Design & Branding
        </h1>
        <p className="text-gray-600 mt-2">
          Manage brand assets, ensure consistency, and organize your creative work
        </p>
      </div>

      {/* Brand Kit Section */}
      {activeBrandKit && (
        <div className="brand-kit bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Active Brand Kit</h2>
          <div className="grid grid-cols-2 gap-6">
            {/* Colors */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Colors</h3>
              <div className="flex gap-2">
                {activeBrandKit.primary_colors.map((color, idx) => (
                  <div
                    key={idx}
                    className="w-12 h-12 rounded border-2 border-gray-200"
                    style={{ backgroundColor: color }}
                    title={color}
                  />
                ))}
              </div>
            </div>

            {/* Typography */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Typography</h3>
              <div className="space-y-1">
                <p className="text-sm">
                  <span className="font-semibold">Heading:</span> {activeBrandKit.heading_font}
                </p>
                <p className="text-sm">
                  <span className="font-semibold">Body:</span> {activeBrandKit.body_font}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Asset Library */}
      <div className="asset-library">
        {/* Search & Upload */}
        <div className="controls flex items-center gap-4 mb-6">
          <div className="search-bar flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search assets by name, tags, or colors..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg"
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
              />
            </div>
          </div>
          
          <label className="btn btn-primary cursor-pointer">
            <Upload size={16} />
            <span>Upload Asset</span>
            <input
              type="file"
              accept="image/*,.psd,.ai,.svg"
              className="hidden"
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  handleAssetUpload(e.target.files[0]);
                }
              }}
            />
          </label>
        </div>

        {/* Asset Grid */}
        <div className="asset-grid grid grid-cols-4 gap-4">
          {assetList.map(asset => (
            <AssetCard
              key={asset.id}
              asset={asset}
              onSelect={() => setSelectedAsset(asset.id)}
              onCheck={() => handleComplianceCheck(asset.id)}
              selected={selectedAsset === asset.id}
            />
          ))}
        </div>
      </div>

      {/* Compliance Results */}
      {complianceResult && (
        <CompliancePanel
          result={complianceResult}
          onClose={() => setComplianceResult(null)}
        />
      )}
    </div>
  );
};

// Sub-components

const AssetCard: React.FC<{
  asset: DesignAsset;
  onSelect: () => void;
  onCheck: () => void;
  selected: boolean;
}> = ({ asset, onSelect, onCheck, selected }) => (
  <div
    className={`asset-card bg-white rounded-lg shadow overflow-hidden cursor-pointer transition-all ${
      selected ? 'ring-2 ring-blue-500' : ''
    }`}
    onClick={onSelect}
  >
    {/* Thumbnail */}
    <div className="aspect-square bg-gray-100 relative">
      <img
        src={asset.thumbnail_url}
        alt={asset.name}
        className="w-full h-full object-cover"
      />
      {/* Type badge */}
      <div className="absolute top-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
        {asset.type}
      </div>
    </div>

    {/* Info */}
    <div className="p-3">
      <h3 className="text-sm font-medium truncate">{asset.name}</h3>
      
      {/* Colors detected */}
      <div className="flex gap-1 mt-2">
        {asset.colors_detected.slice(0, 5).map((color, idx) => (
          <div
            key={idx}
            className="w-4 h-4 rounded-full border border-gray-200"
            style={{ backgroundColor: color }}
          />
        ))}
      </div>

      {/* AI Tags */}
      <div className="flex flex-wrap gap-1 mt-2">
        {asset.ai_tags.slice(0, 3).map((tag, idx) => (
          <span
            key={idx}
            className="text-xs bg-gray-100 text-gray-700 px-2 py-0.5 rounded"
          >
            {tag}
          </span>
        ))}
      </div>

      {/* Action */}
      <button
        className="btn btn-sm btn-secondary w-full mt-3"
        onClick={(e) => {
          e.stopPropagation();
          onCheck();
        }}
      >
        <Check size={14} />
        Check Compliance
      </button>
    </div>
  </div>
);

const CompliancePanel: React.FC<{
  result: any;
  onClose: () => void;
}> = ({ result, onClose }) => (
  <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-auto">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b">
        <h2 className="text-xl font-semibold">Brand Compliance Results</h2>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
          <X size={24} />
        </button>
      </div>

      {/* Overall Score */}
      <div className="p-6 border-b">
        <div className="text-center">
          <div className="text-4xl font-bold mb-2">
            {Math.round(result.compliance.overall_score)}%
          </div>
          <div className="text-gray-600">Overall Compliance Score</div>
        </div>
      </div>

      {/* Individual Checks */}
      <div className="p-6 space-y-4">
        {Object.entries(result.compliance.checks).map(([key, check]: [string, any]) => (
          <div key={key} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <div className="font-medium capitalize">{key.replace('_', ' ')}</div>
              <div className="text-sm text-gray-600">{check.message}</div>
            </div>
            <div className={`text-2xl font-bold ${
              check.score >= 80 ? 'text-green-500' :
              check.score >= 60 ? 'text-yellow-500' :
              'text-red-500'
            }`}>
              {check.score}%
            </div>
          </div>
        ))}
      </div>

      {/* Suggestions */}
      {result.compliance.suggestions && (
        <div className="p-6 border-t">
          <h3 className="font-medium mb-3">Suggestions for Improvement</h3>
          <ul className="space-y-2">
            {result.compliance.suggestions.map((suggestion: string, idx: number) => (
              <li key={idx} className="flex items-start gap-2 text-sm">
                <span className="text-blue-500 mt-0.5">•</span>
                <span>{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  </div>
);

export default DesignDashboard;
