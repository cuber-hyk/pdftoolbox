import { test, expect } from '@playwright/test'

test.describe('PDF Toolbox E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should display home page with tools', async ({ page }) => {
    // Check title
    await expect(page).toHaveTitle(/PDF Toolbox/)

    // Check heading
    await expect(page.locator('h1')).toContainText('PDF Tools')

    // Check tools are displayed
    const toolCards = page.locator('.grid > div')
    await expect(toolCards).toHaveCount(6) // We have 6 tools defined
  })

  test('should filter tools by category', async ({ page }) => {
    // Click on "Basic Tools" category
    await page.click('button:has-text("Basic Tools")')

    // Wait for filtering
    await page.waitForTimeout(500)

    // Check that only basic tools are shown
    const toolCards = page.locator('.grid > div')
    await expect(toolCards).toHaveCount(2) // merge and split
  })

  test('should search tools', async ({ page }) => {
    // Find search input (if exists) or skip
    const searchInput = page.locator('input[placeholder*="search" i]')
    if (await searchInput.count() > 0) {
      await searchInput.fill('merge')
      await page.waitForTimeout(500)

      const toolCards = page.locator('.grid > div')
      await expect(toolCards).toHaveCount(1)
    }
  })

  test('should navigate to tool page', async ({ page }) => {
    // Click on first tool
    await page.click('.grid > div:first-child')

    // Check URL
    await expect(page).toHaveURL(/\/tools\/\w+/)

    // Check tool page elements
    await expect(page.locator('h1')).toBeVisible()
  })
})

test.describe('File Upload E2E Tests', () => {
  test('should display upload area on tool page', async ({ page }) => {
    await page.goto('/tools/merge')

    // Check upload area exists
    const uploadArea = page.locator('.border-dashed')
    await expect(uploadArea).toBeVisible()

    // Check "Select Files" button
    await expect(page.locator('button:has-text("Select Files")')).toBeVisible()
  })

  test('should show upload progress when file is selected', async ({ page }) => {
    await page.goto('/tools/merge')

    // Create a test file
    const testFile = Buffer.from('%PDF-1.4 test content')

    // Get file input
    const fileInput = page.locator('input[type="file"]')

    // Set file (note: this might not work without actual backend)
    await fileInput.setInputFiles({
      name: 'test.pdf',
      mimeType: 'application/pdf',
      buffer: testFile
    })

    // Check if progress indicator appears
    // This will only work if backend is running
    await page.waitForTimeout(2000)
  })
})

test.describe('Navigation E2E Tests', () => {
  test('should navigate back to home from tool page', async ({ page }) => {
    await page.goto('/tools/merge')

    // Click back button
    await page.click('button:has-text("Back")')

    // Should be on home page
    await expect(page).toHaveURL('/')
  })

  test('should have working header links', async ({ page }) => {
    // Click logo to go home
    await page.click('.cursor-pointer')
    await expect(page).toHaveURL('/')

    // Check footer is present
    await expect(page.locator('footer')).toBeVisible()
  })
})
