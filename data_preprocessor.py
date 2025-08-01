import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

def preprocess_stock_data():
    stock_data = []
    
    for filename in os.listdir('data/financial_reports'):
        if filename.endswith('.csv') and 'data' in filename.lower():
            filepath = os.path.join('data/financial_reports', filename)
            try:
                df = pd.read_csv(filepath)
                if not df.empty:
                    for _, row in df.iterrows():
                        content = f"Stock data: {filename} - Date: {row.get('Date', 'Unknown')} - Price: {row.get('Close', 'N/A')} - Volume: {row.get('Volume', 'N/A')}"
                        stock_data.append({
                            'title': f"Stock Data: {filename}",
                            'content': content,
                            'source': filepath,
                            'document_type': 'stock_data'
                        })
            except Exception:
                continue
    
    return stock_data

def preprocess_transactions_data():
    transactions_data = []
    
    for filename in os.listdir('data/financial_reports'):
        if 'transaction' in filename.lower():
            filepath = os.path.join('data/financial_reports', filename)
            try:
                df = pd.read_csv(filepath)
                if not df.empty:
                    for _, row in df.iterrows():
                        content = f"Transaction: {row.get('Transaction_ID', 'Unknown')} - Amount: {row.get('Amount', 'N/A')} - Date: {row.get('Date', 'Unknown')}"
                        transactions_data.append({
                            'title': f"Transaction Record: {row.get('Transaction_ID', 'Unknown')}",
                            'content': content,
                            'source': filepath,
                            'document_type': 'transaction_record'
                        })
            except Exception:
                continue
    
    return transactions_data

def preprocess_sales_data():
    sales_data = []
    
    for filename in os.listdir('data/financial_reports'):
        if 'cosmetic' in filename.lower() or 'sales' in filename.lower():
            filepath = os.path.join('data/financial_reports', filename)
            try:
                df = pd.read_csv(filepath)
                if not df.empty:
                    for _, row in df.iterrows():
                        content = f"Sales Record: {row.get('Product', 'Unknown')} - Salesperson: {row.get('Salesperson', 'Unknown')} - Amount: {row.get('Amount', 'N/A')}"
                        sales_data.append({
                            'title': f"Sales Record: {row.get('Product', 'Unknown')} - {row.get('Salesperson', 'Unknown')}",
                            'content': content,
                            'source': filepath,
                            'document_type': 'sales_record'
                        })
            except Exception:
                continue
    
    return sales_data

def create_synthetic_annual_reports():
    companies = [
        "TechCorp Inc.", "Global Manufacturing Ltd.", "Digital Solutions Corp.",
        "Innovation Systems", "Future Technologies", "Smart Solutions Ltd.",
        "Advanced Analytics Corp.", "NextGen Industries", "Digital Dynamics",
        "Innovation Labs", "Tech Solutions Inc.", "Global Innovations",
        "Digital Enterprises", "Future Systems", "Smart Technologies"
    ]
    
    annual_reports = []
    
    for i, company in enumerate(companies):
        year = 2020 + (i % 4)
        
        content = f"""
        Annual Report for {company} - {year}
        
        Executive Summary:
        {company} achieved significant growth in {year} with revenue increasing by {random.randint(15, 35)}% year-over-year. 
        The company's strategic initiatives in digital transformation and market expansion have yielded positive results.
        
        Financial Performance:
        - Revenue: ${random.randint(100, 500)}M
        - Net Income: ${random.randint(10, 50)}M
        - EBITDA Margin: {random.randint(15, 25)}%
        
        Strategic Initiatives:
        The company continued its investment in R&D, allocating {random.randint(8, 15)}% of revenue to product development.
        Market expansion efforts resulted in {random.randint(5, 15)} new partnerships and {random.randint(10, 30)}% increase in market share.
        
        Risk Factors:
        Market volatility and competitive pressures remain key challenges. Regulatory changes and economic uncertainty
        could impact future performance. The company has implemented comprehensive risk management strategies.
        
        Outlook:
        {company} expects continued growth in {year + 1} with projected revenue increase of {random.randint(10, 25)}%.
        The company remains committed to innovation and sustainable business practices.
        """
        
        annual_reports.append({
            'title': f"Annual Report: {company} - {year}",
            'content': content,
            'source': 'synthetic',
            'document_type': 'annual_report'
        })
    
    return annual_reports

def create_synthetic_earnings_calls():
    companies = [
        "TechCorp Inc.", "Global Manufacturing Ltd.", "Digital Solutions Corp.",
        "Innovation Systems", "Future Technologies", "Smart Solutions Ltd.",
        "Advanced Analytics Corp.", "NextGen Industries", "Digital Dynamics",
        "Innovation Labs"
    ]
    
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    years = [2022, 2023, 2024]
    
    earnings_calls = []
    
    for company in companies:
        for year in years:
            for quarter in quarters:
                content = f"""
                Earnings Call Transcript - {company} {quarter} {year}
                
                CEO Opening Remarks:
                Good afternoon everyone. I'm pleased to report that {company} delivered strong results in {quarter} {year}.
                Our revenue grew {random.randint(8, 25)}% year-over-year to ${random.randint(50, 200)}M.
                
                Financial Highlights:
                - Revenue: ${random.randint(50, 200)}M (up {random.randint(8, 25)}% YoY)
                - EPS: ${random.uniform(0.5, 2.5):.2f} (up {random.randint(10, 30)}% YoY)
                - Gross Margin: {random.randint(60, 80)}%
                
                Business Performance:
                Our core business segments showed solid growth. Digital transformation initiatives contributed
                {random.randint(15, 35)}% to revenue growth. Customer acquisition costs decreased by {random.randint(5, 15)}%.
                
                Guidance:
                For {quarter} {year + 1}, we expect revenue of ${random.randint(60, 250)}M to ${random.randint(70, 300)}M.
                We remain confident in our long-term growth strategy and market position.
                
                Q&A Session:
                Analyst questions focused on market expansion, competitive landscape, and future investment plans.
                Management provided detailed responses on strategic initiatives and operational efficiency measures.
                """
                
                earnings_calls.append({
                    'title': f"Earnings Call: {company} - {quarter} {year}",
                    'content': content,
                    'source': 'synthetic',
                    'document_type': 'earnings_call'
                })
    
    return earnings_calls

def main():
    all_documents = []
    
    stock_data = preprocess_stock_data()
    all_documents.extend(stock_data)
    
    transactions_data = preprocess_transactions_data()
    all_documents.extend(transactions_data)
    
    sales_data = preprocess_sales_data()
    all_documents.extend(sales_data)
    
    annual_reports = create_synthetic_annual_reports()
    all_documents.extend(annual_reports)
    
    earnings_calls = create_synthetic_earnings_calls()
    all_documents.extend(earnings_calls)
    
    df = pd.DataFrame(all_documents)
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/preprocessed_data.csv', index=False)
    
    return df

if __name__ == "__main__":
    main() 