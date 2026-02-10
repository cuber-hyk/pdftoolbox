"""Pytest configuration and fixtures."""
import pytest
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_pdf_path():
    """Get path to sample PDF file for testing.

    Returns:
        Path to sample PDF
    """
    # In production, this would point to a real test PDF
    # For now, we'll create a minimal test PDF when needed
    from pathlib import Path
    test_data_dir = Path(__file__).parent / "fixtures"
    test_data_dir.mkdir(exist_ok=True)
    return test_data_dir / "sample.pdf"


@pytest.fixture
def sample_pdf_content():
    """Get sample PDF content.

    Returns:
        PDF content bytes
    """
    # Minimal valid PDF
    return b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Count 1
/Kids [3 0 R]
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Test PDF) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000226 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
312
%%EOF
"""


@pytest.fixture
def temp_pdf_file(sample_pdf_content, tmp_path):
    """Create temporary PDF file.

    Args:
        sample_pdf_content: PDF content
        tmp_path: Pytest tmp_path fixture

    Returns:
        Path to temporary PDF file
    """
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(sample_pdf_content)
    return pdf_path
