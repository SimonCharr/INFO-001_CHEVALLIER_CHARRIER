# TP1 - INFO001

**Binôme :** CHEVALLIER Jules, CHARRIER Simon

---

## Questions théoriques

### Question 1 : Chiffrement et déchiffrement RSA

**Formules :**
- Chiffrement : `C = M^e mod n` avec e = 65537
- Déchiffrement : `M = C^d mod n` avec `d × e ≡ 1 mod φ(n)`

---

### Question 2 : Rôle de Diffie-Hellman

Protocole d'échange de clés permettant d'établir un secret partagé sur un canal non sécurisé, basé sur le logarithme discret. Utilisé dans TLS pour négocier les clés de session.

---

### Question 3 : Informations importantes dans un certificat

1. **Identité du sujet (Subject)** : DN avec CN, O, C
2. **Clé publique** : Algorithme + modulus + exposant
3. **Identité de l'émetteur (Issuer)** : CA signataire
4. **Période de validité** : Not Before / Not After

---

### Question 4 : Authentification HTTPS

**Processus :** Bob → `https://www.alice.com`

1. ClientHello → ServerHello + chaîne de certificats
2. Vérification du certificat (CN/SAN, validité, révocation)
3. Vérification de la signature : `Hash_calculé = Hash_déchiffré`
4. Validation de la chaîne jusqu'au certificat racine (trust store)
5. Établissement de la session (Diffie-Hellman + clés symétriques)

---

## Pratique RSA

### Question 5 : Analyse de la clé RSA

- **Modulus :** 512 bits
- **publicExponent :** 65537 (valeur standard, sécurité basée sur factorisation de n)

### Question 6 : Chiffrement des clés

- Clé publique : aucun intérêt à chiffrer
- Clé privée : fortement recommandé
```bash
openssl rsa -in rsa_keys.pem -aes128 -out rsa_keys_cyphered.pem
```

### Question 7 : Encodage

Format PEM (Base64) - compatible texte, transmissible facilement

### Question 8 : Clé publique

Contient : Modulus (n) + Exposant public (e)

### Question 9 : Chiffrement d'un message

Utiliser la **clé publique du destinataire**

---

## Chiffrement asymétrique

### Question 10 : Chiffrer un message

```bash
openssl pkeyutl -encrypt -pubin -inkey pub_voisin.pem -in clair.txt -out cipher.bin
```

### Question 11 : Chiffrement multiple

**Résultat :** Contenus différents à chaque chiffrement

**Justification :** Padding aléatoire (PKCS#1/OAEP) pour éviter les attaques par analyse de fréquence

---

## Analyse de certificats

### Question 12 : Option -showcerts

Affiche la chaîne complète de certificats (3 certificats envoyés : serveur + CA intermédiaire + CA supérieure)

---

### Question 13 : Certificat cert0.pem

- **Standard x509 :** Format de certificats PKI
- **Sujet :** `C=FR, ST=Auvergne-Rhône-Alpes, O=Université Grenoble Alpes, CN=*.univ-grenoble-alpes.fr`
- **CN :** Common Name (nom de domaine, wildcard)
- **Émetteur :** GEANT OV RSA CA 4

---

### Question 14 : Subject et Issuer

- **s (subject) :** Propriétaire du certificat
- **i (issuer) :** CA qui a signé le certificat

---

### Question 15 : Contenu du certificat

- **Clé :** Publique RSA uniquement (2048 bits)
- **Signature :** SHA-384 + RSA
- **CN :** `*.univ-grenoble-alpes.fr`
- **SAN :** `*.univ-grenoble-alpes.fr`, `univ-grenoble-alpes.fr`
- **Validité :** 1 an (18/12/2024 → 18/12/2025)
- **.crl :** Certificate Revocation List

---

### Question 16 : Signature du certificat

Signé par GEANT OV RSA CA 4

**Formule :** `Signature = [Hash_SHA384(certificat)]^d mod n`

---

### Question 17 : CA intermédiaire

- **Sujet :** GEANT OV RSA CA 4
- **Clé :** RSA 4096 bits
- **Signé par :** USERTrust RSA CA

---

### Question 18 : Chaîne de certification

**Validation :** Issuer(cert n-1) = Subject(cert n)

**Certificat racine :** AAA Certificate Services (Comodo)

**Emplacement :** `/etc/pki/tls/certs/ca-bundle.crt`

---

### Question 19 : Certificat racine

USERTrust n'est pas auto-signé (Subject ≠ Issuer) → **certificat avec signature croisée** par AAA Certificate Services

**Formule :** `Signature = [Hash_SHA384(certificat)]^d mod n` (avec clé privée AAA)

---

## Question 20

Type de clé : **EC (Elliptic Curve)**
Taille : **256 bits**
Courbe : **prime256v1 (P-256 / secp256r1)**
Validité : **20 ans** (1er novembre 2025 au 27 octobre 2045)
Certificat racine auto-signé : Subject = Issuer = `C=FR, ST=Savoie, L=Chambéry, O=TP Sécurité, CN=Root Lorne`
X509v3 Key Usage : **Digital Signature, Certificate Sign, CRL Sign**

---

## Question 21

Paramètre `dir` : `/home/etudiant/ca`
Clé privée : `/home/etudiant/ca/private/intermediate.key.pem`
Certificat : `/home/etudiant/ca/certs/intermediate.cert.pem`

---

## Question 22

```bash
openssl ecparam -genkey -name prime256v1 | openssl ec -aes128 -out private/intermediate.key.pem
```
Clé EC prime256v1 (256 bits) pour cohérence avec la CA racine.

---

## Question 23

La signature dans le CSR prouve la possession de la clé privée correspondant à la clé publique présentée. Cela empêche qu'un attaquant fasse une demande avec la clé publique d'un tiers (Proof of Possession).

---

## Question 24

La clé doit être générée sur **tls-serv-charrisi** (la machine serveur). La clé privée ne doit jamais quitter la machine qui l'utilise pour des raisons de sécurité. Seul le CSR (contenant la clé publique) est envoyé à la CA.

---

## Question 25

La 3ème solution (faire confiance au certificat racine Root Lorne) est la plus pertinente car :
- Elle permet de valider automatiquement TOUS les certificats signés par la CA racine et ses CA intermédiaires
- C'est scalable : pas besoin d'ajouter chaque nouveau certificat serveur
- C'est la pratique standard des PKI : on fait confiance à la racine, pas aux feuilles

---

## Question 26

Ligne ajoutée dans `/etc/hosts` :
```
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4 www.charrisi.fr
```

Cette modification permet de résoudre `www.charrisi.fr` vers 127.0.0.1, permettant de tester le serveur HTTPS avec le nom de domaine correct (celui du CN du certificat).

**Note :** Les tests avec curl nécessitent l'option `-k` car le certificat racine a été régénéré après la signature de notre CA intermédiaire. L'infrastructure HTTPS fonctionne correctement (chiffrement TLS, chaîne de certificats envoyée), seule la validation automatique échoue.

Tests fonctionnels :
```bash
curl -k https://www.charrisi.fr              # → web1
curl -k https://www.charrisi.fr/admin/       # → web2
curl -k https://www.charrisi.fr/picture/     # → web1
curl -k https://www.charrisi.fr/admin/styles/ # → web2
```

---

## Question 27

### Scénario de tests

#### Test 1 : Connexion sans validation (verify=False)
**Objectif :** Connexion en désactivant la vérification SSL
**Résultat :** OK Connexion réussie (Status 200)

#### Test 2 : Connexion avec validation stricte
**Objectif :** Vérifier le rejet d'un certificat non reconnu
**Résultat :** OK Certificat rejeté avec erreur SSL

#### Test 3 : Validation du hostname
**Objectif :** Contrôler la correspondance certificat/domaine
**Résultat :** OK Connexion rejetée avec 127.0.0.1 (hostname mismatch)

#### Test 4 : Routes du reverse proxy
**Objectif :** Vérifier le fonctionnement HTTPS
**Résultat :** OK Toutes les routes fonctionnent (/, /admin/, /picture/, /admin/styles/)

### Vérification du chiffrement

**Méthode :** Capture tcpdump pendant les requêtes HTTPS

**Commandes :**
```bash
sudo tcpdump -i lo -w capture_https.pcap port 443
python3 client_https.py
sudo tcpdump -r capture_https.pcap -A | grep -i "web1"
```

**Résultats :**
- Handshake TLS visible (pattern `0x1603` dans les trames)
- Aucune donnée HTTP en clair détectée
- Grep sur "web1" et "GET /" : aucun résultat
- Données totalement chiffrées en hexadécimal

### Conclusion

OK - Le client valide correctement les certificats
OK - La vérification du hostname fonctionne
OK - Les communications sont entièrement chiffrées via TLS
OK - Aucune donnée n'est visible en clair sur le réseau