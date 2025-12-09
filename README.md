# Profitable App Profiles for the App Store and Google Play

This project analyzes real App Store and Google Play datasets to understand which **app profiles (genres / categories)** are most promising for a company that builds **free, ad-supported mobile apps**.

The goal is to find **genres that work well on both markets**, balancing:
- User demand (installs / ratings)
- Competition (number of apps)
- Realistic chances for a small team

---

## 📂 Project Structure

- `clean_and_analyze.py` – main Python script that:
  - Loads and cleans the datasets
  - Removes wrong rows and duplicates
  - Filters to English and free apps
  - Computes frequency tables and popularity metrics

- `AppleStore.csv` – App Store dataset (not included here if restricted)
- `googleplaystore.csv` – Google Play dataset (not included here if restricted)

---

## 🧹 Data Cleaning Steps

**Google Play:**

1. Remove rows with inconsistent column lengths (corrupted row).
2. Detect duplicate apps by name.
3. For each duplicated app, keep only the row with the **maximum number of reviews** (assumed to be the most recent / reliable).
4. Filter to:
   - English app names (allowing a few non-ASCII characters)
   - Free apps (price == 0)

**App Store:**

1. Filter to:
   - English app names
   - Free apps (price 0.0 or 0)

---

## 📊 Analysis – What’s Common vs. What’s Popular

### App Store – `prime_genre` (Free, English apps)

From the genre frequency:

- **Games** ≈ 58% of apps  
- **Entertainment** ≈ 7.9%  
- **Photo & Video** ≈ 5.0%  
- **Education** ≈ 3.7%  
- **Social Networking** ≈ 3.3%  
- Practical genres (Productivity, Finance, Health & Fitness, Utilities, etc.) are much smaller.

**Impression:**  
The free English App Store segment is **heavily entertainment-oriented**. However, a high number of apps in a genre only tells us about **supply**, not whether each app gets many users.

To go beyond that, I use `rating_count_tot` as a **proxy for popularity** and compute the **average number of ratings per genre**.

Some of the top genres by **average ratings per app**:

- **Navigation** → ~86,090 ratings per app  
- **Reference** → ~74,942  
- **Social Networking** → ~71,548  
- **Music** → ~57,327  
- **Weather** → ~52,280  
- **Book** → ~39,759  
- **Food & Drink** → ~33,334  
- **Finance** → ~31,468  
- **Photo & Video** → ~28,442  
- **Travel** → ~28,244  

**Key insight:**

- **Games** are the most common genre, but their average ratings per app (~22,789) are **lower** than several practical genres.
- Practical / utility genres like **Navigation, Reference, Weather, Finance** tend to have **fewer apps but more engagement per app**.

➡️ On the App Store, **niche utility apps** can be very attractive even if they’re not the most common.

---

### Google Play – Categories and Genres (Free, English apps)

For Google Play, I look at:

- `Category` (index 1) – broader groups
- `Genres` (index 9) – more granular labels

I use **Installs** as a proxy for popularity:
- Cleaned by removing `+` and `,`, then converting to numeric.
- Compute **average installs per app** for each category.

Some of the top categories by **average installs**:

- **COMMUNICATION** → ~38,456,119 installs/app  
- **VIDEO_PLAYERS** → ~24,727,872  
- **SOCIAL** → ~23,253,652  
- **PHOTOGRAPHY** → ~17,840,110  
- **PRODUCTIVITY** → ~16,787,331  
- **GAME** → ~15,588,016  
- **TRAVEL_AND_LOCAL** → ~13,984,078  
- **TOOLS** → ~10,801,391  
- **NEWS_AND_MAGAZINES** → ~9,549,178  
- **BOOKS_AND_REFERENCE** → ~8,767,812  

**Observations:**

- Categories like **COMMUNICATION, SOCIAL, VIDEO_PLAYERS** are dominated by huge players (WhatsApp, Facebook, YouTube, etc.).
- These are extremely competitive and hard to enter as a small team.
- Practical categories such as **PRODUCTIVITY, TRAVEL_AND_LOCAL, TOOLS, BOOKS_AND_REFERENCE** also have **strong average installs**, but competition is more realistic.

Overall, Google Play looks more **balanced** than the App Store:
- Strong presence of **family/entertainment**, but also
- Many **tools, business, productivity, finance, education** apps.

---

## 🔗 Cross-Market Insights (Apple + Google Play)

Looking at both stores:

**App Store:**

- High engagement in:
  - Navigation  
  - Reference  
  - Weather  
  - Finance  
  - Travel  
  - Music  

**Google Play:**

- High installs in:
  - TRAVEL_AND_LOCAL  
  - BOOKS_AND_REFERENCE  
  - PRODUCTIVITY  
  - TOOLS  
  - (plus big categories like COMMUNICATION and SOCIAL, which are dominated by giants)

There is a **clear overlap** in promising areas:

- Travel & local information  
- Reference / educational content  
- Productivity / tools  
- Weather and other practical utilities  

These profiles tend to:

- Solve real problems
- Have strong user demand
- Be less dominated by a few huge brands (compared to social/communication)

---

## 🎯 Recommended App Profile

Given:

- We build **free, ad-supported apps**
- We want apps that can work on **both iOS and Android**
- We want to avoid categories totally dominated by huge companies

A promising direction is:

> A **content-rich, utility-style app** in the  
> **“Reference / Travel / Productivity” space**

Examples:

- A **Travel & Local guide** app (city guide, public transport helper, offline tips for tourists).
- A **Reference / Education** app (language phrases for travelers, quick lookup for a niche topic, exam helper).
- A **simple Productivity tool** (habit tracker, planner, focus timer) with a specific niche.

These:

- Match high engagement and installs on **both** platforms
- Fit well with **free + ads** monetization
- Are realistic for a small dev team

---

## 🛠️ How to Run the Script

```bash
# 1. Clone the repo
git clone https://github.com/your-username/app-market-analysis.git
cd app-market-analysis

# 2. Make sure the CSV files are in the project folder or in ./data

# 3. Run the analysis
python src/clean_and_analyze.py
