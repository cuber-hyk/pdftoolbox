export default {
  common: {
    // Common buttons and actions
    download: 'Download',
    retry: 'Retry',
    backToHome: 'Back to Home',
    processing: 'Processing...',
    processingComplete: 'Processing Complete',
    uploadFailed: 'Upload failed',
    removeFile: 'Remove file',
    zoomIn: 'Zoom in',
    zoomOut: 'Zoom out',
    reset: 'Reset',
    // Units
    megabyte: 'MB',
    pages: 'pages',
    // Page navigation
    pageNavigation: '{current} / {total}'
  },

  home: {
    title: 'Simple & Fast PDF Tools',
    subtitle: 'No registration required, completely free, protect your privacy',
    allTools: 'All Tools'
  },

  footer: {
    copyright: '© 2026 PDF Toolbox',
    privacy: 'Privacy',
    terms: 'Terms',
    github: 'GitHub'
  },

  paramConfig: {
    permissions: 'Permissions',
    permissionsNote: 'Note: Some PDF viewers (especially browsers) may ignore these restrictions. For full protection, use Adobe Acrobat.'
  },

  fileUpload: {
    dragDropHere: 'Drag files here',
    orClickToSelect: 'Or click to select files (max {max} files)',
    selectFiles: 'Select Files',
    fileSizeLimit: 'Supports {tool} files, max {size}MB per file',
    addMoreFiles: 'Add more files',
    addMoreFilesBtn: 'Add More Files',
    filesSelected: '{count}/{max} files selected',
    maxFilesReached: 'Maximum files reached',
    removeToAddMore: 'Remove some files to add more',
    uploading: 'Uploading...',
    selectedFiles: 'Selected files:',
    dragReorderHint: 'Drag to reorder • Files will be processed in this order',
    dropToUpload: 'Drop files to upload',
    dragPdfHere: 'Drag PDF file here',
    previewWatermark: 'Watermark preview shown in real-time'
  },

  fileList: {
    selectedFiles: 'Selected files ({count}):',
    totalSize: 'Total: {size}'
  },

  resultCard: {
    processingComplete: 'Processing Complete!',
    fileReadyForDownload: 'Your file is ready for download',
    processAgain: 'Process Again',
    autoDeleteNotice: 'Files will be automatically deleted after 2 hours',
    processingFailed: 'Processing Failed'
  },

  removeWatermark: {
    pdfPreview: 'PDF Preview',
    clearMode: 'Clear Mode',
    modeAllPages: 'All pages',
    modePageRange: 'Page range',
    modeEveryNPages: 'Every N pages',
    modeSinglePage: 'Single page',
    pageRange: 'Page Range',
    pageRangePlaceholder: 'e.g. 1-3, 5, 7-9',
    pageRangeHelp: 'Supported formats: single (5), range (1-3), last page (1--1)',
    intervalPages: 'Interval Pages',
    intervalHelp: 'Clear content every {n} pages',
    pageNumber: 'Page Number',
    totalPages: 'Total {count} pages',
    removeWatermark: 'Remove Watermark',
    alertPdfOnly: 'Please upload a PDF file',
    alertEnterPageRange: 'Please enter a page range',
    previewFailed: 'PDF preview failed: {error}'
  },

  removeWatermarkImg: {
    pdfPreview: 'PDF Preview',
    clickToSelectColor: 'Click to select this color',
    watermarkColor: 'Watermark Color',
    selectedColor: 'Selected Color',
    clickWatermarkArea: 'Click the watermark area in the preview to auto-select color',
    colorTolerance: 'Color Tolerance',
    toleranceHelp: 'Higher value matches a wider color range',
    replaceColor: 'Replace Color',
    backgroundColor: 'Background Color',
    clearMode: 'Clear Mode',
    renderQuality: 'Render Quality',
    dpiOptions: {
      fast: '150 DPI (Fast)',
      balanced: '200 DPI (Balanced)',
      high: '300 DPI (High Quality)'
    },
    qualityHelp: 'Higher quality requires longer processing time',
    removeWatermark: 'Remove Watermark',
    alertPdfOnly: 'Please upload a PDF file',
    alertEnterPageRange: 'Please enter a page range',
    previewFailed: 'PDF preview failed: {error}'
  },

  watermark: {
    unknownError: 'Unknown error',
    renderFailed: 'PDF render failed',
    checkConsole: 'Please check console for more details',
    generateFailed: 'Failed to generate watermark, please try again',
    pdfPreview: 'PDF Preview',
    hideThumbnails: 'Hide thumbnails',
    showThumbnails: 'Show thumbnails',
    previousPage: 'Previous page',
    nextPage: 'Next page',
    watermarkContent: 'Watermark Content',
    watermarkTextPlaceholder: 'Enter watermark text',
    watermarkSettings: 'Watermark Settings',
    fontSize: 'Font Size',
    rotation: 'Rotation',
    opacity: 'Opacity',
    color: 'Color',
    size: 'Size',
    watermarkSpacing: 'Watermark Spacing',
    reset: 'Reset',
    watermarkPreview: 'Watermark Preview',
    previewDescription: 'Shows color, rotation, and opacity effects',
    configurePreview: 'Configure to see preview',
    addWatermark: 'Add Watermark',
    processing: 'Processing...',
    processingComplete: 'Processing Complete'
  }
}
