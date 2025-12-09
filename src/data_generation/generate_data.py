
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

def generate_marketing_data(n_samples=5000, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    fake = Faker('fr_FR')

    # Constants and Configurations
    CITIES = [fake.city() for _ in range(20)]
    CHANNELS = ['Social', 'Email', 'SEA', 'Direct', 'Reference']
    CHANNEL_PROBS = [0.30, 0.25, 0.20, 0.15, 0.10]
    CAC_MAPPING = {'Social': 15, 'Email': 8, 'SEA': 25, 'Direct': 0, 'Reference': 5}
    CATEGORIES = ['Électronique', 'Mode', 'Alimentation', 'Loisirs', 'Maison']
    
    data = []
    
    today = datetime.now()
    three_years_ago = today - timedelta(days=3*365)

    for i in range(1, n_samples + 1):
        # 1. ID
        client_id = f"CLIENT_{i:04d}"
        
        # 2. Demographics
        # Age: Normal distribution 18-75. Mean approx 40, std dev 12? 
        # Range 18-75 is huge. Let's try mean=40, std=15 and clip.
        age = int(np.clip(np.random.normal(40, 15), 18, 75))
        
        location = np.random.choice(CITIES)
        gender = np.random.choice(['M', 'F'])
        
        # 3. Acquisition
        channel = np.random.choice(CHANNELS, p=CHANNEL_PROBS)
        cac = CAC_MAPPING[channel]
        
        # 4. Behavior - Dates
        # First purchase uniform in last 3 years
        days_since_start = np.random.uniform(0, 3*365)
        first_purchase_date = today - timedelta(days=days_since_start)
        
        # Last purchase: Exponential since first purchase?
        # Let's interpret "Exponential since first" as the active duration.
        # But we must ensure Last >= First and Last <= Today.
        # Let's model "Days between First and Last" as Exponential.
        # Scale? Maybe mean 200 days?
        duration_days = np.random.exponential(scale=300)
        last_purchase_date = first_purchase_date + timedelta(days=duration_days)
        
        # Clamp LastPurchase to Today. If First was yesterday, Last can't be in 200 days.
        if last_purchase_date > today:
            last_purchase_date = today
            
        # 5. Behavior - Financials
        # Total Spent: Pareto. 80% < 500, 20% > 500.
        # Adjusted for realism: Cap at 50,000€ to avoid billions.
        # Target: P(X < 500) = 0.8.
        # Using a=1.16 (classic 80/20) and tuning m.
        # (m/500)^1.16 = 0.2 => m/500 = 0.2^(1/1.16) = 0.25 => m = 125.
        # Let's try m=100 and a=1.3?
        # (100/500)^a = 0.2 => 0.2^a = 0.2 => a = 1.
        # Let's use m=80 (min spent) and a=1.
        # Or stick to previous logic but cap it.
        # If we use a=0.5, m=20, we satisfied the condition but got huge outliers.
        # Let's increase a to > 1 for finite mean, say a=2.
        # (m/500)^2 = 0.2 => m/500 = sqrt(0.2) = 0.447 => m = 223.
        # Too high min.
        # Let's use a split approach or rejection sampling.
        # We will use Pareto with a=1.5 and m=50.
        # P(X<500) = 1 - (50/500)^1.5 = 1 - 0.1^1.5 = 1 - 0.03 = 0.97. Too high % < 500.
        # We need heavier tail. a=0.6.
        # P(X<500) = 1 - (20/500)^0.6 = 1 - 0.04^0.6 = 1 - 0.14 = 0.86. roughly ok.
        
        while True:
             a_pareto = 0.6
             m_pareto = 30
             total_spent = m_pareto * (np.random.pareto(a_pareto) + 1)
             if total_spent < 50000: 
                 break
        
        total_spent = round(total_spent, 2)
        
        # Frequency: Poisson lambda=3.
        freq = np.random.poisson(lam=3)
        if freq < 1: freq = 1
        
        avg_basket = total_spent / freq
        
        # 6. Engagement
        # Newsletter: 60% Yes.
        newsletter = np.random.choice([True, False], p=[0.6, 0.4])
        
        # Score Satisfaction: 1-5, correlated with TotalSpent.
        # Higher spent -> likely higher satisfaction (or vice versa).
        # Let's normalize spent and use it as a probability bias or mean shifter.
        # Log of spent is better behaved.
        log_spent = np.log(total_spent)
        # Map log_spent roughly to 1-5 range with noise.
        # minimal spent ~20 -> ln(20) ~ 3. Max spent can be huge.
        # Let's use a base correlation:
        base_score = 3
        spent_factor = (log_spent - 3) * 0.5 # shift
        noise = np.random.normal(0, 1)
        score = int(round(base_score + spent_factor + noise))
        score = np.clip(score, 1, 5)
        
        last_visit_days = (today - last_purchase_date).days 
        # Add some noise to last visit, it could be AFTER last purchase
        last_visit_days = max(0, last_visit_days - np.random.randint(0, 30))
        
        # 7. Product
        category = np.random.choice(CATEGORIES)
        products_count = np.random.randint(1, 11) # 1 to 10
        
        data.append({
            'ClientID': client_id,
            'Age': age,
            'Location': location,
            'Gender': gender,
            'DatePremierAchat': first_purchase_date.strftime('%Y-%m-%d'),
            'DateDernierAchat': last_purchase_date.strftime('%Y-%m-%d'),
            'MontantTotalDepense': total_spent,
            'FrequenceAchats': freq,
            'PanierMoyen': round(avg_basket, 2),
            'Canal': channel,
            'CAC_Estime': cac,
            'Newsletter': newsletter,
            'ScoreSatisfaction': score,
            'DerniereVisiteSite': last_visit_days,
            'CategoriePreferee': category,
            'ProduitsDifferentsAchetes': products_count
        })

    df = pd.DataFrame(data)
    
    # Validation
    print(f"Generated {len(df)} records.")
    print(f"Total Spent stats:\n{df['MontantTotalDepense'].describe()}")
    percent_under_500 = (df['MontantTotalDepense'] < 500).mean() * 100
    print(f"Percentage of users spending < 500€: {percent_under_500:.2f}%")
    
    # Save
    output_path = 'data/raw/marketing_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    generate_marketing_data()
