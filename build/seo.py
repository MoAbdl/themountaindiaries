# -*- coding: utf-8 -*-
"""Search and link-preview tags, shared by every page.

WhatsApp, iMessage, LinkedIn and X all read the Open Graph block below to draw
the preview card when someone pastes a link. Without it a shared link is a
bare URL. The image must be an absolute URL.
"""
SITE = 'https://themountaindiaries.com'
NAME = 'The Mountain Diaries'
DEFAULT_IMAGE = 'assets/images/hero-ebc.jpg'

# Social profiles. Empty means the footer icon is not shown at all: an icon
# that links nowhere is worse than no icon. Paste the full profile URL in to
# switch one on, then rebuild.
SOCIAL = {
    'Facebook': '',
    'Instagram': 'https://www.instagram.com/the_mountain_diaries/',
    'TikTok': 'https://www.tiktok.com/@the_mountain_diaries',
    'LinkedIn': 'https://www.linkedin.com/company/themountaindiaries/',
    'YouTube': 'https://www.youtube.com/@The_Mountain_Diaries',
}


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def meta(title, description, path='', image=DEFAULT_IMAGE):
    """The tag block that goes straight after <title>. `title` is plain text."""
    url = SITE + '/' + path
    img = SITE + '/' + image
    return '\n'.join([
        '<meta name="description" content="%s">' % esc(description),
        '<link rel="canonical" href="%s">' % url,
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="%s">' % NAME,
        '<meta property="og:title" content="%s">' % esc(title),
        '<meta property="og:description" content="%s">' % esc(description),
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:image" content="%s">' % img,
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="theme-color" content="#2E3438">',
    ])
