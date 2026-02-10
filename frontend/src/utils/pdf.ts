import * as pdfjsLib from 'pdfjs-dist'

// 设置 PDF.js worker - 使用固定版本避免缓存问题
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js'

export interface PDFPageImage {
  pageNumber: number
  dataUrl: string
  width: number
  height: number
  // 实际 PDF 页面尺寸（未缩放）
  actualWidth: number
  actualHeight: number
}

/**
 * 将 PDF 文件渲染为页面图像列表
 */
export async function renderPDFToImages(
  file: File,
  maxPages: number = 10,
  scale: number = 1.5
): Promise<PDFPageImage[]> {
  if (!file) {
    throw new Error('文件为空')
  }

  const arrayBuffer = await file.arrayBuffer()

  if (!arrayBuffer || arrayBuffer.byteLength === 0) {
    throw new Error('文件内容为空')
  }

  try {
    const loadingTask = pdfjsLib.getDocument({
      data: arrayBuffer
    })

    const pdf = await loadingTask.promise

    const totalPages = pdf.numPages
    const pagesToRender = Math.min(totalPages, maxPages)

    const images: PDFPageImage[] = []

    for (let i = 1; i <= pagesToRender; i++) {
      try {
        const page = await pdf.getPage(i)
        const viewport = page.getViewport({ scale })
        const actualViewport = page.getViewport({ scale: 1 }) // 实际尺寸

        // 创建 canvas
        const canvas = document.createElement('canvas')
        const context = canvas.getContext('2d')

        if (!context) {
          throw new Error('无法创建 canvas context')
        }

        canvas.width = viewport.width
        canvas.height = viewport.height

        // 渲染页面
        const renderContext = {
          canvasContext: context,
          viewport: viewport,
        }

        await page.render(renderContext).promise

        images.push({
          pageNumber: i,
          dataUrl: canvas.toDataURL('image/png'),
          width: viewport.width,
          height: viewport.height,
          actualWidth: actualViewport.width,
          actualHeight: actualViewport.height
        })
      } catch (pageError) {
        console.error(`渲染第 ${i} 页失败:`, pageError)
        // 继续渲染其他页面
      }
    }

    if (images.length === 0) {
      throw new Error('没有成功渲染任何页面')
    }

    return images
  } catch (error: any) {
    console.error('PDF 渲染错误:', error)
    throw new Error(`PDF 渲染失败: ${error.message || error}`)
  }
}

/**
 * 获取 PDF 页数
 */
export async function getPDFPageCount(file: File): Promise<number> {
  const arrayBuffer = await file.arrayBuffer()
  const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer })
  const pdf = await loadingTask.promise
  return pdf.numPages
}
