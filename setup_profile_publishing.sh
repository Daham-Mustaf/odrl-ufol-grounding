#!/usr/bin/env bash
#
# setup_profile_publishing.sh
#
# Scaffolds everything needed to publish the ODRL-Legal profile:
#   - licenses (code + ontology/docs)
#   - w3id.org redirect (.htaccess with content negotiation)
#   - ReSpec/HTML documentation generated from the .ttl with Widoco
#   - a GitHub Pages-ready docs/ folder
#
# It does NOT do the steps that need a human or a browser:
#   - opening the w3id pull request
#   - enabling GitHub Pages in repo settings
#   - pushing to GitHub
# Those are printed as a checklist at the end.
#
# Run from the repository root:  bash setup_profile_publishing.sh

set -euo pipefail

# ---------------------------------------------------------------------------
# Config: edit these to match your setup
# ---------------------------------------------------------------------------
GH_USER="Daham-Mustaf"
REPO="odrl-ufol-grounding"
PAGES_URL="https://daham-mustaf.github.io/${REPO}"
PROFILE_TTL="ODRL-Legal-Profile/odrl-legal-profile.ttl"
CODE_LICENSE="MIT"          # or Apache-2.0 (only MIT text is generated here)
ONTOLOGY_LICENSE_URL="https://creativecommons.org/licenses/by/4.0/"

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
command -v java >/dev/null 2>&1 || { echo "ERROR: java not found (needed for Widoco)."; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "ERROR: curl not found."; exit 1; }
[ -f "$PROFILE_TTL" ] || { echo "ERROR: $PROFILE_TTL not found. Run from the repo root."; exit 1; }

echo ">> Scaffolding publishing files for $REPO"

# ---------------------------------------------------------------------------
# 1. Code license (repo root)
# ---------------------------------------------------------------------------
if [ "$CODE_LICENSE" = "MIT" ]; then
cat > LICENSE <<EOF
MIT License

Copyright (c) $(date +%Y) Daham M. Mustafa, Christoph Lange, Giancarlo Guizzardi,
Diego Collarana, Christoph Quix, Stefan Decker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
echo "   wrote LICENSE (MIT, code)"
else
echo "   skipped LICENSE: set CODE_LICENSE=MIT or add Apache-2.0 text yourself"
fi

# ---------------------------------------------------------------------------
# 2. Ontology/docs license notice
# ---------------------------------------------------------------------------
cat > ODRL-Legal-Profile/LICENSE <<EOF
The ODRL Deontic-Legal Profile (odrl-l:) and its documentation are licensed
under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

  $ONTOLOGY_LICENSE_URL

You are free to share and adapt the material for any purpose, including
commercially, provided you give appropriate credit.
EOF
echo "   wrote ODRL-Legal-Profile/LICENSE (CC BY 4.0, ontology)"

# ---------------------------------------------------------------------------
# 3. w3id redirect (.htaccess): copy this folder into your perma-id fork
# ---------------------------------------------------------------------------
mkdir -p w3id/odrl-legal
cat > w3id/odrl-legal/.htaccess <<EOF
# w3id.org/odrl-legal/  (ODRL Deontic-Legal Profile)
# Copy this folder into a fork of github.com/perma-id/w3id.org and open a PR.
Options +FollowSymLinks
RewriteEngine on

# RDF clients get the Turtle ontology
RewriteCond %{HTTP_ACCEPT} (text/turtle|application/rdf\\+xml|application/ld\\+json|application/n-triples) [NC]
RewriteRule ^(.*)\$ ${PAGES_URL}/odrl-legal-profile.ttl [R=302,L]

# Everyone else gets the HTML documentation
RewriteRule ^(.*)\$ ${PAGES_URL}/ [R=302,L]
EOF
echo "   wrote w3id/odrl-legal/.htaccess"

# ---------------------------------------------------------------------------
# 4. Widoco: fetch latest jar and generate ReSpec docs
# ---------------------------------------------------------------------------
if [ ! -f widoco.jar ]; then
  echo ">> Downloading latest Widoco..."
  # (jq is more robust if you have it; this stays dependency-free)
  WIDOCO_URL=$(curl -sL https://api.github.com/repos/dgarijo/Widoco/releases/latest \
    | grep "browser_download_url.*jar-with-dependencies.jar" \
    | head -n1 | cut -d '"' -f 4 || true)
  [ -n "$WIDOCO_URL" ] || { echo "ERROR: could not resolve Widoco download URL."; exit 1; }
  curl -L -o widoco.jar "$WIDOCO_URL"
fi

echo ">> Generating documentation with Widoco..."
java -jar widoco.jar \
  -ontFile "$PROFILE_TTL" \
  -outFolder docs \
  -rewriteAll -uniteSections -includeAnnotationProperties -lang en

# ---------------------------------------------------------------------------
# 5. Make docs/ Pages-ready: serve the .ttl alongside the HTML
# ---------------------------------------------------------------------------
cp "$PROFILE_TTL" docs/odrl-legal-profile.ttl
[ -f docs/index-en.html ] && cp docs/index-en.html docs/index.html
echo "   copied ontology into docs/ and set docs/index.html"

# ---------------------------------------------------------------------------
# Done: manual steps remaining
# ---------------------------------------------------------------------------
cat <<EOF

==================================================================
Scaffold complete. Files created:
  LICENSE                         (code, $CODE_LICENSE)
  ODRL-Legal-Profile/LICENSE      (ontology, CC BY 4.0)
  w3id/odrl-legal/.htaccess       (for the perma-id PR)
  docs/                           (ReSpec docs + copy of the .ttl)

Manual steps remaining (cannot be scripted):
  1. Commit and push:
       git add -A
       git commit -m "Add profile docs, licenses, w3id redirect"
       git push
  2. Enable GitHub Pages: repo Settings > Pages > deploy from main, /docs
     Confirm it serves: ${PAGES_URL}/
  3. Register the w3id redirect:
       - fork github.com/perma-id/w3id.org
       - copy w3id/odrl-legal/ into the fork
       - open a pull request
  4. After the PR merges, verify resolution:
       curl -sH "Accept: text/turtle" https://w3id.org/odrl-legal/ | head
       (RDF client should get Turtle; a browser should show the HTML docs)
  5. Before the 1 July camera-ready: confirm https://w3id.org/odrl-legal/
     resolves, since the paper hard-codes that IRI.
==================================================================
EOF