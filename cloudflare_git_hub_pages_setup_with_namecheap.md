# Cloudflare + GitHub Pages  
## Setup and Reversal Guide (Minimal & Reversible)

This guide documents **exactly** how to place Cloudflare in front of a GitHub Pages site *and* how to undo it cleanly.

No advanced features. No lock-in.

---

## Assumptions
- You have a **custom domain**
- Your site is already working on **GitHub Pages**
- Your domain registrar is **Namecheap**
- You want **visibility (traffic stats)**, not heavy security or caching

---

## Part A — Setup (Minimal, Safe Configuration)

### 1. Add Site to Cloudflare
1. Create a Cloudflare account
2. Click **Add a Site**
3. Enter your domain (e.g. `korsbergcrafts.com`)
4. Select **Free Plan**

Cloudflare will scan existing DNS records.

---

### 2. Update Nameservers (Namecheap-specific)

1. Log in to **Namecheap**
2. Go to **Domain List** → click **Manage** next to your domain
3. Ensure the **Domain** tab is selected
4. Scroll to the **Nameservers** section
5. Select **Custom DNS**
6. Replace existing nameservers with the **two Cloudflare-provided nameservers**
7. Click the green **✔ Save** button

⚠ **Namecheap notes**:
- Changes usually propagate within **5–30 minutes**, but may take a few hours
- Namecheap may display a confirmation banner — this is normal
- Existing email (MX records) is unaffected as long as DNS records are preserved

---

### 3. DNS Records (Critical Step)

In **Cloudflare → DNS**:

```
Type: A
Name: @
Content: 185.199.108.153
Proxy: ON (orange cloud)

Type: A
Name: @
Content: 185.199.109.153
Proxy: ON

Type: A
Name: @
Content: 185.199.110.153
Proxy: ON

Type: A
Name: @
Content: 185.199.111.153
Proxy: ON

Type: CNAME
Name: www
Content: <username>.github.io
Proxy: ON
```

These are the official GitHub Pages IPs.

---

### 4. SSL Settings (Do Not Deviate)
Go to **SSL/TLS → Overview**

Set:
```
SSL Mode: Full
```

❌ Do NOT use **Flexible**

---

### 5. Leave Everything Else Alone

Do **NOT** enable:
- Cache Rules
- Page Rules
- Always Online
- Transform Rules
- Custom redirects

Minimalism prevents breakage.

---

## Part B — Where to See Traffic Stats

After traffic starts flowing:

**Analytics & Logs → Traffic**
- Requests over time
- Bandwidth
- Countries
- Bot vs non-bot (basic)

Interpretation:
- Requests ≠ visitors
- Watch **trends**, not exact counts

---

## Part C — Optional (Later)
- Enable **Web Analytics** (JS-based, optional)
- Add QR-specific URLs (`?src=qr`)
- Cloudflare Workers (only if curiosity grows)

None required.

---

## Part D — Reversal (Clean Exit)

### Option 1 — Temporary Disable (Fast)
In **Cloudflare → DNS**:
- Toggle records from **orange cloud → grey cloud**

Effect:
- Cloudflare is bypassed
- DNS still managed by Cloudflare

---

### Option 2 — Full Removal (Complete Undo)

1. Log in to **Namecheap**
2. Go to **Domain List → Manage → Domain**
3. Change **Nameservers** from **Custom DNS** back to your previous provider (or Namecheap BasicDNS)
4. Save changes
5. Wait for DNS propagation

Cloudflare is fully removed.

---

## Failure Recovery Checklist
If the site appears broken:
1. Grey-cloud all DNS records
2. Confirm GitHub Pages still loads directly
3. Fix settings or abandon Cloudflare

You can always recover.

---

## Final Notes
- Cloudflare Free is safe for static sites
- Edge request counts are more honest than JS analytics
- Reversible by design

This document exists so future-you doesn’t have to remember any of this.

