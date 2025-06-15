# 🔍 Web Vulnerability Scanner

A lightweight yet powerful web vulnerability scanner built with Python and Streamlit. It detects common web vulnerabilities such as XSS (Cross-Site Scripting) and SQLi (SQL Injection), fetches historical Wayback Machine URLs, discovers subdomains, and scans them for potential weaknesses.

> 🚀 Live Demo (Deploy it on Streamlit Cloud):  
> [https://helloitsrithvik-web-vuln-scanner.streamlit.app](#)

---

## 📸 Screenshot

![Screenshot](https://raw.githubusercontent.com/helloitsrithvik/web-vuln-scanner/main/screenshot.png)

---

## ✨ Features

- ✅ Detects **XSS** and **SQL Injection** vulnerabilities using custom and default payloads
- 🌐 **Subdomain Discovery** using DNS brute-forcing
- 🕵️‍♂️ Extracts **historical URLs** from the Wayback Machine
- 📂 Accepts multiple input formats: single URL or a file of URLs
- ⚡ Fast concurrent scanning using multithreading
- 📊 Real-time progress via Streamlit interface
- 📎 Clean UI, exportable results, and error handling

---

## 🛠️ Modules Used

| Module         | Purpose                                                  |
|----------------|----------------------------------------------------------|
| `requests`     | HTTP requests & payload injection                        |
| `concurrent.futures` | Parallel execution for fast scanning              |
| `streamlit`    | Web-based UI for the scanner                            |
| `subprocess`   | DNS lookups for subdomain detection                     |
| `re`, `json`, `os`, `urllib` | Various data processing and parsing tasks |

---

## 📁 Project Structure

```
web-vuln-scanner/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Dependencies list
├── README.md                   # You are here!
│
├── scanner/
│   ├── __init__.py
│   ├── scanner.py              # Core vulnerability scanning logic
│   ├── subdomain_finder.py     # Subdomain enumeration
│   ├── wayback.py              # Historical URL fetching
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+
- Git

### 📦 Installation

```bash
git clone https://github.com/helloitsrithvik/web-vuln-scanner.git
cd web-vuln-scanner
pip install -r requirements.txt
```

### ▶️ Run the Scanner

```bash
streamlit run app.py
```

Open your browser and go to `http://localhost:8501`

---

## 🧪 How It Works

1. Enter a domain or upload a file with URLs
2. The app will:
   - Extract Wayback URLs
   - Find subdomains (if enabled)
   - Send requests with XSS/SQLi payloads
   - Analyze the responses for vulnerability patterns
3. Results are displayed in real time

---

## 📌 Future Enhancements

- 📡 Add SSRF, LFI, and CSRF vulnerability checks
- 📁 Export scan reports to PDF/CSV
- 🔐 Add authentication-based testing
- 💬 Integrate Slack or email alerting for found issues

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Wayback Machine API](https://archive.org)
- Inspired by OWASP ZAP and Burp Suite concepts

---

## 🔗 Author

Developed with ❤️ by [helloitsrithvik](https://github.com/helloitsrithvik)
