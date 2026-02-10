import html2canvas from 'html2canvas'

export interface WatermarkOptions {
  text: string
  fontSize?: number
  fontFamily?: string
  color?: string
  opacity?: number
  rotation?: number
  width?: number
  height?: number
  spacing?: number  // 间距（像素），用于在图像周围添加透明边距
}

/**
 * Generate watermark image from text options
 * Creates a hidden DOM element, renders it with html2canvas, and returns base64 PNG
 * Note: spacing is NOT included in the image; it's handled separately by CSS/Backend
 */
export async function generateWatermarkImage(options: WatermarkOptions): Promise<string> {
  const {
    text,
    fontSize = 50,
    fontFamily = 'Arial, sans-serif',
    color = 'rgba(128, 128, 128, 0.3)',
    opacity = 0.3,
    rotation = 0,
    width = 200,
    height = 200
  } = options

  // Create a container div for the watermark - use original dimensions only
  const container = document.createElement('div')
  container.style.position = 'absolute'
  container.style.left = '-9999px'
  container.style.top = '-9999px'
  container.style.width = `${width}px`
  container.style.height = `${height}px`
  container.style.display = 'flex'
  container.style.alignItems = 'center'
  container.style.justifyContent = 'center'
  container.style.backgroundColor = 'transparent'

  // Create text element
  const textEl = document.createElement('div')
  textEl.textContent = text
  textEl.style.fontSize = `${fontSize}px`
  textEl.style.fontFamily = fontFamily
  textEl.style.color = color
  textEl.style.opacity = `${opacity}`
  textEl.style.whiteSpace = 'nowrap'
  textEl.style.transform = `rotate(${rotation}deg)`
  textEl.style.transformOrigin = 'center'
  textEl.style.userSelect = 'none'

  container.appendChild(textEl)
  document.body.appendChild(container)

  try {
    // Convert to canvas - this produces the watermark at its actual size
    const canvas = await html2canvas(container, {
      backgroundColor: null,
      scale: 2, // Higher quality
      logging: false,
      useCORS: true
    })

    // Convert to base64
    const base64 = canvas.toDataURL('image/png')
    return base64
  } finally {
    // Clean up
    document.body.removeChild(container)
  }
}

/**
 * Parse RGBA color string to ensure opacity is applied
 */
export function parseColorWithOpacity(color: string, opacity: number): string {
  // If color already has alpha, just return it
  if (color.includes('rgba')) {
    return color
  }

  // Parse hex or rgb color and add opacity
  if (color.startsWith('#')) {
    const hex = color.slice(1)
    const r = parseInt(hex.slice(0, 2), 16)
    const g = parseInt(hex.slice(2, 4), 16)
    const b = parseInt(hex.slice(4, 6), 16)
    return `rgba(${r}, ${g}, ${b}, ${opacity})`
  }

  return color
}

/**
 * Generate unit preview watermark with fixed display parameters
 * This is used for the right-bottom unit preview area
 * Font size is fixed to ensure the preview always shows the complete watermark
 */
export async function generateUnitPreviewWatermark(options: WatermarkOptions): Promise<string> {
  const {
    text,
    fontSize = 50, // Original font size (will be scaled down)
    fontFamily = 'Arial, sans-serif',
    color = 'rgba(128, 128, 128, 0.3)',
    opacity = 0.3,
    rotation = 0,
    width = 200,
    height = 200
  } = options

  // Calculate scale factor to fit in preview container
  // Target container: ~280px width, 120px height
  const maxPreviewWidth = 260
  const maxPreviewHeight = 100

  // Calculate a fixed preview font size that's proportional but readable
  const scale = Math.min(maxPreviewWidth / width, maxPreviewHeight / height, 1)
  const previewFontSize = Math.max(12, fontSize * scale * 0.6) // Scale down but keep minimum 12px
  const previewWidth = width * scale
  const previewHeight = height * scale

  // Create a container div for the watermark
  const container = document.createElement('div')
  container.style.position = 'absolute'
  container.style.left = '-9999px'
  container.style.top = '-9999px'
  container.style.width = `${previewWidth}px`
  container.style.height = `${previewHeight}px`
  container.style.display = 'flex'
  container.style.alignItems = 'center'
  container.style.justifyContent = 'center'
  container.style.backgroundColor = 'transparent'

  // Create text element with FIXED font size for preview
  const textEl = document.createElement('div')
  textEl.textContent = text
  textEl.style.fontSize = `${previewFontSize}px` // Fixed font size for preview
  textEl.style.fontFamily = fontFamily
  textEl.style.color = color
  textEl.style.opacity = `${opacity}`
  textEl.style.whiteSpace = 'nowrap'
  textEl.style.transform = `rotate(${rotation}deg)`
  textEl.style.transformOrigin = 'center'
  textEl.style.userSelect = 'none'

  container.appendChild(textEl)
  document.body.appendChild(container)

  try {
    // Convert to canvas
    const canvas = await html2canvas(container, {
      backgroundColor: null,
      scale: 2, // Higher quality
      logging: false,
      useCORS: true
    })

    // Convert to base64
    const base64 = canvas.toDataURL('image/png')

    return base64
  } finally {
    // Clean up
    document.body.removeChild(container)
  }
}
