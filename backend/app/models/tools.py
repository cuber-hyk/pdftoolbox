TOOLS_DB = [
    {
        'id': 'merge',
        'name': 'PDF Merge',
        'description': 'Combine multiple PDF files into one. Drag to reorder.',
        'icon': 'merge',
        'route': '/tools/merge',
        'category': 'Basic Tools',
        'max_files': 20,
        'max_size_mb': 100,
        'max_total_size_mb': 200,
        'options': [
            {
                'name': 'output_filename',
                'type': 'string',
                'label': 'Output Filename',
                'default': 'merged.pdf',
                'required': False
            }
        ]
    },
    {
        'id': 'split',
        'name': 'PDF Split',
        'description': 'Split a PDF file into multiple files',
        'icon': 'scissors',
        'route': '/tools/split',
        'category': 'Basic Tools',
        'max_files': 1,
        'max_size_mb': 100,
        'max_total_size_mb': 100,
        'options': [
            {
                'name': 'mode',
                'type': 'select',
                'label': 'Split Mode',
                'options': [
                    {'value': 'range', 'label': 'Extract Pages by Range'},
                    {'value': 'every', 'label': 'Split Every N Pages'},
                    {'value': 'single', 'label': 'Split into Single Pages'}
                ],
                'default': 'range'
            },
            {
                'name': 'ranges',
                'type': 'string',
                'label': 'Page Ranges',
                'description': 'Enter page ranges (e.g., 1-3, 5-7). Use -1 for last page.',
                'placeholder': '1-3, 5-7, 9-10',
                'depends_on': {'mode': 'range'},
                'required_when': {'mode': 'range'}
            },
            {
                'name': 'every_n',
                'type': 'number',
                'label': 'Pages per File',
                'description': 'Split the PDF every N pages',
                'min': 1,
                'max': 100,
                'default': 2,
                'depends_on': {'mode': 'every'},
                'required_when': {'mode': 'every'}
            }
        ]
    },
    {
        'id': 'extract_pages',
        'name': 'Extract Pages',
        'description': 'Extract specific pages from PDF to create a new file',
        'icon': 'file-text',
        'route': '/tools/extract-pages',
        'category': 'Extract Tools',
        'max_files': 1,
        'max_size_mb': 100,
        'max_total_size_mb': 100,
        'options': [
            {
                'name': 'pages',
                'type': 'string',
                'label': 'Pages',
                'description': 'e.g., 1,3,5-7,9',
                'placeholder': '1,3,5-7,9',
                'required': True
            }
        ]
    },
    {
        'id': 'extract_text',
        'name': 'Extract Text',
        'description': 'Extract text content from PDF files',
        'icon': 'type',
        'route': '/tools/extract-text',
        'category': 'Extract Tools',
        'max_files': 1,
        'max_size_mb': 50,
        'max_total_size_mb': 50,
        'options': [
            {
                'name': 'format',
                'type': 'select',
                'label': 'Output Format',
                'options': [
                    {'value': 'txt', 'label': 'Plain Text (.txt)'},
                    {'value': 'json', 'label': 'JSON (.json)'}
                ],
                'default': 'txt'
            }
        ]
    },
    {
        'id': 'add_watermark',
        'name': 'Add Watermark',
        'description': 'Add text or image watermark to PDF',
        'icon': 'droplet',
        'route': '/tools/add-watermark',
        'category': 'Watermark Tools',
        'max_files': 1,
        'max_size_mb': 100,
        'max_total_size_mb': 100,
        'options': [
            {
                'name': 'type',
                'type': 'select',
                'label': 'Watermark Type',
                'options': [
                    {'value': 'text', 'label': 'Text Watermark'},
                    {'value': 'image', 'label': 'Image Watermark'}
                ],
                'default': 'text'
            },
            {
                'name': 'text',
                'type': 'string',
                'label': 'Watermark Text',
                'placeholder': 'Enter watermark text',
                'required': False
            },
            {
                'name': 'opacity',
                'type': 'number',
                'label': 'Opacity',
                'min': 0,
                'max': 100,
                'default': 30
            },
            {
                'name': 'rotation',
                'type': 'number',
                'label': 'Rotation Angle',
                'description': 'Any angle from 0 to 360 degrees is supported',
                'min': 0,
                'max': 360,
                'default': 45
            }
        ]
    },
    {
        'id': 'pdf_to_images',
        'name': 'PDF to Images',
        'description': 'Convert PDF pages to images',
        'icon': 'image',
        'route': '/tools/pdf-to-images',
        'category': 'Convert Tools',
        'max_files': 1,
        'max_size_mb': 100,
        'max_total_size_mb': 100,
        'options': [
            {
                'name': 'mode',
                'type': 'select',
                'label': 'Page Selection',
                'options': [
                    {'value': 'all', 'label': 'All Pages'},
                    {'value': 'range', 'label': 'Page Range'},
                    {'value': 'single', 'label': 'Single Page'}
                ],
                'default': 'all'
            },
            {
                'name': 'ranges',
                'type': 'string',
                'label': 'Page Ranges',
                'description': 'Enter page ranges (e.g., 1-3, 5-7)',
                'placeholder': '1-3, 5-7',
                'depends_on': {'mode': 'range'},
                'required_when': {'mode': 'range'}
            },
            {
                'name': 'page',
                'type': 'number',
                'label': 'Page Number',
                'description': 'Single page to convert',
                'min': 1,
                'max': 10000,
                'default': 1,
                'depends_on': {'mode': 'single'},
                'required_when': {'mode': 'single'}
            },
            {
                'name': 'format',
                'type': 'select',
                'label': 'Output Format',
                'options': [
                    {'value': 'png', 'label': 'PNG'},
                    {'value': 'jpg', 'label': 'JPG'},
                    {'value': 'webp', 'label': 'WebP'}
                ],
                'default': 'png'
            },
            {
                'name': 'dpi',
                'type': 'select',
                'label': 'Resolution',
                'options': [
                    {'value': '72', 'label': '72 DPI (Screen)'},
                    {'value': '150', 'label': '150 DPI (HD)'},
                    {'value': '300', 'label': '300 DPI (Print)'}
                ],
                'default': '150'
            }
        ]
    },
    {
        'id': 'remove_watermark',
        'name': 'Remove Watermark',
        'description': 'Remove watermarks and clean PDF pages',
        'icon': 'droplet',
        'route': '/tools/remove-watermark',
        'category': 'Watermark Tools',
        'max_files': 1,
        'max_size_mb': 100,
        'max_total_size_mb': 100,
        'options': [
            {
                'name': 'mode',
                'type': 'select',
                'label': 'Removal Mode',
                'options': [
                    {'value': 'all', 'label': 'Clear All Pages'},
                    {'value': 'range', 'label': 'Page Range'},
                    {'value': 'every', 'label': 'Every N Pages'},
                    {'value': 'single', 'label': 'Single Page'}
                ],
                'default': 'all'
            },
            {
                'name': 'ranges',
                'type': 'string',
                'label': 'Page Ranges',
                'description': 'Enter page ranges (e.g., 1-3, 5-7)',
                'placeholder': '1-3, 5-7',
                'depends_on': {'mode': 'range'},
                'required_when': {'mode': 'range'}
            },
            {
                'name': 'every_n',
                'type': 'number',
                'label': 'Every N Pages',
                'description': 'Remove watermark from every N pages',
                'min': 2,
                'max': 100,
                'default': 2,
                'depends_on': {'mode': 'every'},
                'required_when': {'mode': 'every'}
            },
            {
                'name': 'page',
                'type': 'number',
                'label': 'Page Number',
                'description': 'Single page to remove watermark from',
                'min': 1,
                'max': 10000,
                'default': 1,
                'depends_on': {'mode': 'single'},
                'required_when': {'mode': 'single'}
            }
        ]
    },
    {
        'id': 'remove_watermark_image',
        'name': 'Remove Watermark (Color)',
        'description': 'Remove watermarks by selecting watermark color from preview',
        'icon': 'droplet',
        'route': '/tools/remove-watermark-image',
        'category': 'Watermark Tools',
        'max_files': 1,
        'max_size_mb': 100,
        'max_total_size_mb': 100,
        'options': [
            {
                'name': 'watermark_color',
                'type': 'color',
                'label': 'Watermark Color',
                'description': 'Click on the preview to select the watermark color',
                'default': [200, 200, 200]
            },
            {
                'name': 'tolerance',
                'type': 'number',
                'label': 'Color Tolerance',
                'description': 'Color matching tolerance (higher = more aggressive)',
                'min': 10,
                'max': 100,
                'default': 30
            },
            {
                'name': 'background_color',
                'type': 'color',
                'label': 'Background Color',
                'description': 'Color to replace watermark with',
                'default': [255, 255, 255]
            },
            {
                'name': 'mode',
                'type': 'select',
                'label': 'Removal Mode',
                'options': [
                    {'value': 'all', 'label': 'All Pages'},
                    {'value': 'range', 'label': 'Page Range'},
                    {'value': 'every', 'label': 'Every N Pages'},
                    {'value': 'single', 'label': 'Single Page'}
                ],
                'default': 'all'
            },
            {
                'name': 'ranges',
                'type': 'string',
                'label': 'Page Ranges',
                'description': 'Enter page ranges (e.g., 1-3, 5-7)',
                'placeholder': '1-3, 5-7',
                'depends_on': {'mode': 'range'},
                'required_when': {'mode': 'range'}
            },
            {
                'name': 'every_n',
                'type': 'number',
                'label': 'Every N Pages',
                'description': 'Remove watermark from every N pages',
                'min': 2,
                'max': 100,
                'default': 2,
                'depends_on': {'mode': 'every'},
                'required_when': {'mode': 'every'}
            },
            {
                'name': 'page',
                'type': 'number',
                'label': 'Page Number',
                'description': 'Single page to remove watermark from',
                'min': 1,
                'max': 10000,
                'default': 1,
                'depends_on': {'mode': 'single'},
                'required_when': {'mode': 'single'}
            },
            {
                'name': 'dpi',
                'type': 'select',
                'label': 'Render Quality',
                'description': 'Higher DPI = better quality but slower processing',
                'options': [
                    {'value': '150', 'label': '150 DPI (Fast)'},
                    {'value': '200', 'label': '200 DPI (Balanced)'},
                    {'value': '300', 'label': '300 DPI (High Quality)'}
                ],
                'default': '200'
            }
        ]
    }
]
