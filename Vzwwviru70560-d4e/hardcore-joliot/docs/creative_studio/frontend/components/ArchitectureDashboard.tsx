// Creative Studio - Architecture BIM Dashboard
// React + TypeScript Component

import React, { useState, useEffect } from 'react';
import { Upload, Eye, Download, AlertTriangle, CheckCircle, Clock } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useCreativeStudio } from '@/hooks/useCreativeStudio';
import * as THREE from 'three';

interface BIMProject {
  id: string;
  name: string;
  status: string;
  lastClashCheck?: Date;
  clashCount?: number;
  latestVersion?: number;
}

interface ClashData {
  total: number;
  critical: number;
  major: number;
  minor: number;
}

export const ArchitectureDashboard: React.FC = () => {
  const { user } = useAuth();
  const { bimProjects, uploadModel, runClashDetection } = useCreativeStudio();
  
  const [projects, setProjects] = useState<BIMProject[]>([]);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [clashData, setClashData] = useState<ClashData | null>(null);
  const [uploading, setUploading] = useState(false);
  const [detecting, setDetecting] = useState(false);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    const data = await bimProjects.list();
    setProjects(data);
  };

  const handleModelUpload = async (file: File, projectId: string) => {
    setUploading(true);
    try {
      await uploadModel(file, projectId);
      await loadProjects();
      
      // Auto-run clash detection on new upload
      handleClashDetection(projectId);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleClashDetection = async (projectId: string) => {
    setDetecting(true);
    try {
      const result = await runClashDetection({
        project_id: projectId,
        disciplines: ['architecture', 'structure', 'mep'],
        tolerance: 0.01
      });
      
      setClashData({
        total: result.total_clashes,
        critical: result.critical,
        major: result.major,
        minor: result.minor
      });
    } catch (error) {
      console.error('Clash detection failed:', error);
    } finally {
      setDetecting(false);
    }
  };

  return (
    <div className="architecture-dashboard p-6">
      {/* Header */}
      <div className="header mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Architecture & BIM
        </h1>
        <p className="text-gray-600 mt-2">
          Manage BIM projects, detect clashes, and collaborate with clients
        </p>
      </div>

      {/* Quick Stats */}
      <div className="stats-grid grid grid-cols-4 gap-4 mb-8">
        <StatCard
          title="Active Projects"
          value={projects.filter(p => p.status === 'active').length}
          icon={<CheckCircle className="text-green-500" />}
        />
        <StatCard
          title="Pending Clashes"
          value={projects.reduce((sum, p) => sum + (p.clashCount || 0), 0)}
          icon={<AlertTriangle className="text-yellow-500" />}
        />
        <StatCard
          title="Models Uploaded"
          value={projects.reduce((sum, p) => sum + (p.latestVersion || 0), 0)}
          icon={<Upload className="text-blue-500" />}
        />
        <StatCard
          title="In Review"
          value={projects.filter(p => p.status === 'review').length}
          icon={<Eye className="text-purple-500" />}
        />
      </div>

      {/* Projects List */}
      <div className="projects-section mb-8">
        <h2 className="text-xl font-semibold mb-4">BIM Projects</h2>
        <div className="grid grid-cols-1 gap-4">
          {projects.map(project => (
            <ProjectCard
              key={project.id}
              project={project}
              onSelect={() => setSelectedProject(project.id)}
              onUpload={(file) => handleModelUpload(file, project.id)}
              onClashCheck={() => handleClashDetection(project.id)}
              selected={selectedProject === project.id}
            />
          ))}
        </div>
      </div>

      {/* Clash Detection Results */}
      {clashData && (
        <div className="clash-results bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">
            Clash Detection Results
          </h3>
          <div className="grid grid-cols-4 gap-4">
            <ClashCard
              label="Total Clashes"
              count={clashData.total}
              color="gray"
            />
            <ClashCard
              label="Critical"
              count={clashData.critical}
              color="red"
            />
            <ClashCard
              label="Major"
              count={clashData.major}
              color="yellow"
            />
            <ClashCard
              label="Minor"
              count={clashData.minor}
              color="blue"
            />
          </div>
        </div>
      )}

      {/* 3D Model Viewer */}
      {selectedProject && (
        <ModelViewer projectId={selectedProject} />
      )}
    </div>
  );
};

// Sub-components

const StatCard: React.FC<{ title: string; value: number; icon: React.ReactNode }> = ({
  title,
  value,
  icon
}) => (
  <div className="stat-card bg-white rounded-lg shadow p-4">
    <div className="flex items-center justify-between mb-2">
      <span className="text-sm text-gray-600">{title}</span>
      {icon}
    </div>
    <div className="text-2xl font-bold">{value}</div>
  </div>
);

const ProjectCard: React.FC<{
  project: BIMProject;
  onSelect: () => void;
  onUpload: (file: File) => void;
  onClashCheck: () => void;
  selected: boolean;
}> = ({ project, onSelect, onUpload, onClashCheck, selected }) => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      onUpload(e.target.files[0]);
    }
  };

  return (
    <div 
      className={`project-card bg-white rounded-lg shadow p-6 cursor-pointer transition-all ${
        selected ? 'ring-2 ring-blue-500' : ''
      }`}
      onClick={onSelect}
    >
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold">{project.name}</h3>
          <p className="text-sm text-gray-600">
            Status: <span className="capitalize">{project.status}</span>
          </p>
          {project.clashCount && project.clashCount > 0 && (
            <p className="text-sm text-yellow-600 flex items-center gap-1 mt-1">
              <AlertTriangle size={14} />
              {project.clashCount} clashes detected
            </p>
          )}
        </div>
        
        <div className="flex gap-2">
          <label className="btn btn-primary cursor-pointer">
            <Upload size={16} />
            <span>Upload Model</span>
            <input
              type="file"
              accept=".rvt,.ifc,.nwd"
              className="hidden"
              onChange={handleFileChange}
            />
          </label>
          
          <button
            className="btn btn-secondary"
            onClick={(e) => {
              e.stopPropagation();
              onClashCheck();
            }}
          >
            <AlertTriangle size={16} />
            <span>Check Clashes</span>
          </button>
        </div>
      </div>
    </div>
  );
};

const ClashCard: React.FC<{
  label: string;
  count: number;
  color: 'gray' | 'red' | 'yellow' | 'blue';
}> = ({ label, count, color }) => {
  const colorClasses = {
    gray: 'bg-gray-100 text-gray-800',
    red: 'bg-red-100 text-red-800',
    yellow: 'bg-yellow-100 text-yellow-800',
    blue: 'bg-blue-100 text-blue-800'
  };

  return (
    <div className={`clash-card rounded-lg p-4 ${colorClasses[color]}`}>
      <div className="text-sm font-medium mb-1">{label}</div>
      <div className="text-3xl font-bold">{count}</div>
    </div>
  );
};

const ModelViewer: React.FC<{ projectId: string }> = ({ projectId }) => {
  const viewerRef = React.useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!viewerRef.current) return;

    // Initialize Three.js viewer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    
    renderer.setSize(viewerRef.current.clientWidth, viewerRef.current.clientHeight);
    viewerRef.current.appendChild(renderer.domElement);

    // Load BIM model
    // ... (model loading logic)

    return () => {
      renderer.dispose();
    };
  }, [projectId]);

  return (
    <div className="model-viewer mt-8">
      <h3 className="text-lg font-semibold mb-4">3D Model Viewer</h3>
      <div ref={viewerRef} className="bg-gray-100 rounded-lg" style={{ height: '600px' }} />
    </div>
  );
};

export default ArchitectureDashboard;
