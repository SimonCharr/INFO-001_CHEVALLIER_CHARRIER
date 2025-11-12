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

**Réponse :**

La clé doit être générée sur **tls-serv-charrisi** (la machine serveur). La clé privée ne doit jamais quitter la machine qui l'utilise pour des raisons de sécurité. Seul le CSR (contenant la clé publique) est envoyé à la CA.

---