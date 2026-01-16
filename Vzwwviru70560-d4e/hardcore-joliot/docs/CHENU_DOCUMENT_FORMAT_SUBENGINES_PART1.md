============================================================
DOCUMENT FORMAT ENGINE — 12 SUB-ENGINES (PART 1: 1-6)
============================================================

============================================================
17.1 — FORMAT SELECTOR SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/document-format/format-selector.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Format Selector Engine
 * ====================================
 * SAFE · REPRESENTATIONAL
 */

import type { 
  DocumentFormat, 
  FormatCategory, 
  UsageContext, 
  FormatProfile, 
  FormatRecommendation,
  FormatFeatures,
  CompatibilityInfo,
  FormatMeta 
} from '../document-format';

export class FormatSelectorEngine {
  private readonly VERSION = '1.0.0';

  recommend(context: UsageContext, input?: DocumentFormat): FormatRecommendation {
    const recommendation = this.getRecommendationForContext(context);
    
    return {
      id: `rec-${Date.now()}`,
      context,
      inputFormat: input || null,
      recommendedFormat: recommendation.primary,
      alternativeFormats: recommendation.alternatives,
      rationale: recommendation.rationale,
      considerations: recommendation.considerations,
      transformationRequired: input ? input !== recommendation.primary : false,
      meta: this.createMeta(context),
    };
  }

  getProfile(format: DocumentFormat): FormatProfile {
    const profiles = this.getAllProfiles();
    return profiles[format] || this.createDefaultProfile(format);
  }

  compare(formats: DocumentFormat[], context: UsageContext): FormatProfile[] {
    return formats.map(f => this.getProfile(f));
  }

  private getRecommendationForContext(context: UsageContext): {
    primary: DocumentFormat;
    alternatives: DocumentFormat[];
    rationale: string;
    considerations: string[];
  } {
    const recommendations: Record<UsageContext, {
      primary: DocumentFormat;
      alternatives: DocumentFormat[];
      rationale: string;
      considerations: string[];
    }> = {
      print: {
        primary: 'pdf',
        alternatives: ['docx', 'pptx'],
        rationale: 'PDF ensures consistent layout across all printers and devices',
        considerations: ['Embed fonts', 'Use CMYK colors', 'Check margins', 'Consider bleed'],
      },
      web: {
        primary: 'html',
        alternatives: ['md', 'pdf', 'svg'],
        rationale: 'HTML provides native web rendering with responsive capabilities',
        considerations: ['Optimize images', 'Ensure accessibility', 'Mobile responsive', 'SEO'],
      },
      email: {
        primary: 'pdf',
        alternatives: ['docx', 'html'],
        rationale: 'PDF is universally viewable and preserves formatting',
        considerations: ['File size limits', 'Preview compatibility', 'Security scanning'],
      },
      archive: {
        primary: 'pdf',
        alternatives: ['docx', 'xml'],
        rationale: 'PDF/A standard ensures long-term preservation',
        considerations: ['Use PDF/A format', 'Embed metadata', 'Include OCR layer'],
      },
      collaboration: {
        primary: 'docx',
        alternatives: ['md', 'html', 'xlsx'],
        rationale: 'DOCX supports track changes and comments natively',
        considerations: ['Version control', 'Cloud platform', 'Permission levels'],
      },
      presentation: {
        primary: 'pptx',
        alternatives: ['pdf', 'html', 'key'],
        rationale: 'PPTX provides full presentation features with animations',
        considerations: ['Embed fonts', 'Include media', 'Speaker notes', 'Compatibility mode'],
      },
      'data-exchange': {
        primary: 'json',
        alternatives: ['xml', 'csv', 'yaml'],
        rationale: 'JSON is lightweight, widely supported, and human-readable',
        considerations: ['Schema validation', 'Character encoding', 'Nested data support'],
      },
      api: {
        primary: 'json',
        alternatives: ['xml', 'yaml'],
        rationale: 'JSON is the standard for REST APIs',
        considerations: ['Schema definition', 'Versioning', 'Compression', 'Content negotiation'],
      },
      mobile: {
        primary: 'html',
        alternatives: ['pdf', 'json'],
        rationale: 'HTML adapts to mobile screens natively',
        considerations: ['Responsive design', 'Touch targets', 'Bandwidth', 'Offline support'],
      },
      accessibility: {
        primary: 'html',
        alternatives: ['pdf', 'docx', 'epub'],
        rationale: 'HTML provides best screen reader support',
        considerations: ['WCAG compliance', 'Alt text', 'Heading structure', 'Color contrast'],
      },
    };

    return recommendations[context] || recommendations.web;
  }

  private getAllProfiles(): Record<DocumentFormat, FormatProfile> {
    const createProfile = (
      format: DocumentFormat,
      category: FormatCategory,
      mimeType: string,
      description: string,
      features: Partial<FormatFeatures>,
      bestFor: string[],
      limitations: string[]
    ): FormatProfile => ({
      format,
      category,
      extension: `.${format}`,
      mimeType,
      description,
      features: {
        supportsFormatting: false,
        supportsImages: false,
        supportsTables: false,
        supportsHyperlinks: false,
        supportsEmbedding: false,
        supportsMetadata: false,
        supportsVersioning: false,
        supportsComments: false,
        supportsTrackedChanges: false,
        isEditable: true,
        isSearchable: true,
        isCompressible: true,
        preservesLayout: false,
        ...features,
      },
      compatibility: {
        platforms: ['Windows', 'macOS', 'Linux'],
        software: [],
        browsers: [],
        mobileSupport: true,
        offlineSupport: true,
      },
      bestFor,
      limitations,
    });

    return {
      // Documents
      pdf: createProfile('pdf', 'document', 'application/pdf', 'Portable Document Format',
        { supportsFormatting: true, supportsImages: true, supportsTables: true, supportsHyperlinks: true, supportsEmbedding: true, supportsMetadata: true, isEditable: false, preservesLayout: true },
        ['Print', 'Archive', 'Distribution', 'Official documents'],
        ['Not easily editable', 'Large file sizes with images', 'Limited accessibility if not tagged']
      ),
      docx: createProfile('docx', 'document', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'Microsoft Word Document',
        { supportsFormatting: true, supportsImages: true, supportsTables: true, supportsHyperlinks: true, supportsEmbedding: true, supportsMetadata: true, supportsVersioning: true, supportsComments: true, supportsTrackedChanges: true, preservesLayout: true },
        ['Collaboration', 'Editing', 'Business documents'],
        ['Requires Word or compatible software', 'Can have compatibility issues between versions']
      ),
      md: createProfile('md', 'document', 'text/markdown', 'Markdown',
        { supportsFormatting: true, supportsImages: true, supportsTables: true, supportsHyperlinks: true, isSearchable: true },
        ['Documentation', 'README files', 'Technical writing', 'Version control'],
        ['No native formatting in plain view', 'Limited complex formatting', 'Varies by renderer']
      ),
      html: createProfile('html', 'document', 'text/html', 'HyperText Markup Language',
        { supportsFormatting: true, supportsImages: true, supportsTables: true, supportsHyperlinks: true, supportsEmbedding: true, supportsMetadata: true, isSearchable: true },
        ['Web pages', 'Emails', 'Documentation', 'Accessibility'],
        ['Requires browser', 'Styling complexity', 'Security considerations']
      ),
      txt: createProfile('txt', 'document', 'text/plain', 'Plain Text',
        { isEditable: true, isSearchable: true, isCompressible: true },
        ['Simple notes', 'Logs', 'Configuration', 'Maximum compatibility'],
        ['No formatting', 'No images', 'No structure']
      ),
      // Presentations
      pptx: createProfile('pptx', 'presentation', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'Microsoft PowerPoint',
        { supportsFormatting: true, supportsImages: true, supportsTables: true, supportsHyperlinks: true, supportsEmbedding: true, supportsMetadata: true, supportsComments: true, preservesLayout: true },
        ['Presentations', 'Slides', 'Visual content'],
        ['Large file sizes', 'Requires PowerPoint or compatible', 'Animation compatibility']
      ),
      // Spreadsheets
      xlsx: createProfile('xlsx', 'spreadsheet', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'Microsoft Excel',
        { supportsFormatting: true, supportsImages: true, supportsTables: true, supportsHyperlinks: true, supportsEmbedding: true, supportsMetadata: true, supportsComments: true },
        ['Data analysis', 'Financial data', 'Calculations', 'Charts'],
        ['Requires Excel or compatible', 'Formula compatibility issues', 'Size limits']
      ),
      csv: createProfile('csv', 'spreadsheet', 'text/csv', 'Comma-Separated Values',
        { isEditable: true, isSearchable: true },
        ['Data exchange', 'Import/export', 'Simple data'],
        ['No formatting', 'Delimiter issues', 'No multiple sheets']
      ),
      // Data
      json: createProfile('json', 'data', 'application/json', 'JavaScript Object Notation',
        { supportsMetadata: false, isEditable: true, isSearchable: true },
        ['APIs', 'Configuration', 'Data exchange', 'Web applications'],
        ['No comments allowed', 'Limited data types', 'No schema by default']
      ),
      xml: createProfile('xml', 'data', 'application/xml', 'eXtensible Markup Language',
        { supportsMetadata: true, isEditable: true, isSearchable: true },
        ['Data exchange', 'Configuration', 'Document markup', 'Enterprise systems'],
        ['Verbose', 'Complex parsing', 'Larger file sizes']
      ),
      yaml: createProfile('yaml', 'data', 'application/x-yaml', 'YAML Ain\'t Markup Language',
        { isEditable: true, isSearchable: true },
        ['Configuration', 'CI/CD', 'Human-readable data'],
        ['Indentation sensitive', 'Less common in APIs', 'Parsing complexity']
      ),
      // Images
      png: createProfile('png', 'image', 'image/png', 'Portable Network Graphics',
        { supportsMetadata: true, isCompressible: false },
        ['Screenshots', 'Graphics with transparency', 'Web images'],
        ['Large file size for photos', 'No animation']
      ),
      jpg: createProfile('jpg', 'image', 'image/jpeg', 'JPEG Image',
        { supportsMetadata: true, isCompressible: true },
        ['Photos', 'Web images', 'Email attachments'],
        ['Lossy compression', 'No transparency', 'Artifacts on text']
      ),
      svg: createProfile('svg', 'vector', 'image/svg+xml', 'Scalable Vector Graphics',
        { supportsMetadata: true, isEditable: true, isSearchable: true },
        ['Logos', 'Icons', 'Diagrams', 'Responsive graphics'],
        ['Complex for photos', 'Browser variations', 'Security concerns']
      ),
    } as Record<DocumentFormat, FormatProfile>;
  }

  private createDefaultProfile(format: DocumentFormat): FormatProfile {
    return {
      format,
      category: 'document',
      extension: `.${format}`,
      mimeType: 'application/octet-stream',
      description: `${format.toUpperCase()} format`,
      features: {
        supportsFormatting: false,
        supportsImages: false,
        supportsTables: false,
        supportsHyperlinks: false,
        supportsEmbedding: false,
        supportsMetadata: false,
        supportsVersioning: false,
        supportsComments: false,
        supportsTrackedChanges: false,
        isEditable: true,
        isSearchable: false,
        isCompressible: true,
        preservesLayout: false,
      },
      compatibility: {
        platforms: ['Windows', 'macOS', 'Linux'],
        software: [],
        browsers: [],
        mobileSupport: false,
        offlineSupport: true,
      },
      bestFor: [],
      limitations: [],
    };
  }

  private createMeta(source: string): FormatMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'FormatSelectorEngine', version: this.VERSION, parent: 'DocumentFormatEngine' };
  }
}

export default FormatSelectorEngine;

============================================================
17.2 — TRANSFORMATION SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/document-format/transformation.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Transformation Engine
 * ===================================
 * SAFE · REPRESENTATIONAL
 */

import type { 
  DocumentFormat, 
  TransformationSpec, 
  TransformationTechnique, 
  TransformationStep,
  TransformationOptions,
  QualityPreservation,
  FormatMeta 
} from '../document-format';

export class TransformationEngine {
  private readonly VERSION = '1.0.0';

  plan(source: DocumentFormat, target: DocumentFormat): TransformationSpec {
    return {
      id: `transform-${Date.now()}`,
      source,
      target,
      technique: this.selectTechnique(source, target),
      steps: this.generateSteps(source, target),
      options: this.getDefaultOptions(),
      qualityPreservation: this.assessQuality(source, target),
      estimatedTime: this.estimateTime(source, target),
      meta: this.createMeta(`${source}->${target}`),
    };
  }

  getTechniques(source: DocumentFormat, target: DocumentFormat): TransformationTechnique[] {
    const techniquesMap: Record<string, TransformationTechnique[]> = {
      'docx->pdf': ['direct-conversion', 'parsing-rendering'],
      'md->html': ['direct-conversion', 'parsing-rendering'],
      'html->pdf': ['direct-conversion', 'parsing-rendering'],
      'xlsx->csv': ['direct-conversion', 'extraction-reconstruction'],
      'json->xml': ['direct-conversion', 'parsing-rendering'],
      'pdf->docx': ['ocr-based', 'extraction-reconstruction'],
      'jpg->png': ['direct-conversion'],
      'default': ['direct-conversion', 'intermediate-format'],
    };

    const key = `${source}->${target}`;
    return techniquesMap[key] || techniquesMap.default;
  }

  assessQuality(source: DocumentFormat, target: DocumentFormat): QualityPreservation {
    const qualityMap: Record<string, QualityPreservation> = {
      'docx->pdf': {
        formatting: 'full',
        layout: 'full',
        images: 'full',
        tables: 'full',
        hyperlinks: 'full',
        metadata: 'partial',
        warnings: ['Some dynamic elements may be flattened'],
      },
      'pdf->docx': {
        formatting: 'partial',
        layout: 'partial',
        images: 'full',
        tables: 'partial',
        hyperlinks: 'partial',
        metadata: 'partial',
        warnings: ['Complex layouts may not convert accurately', 'Scanned PDFs require OCR'],
      },
      'md->html': {
        formatting: 'full',
        layout: 'full',
        images: 'full',
        tables: 'full',
        hyperlinks: 'full',
        metadata: 'none',
        warnings: ['Extended markdown features depend on renderer'],
      },
      'xlsx->csv': {
        formatting: 'none',
        layout: 'none',
        images: 'none',
        tables: 'partial',
        hyperlinks: 'none',
        metadata: 'none',
        warnings: ['Only active sheet exported', 'Formulas become values', 'All formatting lost'],
      },
      'default': {
        formatting: 'partial',
        layout: 'partial',
        images: 'partial',
        tables: 'partial',
        hyperlinks: 'partial',
        metadata: 'partial',
        warnings: ['Quality may vary based on content complexity'],
      },
    };

    const key = `${source}->${target}`;
    return qualityMap[key] || qualityMap.default;
  }

  getMatrix(): Record<string, DocumentFormat[]> {
    return {
      pdf: ['docx', 'html', 'txt', 'png', 'jpg'],
      docx: ['pdf', 'html', 'txt', 'md', 'odt', 'rtf'],
      md: ['html', 'pdf', 'docx', 'txt'],
      html: ['pdf', 'docx', 'md', 'txt', 'epub'],
      xlsx: ['csv', 'pdf', 'html', 'json', 'xml'],
      csv: ['xlsx', 'json', 'xml'],
      json: ['xml', 'yaml', 'csv'],
      xml: ['json', 'yaml', 'csv', 'html'],
      pptx: ['pdf', 'html', 'png', 'jpg'],
      png: ['jpg', 'webp', 'gif', 'pdf'],
      jpg: ['png', 'webp', 'pdf'],
      svg: ['png', 'pdf', 'eps'],
    };
  }

  private selectTechnique(source: DocumentFormat, target: DocumentFormat): TransformationTechnique {
    const techniques = this.getTechniques(source, target);
    return techniques[0];
  }

  private generateSteps(source: DocumentFormat, target: DocumentFormat): TransformationStep[] {
    return [
      {
        id: 'step-1',
        order: 1,
        name: 'Parse Source',
        action: 'Read and parse source document',
        input: source,
        output: 'internal-representation',
        tool: 'parser',
        options: { preserveStructure: true },
      },
      {
        id: 'step-2',
        order: 2,
        name: 'Transform Structure',
        action: 'Convert internal structure to target format',
        input: 'internal-representation',
        output: 'transformed-structure',
        tool: 'transformer',
        options: { mapping: `${source}-to-${target}` },
      },
      {
        id: 'step-3',
        order: 3,
        name: 'Render Output',
        action: 'Generate target format output',
        input: 'transformed-structure',
        output: target,
        tool: 'renderer',
        options: { optimize: true },
      },
      {
        id: 'step-4',
        order: 4,
        name: 'Validate Output',
        action: 'Verify output format validity',
        input: target,
        output: 'validation-result',
        tool: 'validator',
        options: { strict: true },
      },
    ];
  }

  private getDefaultOptions(): TransformationOptions {
    return {
      preserveFormatting: true,
      preserveImages: true,
      preserveLinks: true,
      preserveMetadata: true,
      preserveStructure: true,
      embedFonts: true,
      compressOutput: false,
      optimizeForWeb: false,
      maintainAccessibility: true,
      quality: 'high',
    };
  }

  private estimateTime(source: DocumentFormat, target: DocumentFormat): string {
    const complexTransforms = ['pdf->docx', 'docx->html', 'xlsx->json'];
    if (complexTransforms.includes(`${source}->${target}`)) {
      return '5-30 seconds depending on file size';
    }
    return '1-5 seconds for typical documents';
  }

  getTransformationTools(): Record<string, string[]> {
    return {
      'docx->pdf': ['LibreOffice', 'Microsoft Word', 'Pandoc', 'docx4j'],
      'md->html': ['marked', 'markdown-it', 'Pandoc', 'remark'],
      'html->pdf': ['Puppeteer', 'wkhtmltopdf', 'Prince', 'WeasyPrint'],
      'xlsx->csv': ['SheetJS', 'ExcelJS', 'pandas', 'LibreOffice'],
      'json->xml': ['xml2js', 'fast-xml-parser', 'Custom converter'],
      'pdf->docx': ['pdf2docx', 'Adobe Acrobat', 'ABBYY FineReader'],
      'image->image': ['Sharp', 'ImageMagick', 'Pillow', 'GraphicsMagick'],
    };
  }

  private createMeta(source: string): FormatMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'TransformationEngine', version: this.VERSION, parent: 'DocumentFormatEngine' };
  }
}

export default TransformationEngine;

============================================================
17.3 — TEMPLATE SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/document-format/template.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Template Engine
 * =============================
 * SAFE · REPRESENTATIONAL
 */

import type { 
  DocumentFormat, 
  DocumentTemplate, 
  TemplateStructure,
  TemplateSection,
  TemplatePlaceholder,
  TemplateStyles,
  PageSetup,
  FormatMeta 
} from '../document-format';

export class TemplateEngine {
  private readonly VERSION = '1.0.0';

  getTemplates(format: DocumentFormat, category?: string): DocumentTemplate[] {
    const templates = this.getAllTemplates();
    let result = templates.filter(t => t.format === format);
    if (category) {
      result = result.filter(t => t.category === category);
    }
    return result;
  }

  create(input: string): DocumentTemplate {
    return {
      id: `template-${Date.now()}`,
      name: 'Custom Template',
      format: 'docx',
      category: 'custom',
      description: 'Custom document template',
      structure: this.createDefaultStructure(),
      placeholders: this.createDefaultPlaceholders(),
      styles: this.createDefaultStyles(),
      meta: this.createMeta(input),
    };
  }

  private getAllTemplates(): DocumentTemplate[] {
    return [
      // Document Templates
      {
        id: 'tpl-report',
        name: 'Business Report',
        format: 'docx',
        category: 'business',
        description: 'Professional business report template',
        structure: this.createReportStructure(),
        placeholders: [
          { id: 'p1', name: 'Title', type: 'text', required: true },
          { id: 'p2', name: 'Author', type: 'text', required: true },
          { id: 'p3', name: 'Date', type: 'date', required: true },
          { id: 'p4', name: 'Executive Summary', type: 'text', required: true },
          { id: 'p5', name: 'Data Table', type: 'table', required: false },
        ],
        styles: this.createDefaultStyles(),
        meta: this.createMeta('business-report'),
      },
      {
        id: 'tpl-memo',
        name: 'Internal Memo',
        format: 'docx',
        category: 'business',
        description: 'Standard internal memo template',
        structure: this.createMemoStructure(),
        placeholders: [
          { id: 'p1', name: 'To', type: 'text', required: true },
          { id: 'p2', name: 'From', type: 'text', required: true },
          { id: 'p3', name: 'Subject', type: 'text', required: true },
          { id: 'p4', name: 'Date', type: 'date', required: true },
          { id: 'p5', name: 'Body', type: 'text', required: true },
        ],
        styles: this.createDefaultStyles(),
        meta: this.createMeta('memo'),
      },
      {
        id: 'tpl-readme',
        name: 'README',
        format: 'md',
        category: 'technical',
        description: 'Project README template',
        structure: this.createReadmeStructure(),
        placeholders: [
          { id: 'p1', name: 'Project Name', type: 'text', required: true },
          { id: 'p2', name: 'Description', type: 'text', required: true },
          { id: 'p3', name: 'Installation', type: 'text', required: true },
          { id: 'p4', name: 'Usage', type: 'text', required: true },
        ],
        styles: this.createDefaultStyles(),
        meta: this.createMeta('readme'),
      },
      // Presentation Templates
      {
        id: 'tpl-pitch',
        name: 'Pitch Deck',
        format: 'pptx',
        category: 'business',
        description: 'Investor pitch deck template',
        structure: this.createPitchStructure(),
        placeholders: [
          { id: 'p1', name: 'Company Name', type: 'text', required: true },
          { id: 'p2', name: 'Problem', type: 'text', required: true },
          { id: 'p3', name: 'Solution', type: 'text', required: true },
          { id: 'p4', name: 'Market Size', type: 'text', required: true },
        ],
        styles: this.createDefaultStyles(),
        meta: this.createMeta('pitch-deck'),
      },
      // Spreadsheet Templates
      {
        id: 'tpl-budget',
        name: 'Budget Template',
        format: 'xlsx',
        category: 'finance',
        description: 'Monthly budget tracking template',
        structure: this.createBudgetStructure(),
        placeholders: [
          { id: 'p1', name: 'Month', type: 'text', required: true },
          { id: 'p2', name: 'Income Items', type: 'list', required: true },
          { id: 'p3', name: 'Expense Items', type: 'list', required: true },
        ],
        styles: this.createDefaultStyles(),
        meta: this.createMeta('budget'),
      },
      // Data Templates
      {
        id: 'tpl-api-response',
        name: 'API Response',
        format: 'json',
        category: 'technical',
        description: 'Standard API response template',
        structure: this.createApiStructure(),
        placeholders: [
          { id: 'p1', name: 'Data', type: 'text', required: true },
          { id: 'p2', name: 'Status', type: 'text', required: true },
        ],
        styles: this.createDefaultStyles(),
        meta: this.createMeta('api-response'),
      },
    ];
  }

  private createDefaultStructure(): TemplateStructure {
    return {
      sections: [
        { id: 'header', name: 'Header', type: 'header', required: true, repeatable: false, content: '' },
        { id: 'body', name: 'Body', type: 'body', required: true, repeatable: true, content: '' },
        { id: 'footer', name: 'Footer', type: 'footer', required: false, repeatable: false, content: '' },
      ],
      layout: 'single-column',
      pageSetup: { size: 'letter', orientation: 'portrait', margins: { top: '1in', right: '1in', bottom: '1in', left: '1in' } },
    };
  }

  private createReportStructure(): TemplateStructure {
    return {
      sections: [
        { id: 'title', name: 'Title Page', type: 'header', required: true, repeatable: false, content: 'Title, Author, Date' },
        { id: 'toc', name: 'Table of Contents', type: 'body', required: false, repeatable: false, content: 'Auto-generated TOC' },
        { id: 'exec', name: 'Executive Summary', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'intro', name: 'Introduction', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'findings', name: 'Findings', type: 'body', required: true, repeatable: true, content: '' },
        { id: 'conclusion', name: 'Conclusion', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'appendix', name: 'Appendix', type: 'body', required: false, repeatable: true, content: '' },
      ],
      layout: 'report',
      pageSetup: { size: 'letter', orientation: 'portrait', margins: { top: '1in', right: '1in', bottom: '1in', left: '1.5in' } },
    };
  }

  private createMemoStructure(): TemplateStructure {
    return {
      sections: [
        { id: 'header', name: 'Memo Header', type: 'header', required: true, repeatable: false, content: 'TO, FROM, DATE, SUBJECT' },
        { id: 'body', name: 'Body', type: 'body', required: true, repeatable: false, content: '' },
      ],
      layout: 'memo',
      pageSetup: { size: 'letter', orientation: 'portrait', margins: { top: '1in', right: '1in', bottom: '1in', left: '1in' } },
    };
  }

  private createReadmeStructure(): TemplateStructure {
    return {
      sections: [
        { id: 'title', name: 'Title', type: 'header', required: true, repeatable: false, content: '# Project Name' },
        { id: 'badges', name: 'Badges', type: 'body', required: false, repeatable: false, content: 'Status badges' },
        { id: 'description', name: 'Description', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'installation', name: 'Installation', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'usage', name: 'Usage', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'contributing', name: 'Contributing', type: 'body', required: false, repeatable: false, content: '' },
        { id: 'license', name: 'License', type: 'footer', required: false, repeatable: false, content: '' },
      ],
      layout: 'readme',
      pageSetup: { size: 'letter', orientation: 'portrait', margins: { top: '0', right: '0', bottom: '0', left: '0' } },
    };
  }

  private createPitchStructure(): TemplateStructure {
    return {
      sections: [
        { id: 'cover', name: 'Cover Slide', type: 'header', required: true, repeatable: false, content: 'Company Name, Tagline' },
        { id: 'problem', name: 'Problem', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'solution', name: 'Solution', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'market', name: 'Market', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'business', name: 'Business Model', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'traction', name: 'Traction', type: 'body', required: false, repeatable: false, content: '' },
        { id: 'team', name: 'Team', type: 'body', required: true, repeatable: false, content: '' },
        { id: 'ask', name: 'The Ask', type: 'footer', required: true, repeatable: false, content: '' },
      ],
      layout: 'slides',
      pageSetup: { size: 'custom', orientation: 'landscape', margins: { top: '0', right: '0', bottom: '0', left: '0' } },
    };
  }

  private createBudgetStructure(): TemplateStructure {
    return {
      sections: [
        { id: 'header', name: 'Header', type: 'header', required: true, repeatable: false, content: 'Month, Year' },
        { id: 'income', name: 'Income', type: 'body', required: true, repeatable: true, content: 'Income items' },
        { id: 'expenses', name: 'Expenses', type: 'body', required: true, repeatable: true, content: 'Expense categories' },
        { id: 'summary', name: 'Summary', type: 'footer', required: true, repeatable: false, content: 'Totals, Balance' },
      ],
      layout: 'spreadsheet',
      pageSetup: { size: 'letter', orientation: 'portrait', margins: { top: '0.5in', right: '0.5in', bottom: '0.5in', left: '0.5in' } },
    };
  }

  private createApiStructure(): TemplateStructure {
    return {
      sections: [
        { id: 'root', name: 'Root', type: 'body', required: true, repeatable: false, content: '{ "success": true, "data": {}, "meta": {} }' },
      ],
      layout: 'json',
      pageSetup: { size: 'letter', orientation: 'portrait', margins: { top: '0', right: '0', bottom: '0', left: '0' } },
    };
  }

  private createDefaultPlaceholders(): TemplatePlaceholder[] {
    return [
      { id: 'p1', name: 'Title', type: 'text', required: true },
      { id: 'p2', name: 'Content', type: 'text', required: true },
    ];
  }

  private createDefaultStyles(): TemplateStyles {
    return {
      fonts: [
        { name: 'heading', family: 'Arial, sans-serif', size: '24px', weight: 'bold', usage: 'Headings' },
        { name: 'body', family: 'Georgia, serif', size: '12px', weight: 'normal', usage: 'Body text' },
      ],
      colors: {
        primary: '#1a1a1a',
        secondary: '#666666',
        accent: '#0066cc',
        text: '#333333',
        background: '#ffffff',
      },
      headings: {
        h1: { fontFamily: 'Arial', fontSize: '24px', fontWeight: 'bold', color: '#1a1a1a', marginTop: '24px', marginBottom: '16px' },
        h2: { fontFamily: 'Arial', fontSize: '20px', fontWeight: 'bold', color: '#1a1a1a', marginTop: '20px', marginBottom: '12px' },
        h3: { fontFamily: 'Arial', fontSize: '16px', fontWeight: 'bold', color: '#333333', marginTop: '16px', marginBottom: '8px' },
        h4: { fontFamily: 'Arial', fontSize: '14px', fontWeight: 'bold', color: '#333333', marginTop: '12px', marginBottom: '6px' },
      },
      paragraphs: {
        fontFamily: 'Georgia',
        fontSize: '12px',
        lineHeight: '1.6',
        color: '#333333',
        marginBottom: '12px',
      },
    };
  }

  private createMeta(source: string): FormatMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'TemplateEngine', version: this.VERSION, parent: 'DocumentFormatEngine' };
  }
}

export default TemplateEngine;

============================================================
17.4 — STRUCTURE SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/document-format/structure.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Structure Engine
 * ==============================
 * SAFE · REPRESENTATIONAL
 */

import type { DocumentFormat, DocumentStructure, StructureSchema, StructureElement, ElementRelationship, FormatMeta } from '../document-format';

export class StructureEngine {
  private readonly VERSION = '1.0.0';

  get(format: DocumentFormat): DocumentStructure {
    const structures = this.getAllStructures();
    return structures[format] || this.createDefaultStructure(format);
  }

  define(input: string): DocumentStructure {
    return {
      id: `structure-${Date.now()}`,
      format: 'custom' as DocumentFormat,
      schema: { name: 'custom', version: '1.0', root: 'document', required: [], optional: [] },
      elements: [],
      relationships: [],
      meta: this.createMeta(input),
    };
  }

  private getAllStructures(): Record<string, DocumentStructure> {
    return {
      docx: {
        id: 'struct-docx',
        format: 'docx',
        schema: { name: 'OOXML WordprocessingML', version: '2019', root: 'document', required: ['body'], optional: ['header', 'footer', 'styles'] },
        elements: [
          { id: 'doc', name: 'document', type: 'root', parent: null, children: ['body'], attributes: {}, content: '' },
          { id: 'body', name: 'body', type: 'container', parent: 'doc', children: ['paragraph', 'table'], attributes: {}, content: '' },
          { id: 'p', name: 'paragraph', type: 'block', parent: 'body', children: ['run'], attributes: {}, content: '' },
          { id: 'r', name: 'run', type: 'inline', parent: 'p', children: ['text'], attributes: {}, content: '' },
          { id: 't', name: 'text', type: 'text', parent: 'r', children: [], attributes: {}, content: '' },
        ],
        relationships: [
          { from: 'doc', to: 'body', type: 'contains' },
          { from: 'body', to: 'p', type: 'contains' },
          { from: 'p', to: 'r', type: 'contains' },
        ],
        meta: this.createMeta('docx'),
      },
      html: {
        id: 'struct-html',
        format: 'html',
        schema: { name: 'HTML5', version: '5.0', root: 'html', required: ['head', 'body'], optional: [] },
        elements: [
          { id: 'html', name: 'html', type: 'root', parent: null, children: ['head', 'body'], attributes: { lang: 'en' }, content: '' },
          { id: 'head', name: 'head', type: 'container', parent: 'html', children: ['title', 'meta', 'link'], attributes: {}, content: '' },
          { id: 'body', name: 'body', type: 'container', parent: 'html', children: ['header', 'main', 'footer'], attributes: {}, content: '' },
        ],
        relationships: [
          { from: 'html', to: 'head', type: 'contains' },
          { from: 'html', to: 'body', type: 'contains' },
          { from: 'head', to: 'body', type: 'precedes' },
        ],
        meta: this.createMeta('html'),
      },
      json: {
        id: 'struct-json',
        format: 'json',
        schema: { name: 'JSON', version: 'RFC 8259', root: 'value', required: [], optional: [] },
        elements: [
          { id: 'value', name: 'value', type: 'any', parent: null, children: ['object', 'array', 'string', 'number', 'boolean', 'null'], attributes: {}, content: '' },
          { id: 'object', name: 'object', type: 'container', parent: 'value', children: ['member'], attributes: {}, content: '{}' },
          { id: 'array', name: 'array', type: 'container', parent: 'value', children: ['value'], attributes: {}, content: '[]' },
        ],
        relationships: [
          { from: 'object', to: 'member', type: 'contains' },
          { from: 'array', to: 'value', type: 'contains' },
        ],
        meta: this.createMeta('json'),
      },
      md: {
        id: 'struct-md',
        format: 'md',
        schema: { name: 'CommonMark', version: '0.30', root: 'document', required: [], optional: [] },
        elements: [
          { id: 'doc', name: 'document', type: 'root', parent: null, children: ['block'], attributes: {}, content: '' },
          { id: 'heading', name: 'heading', type: 'block', parent: 'doc', children: ['inline'], attributes: { level: '1-6' }, content: '' },
          { id: 'paragraph', name: 'paragraph', type: 'block', parent: 'doc', children: ['inline'], attributes: {}, content: '' },
          { id: 'list', name: 'list', type: 'block', parent: 'doc', children: ['item'], attributes: { type: 'ordered|unordered' }, content: '' },
          { id: 'code', name: 'code-block', type: 'block', parent: 'doc', children: [], attributes: { language: '' }, content: '' },
        ],
        relationships: [
          { from: 'doc', to: 'heading', type: 'contains' },
          { from: 'doc', to: 'paragraph', type: 'contains' },
          { from: 'list', to: 'item', type: 'contains' },
        ],
        meta: this.createMeta('md'),
      },
    };
  }

  private createDefaultStructure(format: DocumentFormat): DocumentStructure {
    return {
      id: `struct-${format}`,
      format,
      schema: { name: format, version: '1.0', root: 'root', required: [], optional: [] },
      elements: [{ id: 'root', name: 'root', type: 'root', parent: null, children: [], attributes: {}, content: '' }],
      relationships: [],
      meta: this.createMeta(format),
    };
  }

  private createMeta(source: string): FormatMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'StructureEngine', version: this.VERSION, parent: 'DocumentFormatEngine' };
  }
}

export default StructureEngine;

============================================================
17.5 — VALIDATION SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/document-format/validation.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Format Validation Engine
 * ======================================
 * SAFE · REPRESENTATIONAL
 */

import type { DocumentFormat, ValidationResult, ValidationError, ValidationWarning, FormatMeta } from '../document-format';

export class FormatValidationEngine {
  private readonly VERSION = '1.0.0';

  validate(format: DocumentFormat, content?: string): ValidationResult {
    return {
      id: `validation-${Date.now()}`,
      format,
      isValid: true, // Representational - actual validation would check content
      errors: this.getCommonErrors(format),
      warnings: this.getCommonWarnings(format),
      suggestions: this.getSuggestions(format),
      meta: this.createMeta(format),
    };
  }

  getSpecs(format: DocumentFormat): Record<string, unknown> {
    const specs: Record<string, Record<string, unknown>> = {
      pdf: {
        name: 'PDF',
        versions: ['1.0', '1.4', '1.5', '1.6', '1.7', '2.0'],
        substandards: ['PDF/A-1', 'PDF/A-2', 'PDF/A-3', 'PDF/X', 'PDF/UA'],
        maxSize: 'No official limit, practical ~100MB',
        specification: 'ISO 32000',
      },
      docx: {
        name: 'OOXML',
        versions: ['2007', '2010', '2013', '2016', '2019', '365'],
        specification: 'ISO/IEC 29500',
        maxSize: '512MB',
        encoding: 'UTF-8',
      },
      json: {
        name: 'JSON',
        specification: 'RFC 8259',
        encoding: 'UTF-8',
        dataTypes: ['string', 'number', 'boolean', 'null', 'array', 'object'],
        maxDepth: 'No limit, practical ~100 levels',
      },
      html: {
        name: 'HTML5',
        specification: 'WHATWG Living Standard',
        doctype: '<!DOCTYPE html>',
        encoding: 'UTF-8 recommended',
      },
      csv: {
        name: 'CSV',
        specification: 'RFC 4180',
        delimiter: 'Comma (configurable)',
        encoding: 'UTF-8 recommended',
        lineEnding: 'CRLF (cross-platform)',
      },
    };

    return specs[format] || { name: format, specification: 'Unknown' };
  }

  private getCommonErrors(format: DocumentFormat): ValidationError[] {
    const errorPatterns: Record<string, ValidationError[]> = {
      json: [
        { code: 'JSON001', message: 'Invalid JSON syntax', location: 'document', severity: 'critical', fix: 'Check for missing commas, brackets' },
        { code: 'JSON002', message: 'Trailing comma not allowed', location: 'object/array', severity: 'error', fix: 'Remove trailing comma' },
      ],
      xml: [
        { code: 'XML001', message: 'Malformed XML', location: 'document', severity: 'critical', fix: 'Check tag matching' },
        { code: 'XML002', message: 'Missing declaration', location: 'start', severity: 'error', fix: 'Add <?xml version="1.0"?>' },
      ],
      html: [
        { code: 'HTML001', message: 'Missing doctype', location: 'start', severity: 'error', fix: 'Add <!DOCTYPE html>' },
        { code: 'HTML002', message: 'Unclosed tags', location: 'various', severity: 'error', fix: 'Close all tags properly' },
      ],
      csv: [
        { code: 'CSV001', message: 'Inconsistent column count', location: 'rows', severity: 'error', fix: 'Ensure all rows have same columns' },
        { code: 'CSV002', message: 'Unescaped delimiter in field', location: 'field', severity: 'error', fix: 'Quote fields containing delimiters' },
      ],
    };

    return errorPatterns[format] || [];
  }

  private getCommonWarnings(format: DocumentFormat): ValidationWarning[] {
    return [
      { code: 'WARN001', message: 'Large file size may impact performance', location: 'document', suggestion: 'Consider compression or splitting' },
      { code: 'WARN002', message: 'Non-standard encoding detected', location: 'document', suggestion: 'Convert to UTF-8 for compatibility' },
    ];
  }

  private getSuggestions(format: DocumentFormat): string[] {
    return [
      'Validate against official schema',
      'Test in multiple applications',
      'Check accessibility compliance',
      'Verify metadata is complete',
      'Consider file size optimization',
    ];
  }

  getValidationTools(): Record<string, string[]> {
    return {
      json: ['jsonlint', 'ajv', 'JSON Schema Validator'],
      xml: ['xmllint', 'Xerces', 'XML Schema Validator'],
      html: ['W3C Validator', 'HTMLHint', 'axe-core'],
      css: ['CSSLint', 'stylelint', 'W3C CSS Validator'],
      pdf: ['JHOVE', 'veraPDF', 'Adobe Preflight'],
      docx: ['Open XML SDK', 'Office Validation Tool'],
    };
  }

  private createMeta(source: string): FormatMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'FormatValidationEngine', version: this.VERSION, parent: 'DocumentFormatEngine' };
  }
}

export default FormatValidationEngine;

============================================================
17.6 — OPTIMIZATION SUB-ENGINE
============================================================

--- FILE: /che-nu-sdk/core/document-format/optimization.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Optimization Engine
 * =================================
 * SAFE · REPRESENTATIONAL
 */

import type { DocumentFormat, OptimizationResult, OptimizationTechnique, FormatMeta } from '../document-format';

export class OptimizationEngine {
  private readonly VERSION = '1.0.0';

  plan(format: DocumentFormat, target: 'size' | 'quality' | 'web'): OptimizationResult {
    return {
      id: `optimize-${Date.now()}`,
      format,
      originalSize: 'Variable',
      optimizedSize: 'Depends on content',
      reduction: '10-90% typical',
      techniques: this.getTechniques(format).filter(t => this.isApplicable(t, target)),
      qualityImpact: this.getQualityImpact(target),
      meta: this.createMeta(format),
    };
  }

  getTechniques(format: DocumentFormat): OptimizationTechnique[] {
    const techniquesMap: Record<string, OptimizationTechnique[]> = {
      pdf: [
        { name: 'Image Compression', description: 'Compress embedded images', applied: true, impact: '30-70% size reduction' },
        { name: 'Font Subsetting', description: 'Include only used characters', applied: true, impact: '5-20% size reduction' },
        { name: 'Remove Metadata', description: 'Strip unnecessary metadata', applied: false, impact: '1-5% size reduction' },
        { name: 'Linearization', description: 'Optimize for web viewing', applied: true, impact: 'Faster first page display' },
        { name: 'Downsampling', description: 'Reduce image resolution', applied: false, impact: '20-50% size reduction' },
      ],
      docx: [
        { name: 'Image Compression', description: 'Compress embedded images', applied: true, impact: '20-60% size reduction' },
        { name: 'Remove Revisions', description: 'Clear tracked changes', applied: false, impact: '5-30% size reduction' },
        { name: 'Compress Media', description: 'Optimize embedded media', applied: true, impact: '30-50% size reduction' },
      ],
      png: [
        { name: 'Lossless Compression', description: 'Better PNG compression', applied: true, impact: '10-30% size reduction' },
        { name: 'Color Palette Reduction', description: 'Reduce color depth', applied: false, impact: '30-70% size reduction' },
        { name: 'Remove Metadata', description: 'Strip EXIF and chunks', applied: true, impact: '1-5% size reduction' },
      ],
      jpg: [
        { name: 'Quality Adjustment', description: 'Balance quality vs size', applied: true, impact: '20-80% size reduction' },
        { name: 'Progressive Encoding', description: 'Enable progressive load', applied: true, impact: 'Better perceived performance' },
        { name: 'Remove EXIF', description: 'Strip metadata', applied: true, impact: '1-10% size reduction' },
        { name: 'Chroma Subsampling', description: 'Reduce color resolution', applied: false, impact: '10-20% size reduction' },
      ],
      json: [
        { name: 'Minification', description: 'Remove whitespace', applied: true, impact: '20-40% size reduction' },
        { name: 'Key Shortening', description: 'Use shorter key names', applied: false, impact: '10-30% size reduction' },
        { name: 'Compression', description: 'GZIP compression', applied: true, impact: '70-90% transfer size reduction' },
      ],
      html: [
        { name: 'Minification', description: 'Remove whitespace and comments', applied: true, impact: '10-30% size reduction' },
        { name: 'Inline Critical CSS', description: 'Inline above-fold styles', applied: true, impact: 'Faster render' },
        { name: 'Lazy Loading', description: 'Defer non-critical resources', applied: true, impact: 'Faster initial load' },
        { name: 'Compression', description: 'GZIP/Brotli compression', applied: true, impact: '60-80% transfer size' },
      ],
    };

    return techniquesMap[format] || [];
  }

  private isApplicable(technique: OptimizationTechnique, target: string): boolean {
    if (target === 'quality') return !technique.name.includes('Reduction') && !technique.name.includes('Downsampling');
    if (target === 'size') return true;
    if (target === 'web') return technique.name.includes('Compression') || technique.name.includes('Minification') || technique.name.includes('Web');
    return true;
  }

  private getQualityImpact(target: 'size' | 'quality' | 'web'): string {
    const impacts: Record<string, string> = {
      size: 'Quality may be reduced depending on techniques applied',
      quality: 'Minimal to no quality loss',
      web: 'Optimized for fast loading with acceptable quality trade-offs',
    };
    return impacts[target];
  }

  getOptimizationTools(): Record<string, string[]> {
    return {
      pdf: ['Ghostscript', 'QPDF', 'Adobe Acrobat', 'PDF Compressor'],
      png: ['pngquant', 'optipng', 'pngcrush', 'TinyPNG'],
      jpg: ['jpegoptim', 'MozJPEG', 'jpegtran', 'TinyJPG'],
      svg: ['SVGO', 'svgcleaner', 'Nano SVG'],
      html: ['HTMLMinifier', 'html-minifier-terser'],
      css: ['cssnano', 'clean-css', 'PurgeCSS'],
      js: ['Terser', 'UglifyJS', 'esbuild'],
      json: ['json-minify', 'Native JSON.stringify'],
    };
  }

  private createMeta(source: string): FormatMeta {
    return {
      source,
      generated: new Date().toISOString(),
      version: this.VERSION,
      moduleType: 'operational_module',
      classification: 'not_a_sphere',
      safe: { isRepresentational: true },
    };
  }

  meta(): Record<string, unknown> {
    return { name: 'OptimizationEngine', version: this.VERSION, parent: 'DocumentFormatEngine' };
  }
}

export default OptimizationEngine;
