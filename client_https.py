#!/usr/bin/env python3

import requests
import sys
import urllib3

def test_connexion_sans_ca():
    print("\n=== TEST 1: Connexion HTTPS sans CA racine ===")
    print("Objectif: Le client doit rejeter le certificat")
    
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.get('https://www.charrisi.fr', verify=False, timeout=5)
        print(f"✗ ÉCHEC: Connexion acceptée sans vérification (Status: {response.status_code})")
        print(f"  Contenu reçu: {response.text[:50]}...")
        
        try:
            response = requests.get('https://www.charrisi.fr', verify=True, timeout=5)
            print("✗ ÉCHEC: Certificat accepté sans CA")
        except requests.exceptions.SSLError as e:
            print(f"✓ SUCCÈS: Certificat rejeté comme attendu")
            print(f"  Erreur: {str(e)[:100]}...")
            
    except Exception as e:
        print(f"Erreur inattendue: {e}")

def test_connexion_avec_ca():
    print("\n=== TEST 2: Connexion HTTPS avec CA racine ===")
    print("Objectif: Le client doit accepter le certificat")
    
    ca_bundle = '/etc/pki/ca-trust/source/anchors/root-ca-lorne.pem'
    
    try:
        response = requests.get('https://www.charrisi.fr', verify=ca_bundle, timeout=5)
        print(f"✓ SUCCÈS: Connexion établie (Status: {response.status_code})")
        print(f"  Contenu reçu: {response.text[:80]}...")
        return True
    except requests.exceptions.SSLError as e:
        print(f"✗ ÉCHEC: Certificat rejeté")
        print(f"  Erreur: {str(e)[:100]}...")
        return False
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False

def test_hostname_mismatch():
    print("\n=== TEST 3: Validation du nom de domaine ===")
    print("Objectif: Rejeter si le hostname ne correspond pas")
    
    try:
        response = requests.get('https://127.0.0.1', verify=True, timeout=5)
        print("✗ ÉCHEC: Connexion acceptée malgré hostname incorrect")
    except requests.exceptions.SSLError as e:
        print("✓ SUCCÈS: Connexion rejetée (hostname mismatch)")
        print(f"  Erreur: {str(e)[:100]}...")
    except Exception as e:
        print(f"Erreur: {e}")

def test_routes():
    print("\n=== TEST 4: Test des différentes routes ===")
    
    routes = ['/', '/admin/', '/picture/', '/admin/styles/']
    
    for route in routes:
        try:
            response = requests.get(f'https://www.charrisi.fr{route}', 
                                   verify=False, timeout=5)
            print(f"✓ {route:<20} → Status {response.status_code}")
            print(f"  Contenu: {response.text[:50]}...")
        except Exception as e:
            print(f"✗ {route:<20} → Erreur: {e}")

def afficher_info_certificat():
    print("\n=== Informations sur le certificat ===")
    import ssl
    import socket
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    with socket.create_connection(("www.charrisi.fr", 443)) as sock:
        with context.wrap_socket(sock, server_hostname="www.charrisi.fr") as ssock:
            cert = ssock.getpeercert()
            print(f"Subject: {dict(x[0] for x in cert['subject'])}")
            print(f"Issuer: {dict(x[0] for x in cert['issuer'])}")
            print(f"Version: {cert['version']}")
            print(f"Not Before: {cert['notBefore']}")
            print(f"Not After: {cert['notAfter']}")

if __name__ == "__main__":
    print("="*60)
    print("CLIENT HTTPS - TESTS DE VALIDATION CERTIFICAT")
    print("="*60)
    
    test_connexion_sans_ca()
    test_connexion_avec_ca()
    test_hostname_mismatch()
    test_routes()
    
    try:
        afficher_info_certificat()
    except Exception as e:
        print(f"\nImpossible d'afficher les infos du certificat: {e}")
    
    print("\n" + "="*60)
    print("TESTS TERMINÉS")
    print("="*60)