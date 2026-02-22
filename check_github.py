#!/usr/bin/env python3
# check_github.py - Provera konekcije ka GitHub-u

import requests
import sys
import os
from datetime import datetime

# Konfiguracija
GITHUB_API = "https://api.github.com"
GITHUB_RAW = "https://raw.githubusercontent.com"
REPO_OWNER = "mpile"
REPO_NAME = "moj-astro-sajt"  # Promeni ako je drugačije ime repoa
TEST_FILE = "README.md"  # Fajl koji proveravamo (ako postoji)

def proveri_internet():
    """Provera osnovne internet konekcije"""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.RequestException:
        return False

def proveri_github_api():
    """Provera da li je GitHub API dostupan"""
    try:
        response = requests.get(f"{GITHUB_API}/zen", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def proveri_repo_postoji():
    """Provera da li repozitorijum postoji"""
    try:
        response = requests.get(
            f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}",
            timeout=5,
            headers={"Accept": "application/vnd.github.v3+json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "postoji",
                "privatno": data.get("private", False),
                "url": data.get("html_url", ""),
                "opis": data.get("description", "Nema opisa")
            }
        elif response.status_code == 404:
            return {"status": "ne_postoji"}
        else:
            return {"status": "greska", "kod": response.status_code}
    except requests.RequestException as e:
        return {"status": "greska", "error": str(e)}

def proveri_pristup_fajlu():
    """Provera da li može da pristupi fajlu u repozitorijumu"""
    try:
        url = f"{GITHUB_RAW}/{REPO_OWNER}/{REPO_NAME}/main/{TEST_FILE}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return {"status": "dostupan", "velicina": len(response.text)}
        elif response.status_code == 404:
            return {"status": "ne_postoji"}
        else:
            return {"status": "greska", "kod": response.status_code}
    except requests.RequestException as e:
        return {"status": "greska", "error": str(e)}

def main():
    print("=" * 60)
    print(f"🔍 PROVERA KONEKCIJE KA GITHUB-U")
    print(f"📅 Vreme: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"📁 Repo: {REPO_OWNER}/{REPO_NAME}")
    print("=" * 60)
    
    # Korak 1: Provera interneta
    print("\n1️⃣ Provera internet konekcije...")
    if proveri_internet():
        print("   ✅ Internet konekcija je aktivna")
    else:
        print("   ❌ Nema internet konekcije!")
        print("\n🏁 ZAKLJUČAK: Provera nije uspela - proveri internet.")
        sys.exit(1)
    
    # Korak 2: Provera GitHub API-ja
    print("\n2️⃣ Provera GitHub API-ja...")
    if proveri_github_api():
        print("   ✅ GitHub API je dostupan")
    else:
        print("   ❌ GitHub API nije dostupan (možda je blokiran)")
        print("\n🏁 ZAKLJUČAK: Provera nije uspela - GitHub možda nije dostupan.")
        sys.exit(1)
    
    # Korak 3: Provera repozitorijuma
    print(f"\n3️⃣ Provera repozitorijuma {REPO_OWNER}/{REPO_NAME}...")
    repo_status = proveri_repo_postoji()
    
    if repo_status["status"] == "postoji":
        print(f"   ✅ Repozitorijum postoji")
        print(f"   📌 URL: {repo_status['url']}")
        print(f"   🔒 Privatan: {'DA' if repo_status['privatno'] else 'NE'}")
        print(f"   📝 Opis: {repo_status['opis']}")
    elif repo_status["status"] == "ne_postoji":
        print(f"   ❌ Repozitorijum {REPO_OWNER}/{REPO_NAME} NE POSTOJI!")
        print(f"   💡 Predlog: Prvo ga kreiraj na https://github.com/new")
        print("\n🏁 ZAKLJUČAK: Repozitorijum ne postoji - kreiraj ga pa probaj ponovo.")
        sys.exit(1)
    else:
        print(f"   ❌ Greška pri proveri repozitorijuma: {repo_status}")
        print("\n🏁 ZAKLJUČAK: Provera nije uspela.")
        sys.exit(1)
    
    # Korak 4: Provera pristupa fajlu (opciono)
    print(f"\n4️⃣ Provera pristupa fajlu ({TEST_FILE})...")
    fajl_status = proveri_pristup_fajlu()
    
    if fajl_status["status"] == "dostupan":
        print(f"   ✅ Fajl {TEST_FILE} je dostupan (veličina: {fajl_status['velicina']} karaktera)")
    elif fajl_status["status"] == "ne_postoji":
        print(f"   ⚠️ Fajl {TEST_FILE} ne postoji u repozitorijumu (to nije problem)")
    else:
        print(f"   ⚠️ Ne mogu da proverim fajl: {fajl_status}")
    
    # Kraj
    print("\n" + "=" * 60)
    print("🎉 ZAKLJUČAK: SVE JE U REDU!")
    print("✅ GitHub konekcija funkcioniše")
    print("✅ Repozitorijum postoji i dostupan je")
    print("=" * 60)
    
    # Dodatne informacije za git
    print("\n📋 Za push na GitHub koristi:")
    print("   git push -u origin main")
    print("\n   (ako te pita za password, koristi TOKEN, ne lozinku!)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Provera prekinuta od strane korisnika.")
        sys.exit(1)
    except Exception as e:
        print(f"\n🔥 Neočekivana greška: {e}")
        sys.exit(1)