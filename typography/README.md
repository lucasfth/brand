# Website typography

Lucas approved this pairing on 2026-11-04 for the portfolio and links websites. It is separate from the existing Space Mono outlined wordmark, marks, favicons, QR codes and e-mail signatures. Those assets remain unchanged and keep their existing release pins.

| Role | Family | Consumers |
| --- | --- | --- |
| Editorial headings | Source Serif 4 | Portfolio and links |
| Reading text | Source Sans 3 | Portfolio |
| Navigation, metadata and code | Obel Mono | Portfolio |
| Buttons and supporting text | Obel Mono | Links |
| Terminal-style interface | Obel Mono | Hbit |
| Outlined wordmark | Space Mono | Existing logo assets, unchanged |

Self-host the required files from `fonts/`, preserving each family's OFL and provenance notices. `tokens.css` supplies font-face declarations and role variables without applying global styles. Copy the directory together with the CSS to preserve relative URLs, or use the same files through a framework's local-font loader.

Obel secret masking (`ss01`) is not enabled. Keep icon fonts separate. Links deliberately uses only serif and mono; Hbit stays entirely monospace. Developer terminal settings are managed separately in Config and retain Nerd Font fallback.

## Verification

```sh
python3 scripts/check-typography.py
```

The Source families are unmodified WOFF2 variable fonts from pinned commits in Adobe's official repositories. Obel Mono 1.000 comes from Typographic Systems. Each family's `SOURCE.txt` records source revisions or the archive URL, plus SHA-256 checksums. Each directory includes the corresponding OFL licence.

This website typography release does not re-typeset the logo or require consumers to bump their existing icon or signature release pins.
