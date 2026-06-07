# Findings — what the Ames Housing data told us

*Written for anyone. No data background required.*

---

## The one-paragraph summary

House prices in Ames, Iowa are driven by a simple formula: quality first, size second, location third. The single biggest driver is how well the house was built and finished — not how big it is. A small, excellently built house routinely outsells a large, average one. And the neighbourhood adds a silent premium — or penalty — that no amount of renovation can fully overcome.

---

## Five things worth knowing

### 1. Quality is the #1 price driver — not size
Everyone assumes bigger = more expensive. The data disagrees. OverallQual (a 1–10 rating of construction quality) has a stronger correlation with SalePrice (r ≈ 0.79) than GrLivArea (living area in sq ft). At the same square footage, a quality-9 home can cost 50–80% more than a quality-5 home.

### 2. The neighbourhood premium is real and large
Two houses — identical size, identical quality — can differ by more than $150,000 based purely on which street they're on. The most expensive neighbourhoods in Ames aren't just slightly better. They represent an entirely different price tier.

### 3. Ames barely felt the 2008 financial crisis
The data runs from 2006–2010, right through the worst US housing crash in a generation. Sales volume in Ames dropped sharply — fewer people were buying — but median prices held steady. Iowa State University acts as an economic anchor: the university keeps demand stable even when the broader market collapses.

### 4. Newer homes earn a clear premium — but remodelling helps
Homes built after 2000 sell for significantly more than pre-1940 builds at the same quality level. However, a well-remodelled older home (check YearRemodAdd) can close most of that gap. Age is not destiny.

### 5. The thing that surprised me most
Two specific houses in the dataset have massive above-ground living areas (>4,000 sq ft) but sold at well below the median price. These appear to be data entry errors, not genuine sales — and including them would make any prediction model meaningfully worse. Catching data errors like this is exactly why EDA matters before modelling.

---

## What this does NOT tell us

- Why OverallQual ratings were assigned — we only know the scores, not the criteria
- Whether the neighbourhood gap is growing or shrinking over time (limited to 2006–2010)
- Causation — higher quality correlates with higher price, but we cannot say quality *causes* price
- How the market behaved after 2010 — the dataset ends there

---

## Questions this raises

- Would a quality-7 house in a top neighbourhood beat a quality-9 house in a bottom neighbourhood?
- Which specific features most explain OverallQual differences (roof type? Foundation? Exterior?)
- Could a regression model using just 5 features (OverallQual, GrLivArea, TotalBsmtSF, Neighborhood, YearBuilt) predict SalePrice within 15% accuracy?
