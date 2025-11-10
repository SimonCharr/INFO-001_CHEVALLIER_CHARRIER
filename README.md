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

### Question 13 : Certificat cert0.pem

- **Standard x509 :** Format de certificats PKI
- **Sujet :** `C=FR, ST=Auvergne-Rhône-Alpes, O=Université Grenoble Alpes, CN=*.univ-grenoble-alpes.fr`
- **CN :** Common Name (nom de domaine, wildcard)
- **Émetteur :** GEANT OV RSA CA 4

### Question 14 : Subject et Issuer

- **s (subject) :** Propriétaire du certificat
- **i (issuer) :** CA qui a signé le certificat

### Question 15 : Contenu du certificat

- **Clé :** Publique RSA uniquement (2048 bits)
- **Signature :** SHA-384 + RSA
- **CN :** `*.univ-grenoble-alpes.fr`
- **SAN :** `*.univ-grenoble-alpes.fr`, `univ-grenoble-alpes.fr`
- **Validité :** 1 an (18/12/2024 → 18/12/2025)
- **.crl :** Certificate Revocation List

### Question 16 : Signature du certificat

Signé par GEANT OV RSA CA 4

**Formule :** `Signature = [Hash_SHA384(certificat)]^d mod n`

### Question 17 : CA intermédiaire

- **Sujet :** GEANT OV RSA CA 4
- **Clé :** RSA 4096 bits
- **Signé par :** USERTrust RSA CA

### Question 18 : Chaîne de certification

**Validation :** Issuer(cert n-1) = Subject(cert n)

**Certificat racine :** AAA Certificate Services (Comodo)

**Emplacement :** `/etc/pki/tls/certs/ca-bundle.crt`

### Question 19 : Certificat racine

USERTrust n'est pas auto-signé (Subject ≠ Issuer) → **certificat avec signature croisée** par AAA Certificate Services

**Formule :** `Signature = [Hash_SHA384(certificat)]^d mod n` (avec clé privée AAA)

---
