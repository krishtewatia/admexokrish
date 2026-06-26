"""
1×1 transparent GIF pixel for email open tracking.
Pre-computed as raw bytes — no file I/O at request time.
"""

import base64

# Minimal 1×1 transparent GIF (43 bytes)
TRANSPARENT_GIF_B64 = (
    "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
)

TRANSPARENT_GIF_BYTES: bytes = base64.b64decode(TRANSPARENT_GIF_B64)

# Response headers for the tracking pixel
PIXEL_HEADERS = {
    "Content-Type": "image/gif",
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0",
}
