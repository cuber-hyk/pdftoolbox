export default {
  common: {
    // 通用按钮和操作
    download: '下载',
    retry: '重试',
    backToHome: '返回首页',
    processing: '处理中...',
    processingComplete: '处理完成',
    uploadFailed: '上传失败',
    removeFile: '删除文件',
    zoomIn: '放大',
    zoomOut: '缩小',
    reset: '重置',
    // 单位
    megabyte: 'MB',
    pages: '页',
    // 页面导航
    pageNavigation: '{current} / {total}'
  },

  home: {
    title: '简单快速的 PDF 工具',
    subtitle: '无需注册，完全免费，保护您的隐私',
    allTools: '所有工具'
  },

  footer: {
    copyright: '© 2026 PDF Toolbox',
    privacy: '隐私政策',
    terms: '服务条款',
    github: 'GitHub'
  },

  paramConfig: {
    permissions: '权限',
    permissionsNote: '注意：某些 PDF 阅读器（尤其是浏览器）可能会忽略这些限制。为了完全保护，请使用 Adobe Acrobat。'
  },

  fileUpload: {
    dragDropHere: '拖拽文件到此处',
    orClickToSelect: '或点击选择文件 (最多 {max} 个)',
    selectFiles: '选择文件',
    fileSizeLimit: '支持 {tool} 文件，单文件最大 {size}MB',
    addMoreFiles: '添加更多文件',
    addMoreFilesBtn: '添加更多文件',
    filesSelected: '{count}/{max} 个文件已选择',
    maxFilesReached: '已达到最大文件数',
    removeToAddMore: '删除部分文件后可添加其他文件',
    uploading: '正在上传...',
    selectedFiles: '已选文件:',
    dragReorderHint: '拖拽可调整顺序 • 文件将按此顺序处理',
    dropToUpload: '释放文件开始上传',
    dragPdfHere: '拖拽 PDF 文件到此处',
    previewWatermark: '预览水印效果实时显示'
  },

  fileList: {
    selectedFiles: '已选文件 ({count} 个):',
    totalSize: '总计: {size}'
  },

  resultCard: {
    processingComplete: '处理完成!',
    fileReadyForDownload: '您的文件已准备好下载',
    processAgain: '再次处理',
    autoDeleteNotice: '文件将在 2 小时后自动删除',
    processingFailed: '处理失败'
  },

  removeWatermark: {
    pdfPreview: 'PDF 预览',
    clearMode: '清除模式',
    modeAllPages: '清除所有页面',
    modePageRange: '指定页面范围',
    modeEveryNPages: '每隔 N 页',
    modeSinglePage: '指定单页',
    pageRange: '页面范围',
    pageRangePlaceholder: '例如: 1-3, 5, 7-9',
    pageRangeHelp: '支持格式：单页(5)、范围(1-3)、末页(1--1)',
    intervalPages: '间隔页数',
    intervalHelp: '清除每 {n} 页的内容',
    pageNumber: '指定页码',
    totalPages: '共 {count} 页',
    removeWatermark: '清除水印',
    alertPdfOnly: '请上传 PDF 文件',
    alertEnterPageRange: '请输入页面范围',
    previewFailed: 'PDF 预览失败: {error}'
  },

  removeWatermarkImg: {
    pdfPreview: 'PDF 预览',
    clickToSelectColor: '点击选择此颜色',
    watermarkColor: '水印颜色',
    selectedColor: '选中颜色',
    clickWatermarkArea: '点击预览图中的水印区域自动选择颜色',
    colorTolerance: '颜色容差',
    toleranceHelp: '值越大，匹配颜色范围越广',
    replaceColor: '替换颜色',
    backgroundColor: '背景颜色',
    clearMode: '清除模式',
    renderQuality: '渲染质量',
    dpiOptions: {
      fast: '150 DPI (快速)',
      balanced: '200 DPI (平衡)',
      high: '300 DPI (高质量)'
    },
    qualityHelp: '更高的质量需要更长的处理时间',
    removeWatermark: '去除水印',
    alertPdfOnly: '请上传 PDF 文件',
    alertEnterPageRange: '请输入页面范围',
    previewFailed: 'PDF 预览失败: {error}'
  },

  watermark: {
    unknownError: '未知错误',
    renderFailed: 'PDF 渲染失败',
    checkConsole: '请检查控制台获取更多信息',
    generateFailed: '生成水印失败，请重试',
    pdfPreview: 'PDF 预览',
    hideThumbnails: '隐藏缩略图',
    showThumbnails: '显示缩略图',
    previousPage: '上一页',
    nextPage: '下一页',
    watermarkContent: '水印内容',
    watermarkTextPlaceholder: '输入水印文字',
    watermarkSettings: '水印设置',
    fontSize: '字体大小',
    rotation: '旋转角度',
    opacity: '不透明度',
    color: '颜色',
    size: '尺寸',
    watermarkSpacing: '水印间距',
    reset: '重置',
    watermarkPreview: '水印预览',
    previewDescription: '显示颜色、旋转和不透明度效果',
    configurePreview: '配置后查看预览',
    addWatermark: '添加水印',
    processing: '处理中...',
    processingComplete: '处理完成'
  }
}
