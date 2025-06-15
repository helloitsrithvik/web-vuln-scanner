import streamlit as st
import os
from scanner.wayback import get_wayback_urls
from scanner.subdomain_finder import find_subdomains
from scanner.crawler import Crawler
from scanner.xss_scanner import check_xss
from scanner.sql_scanner import check_sqli

st.set_page_config(page_title="Web Vulnerability Scanner", layout="wide")
st.title("🔥 Web Vulnerability Toolkit")

tabs = st.tabs(["🛡️ Scanner", "📜 Wayback URLs", "🌐 Subdomain Finder"])

# Shared session memory
wayback_storage = {}
subdomain_storage = {}

# ---------------------- Scanner Tab ----------------------
with tabs[0]:
    st.header("🛡️ Vulnerability Scanner")

    mode = st.radio("Scan Mode:", ["Single URL", "Bulk URLs (.txt)"])
    use_advanced = st.checkbox("Use Advanced Payloads (from uploaded files)")
    include_wayback = st.checkbox("Include Wayback URLs (if available)")

    # Upload advanced payloads
    xss_payloads_file = st.file_uploader("Upload XSS Payloads (.txt)", type="txt") if use_advanced else None
    sqli_payloads_file = st.file_uploader("Upload SQLi Payloads (.txt)", type="txt") if use_advanced else None

    # Collect target URLs
    target_urls = []
    if mode == "Single URL":
        single_url = st.text_input("Enter Target URL:", "")
        if single_url:
            target_urls.append(single_url.strip())
    else:
        uploaded_file = st.file_uploader("Upload a file with subdomains (one per line)", type=["txt"])
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            urls = [line.strip() for line in content.splitlines() if line.strip()]
            target_urls.extend(urls)
            st.success(f"{len(target_urls)} target(s) loaded.")

    # Read payloads
    xss_payloads = xss_payloads_file.read().decode("utf-8").splitlines() if xss_payloads_file else []
    sqli_payloads = sqli_payloads_file.read().decode("utf-8").splitlines() if sqli_payloads_file else []

    if st.button("Start Scan"):
        for url in target_urls:
            st.markdown(f"### 🔍 Scanning: {url}")
            urls_to_scan = set(Crawler(url).crawl())
            if include_wayback and url in wayback_storage:
                urls_to_scan.update(wayback_storage[url])

            total = len(urls_to_scan)
            found_any = False
            progress = st.empty()

            for i, page_url in enumerate(urls_to_scan):
                if "?" in page_url:
                    progress.markdown(f"**Scanning {i+1}/{total}:** `{page_url}`")
                    xss_vuls = check_xss(page_url, xss_payloads if xss_payloads else None)
                    sqli_vuls = check_sqli(page_url, sqli_payloads if sqli_payloads else None)
                    for vuln in xss_vuls + sqli_vuls:
                        found_any = True
                        st.code(f"🔴 {vuln}")
            if not found_any:
                st.success("✅ No vulnerabilities found.")

# ---------------------- Wayback Tab ----------------------
with tabs[1]:
    st.header("📜 Wayback URL Extractor")
    domain = st.text_input("Enter domain for Wayback scraping:")
    if st.button("Fetch Wayback URLs"):
        with st.spinner("Fetching..."):
            urls = get_wayback_urls(domain)
            wayback_storage[domain] = urls
            st.success(f"Found {len(urls)} URLs from Wayback Machine.")
            st.code("\n".join(urls[:100]), language="text")

# ---------------------- Subdomain Finder Tab ----------------------
with tabs[2]:
    st.header("🌐 Subdomain Finder")
    domain = st.text_input("Enter main domain:")
    if st.button("Find Subdomains"):
        with st.spinner("Enumerating..."):
            subs = find_subdomains(domain)
            subdomain_storage[domain] = subs
            st.success(f"Found {len(subs)} subdomains.")
            st.code("\n".join(subs[:100]), language="text")
