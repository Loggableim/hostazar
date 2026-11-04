"""Shared HTML fragments for hostazar generators (AdSense, performance, consent)."""

# Placeholder until ads.txt / Publisher-ID is configured in deploy (see Levin).
ADSENSE_CLIENT_ID = 'ca-pub-XXXXXXXXXXXXXXXX'

ADSENSE_LOADER_SCRIPT = (
    '  <script data-hz-src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
    + ADSENSE_CLIENT_ID
    + '" crossorigin="anonymous"></script>\n'
)

CONSENT_CSS = '  <link rel="stylesheet" href="/css/consent-banner.css">\n'

BODY_SCRIPTS = (
    '<script src="/data/script.js" defer></script>\n'
    '<script src="/js/consent-manager.js" defer></script>\n'
)


def ad_slot_responsive(label='Anzeige', slot_id='0000000000'):
    """Reserved ad area with fixed min-height to limit CLS."""
    return (
        '\n<!-- AdSense slot (reserved space) -->\n'
        '<div class="ad-slot ad-slot--responsive" role="complementary" aria-label="Werbung">\n'
        '  <span class="ad-slot-label">' + label + '</span>\n'
        '  <ins class="adsbygoogle"\n'
        '       style="display:block"\n'
        '       data-ad-client="' + ADSENSE_CLIENT_ID + '"\n'
        '       data-ad-slot="' + slot_id + '"\n'
        '       data-ad-format="auto"\n'
        '       data-full-width-responsive="true"></ins>\n'
        '</div>\n'
    )


def ad_slot_mid_article():
    return ad_slot_responsive('Anzeige — Artikelmitte')


def ad_slot_end_article():
    return ad_slot_responsive('Anzeige — Ende des Artikels')
