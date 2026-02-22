#!/usr/bin/env python3
# github_tool.py - Alat za rad sa GitHub repozitorijumom

import os
import subprocess
import sys
from datetime import datetime
import requests

# Konfiguracija
REPO_OWNER = "mpile"
REPO_NAME = "moj-astro-sajt"
GITHUB_API = "https://api.github.com"

def print_header(tekst):
    """Ispisuje lepo formatiran header"""
    print("\n" + "=" * 60)
    print(f" {tekst}")
    print("=" * 60)

def print_uspeh(tekst):
    print(f"✅ {tekst}")

def print_greska(tekst):
    print(f"❌ {tekst}")

def print_info(tekst):
    print(f"📌 {tekst}")

def izvrsi_komandu(komanda):
    """Izvršava komandu u terminalu i vraća rezultat"""
    try:
        result = subprocess.run(
            komanda,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return {
            "uspeh": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"uspeh": False, "error": str(e)}

def proveri_git_status():
    """Proverava status git repozitorijuma"""
    print_header("📊 GIT STATUS")
    
    # Provera da li smo u git repozitorijumu
    result = izvrsi_komandu("git rev-parse --git-dir")
    if not result["uspeh"]:
        print_greska("Niste u git repozitorijumu!")
        print_info("Pokrenite: git init")
        return False
    
    # Status
    result = izvrsi_komandu("git status")
    print(result["stdout"])
    
    # Remote
    result = izvrsi_komandu("git remote -v")
    if result["stdout"]:
        print("\n🔗 Remote adrese:")
        print(result["stdout"])
    else:
        print_greska("Nema remote adrese!")
        print_info("Pokrenite: git remote add origin https://github.com/mpile/moj-astro-sajt.git")
    
    return True

def dodaj_sve_i_commit(poruka):
    """Dodaje sve fajlove i pravi commit"""
    print_header("📝 DODAVANJE I COMMIT")
    
    # git add .
    result = izvrsi_komandu("git add .")
    if not result["uspeh"]:
        print_greska("Greška pri dodavanju fajlova")
        return False
    
    print_uspeh("Fajlovi dodani")
    
    # git commit
    result = izvrsi_komandu(f'git commit -m "{poruka}"')
    if result["uspeh"]:
        print_uspeh("Commit kreiran")
        return True
    else:
        if "nothing to commit" in result["stderr"]:
            print_info("Nema novih izmena za commit")
            return True
        else:
            print_greska(f"Greška pri commit-u: {result['stderr']}")
            return False

def push_na_github(token):
    """Pushuje kod na GitHub"""
    print_header("📤 PUSH NA GITHUB")
    
    # Prvo proveri remote
    result = izvrsi_komandu("git remote -v")
    if "moj-astro-sajt" not in result["stdout"]:
        print_greska("Nije postavljena remote adresa!")
        print_info("Pokrenite: git remote add origin https://github.com/mpile/moj-astro-sajt.git")
        return False
    
    # Push sa tokenom
    komanda = f'git push https://{REPO_OWNER}:{token}@github.com/{REPO_OWNER}/{REPO_NAME}.git main'
    result = izvrsi_komandu(komanda)
    
    if result["uspeh"]:
        print_uspeh("Kod uspešno poslat na GitHub!")
        print_info(f"https://github.com/{REPO_OWNER}/{REPO_NAME}")
        return True
    else:
        print_greska(f"Push nije uspeo: {result['stderr']}")
        return False

def pull_sa_github():
    """Povlači izmene sa GitHub-a"""
    print_header("📥 PULL SA GITHUB-A")
    
    result = izvrsi_komandu("git pull origin main")
    if result["uspeh"]:
        print_uspeh("Izmene uspešno povučene")
        return True
    else:
        print_greska(f"Pull nije uspeo: {result['stderr']}")
        return False

def proveri_github_api(token=None):
    """Proverava GitHub API"""
    print_header("🔍 PROVERA GITHUB API")
    
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = requests.get(
            f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print_uspeh("Repozitorijum je dostupan")
            print_info(f"URL: {data['html_url']}")
            print_info(f"Privatan: {'DA' if data['private'] else 'NE'}")
            print_info(f"Zvezdice: {data['stargazers_count']}")
            return True
        elif response.status_code == 404:
            print_greska("Repozitorijum ne postoji!")
            return False
        else:
            print_greska(f"Greška: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_greska(f"Greška pri povezivanju: {e}")
        return False

def main():
    print("\n🐍 GITHUB ALAT ZA ASTRO PROJEKAT")
    print(f"📁 Repo: {REPO_OWNER}/{REPO_NAME}")
    print(f"📅 Vreme: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    
    while True:
        print_header("📋 MENI")
        print("1. 📊 Proveri status git-a")
        print("2. 📝 Dodaj sve i commit")
        print("3. 📤 Push na GitHub")
        print("4. 📥 Pull sa GitHub-a")
        print("5. 🔍 Proveri GitHub API")
        print("6. 🚀 Kompletna akcija (add + commit + push)")
        print("7. ❌ Izlaz")
        
        izbor = input("\n🔹 Izaberite opciju (1-7): ").strip()
        
        if izbor == "1":
            proveri_git_status()
        
        elif izbor == "2":
            poruka = input("Unesite poruku za commit: ").strip()
            if poruka:
                dodaj_sve_i_commit(poruka)
            else:
                print_greska("Poruka ne može biti prazna!")
        
        elif izbor == "3":
            token = input("Unesite GitHub token: ").strip()
            if token:
                push_na_github(token)
            else:
                print_greska("Token je obavezan!")
        
        elif izbor == "4":
            pull_sa_github()
        
        elif izbor == "5":
            token = input("Unesite GitHub token (Enter za bez tokena): ").strip()
            proveri_github_api(token if token else None)
        
        elif izbor == "6":
            print_header("🚀 KOMPLETNA AKCIJA")
            poruka = input("Unesite poruku za commit: ").strip()
            token = input("Unesite GitHub token: ").strip()
            
            if poruka and token:
                if dodaj_sve_i_commit(poruka):
                    push_na_github(token)
            else:
                print_greska("Poruka i token su obavezni!")
        
        elif izbor == "7":
            print("\n👋 Doviđenja!")
            break
        
        else:
            print_greska("Nepostojeća opcija!")
        
        input("\nPritisnite Enter za nastavak...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Prekinuto od strane korisnika")
        sys.exit(0)